# -*- coding: utf-8 -*-
import numpy as np
from collections import deque
from itertools import count
from copy import deepcopy


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
            return "{}-->N{}-C({:.2f}, {:.2f})".format(self.f_attribute, self.id,  self.C[0], self.C[1])

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
        m_funcs = self.fuzzy_attributes[attribute]['functions']
        MF = np.hstack([func(X[:, col].reshape((X.shape[0], 1))) for func in m_funcs])
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
        m_funcs = self.fuzzy_attributes[attribute]['functions']
        names = self.fuzzy_attributes[attribute]['names']
        M = np.hstack([func(node.X[:, col].reshape((node.X.shape[0], 1))) for func in m_funcs])
        for m_func, f_attribute, M_col in zip(m_funcs, names, M.T):
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
                    m_func = self.fuzzy_attributes[attribute]['functions'][i]
                    child.m = cur_node.m * m_func(X[col])
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


if __name__ == '__main__':
    
    # Загрузим датасет, исключив 1 строку
    dataset = np.loadtxt('input.csv', delimiter=",", skiprows=1)
    X = dataset[:, :-1]
    y = dataset[:, -1].astype(int)
    
    # Создадим функции для вычисления нечтких аргументов
    def t_cool(x):
        if x < 15:
            return 1.0
        else:
            return 0.0

    def t_mild(x):
        if x < 5:
            return 0.0
        elif x < 20:
            return x/15 - 1/3
        elif x < 30:
            return 1.0
        elif x < 35:
            return -x/5 + 7
        else:
            return 0.0

    def t_hot(x):
        if x < 25:
            return 0.0
        elif x <= 35:
            return x/10 - 2.5
        else:
            return 1.0

    def w_weak(x):
        if x < 3:
            return 1.0
        elif x <= 5:
            return 2.5 - x/2
        else:
            return 0.0

    def w_strong(x):
        if x < 3:
            return 0.0
        elif x <= 8:
            return x/5 - 0.6
        else:
            return 1.0

    def tj_short(x):
        if x < 3:
            return 1.0
        elif x <= 9:
            return 1.5 - x/6
        else:
            return 0.0

    def tj_long(x):
        if x < 5:
            return 0.0
        elif x <= 15:
            return x/10 - 0.5
        else:
            return 1.0
    
    # Векторизуем функции, чтобы они могли работать сразу с массивами
    # в качестве входных аргументов
    t_hot = np.vectorize(t_hot)
    t_mild = np.vectorize(t_mild)
    t_cool = np.vectorize(t_cool)

    w_weak = np.vectorize(w_weak)
    w_strong = np.vectorize(w_strong)

    tj_short = np.vectorize(tj_short)
    tj_long = np.vectorize(tj_long)
    
    fuzzy_attributes = {
        'temperature': {
            'functions': [t_hot, t_mild, t_cool],
            'names': ['hot', 'mild', 'cool'],
            'column': 0,
        },                      
        'wind': {
            'functions': [w_weak, w_strong],
            'names': ['weak', 'strong'],
            'column': 1,
        },
        'traffic': {
            'functions': [tj_long, tj_short],
            'names': ['tj_long', 'tj_short'],
            'column': 2,
        },
    }
    classes = [0, 1]
    
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
