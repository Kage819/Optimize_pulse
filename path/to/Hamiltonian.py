import numpy as np
from data import n,sigmaI,sigmax,sigmay,sigmaz
from sympy.physics.quantum import TensorProduct

# Iのｎ回テンソル積をとるメソッド
def I(n):
    res = sigmaI
    for i in range(1,n):
        res = TensorProduct(res,sigmaI)
    return res



#スピン数をいれたらZZを計算するメソッド
"""
n=4のとき, ZZII + ZIZI + ZIIZ + IZZI + IZIZ + IIZZ　を計算する
"""
def ZZ(n):
    for i in range(n-1):
        if i == 0:
            pre = sigmaz
        else:
            pre = TensorProduct(I(i),sigmaz)
        for j in range(i+1,n):
            sa = j - i
            if sa == 1:
                pre_ = TensorProduct(pre,sigmaz)
                if n-j-1 != 0:
                    pre_ = TensorProduct(pre_,I(n-j-1))
            else:
                pre_ = TensorProduct(pre,I(sa-1),sigmaz)
                if n-j-1 != 0:
                    pre_ = TensorProduct(pre_,I(n-j-1))
            if j == 1:
                res = pre_
            else:
                res += pre_
    return res/4


def XX(n):
    for i in range(n-1):
        if i == 0:
            pre = sigmax
        else:
            # print(i)
            pre = TensorProduct(I(i),sigmax)
            # print(pre)
            # print(len(pre))
        for j in range(i+1,n):
            sa = j - i
            if sa == 1:
                pre_ = TensorProduct(pre,sigmax)
                #ここ修正 I(n-j)　→ I(n-j-1)
                if n-j-1 != 0:
                    pre_ = TensorProduct(pre_,I(n-j-1))
            else:
                pre_ = TensorProduct(pre,I(sa-1),sigmax)
                if n-j-1 != 0:
                    pre_ = TensorProduct(pre_,I(n-j-1))
            if j == 1:
                res = pre_
                # print(i)
                # print(j)
                # print(len(res))
            else:
                # print(i)
                # print(j)
                # print(len(pre_))
                res += pre_
                # print(res)
    return res/4


def YY(n):
    for i in range(n-1):
        if i == 0:
            pre = sigmay
        else:
            # print(i)
            pre = TensorProduct(I(i),sigmay)
            # print(pre)
            # print(len(pre))
        for j in range(i+1,n):
            sa = j - i
            if sa == 1:
                pre_ = TensorProduct(pre,sigmay)
                #ここ修正 I(n-j)　→ I(n-j-1)
                if n-j-1 != 0:
                    pre_ = TensorProduct(pre_,I(n-j-1))
            else:
                pre_ = TensorProduct(pre,I(sa-1),sigmay)
                if n-j-1 != 0:
                    pre_ = TensorProduct(pre_,I(n-j-1))
            if j == 1:
                res = pre_
                # print(i)
                # print(j)
                # print(len(res))
            else:
                # print(i)
                # print(j)
                # print(len(pre_))
                res += pre_
                # print(res)
    return res/4


def XY(n):
    for i in range(n-1):
        if i == 0:
            pre = sigmax
        else:
            pre = TensorProduct(I(i),sigmax)
        for j in range(i+1,n):
            sa = j - i
            if sa == 1:
                pre_ = TensorProduct(pre,sigmay)
                if n-j-1 != 0:
                    pre_ = TensorProduct(pre_,I(n-j-1))
            else:
                pre_ = TensorProduct(pre,I(sa-1),sigmay)
                if n-j-1 != 0:
                    pre_ = TensorProduct(pre_,I(n-j-1))
            if j == 1:
                res = pre_
            else:
                res += pre_
    return res/4

def XZ(n):
    for i in range(n-1):
        if i == 0:
            pre = sigmax
        else:
            pre = TensorProduct(I(i),sigmax)
        for j in range(i+1,n):
            sa = j - i
            if sa == 1:
                pre_ = TensorProduct(pre,sigmaz)
                if n-j-1 != 0:
                    pre_ = TensorProduct(pre_,I(n-j-1))
            else:
                pre_ = TensorProduct(pre,I(sa-1),sigmaz)
                if n-j-1 != 0:
                    pre_ = TensorProduct(pre_,I(n-j-1))
            if j == 1:
                res = pre_
            else:
                res += pre_
    return res/4

def YZ(n):
    for i in range(n-1):
        if i == 0:
            pre = sigmay
        else:
            pre = TensorProduct(I(i),sigmay)
        for j in range(i+1,n):
            sa = j - i
            if sa == 1:
                pre_ = TensorProduct(pre,sigmaz)
                if n-j-1 != 0:
                    pre_ = TensorProduct(pre_,I(n-j-1))
            else:
                pre_ = TensorProduct(pre,I(sa-1),sigmaz)
                if n-j-1 != 0:
                    pre_ = TensorProduct(pre_,I(n-j-1))
            if j == 1:
                res = pre_
            else:
                res += pre_
    return res/4

# \sum^n_i I^i_xを計算するメソッド
#つまり、n=4のとき　XIII + IXII + IIXI + IIIX　を計算する
def Ix(n):
    for i in range(n):
        if i == 0:
            pre = sigmax
            res = TensorProduct(pre,I(n-1))
        else:
            pre = TensorProduct(I(i),sigmax)
            if n-i-1 != 0:
                res += TensorProduct(pre,I(n-i-1))
            else:
                res += pre
    return res

def Iy(n):
    for i in range(n):
        if i == 0:
            pre = sigmay
            res = TensorProduct(pre,I(n-1))
        else:
            pre = TensorProduct(I(i),sigmay)
            if n-i-1 != 0:
                res += TensorProduct(pre,I(n-i-1))
            else:
                res += pre
    return res

def Iz(n):
    for i in range(n):
        if i == 0:
            pre = sigmaz
            res = TensorProduct(pre,I(n-1))
        else:
            pre = TensorProduct(I(i),sigmaz)
            if n-i-1 != 0:
                res += TensorProduct(pre,I(n-i-1))
            else:
                res += pre
    return res

#ダガーを計算するメソッド
def dagger(matrix):
    a = np.conj(matrix)
    a = a.T
    return a