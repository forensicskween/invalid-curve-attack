"""Adapted from HTB Challenge 400 Curves - https://app.hackthebox.com/challenges/368 written by WizardAlfredo https://app.hackthebox.com/users/201215"""

from Crypto.Util.number import inverse
import random

a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff

random.seed('i_love_crypto')
secret = random.getrandbits(255)

E = {'a': a, 'b': b, 'p': p}

def add(P, Q, E):
    if (P == (0, 0)):
        return Q
    elif (Q == (0, 0)):
        return P
    else:
        Ea, Ep = E['a'], E['p']
        x1, y1 = P
        x2, y2 = Q
        if ((x1 == x2) & (y1 == -y2)):
            return ((0, 0))
        else:
            if (P != Q):
                l = (y2 - y1) * inverse(x2 - x1, Ep)
            else:
                l = (3 * (x1**2) + Ea) * inverse(2 * y1, Ep)
        x3 = ((l**2) - x1 - x2) % Ep
        y3 = (l * (x1 - x3) - y1) % Ep
        return x3, y3


def multiply(P, n, E):
    Q = P
    R = (0, 0)
    while (n > 0):
        if (n % 2 == 1):
            R = add(R, Q, E)
        Q = add(Q, Q, E)
        n = n // 2
    return R

def server_oracle(C):
    try:
        x, y = [int(i) for i in C]
        S = multiply((x, y), secret, E)
        return S 
    except:
        return None
