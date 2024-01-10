import numpy as np


def weights(x: np.ndarray):
    n = len(x)
    temp = np.identity(n)
    for i in range(n):
        temp[i, i] = 1 / x[i]

    return temp


class Curve:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def conc(self, response):
        a = self.a
        b = self.b
        c = self.c - response
        return (-b + (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)

    def resp(self, conc):
        return self.a * conc ** 2 + self.b * conc + self.c


def regress(x: np.ndarray, y: np.ndarray):
    W = weights(x)
    X = np.vstack([x ** 2, x, np.ones_like(x)]).T
    Y = np.array([y]).T

    m = np.matmul

    a = m(X.T, m(W, X))
    b = m(X.T, m(W, Y))

    ans = m(np.linalg.inv(a), b)

    return Curve(ans[0, 0], ans[1, 0], ans[2, 0])
