# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
import csv

data_1 = {}
# Считаем данные ведомости
with open('result_1.csv',  encoding='utf-8') as result_1_f:
    result = csv.reader(result_1_f, delimiter=',')
    for row in result:
        data_1.update({row[0]: row[1:]})

data_2 = {}
# Считаем данные ведомости пересдач
with open('result_2.csv',  encoding='utf-8') as result_2_f:
    result = csv.reader(result_2_f, delimiter=',')
    for row in result:
        data_2.update({row[0]: row[1:]})

# Всего студентов
num_stud = len(data_1)
# Найдем число студентов имеющих только пятерки
num_stud_only5 = 0
for name, marks in data_1.items():
    # Находим какие оценки вообще есть у студента
    mark_types = set(marks)
    print(mark_types)
    print(len(mark_types))
    # Если только один тип оценок и это пятерки то увеличиваем счетчик
    if len(mark_types) == 1 and '5' in mark_types:
        num_stud_only5 += 1

labels = 'Other', 'Only 5'
sizes =  num_stud-num_stud_only5, num_stud_only5
explode = (0, 0.1)  # Выделим второй слайс

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')

plt.show()

