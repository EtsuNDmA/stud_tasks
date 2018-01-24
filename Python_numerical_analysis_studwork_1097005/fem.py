"""
Реализация метода конечных элементов (finite element method) для решения краевой задачи

y''+p(x)*y'+q(x)*y=f(x)

alpha0*y(a)+beta0*y'(a)=gamma0
alpha1*y(b)+beta1*y'(b)=gamma1

y''-xy'+2y=x+1, y(0.9)-0.5y'(0.9)=2, y(1.2)=1
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfi
from scipy.integrate import quad


def phi(x, i, X):
    """Базисные функции"""
    if i > 0 and x[i-1] <= X <= x[i]:
        return (X - x[i-1])/(x[i] - x[i-1])
    elif i < len(x) - 1 and x[i] <= X <= x[i+1]:
        return (x[i+1] - X)/(x[i+1] - x[i])
    else:
        return 0


def dphi(x, i, X):
    """Производные базисных функций"""
    if i > 0 and x[i-1] <= X <= x[i]:
        return 1/(x[i] - x[i-1])
    elif  i < len(x) - 1 and x[i] <= X <= x[i+1]:
        return -1/(x[i+1] - x[i])
    else:
        return 0



def solve(p, q, f, alpha, beta, gamma, M):
    """Решатель"""
    x = np.linspace(a, b, M+1)
    A = np.zeros([M + 1, M + 1])
    B = np.zeros(M+1)
    # Рассчитываем матрицу жесткости А
    for i in range(M):
        m = i

        A_ = [
            lambda X: -dphi(x, m, X)**2
                      + p(X)*dphi(x, m, X)*phi(x, m, X)
                      + q(X)*phi(x, m, X)**2,
            lambda X: -dphi(x, m, X)*dphi(x, m+1, X)
                      + p(X)*phi(x, m, X)*dphi(x, m+1, X)
                      + q(X)*phi(x, m, X)*phi(x, m+1, X),
            lambda X: -dphi(x, m+1, X)*dphi(x, m, X)
                      + p(X)*phi(x, m+1, X)*dphi(x, m, X)
                      + q(X)*phi(x, m+1, X)*phi(x, m, X),
            lambda X: -dphi(x, m+1, X)**2
                      + p(X)*dphi(x, m+1, X)*phi(x, m+1, X)
                      + q(X)*phi(x, m+1, X)**2,
        ]

        A[i, i] += quad(A_[0], x[m], x[m+1])[0]
        A[i, i+1] += quad(A_[1], x[m], x[m+1])[0]
        A[i+1, i] += quad(A_[2], x[m], x[m+1])[0]
        A[i+1, i+1] += quad(A_[3], x[m], x[m+1])[0]
        

    B = np.zeros(M + 1)
    for m in range(M):
        B[m] += quad(lambda X: phi(x, m, X) * f(X), x[m], x[m+1])[0]
        B[m+1] += quad(lambda X: phi(x, m+1, X) * f(X), x[m], x[m+1])[0]
    
    # Различные типы краевых условий обрабатываем каждый по своему
    # Задача сводится к решению системы алгебраических уравнений Au=B
    # Где ui - решения задачи в узлах сетки
    if beta[0] != 0 and beta[1] != 0:
        B[0] += gamma[0]/beta[0]
        B[-1] -= gamma[1]/beta[1]
        A[0,0] += alpha[0]/beta[0]
        A[-1, -1] -= alpha[1]/beta[1]
        u = np.linalg.solve(A, B)
    elif beta[0] == 0 and beta[1] != 0:
        B = B[1:]
        B[0] -= A[1, 0] * gamma[0]
        B[-1] -= gamma[1]/beta[1]
        A = A[1:, 1:]
        A[-1, -1] -= alpha[1]/beta[1]
        u_ = np.linalg.solve(A, B)
        u = np.append([gamma[0]], u_)
    elif beta[0] != 0 and beta[1] == 0:
        B = B[:-1]
        B[-1] -= A[-2, -1] * gamma[1]
        B[0] += gamma[0]/beta[0]
        A = A[:-1, :-1]
        A[0,0] += alpha[0]/beta[0]
        u_ = np.linalg.solve(A, B)
        u = np.concatenate([u_, [gamma[1]]])
    else:
        B = B[1:-1]
        B[0] -= A[1, 0] * gamma[0]
        B[-1] -= A[-2, -1] * gamma[1]
        A = A[1:-1, 1:-1]
        u_ = np.linalg.solve(A, B)
        u = np.concatenate([[gamma[0]], u_, [gamma[1]]])
        
    y = np.zeros(len(x))
    for i, X in enumerate(x):
        y[i] = np.sum([U*phi(x, m, X) for m, U in enumerate(u)])
    print(A)
    print(B)
    print(u)
    print(y)
    return x, y


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
    alpha = [1, 1]
    beta = [-0.5, 0]
    gamma = np.array([2, 1])
    # Численное решение
    elements = 3
    x, y = solve(p, q, f, alpha, beta, gamma, elements)

    # Точное решение полученное с помощью wolframalpha.com
    x_exact = np.linspace(a, b, num=20)
    y_exact = 1.61517 + (1. - 0.117744*np.exp(x_exact**2/2))*x_exact - 1.11517*x_exact**2 + (-0.14757 + 0.14757*x_exact**2)*erfi(x_exact/np.sqrt(2))

    # Строим графики
    marker = '.' if elements < 20 else None
    plt.plot(x, y, label='Numerical', marker=marker)
    plt.plot(x_exact, y_exact, label='Exact')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid()
    plt.legend()
    plt.show()
