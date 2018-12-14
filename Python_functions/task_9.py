# -*- coding: utf-8 -*-

def count_digits(num):
    counter = 1
    num = abs(num)
    while num >= 10:
        num = num // 10
        counter += 1
    return counter


def istrcmp(s1, s2):
    print(s1.lower(), s2.lower())
    return s1.lower() == s2.lower()


def count_vowels(string):
    vowels = 'a', 'e', 'i', 'o', 'u', 'y'
    # Создаем словарь вида {буква: счетчик}. Счетчики заполоняем нулями
    vowels_counter = {letter: 0 for letter in vowels}
    for symbol in string:
        symbol = symbol.lower()
        if symbol in vowels:
            vowels_counter[symbol] += 1
    return vowels_counter


def sameVowels(s1, s2):
    # Регистр гласных букв не учитывается!
    s1_vowels_counter = count_vowels(s1)
    s2_vowels_counter = count_vowels(s2)
    return s1_vowels_counter.items() == s2_vowels_counter.items()


if __name__ == '__main__':
    print('Task 1 "count digits"')
    num = int(input('Enter num: '))
    print('Num {} has {} digits'.format(num, count_digits(num)))

    print('\nTask 2 "istrcmp"')
    s1 = input('Enter string 1: ')
    s2 = input('Enter string 2: ')
    print('"{}" is {} to "{}" ignoring case'.format(s1, 'equal' if istrcmp(s1, s2) else 'not equal', s2))

    print('\nTask 3 "sameVowels"')
    s1 = input('Enter string 1: ')
    s2 = input('Enter string 2: ')
    print('"{}" {} the same vowels as "{}"'.format(s1, 'has' if sameVowels(s1, s2) else 'has not', s2))
