# -*- coding: utf-8 -*-
from collections import Hashable
from random import randint

def create_dict_1(L1, L2):
    return dict(zip(L1, L2))

def create_dict_2(list_):
    keys = []
    values = []
    for element in list_:
        if isinstance(element, Hashable):
            keys.append(element)
        else:
            values.append(element)
    return dict(zip(keys, values))


def random_list(a, b, size):
    return [randint(a, b) for _ in range(size)]

def count_ints(list_):
    counter = {}
    for num in list_:
        try:
            counter[num] += 1
        except KeyError:
            counter[num] = 1
    return counter


if __name__ == '__main__':
    print('Task 1 "create_dict_1"')
    L1 = [1, 2, 'a', 'b']
    L2 = [(22, 'aa'), ['x'], ('3',), ('s', 3)]
    print('Input data: {}, {}'.format(L1, L2))
    print(create_dict_1(L1, L2))

    print('\nTask 2 "create_dict_2"')
    list_ = L = [1, 2, [22], 'a', 'b', [33], [44], [55]]
    print('Input data: {}'.format(list_))
    print(create_dict_2(list_))

    print('\nTask 3 "random_list_count"')
    a, b, size = 1, 100, 100
    list_ = random_list(a, b, size)
    print('Input data first 10 items: {}'.format(list_[:10]))
    dict_ = count_ints(list_)
    for key in range(a, a+10):
        cnt = dict_.get(key, 0)
        print('{}, times {}'.format(key, cnt))
