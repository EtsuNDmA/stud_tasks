# -*- coding: utf-8 -*-
def input_data():
    # Вводим параметры
    n_cities = int(input(" - Введите количество городов: "))
    lower_bound = float(input(" - Введите нижнюю границу высот: "))
    upper_bound = float(input(" - Введите верхнюю границу высот: "))
    if lower_bound > upper_bound:
        raise ValueError("Нижняя граница не может быть больше верхней")
    # Вводим города
    cities = []
    for i in range(n_cities):
        city_data = input("{}/{} > ".format(i+1, n_cities))
        # Разделяем строку по пробелам и создаем список
        city_data = city_data.split()
        # Отрезаем из списка последний элемент, это и есть высота
        height = float(city_data.pop())
        # Оставшиеся элементы снова собираем в строку, это название города
        # Название города может состоять из нескольких слов, например Нижний Новгород
        city = ' '.join(city_data)

        cities.append((city, height))
    return lower_bound, upper_bound, cities


def quick_sort(arr, col):
    """
    Алгоритм быстрой сортировки
    https://ru.wikipedia.org/wiki/Быстрая_сортировка

    arr - список для сортировки
    col - номер элемента по которому сортируем
    descend - сортировать в обратном порядке
    """
    less = []
    equal = []
    greater = []

    if len(arr) > 1:
        pivot = arr[0][col]
        for x in arr:
            if x[col] < pivot:
                less.append(x)
            if x[col] == pivot:
                equal.append(x)
            if x[col] > pivot:
                greater.append(x)
        return quick_sort(less, col)+equal+quick_sort(greater, col)
    else:
        return arr


def find_upper_bound(arr, key):
    """Возвращает индекс наименьшего элемента из arr > key с помощью двоичного поиска"""
    left = -1
    right = len(arr)
    while right > left + 1:
        middle = (left + right) // 2
        if arr[middle] > key:
            right = middle
        else:
            left = middle
    # Возвращаем индекс элемента или None, если нет элементов удовлетворяющих поиску
    return right if right < len(arr) else None


def find_lower_bound(arr, key):
    """Возвращает индекс наибольшего элемента из arr < key с помощью двоичного поиска"""
    left = -1
    right = len(arr)
    while right > left + 1:
        middle = (left + right) // 2
        if arr[middle] >= key:
            right = middle
        else:
            left = middle
    # Возвращаем индекс элемента или None, если нет элементов удовлетворяющих поиску
    return left if left > 0 else None


def binary_search_range(arr, lower, upper):
    # Находим индекс наименьшего элемента, значение которого > нижней границы
    l_idx = find_upper_bound(arr, lower)
    # Находим индекс наибольшего элемента, значение которого < верхней границы
    u_idx = find_lower_bound(arr, upper)
    return l_idx, u_idx


if __name__ == '__main__':
    # Ввод данных
    lower_bound, upper_bound, cities = input_data()
    # Сортировка
    cities = quick_sort(cities, 1)
    # Вывод отсортированного по возрастанию высоты списка
    for city, height in cities:
        print(city, height)
    print('='*20)

    heights = [item[1] for item in cities]  # список высот
    # Поиск городов из заданного диапазон высот
    l_idx, u_idx = binary_search_range(heights, lower_bound, upper_bound)
    # Вывод того,что нашли
    if l_idx is None or u_idx is None:
        print('Нет городов, удовлетворяющих условиям поиска')
    else:
        for city, height in cities[l_idx:u_idx+1]:
            print('{} {} < {} < {}'.format(city, lower_bound, height, upper_bound))
