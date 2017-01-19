# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib import cm, ticker
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Получим точки поверхности
X = np.arange(-3, 3, 0.02)
Y = np.arange(-3, 3, 0.02)
X, Y = np.meshgrid(X, Y)
Z = X**2 + Y**2

# Строим окно фигуры
fig1 = plt.figure(figsize=(10, 10))
# Добавляем оси
ax1 = fig1.add_subplot(111)
ax1.axis('equal')
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_title("Contour plot for Z=X^2+Y^2")

# Добавляем график к осям
cs = ax1.contourf(X, Y, Z, cmap=cm.autumn)
plt.savefig('contour.png')
plt.show()

# Строим окно фигуры
fig2 = plt.figure(figsize=(10, 10))
# Добавляем оси
ax2 = fig2.add_subplot(111, projection='3d')
ax2.axis('equal')
ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.set_zlabel('z')
ax2.set_title("3D plot for Z=X^2+Y^2")
# Чтобы 3d график полностью помещался в осях
fig2.tight_layout()
# Добавляем график к осям
surf = ax2.plot_surface(X, Y, Z, cmap=cm.autumn, linewidth=0)
plt.savefig('3d.png')
plt.show()