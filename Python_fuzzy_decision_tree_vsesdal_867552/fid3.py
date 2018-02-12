# -*- coding: utf-8 -*-
import numpy as np
from collections import deque
from itertools import count
from copy import deepcopy
import skfuzzy as fuzz
import json


def pprint(tree, level=0, file=None):
    """Рекурсивная распечатка дерева в глубину"""
    print("--" * level + repr(tree) + "\n", file=file)
    for child in tree.children:
        pprint(child, (level + 1), file=file)
    return None


c = count(1)
tol = 1e-10


class Node(object):
    def __init__(self, X, y, attribute=None, f_attribute=None, id_=0, m=1, classes=None):
        self.attribute = attribute
        self.f_attribute = f_attribute
        self.X = X
        self.y = y
        self.children = []
        self.id = id_
        self.m = m
        self.classes = classes

    def __repr__(self):
        if self.children:
            return "{}-->N{}-{}".format(self.f_attribute or "Root", self.id, self.attribute)
        else:
            return "{}-->N{}-C({})".format(self.f_attribute, self.id,  self.C)

    def add_child(self, node):
        """Добавляет дочерний узел"""
        node.id = next(c)
        self.children.append(node)

    def get_rev_children(self):
        """Возвращает дочерние узлы в обратном порядке"""
        children = self.children[:]
        children.reverse()
        return children

    @property
    def C(self):
        """Подсчитывает вес классов в текущем узле"""
        counts = np.zeros(len(self.classes))
        for i, cl in enumerate(self.classes):
            counts[i] = self.y[self.y == cl].size
        return counts / (np.sum(counts)+tol)


class FuzzyID3Classifier:
    def __init__(self, control_threshold=0.85, decision_threshold=0.02):
        self.control_threshold = control_threshold
        self.decision_threshold = decision_threshold
        self.fuzzy_attributes = None
        self.tree = None
        self.classes = None
        self._attribute_columns = None

        self._train_len = None
        self._fitted = False

    def _entropy(self, y):
        """Вычисляет энтропию для y"""
        n = y.shape[0]
        counts = np.zeros(len(self.classes))
        for i, cl in enumerate(counts):
            counts[i] = y[y == cl].size
        P = counts / n
        return np.sum(-P * np.log2(P+tol))

    def _fuzzy_entropy(self, X, y, attribute):
        """Вычисляет нечеткую энтропию для каждого столбца из X по классам из y"""
        col = self.fuzzy_attributes[attribute]['column']
        f_params = self.fuzzy_attributes[attribute]['params']
        MF = np.hstack([fuzzy_func(X[:, col], params).reshape(X.shape[0], 1) for params in f_params])
        S = np.sum(MF, axis=0)

        Sc = np.zeros((len(self.classes), MF.shape[1]))
        for i, c in enumerate(self.classes):
            Sc[i, :] = np.sum(MF[y == c, :], axis=0)

        Pc = Sc / (S+tol)
        return np.sum(-Pc * np.log2(Pc+tol), axis=0), Sc, np.sum(S)

    def _information_gain(self, X, y, attribute):
        """Вычисляет прибавку информации"""
        Hfs, Sc, S = self._fuzzy_entropy(X, y, attribute)
        Sv = np.sum(Sc, axis=0)
        Hf = self._entropy(y)
        return Hf - np.sum(Sv / S * Hfs)

    def _stop(self, node):
        """Решает, нужно ли остановить разбиение дерева"""
        if node.X.shape[1] == 0:
            return True
        if node.X.shape[0] < self.decision_threshold * self._train_len:
            return True
        if np.any(node.C >= self.control_threshold):
            return True
        return False

    def _get_max_attr(self, node):
        """
        Возвращает аттрибут с максимальной прибавкой информации
        т.е. аттрибут, по которому будем разбивать текущий узел дерева
        """
        max_attr = None
        max_attr_gain = 0
        for attribute in self._attribute_columns.keys():
            G = self._information_gain(node.X, node.y, attribute)
            if G > max_attr_gain:
                max_attr_gain = G
                max_attr = attribute
        return max_attr

    def _expand_tree(self, node):
        """Разбивает дерево в указанном узле"""
        attribute = self._get_max_attr(node)
        if attribute is None:
            return []
        node.attribute = attribute

        col = self._attribute_columns[attribute]
        f_params = self.fuzzy_attributes[attribute]['params']
        names = self.fuzzy_attributes[attribute]['names']
        M = np.hstack([fuzzy_func(node.X[:, col], params).reshape(node.X.shape[0], 1) for params in f_params])
        for f_attribute, M_col in zip(names, M.T):
            X = node.X[M_col > 0, :]
            y = node.y[M_col > 0]
            node.add_child(Node(X, y, f_attribute=f_attribute, classes=self.classes))
        self._attribute_columns.pop(attribute)
        return node.children

    def _build_tree(self, X, y):
        """Строит нечеткое решающее дерево"""
        self.tree = Node(X, y, classes=self.classes)
        queue = deque()
        queue.append(self.tree)
        while queue:
            cur_node = queue.popleft()
            if not self._stop(cur_node):
                queue.extend(self._expand_tree(cur_node))

    def fit(self, X, y, fuzzy_attributes, classes):
        """Обучает решающее дерево"""
        self._train_len = X.shape[0]
        self._attribute_columns = deepcopy({k: v['column'] for k, v in fuzzy_attributes.items()})
        self.fuzzy_attributes = fuzzy_attributes
        self.classes = classes

        self._build_tree(X, y)

        self._fitted = True
        return self

    def confusion_matrix(self, y_pred, y_true):
        """Вычисляет матрицу ошибок"""
        n_labels = len(self.classes)

        CM = np.zeros((n_labels, n_labels))
        for yp, yt in zip(y_pred, y_true):
            CM[int(yt), int(yp)] += 1

        return CM

    def score(self, y_pred, y):
        """Возвращает метрики качества precision и recall"""
        CM = self.confusion_matrix(y_pred, y)

        precision = np.zeros(CM.shape[0])
        recall = np.zeros(CM.shape[0])
        for i in range(CM.shape[0]):
            precision[i] = CM[i, i] / (np.sum(CM[:, i])+tol)
            recall[i] = CM[i, i] / (np.sum(CM[i, :]) + tol)

        return precision, recall

    def predict(self, X):
        """По обученному дереву делает предсказание класса"""
        if not self._fitted:
            raise RuntimeError('You must call "fit" method before prediction')

        return np.vstack([self._get_classes(x) for x in X])

    def _get_classes(self, X):
        """Возвращает вес классов"""
        leafs = []
        stack = [self.tree]
        while stack:
            cur_node = stack.pop()
            cur_node_children = cur_node.get_rev_children()
            if cur_node_children:
                attribute = cur_node.attribute
                col = self.fuzzy_attributes[attribute]['column']
                for i, child in enumerate(cur_node.children):
                    f_params = self.fuzzy_attributes[attribute]['params'][i]
                    child.m = cur_node.m * fuzzy_func(X[col], f_params)
                    stack.append(child)
            else:
                leafs.append(cur_node)
        return np.sum(np.vstack([leaf.m*leaf.C for leaf in leafs]), axis=0)


def train_test_split(X, y, test_size=0.33):
    """Разделяет данные на тренировочные и тестовые"""
    assert 0 < test_size < 1
    assert X.shape[0] == y.shape[0]
    indexes = range(X.shape[0])
    test_indexes = np.random.choice(indexes, int(test_size*X.shape[0]), replace=False)
    train_indexes = np.array(tuple(set(indexes) - set(test_indexes)))
    return X[train_indexes, :], X[test_indexes, :], y[train_indexes], y[test_indexes]

def fuzzy_func(x, params):
    x = np.array(x)
    if x.shape == ():
        x = x.reshape(1)
    params = np.array(params)
    if params.size == 2 and params[0] <= params[1]:
        return fuzz.smf(x, *params)
    elif params.size == 2 and params[0] > params[1]:
        return fuzz.zmf(x, *params[::-1])
    elif params.size == 3:
        assert params[0] <= params[1] <= params[2]
        return fuzz.trimf(x, params)
    elif params.size == 4:
        assert params[0] <= params[1] <= params[2] <= params[3]
        return fuzz.trapmf(x, params)
    else:
        raise ValueError('Wrong number of params')


if __name__ == '__main__':
    # Загрузим параметры нечетких функций
    with open('params.json', 'r') as fp:
      params = json.load(fp)

    classes = params['classes']
    fuzzy_attributes = params['attributes']
    # Загрузим датасет, исключив 1 строку
    dataset = np.loadtxt('input.csv', delimiter=",", skiprows=1)
    X = dataset[:, :-1]
    y = dataset[:, -1].astype(int)
    # Разделим датасет
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)

    # Создадим и обучим классификатор
    clf = FuzzyID3Classifier(control_threshold=0.85, decision_threshold=0.02)
    clf.fit(X_train, y_train, fuzzy_attributes, classes)

    # Распечатаем дерево в файл
    with open('out_tree.txt', 'w') as f:
        pprint(clf.tree, file=f)

    # Предсказанные классов
    c_memb = clf.predict(X_test)
    # Предсказанные классы
    y_pred = np.argmax(c_memb, axis=1)
    # Матрица ошибок
    confusion_matrix = clf.confusion_matrix(y_pred, y_test)
    # Метрики precision и recall
    precision, recall = clf.score(y_pred, y_test)
    # Печатаем результаты в файл
    with open('out_result.txt', 'w') as f:
        print("Class memberships for classes {}\n{}".format(classes, c_memb), file=f)
        print("Test dataset contains {} members".format(X_test.shape[0]), file=f)
        print("X_test:\n{}".format(X_test), file=f)
        print("Prediction:\n{}\nTrue:\n{}".format(y_pred, y_test), file=f)
        print("Confusion matrix:\n{}".format(confusion_matrix), file=f)
        print("Correctly classified {:.0f}/{} samples".format(np.trace(confusion_matrix), X_test.shape[0]), file=f)
        print("Precision: ["+" ".join(['{:.2f}'.format(i) for i in precision])+"]", file=f)
        print("Recall: ["+" ".join(['{:.2f}'.format(i) for i in recall])+"]", file=f)
