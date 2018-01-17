#___________________Импорт библиотек_________
import numpy as np
from matplotlib import pyplot

#___________________Условие задачи__________
alpha1 = 0
alpha2 = 0
beta1 = 1
beta2 = 1
gamma1 = 1
gamma2 = -1
a = 0
b = 1

#_________________Функции p(x),q(x),f(x)_____
def P(x):
    return 1
def q(x):
    return -12
def f(x):
    return x**2

#_________________Реализация МКР______________
size = 8 
X = np.linspace(a, b, size)
h = (b - a) / (size - 1)

array = [[0 for _ in range(size)] for _ in range(size)]
array2 = [[0] for _ in range(size)]

array = np.array(array, np.float)
array2 = np.array(array2, np.float)

array[0][0] = beta1 - alpha1 / h
array[0][1] = alpha1 / h
array2[0] = gamma1

array[-1][-1] = beta2 + alpha2 / h
array[-1][-2] = -alpha2 / h
array2[-1] = gamma2

for i in range(1, size - 1):
    array[i][i - 1] = 1 / h ** 2 - P(X[i]) / (2 * h)
    array[i][i] = q(X[i]) - 2 / h ** 2
    array[i][i + 1] = 1 / h ** 2 + P(X[i]) / (2 * h)
    array2[i] = f(X[i])

aa = [0]
for i in range(1, size - 1):
    aa.append(array[i][i - 1])

bb = []
for i in range(0, size - 2):
    bb.append(array[i][i + 1])
bb.append(0)

cc = []
for i in range(size):
    cc.append(array[i][i])

res = np.linalg.solve(array, array2)
res = res.flat

pyplot.plot(X, res, label="МКР (8 точек)")

#__________________________Точное решение__________

ls = np.linspace(a, b, 20)

def best_sol(x):
    C1 = (np.exp(4) * (767 + 877 * np.exp(3))) / (864 * (-1 + np.exp(7)))
    C2 = -(877 + 767 * np.exp(4)) / (864 * (-1 + np.exp(7)))
    return C1 * np.exp(-4*x) + C2 * np.exp(3*x) - x*x/12 - x/72 - 13/864

calculated_f = []
for i in ls:
    calculated_f.append(best_sol(i))

pyplot.plot(ls, calculated_f, label="Точное решение")
pyplot.legend()
pyplot.grid()
pyplot.show()


