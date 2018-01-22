"""
Реализация неявного метода Эйлера для решения начально-краевой задачи

du/dt=a**2*d2u/dt^2+f

alpha0*y(a)+alpha1*y'(a)=gamma0
beta0*y(b)+beta1*y'(b)=gamma1

y''-xy'+2y=x+1, y(0.9)-0.5y'(0.9)=2, y(1.2)=1
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
    
    y = np.zeros([Nt+1, Nx+1])
    
    y[0, :] = u_Tb_x(x)
    y[:, 0] = u_t_Xb(t)
    y[:, -1] = u_t_Xe(t)
    
    A = a2 / hx**2
    B = -(1/ht + 2*a2/hx**2)
    C = a2 / hx**2
    
    M = np.zeros([Nx-1, Nx-1])
    M[0, 0] = B
    M[0, 1] = C
    M[-1, -2] = A
    M[-1, -1] = B
    for i in range(1,Nx-2):
            M[i, i-1:i+2] = np.array([A, B, C])    
    
    for i in range(1, Nt):
        F = -f(t[i] , x[1:-1]) - y[i-1, 1:-1]
        F[0] -= A * y[i, 0]
        F[-1] -= C * y[i, -1]
        # Решаем задачу M*y = F для каждого слоя по t
        y[i, 1:-1] = np.linalg.solve(M, F)
        print(M)
        print(F)
        print(y[i,:])
    return x, t, y
    
if __name__ == '__main__':
    # Условие задачи
    T_begin = 0
    T_end = 10
    a2 = 1e-6
    
    X_begin = 0
    X_end = 0.025
    
    def f(t, x):
        return np.exp(10*x - t/T_end)
    
    # Начальное условие
    def u_Tb_x(x):
        return 1
    # Краевые условия
    def u_t_Xb(t):
        return np.exp(-10*t/T_end)
    def u_t_Xe(t):
        return np.cos(10*t/T_end)
        
    # Численное решение
    Nx = 100
    Nt = 500
    
    x, t, y = solve(a2, f, X_begin, X_end, Nx, T_begin, T_end, Nt, u_Tb_x, u_t_Xb, u_t_Xe)

    # Точное решение полученное с помощью wolframalpha.com
    # x_exact = np.linspace(a, b, num=steps + 1)
    # y_exact = 1.61517 + (1. - 0.117744*np.exp(x_exact**2/2))*x - 1.11517*x_exact**2 + (-0.14757 + 0.14757*x_exact**2)*erfi(x_exact/np.sqrt(2))

    # Строим графики
    x, t = np.meshgrid(x, t)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_surface(x, t, y)
    # marker = '.' if steps < 20 else None
    # plt.plot(x, y, label='Numerical', marker=marker)
    # plt.plot(x_exact, y_exact, label='Exact')
    ax.set_xlabel('x')
    ax.set_ylabel('t')
    ax.set_zlabel('y')
    # plt.grid()
    # plt.legend()
    plt.show()
