# -*- coding: utf-8 -*-

VOWELS = 'a', 'e', 'i', 'o', 'u', 'y'

def string_to_groups(string):
    list_words = string.split()
    assert len(list_words) == 3, 'String have to consist of exactly 3 words'

    result = {}
    for word in list_words:
        group0 = set()
        group1 = set()
        group2 = set()
        for letter in word:
            letter = letter.lower()
            if letter in VOWELS:
                group0.add(letter)
            elif 'a' <= letter <= 'm':
                group1.add(letter)
            else:
                group2.add(letter)
        result[word] = group0, group1, group2
    return result


def count_items(list_):
    counter = {'int': 0, 'str': 0}
    for item in list_:
        if isinstance(item, int):
            counter['int'] += 1
        elif isinstance(item, str):
            counter['str'] += 1
        else:
            # Рекурсивно вызываем эту же функцию
            cnt = count_items(item)
            counter['int'] += cnt['int']
            counter['str'] += cnt['str']
    return counter

def dict_to_groups(dict_):
    d1 = {}
    d2 = {}
    d3 = {}
    for key, value in dict_.items():
        if isinstance(key, int):
            d1[key] = value
        if isinstance(key, str):
            d2[key] = value
        else:
            try:
                if any([isinstance(key_item, str) for key_item in key]):
                    d2[key] = value
            except TypeError:
                pass
        if isinstance(key, tuple):
            d3[key] = value
    return d1, d2, d3

if __name__ == '__main__':
    print('Task 1 "string_to_groups digits"')
    string = 'Hello pretty World'
    print('Input data: {}'.format(string))
    print(string_to_groups(string))

    print('\nTask 2 "count_items"')
    list_ = [1, 2, ['abc', 5], (32,), 'zyx']
    print('Input data: {}'.format(list_))
    print(count_items(list_))

    print('\nTask 3 "dict_to_groups"')
    dict_ = {1: 2, 'abc': 42, (7, 8): 'hello', ('xyz', 55): 'world'}
    print('Input data: {}'.format(dict_))
    print(dict_to_groups(dict_))


