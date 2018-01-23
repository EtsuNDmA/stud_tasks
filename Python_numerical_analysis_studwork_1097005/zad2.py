"""
Реализация неявного метода Эйлера для решения начально-краевой задачи

du/dt=a**2*d2u/dt^2+f
u(0,t)=phi1(t)
u(L,t)=phi2(t)
u(x,0)=psi(x)
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def solve(a2, f, X_begin, X_end, Nx, T_begin, T_end, Nt, u_Tb_x, u_t_Xb, u_t_Xe):
    """Решатель"""
    hx = (X_end - X_begin) / Nx
    ht = (T_end - T_begin) / Nt

    x = np.linspace(X_begin, X_end, num=Nx+1)
    t = np.linspace(T_begin, T_end, num=Nt+1)

    u = np.zeros([Nt+1, Nx+1])

    u[0, :] = u_Tb_x(x)
    u[:, 0] = u_t_Xb(t)
    u[:, -1] = u_t_Xe(t)

    A = a2 / hx**2
    B = -(1/ht + 2*a2/hx**2)
    C = a2 / hx**2

    M = np.zeros([Nx-1, Nx-1])
    M[0, 0] = B
    M[0, 1] = C
    M[-1, -2] = A
    M[-1, -1] = B
    for i in range(1, Nx-2):
            M[i, i-1:i+2] = np.array([A, B, C])

    for i in range(1, Nt):
        F = -f(t[i], x[1:-1]) - u[i-1, 1:-1]
        F[0] -= A * u[i, 0]
        F[-1] -= C * u[i, -1]
        # Решаем задачу M*u = F для каждого слоя по t
        u[i, 1:-1] = np.linalg.solve(M, F)  # В идеале СЛАУ с трехдиагональной матрицей должно решаться методом прогонки
    return x, t, u


if __name__ == '__main__':
    # Условие задачи
    T_begin = 0
    T_end = 1
    a2 = 1e-6

    X_begin = 0
    X_end = 0.025

    def f(t, x):
        return -np.exp(10*x - t/T_end)

    # Начальное условие
    def u_Tb_x(x):
        return 1
    # Краевые условия
    def u_t_Xb(t):
        return np.exp(-10*t/T_end)
    def u_t_Xe(t):
        return np.cos(10*t/T_end)

    # Численное решение
    Nx = 20
    Nt = 70

    x, t, u = solve(a2, f, X_begin, X_end, Nx, T_begin, T_end, Nt, u_Tb_x, u_t_Xb, u_t_Xe)

    # Строим графики
    x, t = np.meshgrid(x, t)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_wireframe(x, t, u)
    ax.set_xlabel('x')
    ax.set_ylabel('t')
    ax.set_zlabel('u')
    plt.show()
