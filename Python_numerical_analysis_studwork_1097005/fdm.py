"""
Реализация метода конечных разностей (finite difference method) для решения краевой задачи

y''+p(x)*y'+q(x)*y=f(x)

alpha0*y(a)+alpha1*y'(a)=gamma0
beta0*y(b)+beta1*y'(b)=gamma1

y''-xy'+2y=x+1, y(0.9)-0.5y'(0.9)=2, y(1.2)=1
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfi


def solve(p, q, f, alpha, beta, gamma, N):
    """Решатель"""
    h = (b - a) / N  # Шаг разностной схемы
    x = np.linspace(a, b, num=N+1)

    A = np.zeros([N + 1, N + 1])
    B = np.zeros(N + 1)
    for i in range(0, N - 1):
        A[i, i] = h ** 2 * q(x[i]) - h * p(x[i]) + 1
        A[i, i + 1] = h * p(x[i]) - 2
        A[i, i + 2] = 1
        B[i] = h ** 2 * f(x[i])
    # Учет кравевых условий
    A[N - 1, 0] = alpha[0] * h - alpha[1]
    A[N - 1, 1] = alpha[1]
    A[N, N - 1] = -beta[1]
    A[N, N] = beta[0] * h + beta[1]
    B[N - 1] = h * gamma[0]
    B[N] = h * gamma[1]
    # Решение исходной задачи свелось к решению матричного уравнения Ay=B
    return x, np.linalg.solve(A, B)


if __name__ == '__main__':
    # Условие задачи
    def p(x):
        return -x

    def q(x):
        return 2

    def f(x):
        return x + 1

    a = 0.9
    b = 1.2
    alpha = [1, -0.5]
    beta = [1, 0]
    gamma = np.array([2, 1])

    # Численное решение
    steps = 5
    x, y = solve(p, q, f, alpha, beta, gamma, steps)

    # Точное решение полученное с помощью wolframalpha.com
    x_exact = np.linspace(a, b, num=steps + 1)
    y_exact = 1.61517 + (1. - 0.117744*np.exp(x_exact**2/2))*x - 1.11517*x_exact**2 + (-0.14757 + 0.14757*x_exact**2)*erfi(x_exact/np.sqrt(2))

    # Строим графики
    marker = '.' if steps < 20 else None
    plt.plot(x, y, label='Numerical', marker=marker)
    plt.plot(x_exact, y_exact, label='Exact')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid()
    plt.legend()
    plt.show()
