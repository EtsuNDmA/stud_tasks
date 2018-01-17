
# coding: utf-8
import numpy as np
import scipy.integrate as spint
from matplotlib import pyplot

a, b = 0,1.0
alf_1, btt_1, gmm_1 = 1, 1e-17, 1
alf_2, btt_2, gmm_2 = 1, 1e-17, -1
M = 8  
x = [a + i*(b-a)/M for i in range(M+1)]

def P(x):
    return 1
def q(x):
    return -12
def phi(x): 
    return x*x
def int_f(f, m):
    return spint.quad(f, x[m], x[m+1])[0]


def N(m, xx):
    if x[m-1] <= xx <= x[m]:
        return (xx - x[m-1])/(x[m] - x[m-1])
    elif x[m] <= xx <= x [m+1]:
        return (x[m+1] - xx)/(x[m+1] - x[m])
    else: return 0

def dN(m, e):
    if m == e:
        return -1/(x[m+1] - x[m])
    elif m == e+1:
        return 1/(x[m] - x[m-1])

def res(u, k=M+1):
    y = []
    x = np.linspace(a, b, k)
    for i in x:
        u_ = 0
        for m in range(M+1):
            u_ += u[m]*N(m, i)
        y.append(u_)
    return x, y

def solve():
    u = np.zeros([M+1, M+1])
    for e in range(M):
        m = e
        u[e, e] += int_f(lambda xx: dN(m, e)**2 - N(m, xx)*(P(xx)*dN(m, e)+q(xx)*N(m, xx)), m)
        u[e, e+1] += int_f(lambda xx: dN(m, e)*dN(m+1, e) - N(m, xx)*(P(xx)*dN(m+1, e)+q(xx)*N(m+1, xx)), m)
        u[e+1, e] += int_f(lambda xx: dN(m+1, e)*dN(m, e) - N(m+1, xx)*(P(xx)*dN(m, e)+q(xx)*N(m, xx)), m)
        u[e+1, e+1] += int_f(lambda xx: dN(m+1, e)**2 - N(m+1, xx)*(P(xx)*dN(m+1, e)+q(xx)*N(m+1, xx)), m)

    f = np.zeros(M+1)


    if btt_1 != 0 and btt_2 != 0:
        for m in range(M):
            f[m] += -int_f(lambda xx: N(m, xx)*phi(xx), m)
            f[m+1] += -int_f(lambda xx: N(m+1, xx)*phi(xx), m)
        f[0] -= gmm_1/btt_1
        f[M] += gmm_2/btt_2

        u[0,0] -= alf_1/btt_1
        u[M,M] += alf_2/btt_2

        y = np.linalg.solve(u, f)

        return y


        return np.append([gmm_1], y)
        
        u = u[:-1, :-1]
        f = f[:-1]
        print(u)
        print(f)
        y = np.linalg.solve(u, f)

        return np.append(y, [gmm_2])

sol = res(solve()) 
pyplot.plot(sol[0], sol[1], color='r', label='МКЭ разбиение на 5')

size = 4
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
pyplot.title('8 точек')
pyplot.show()


