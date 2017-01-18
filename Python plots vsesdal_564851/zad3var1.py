# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
import csv

data_1 = {}
# Считаем данные ведомости
with open('result_1.csv') as result_1_f:
    result = csv.reader(result_1_f, delimiter=',')
    for row in result:
        data_1.update({row[0]: row[1:]})

data_2 = {}
# Считаем данные ведомости пересдач
with open('result_2.csv') as result_2_f:
    result = csv.reader(result_2_f, delimiter=',')
    for row in result:
        data_2.update({row[0]: row[1:]})

# Всего студентов
num_stud = len(data_1)


    
