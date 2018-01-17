"""
Реализация метода конечных элементов (finite element method) для решения краевой задачи

y''+p(x)*y'+q(x)*y=f(x)

k00*y(a)+k01*y'(a)=A0
k10*y(b)+k11*y'(b)=A1

или в матричном виде
K*Y=R
где
K = [k00, k01;
     k10, k11]
Y = [y(a), y(b);
     y'(a), y'(b)]
R = [R0, R1]T


y''-xy'+2y=x+1, y(0,9)-0.5y'(0,9)=2, y(1,2)=1
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfi
from scipy.integrate import quad


def N(x, i, X):
    if x[i-1] <= X <= x[i]:
        return (X - x[i-1])/(x[i] - x[i-1])
    elif x[i] <= X <= x[i+1]:
        return (x[i+1] - X)/(x[i+1] - x[i])
    else:
        return 0


def dN(x, i, j):
    if i == j:
        return -1/(x[i+1] - x[i])
    elif i == j+1:
        return 1/(x[i] - x[i-1])
    else:
        return 0



def solve(p, q, f, alpha, beta, gamma, M):
    x = np.linspace(a, b, M+1)
    A = np.zeros([M + 1, M + 1])
    B = np.zeros(M+1)

    for i in range(M):
        m = i

        fi = [
            lambda X: dN(x, m, i) ** 2 - N(x, m, X) * (p(X) * dN(x, m, i) + q(X) * N(x, m, X)),
            lambda X: dN(x, m, i) * dN(x, m + 1, i) - N(x, m, X) * (p(X) * dN(x, m + 1, i) + q(X) * N(x, m + 1, X)),
            lambda X: dN(x, m + 1, i) * dN(x, m, i) - N(x, m + 1, X) * (p(X) * dN(x, m, i) + q(X) * N(x, m, X)),
            lambda X: dN(x, m + 1, i) ** 2 - N(x, m + 1, X) * (p(X) * dN(x, m + 1, i) + q(X) * N(x, m + 1, X)),
        ]

        A[i, i] += quad(fi[0], x[m], x[m+1])[0]
        A[i, i+1] += quad(fi[1], x[m], x[m+1])[0]
        A[i+1, i] += quad(fi[2], x[m], x[m+1])[0]
        A[i+1, i+1] += quad(fi[3], x[m], x[m+1])[0]

    B = np.zeros(M + 1)

    if beta[0] != 0 and beta[1] != 0:
        for m in range(M):
            B[m] += -quad(lambda X: N(x, m, X) * f(X), x[m], x[m+1])[0]
            B[m + 1] += -quad(lambda X: N(x, m + 1, X) * f(X), x[m], x[m+1])[0]

        A[0, 0] -= alpha[0] / beta[0]
        A[M, M] += alpha[1] / beta[1]
        B[0] -= gamma[0] / beta[0]
        B[M] += gamma[1] / beta[1]

        u = np.linalg.solve(A, B)
        y = np.zeros(len(x))
        for i, X in enumerate(x):
            y[i] = np.sum([u[m]*N(x, m, X) for m in range(M+1)])
        return x, y
    A = A[:-1, :-1]
    B = B[:-1]
    u = np.linalg.solve(A, B)
    y = []
    for i, X in enumerate(x):
      y.append(np.sum([u[m] * N(x, m, X) for m in range(M+1)]))
    return x, np.append(y, [gamma[1]])


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

    # Точное решение
    x_exact = np.linspace(a, b, num=steps + 1)
    y_exact = 1.61517 + (1. - 0.117744 * np.exp(x_exact ** 2 / 2)) * x - 1.11517 * x_exact ** 2 + (
      -0.14757 + 0.14757 * x_exact ** 2) * erfi(x_exact / np.sqrt(2))

    # Строим графики
    marker = '.' if steps < 20 else None
    plt.plot(x, y, label='Numerical', marker=marker)
    plt.plot(x_exact, y_exact, label='Exact')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid()
    plt.legend()
    plt.show()
