# -*- coding: utf-8 -*-
import math


def count(sequence):
    counter = {}
    for element in sequence:
        counter[element] = counter.get(element, 0) + 1
    return counter


def task_1(string):
    words = string.lower().split()
    counter = count(words)
    for key, value in sorted(counter.items(), key=lambda x: x[1], reverse=True):
        print(key, value)


def task_2(string):
    words = string.lower().split(',')
    counter = count(words)
    max_value = max(counter.values())
    for key, value in counter.items():
        if value == max_value:
            print(key)


def task_3(string):
    words = string.lower().split()
    mapping = {
        'д': 2,
        'т': 3,
        'ч': 4,
        'п': 5,
    }
    num = mapping[words[0][0]]*10 + mapping[words[1][0]]
    return math.sqrt(num)

def task_4():
    months = ['января', 'февраля', 'марта',
              'апреля', 'мая', 'июня',
              'июля', 'августа', 'сентября',
              'октября', 'ноября', 'декабря']

    months_dict = dict(zip(months, range(1, 13)))
    print(months_dict)


if __name__ == '__main__':
    print("="*20, "task 1", "="*20)

    string = "The quick brown fox jumps over a lazy dog " \
             "DJs flock by when MTV ax quiz prog " \
             "Bawds jog flick quartz vex nymphs " \
             "Waltz bad nymph for quick jigs vex " \
             "Quick wafting zephyrs vex bold Jim " \
             "A wizard's job is to vex chumps quickly in fog"
    print(">> Input data:\n{}".format(string))
    print(">> Result:")
    task_1(string)

    print("=" * 20, "task 2", "=" * 20)
    string = "яблоки,груши,сливы,ананасы,яблоки,помидоры,груши"
    print(">> Input data:\n{}".format(string))
    print(">> Result:")
    task_2(string)

    print("=" * 20, "task 3", "=" * 20)
    string = "двадцать пять"
    print(">> Input data:\n{}".format(string))
    print(">> sqrt({}) = {}".format(string, task_3(string)))


    print("=" * 20, "task 4", "=" * 20)
    string = "двадцать пять"
    print(">> Result:")
    task_4()
