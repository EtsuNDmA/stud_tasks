# -*- coding: utf-8 -*-

from matplotlib import pyplot as plt
from numpy import arange

step = 0.1
start = -2.0
stop = 2.0
# Рассчитаем точки
x = arange(start, stop+step, step)
y = x**2
# Построим график зеленого цвета сплошной линией
# и с круглыми маркерами
plt.plot(x, y, 'go-', label='line 1', linewidth=2)
plt.grid()  # Сетка
plt.xlabel('x')  # Подпись оси X
plt.ylabel('y')  # Подпись оси Y
plt.xlim([start-step, stop+step])  # Ограничение по оси X
plt.ylim([min(y)-step, max(y)+step])  # Ограничение по оси Y
plt.title('График функции $y=x^2$', family='verdana')  # Подпись
plt.savefig('fig1.png')  # Сохраним график
plt.show()  # Отобразим график