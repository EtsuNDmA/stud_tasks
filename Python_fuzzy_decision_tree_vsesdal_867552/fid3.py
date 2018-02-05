# -*- coding: utf-8 -*-
import numpy as np


def unique(array):
    if getattr(array, "dtype", None) == np.float32:
        array = array.astype(int)
    counts = np.bincount(array)
    mask = counts != 0
    return np.nonzero(mask)[0], counts[mask]


class FuzzyID3Classifier:
    def __init__(self, control_threshold=0.85, decision_threshold=0.02, attribute_columns=None, memberships=None, tree=None):
        self.control_threshold = control_threshold
        self.decision_threshold = decision_threshold
        self.attribute_columns = attribute_columns
        self.memberships = memberships
        self.tree = tree
        self._fitted = False

    @staticmethod
    def _entropy(y):
        """Вычисляет энтропию для y"""
        n = y.shape[0]
        _, counts = unique(y)
        P = counts / n
        return np.sum(-P * np.log2(P))

    def _fuzzy_entropy(self, X, y, attribute):
        """Вычисляет энтропию для каждого столбца из X по классам из y"""
        classes, _ = unique(y)

        col = self.attribute_columns[attribute]
        MF = np.hstack([func(X[:, col]) for func in self.memberships[attribute]])

        S = np.sum(MF, axis=0)

        Sc = np.zeros((classes.shape[0], MF.shape[1]))
        for i, c in enumerate(classes):
            Sc[i, :] = np.sum(MF[y == c, :], axis=0)

        Pc = Sc / S
        return np.sum(-Pc * np.log2(Pc), axis=0), Sc, np.sum(S)

    def _information_gain(self, X, y, attribute):
        Hfs, Sc, S = self._fuzzy_entropy(X, y, attribute)
        Sv = np.sum(Sc, axis=0)
        Hf = self._entropy(y)
        return Hf - np.sum(Sv / S * Hfs)

    def _build_tree(self):
        mf = np.ones(X.shape[0])
        self.tree = Tree(mf, X, y)

    def fit(self, X, y, attribute_columns, memberships):
        self.attribute_columns = attribute_columns
        self.memberships = memberships

        max_attr = None
        max_attr_gain = 0
        for attribute in attribute_columns.keys():
            G = self._information_gain(X, y, attribute)
            if G > max_attr_gain:
                max_attr_gain = G
                max_attr = attribute


        self._fitted = True
        return self

    def predict(self, X):
        if not self._fitted:
            raise RuntimeError('You must call "fit" method before prediction')


if __name__ == '__main__':
    # X = np.array(
    #     [[32, 0.7, 0.6, 0, 3, 1, 0, 7.5, 0.25, 0.25],
    #      [33, 0.8, 0.4, 0, 4.5, 0.25, 0.3, 6.8, 0.18, 0.37],
    #      [30, 0.5, 1, 0, 2.5, 1, 0, 8.3, 0.33, 0.12],
    #      [24, 0, 1, 0, 1.5, 1, 0, 9, 0.4, 0],
    #      [3, 0, 0, 1, 2.5, 1, 0, 3.8, 0, 0.87],
    #      [1, 0, 0, 1, 5, 0, 0.4, 4.2, 0, 0.8],
    #      [8, 0, 0.2, 1, 4, 0.5, 0.2, 2.7, 0, 1],
    #      [12, 0, 0.47, 1, 3, 1, 0, 6.7, 0.17, 0.38],
    #      [-5, 0, 0, 1, 2, 1, 0, 3.5, 0, 0.92],
    #      [12, 0, 0.47, 1, 2.5, 1, 0, 4.1, 0, 0.82],
    #      [15, 0, 0.67, 0, 6, 0, 0.5, 2.3, 0, 1],
    #      [22, 0, 1, 0, 5, 0, 0.4, 7.3, 0.23, 0.28],
    #      [32, 0.7, 0.6, 0, 2.5, 1, 0, 2.6, 0, 1],
    #      [25, 0, 1, 0, 4, 0.25, 0.3, 10.3, 0.53, 0]]
    # )
    X = np.array(
        [[32,3, 7.5],
         [33, 4.5, 6.8],
         [30, 2.5, 8.3],
         [24, 1.5, 9],
         [3, 2.5, 3.8],
         [1, 5, 4.2],
         [8, 4, 2.7],
         [12, 3, 6.7],
         [-5, 2, 3.5],
         [12, 2.5, 4.1],
         [15, 6, 2.3],
         [22, 5, 7.3],
         [32, 2.5, 2.6],
         [25, 4, 10.3]]
    )
    y = np.array([0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0])

    def t_cool(x):
        if x < 0:
            return 1
        elif x <= 15:
            return 1 - x/15
        else:
            return 0

    def t_mild(x):
        if x < 5:
            return 0
        elif x < 20:
            return x/15 - 1/3
        elif x < 30:
            return 1
        elif x < 35:
            return -x/5 + 7
        else:
            return 0

    def t_hot(x):
        if x < 25:
            return 0
        elif x <= 35:
            return x/10 - 2.5
        else:
            return 1

    def w_weak(x):
        if x < 3:
            return 1
        elif x <= 5:
            return 2.5 - x/2
        else:
            return 0

    def w_strong(x):
        if x < 3:
            return 0
        elif x <= 8:
            return x/5 - 0.6
        else:
            return 1

    def tj_short(x):
        if x < 3:
            return 1
        elif x <= 9:
            return 1.5 - x/6
        else:
            return 0

    def tj_long(x):
        if x < 5:
            return 0
        elif x <= 15:
            return x/10 - 0.5
        else:
            return 1

    t_cool = np.vectorize(t_cool)
    t_mild = np.vectorize(t_mild)
    t_hot = np.vectorize(t_hot)

    w_weak = np.vectorize(w_weak)
    w_strong = np.vectorize(w_strong)

    tj_short = np.vectorize(tj_short)
    tj_long = np.vectorize(tj_long)

    memberships = {'temperature': [t_cool, t_mild, t_hot],
                   'wind': [w_weak, w_strong],
                   'traffic': [tj_short, tj_long]}
    attribute_columns = {'temperature': 0,
                         'wind': 1,
                         'traffic': 3}

    clf = FuzzyID3Classifier()

    clf.fit(X, y, attribute_columns, memberships)

    print(clf._information_gain(X, y, 'temperature'))
    print(clf._information_gain(X, y, 'wind'))
    print(clf._information_gain(X, y, 'traffic'))
