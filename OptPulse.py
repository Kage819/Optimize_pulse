import numpy as np
from data import M,tlist,T1,dt,n
from Hamiltonian import Ix, Iy,Iz,dagger,I
from copy import deepcopy
from scipy.linalg import expm
from sympy.physics.quantum import TensorProduct

#実験で使用したパルス
pulse1 = np.array([ 6.21597777e+00,  5.36694385e+00, -1.14302580e+00, -3.86576606e-01,
        6.43805043e-01,  4.85145566e-01, -2.87440737e-01, -1.21517790e+00,
       -1.56504259e+00, -6.48749414e-01, -3.17065381e+00,  9.27122455e-01,
       -6.39716761e-01, -8.96693527e-01,  3.47838118e+00, -1.29713162e+00,
        1.73450606e+00, -1.19044269e-01,  1.09794646e+00, -4.42620940e-03,
        6.83051136e-01, -3.87918364e+00,  1.64772630e-01,  3.10393046e+00,
        2.71449895e+00, -8.78970307e-01,  7.40705429e-01,  6.88812722e-01,
       -1.88616064e+00,  3.63184498e+00,  4.40115174e-01, -2.28542655e+00,
       -6.62606647e-01, -3.99838333e-01,  6.65898935e-01, -3.00834380e+00,
       -1.55987661e+00,  5.82022646e-01, -6.17565906e-01, -6.13967025e-01])
Nmine = 20


#エラーを考慮して得た最適化パルス
pulse1 = np.array([ 16.60820624,  -8.72890604,  -3.67009343, -13.72420496,
        -0.09953142,  -4.39913277, -10.12010491,   3.7337205 ,
        -2.73533412,  -6.45641815,   5.7202312 ,  -3.07167833,
        -4.41212257,   0.26602957,   2.90161181,  -5.85075018,
        -1.43708625,   0.17935866,  -7.24154305,   9.75845701,
        -7.94105325,  -1.52080128,   5.60143324,  -5.15544351,
         5.89999033,   1.22978401,  -9.07040322,   0.32234189,
         1.15099866,  -1.13624081,   6.92629515,   6.99486719,
        -4.33358343,   2.72271662,  -1.21645636,   1.84571508,
        -8.58906775,   3.13720432,  -1.91366915,   5.20720034,
         3.19020651,  -7.44247501])

Nmine = 21



myvx1 = pulse1[:Nmine]
myvy1 = pulse1[Nmine:]

myvxopt = deepcopy(myvx1)/T1
myvyopt = deepcopy(myvy1)/T1

#最適化パルス(I成分)を生成するメソッド
def myFvx1(vx):
    Fvxlist = []
    omega_xlist = np.zeros((Nmine,M))
    for i in range(Nmine):
        omegax_n = vx[i]*np.sin(2*(i+1)*np.pi*tlist/T1)
        omega_xlist[i,:] = omegax_n
    Fvxlist = np.sum(omega_xlist, axis=0)
    return Fvxlist

#最適化パルス(Q成分)を生成するメソッド
def myFvy1(vy):
    Fvylist = []
    omega_ylist = np.zeros((Nmine,M))
    for i in range(Nmine):
        omegay_n = vy[i]*np.sin(2*(i+1)*np.pi*tlist/T1)
        omega_ylist[i,:] = omegay_n
    Fvylist = np.sum(omega_ylist, axis=0)
    return Fvylist

#I成分とQ成分を入れたら、ラジオ波のハミルトニアンを計算するメソッド
def Hamiltonian1(Fvx,Fvy):
    alist = []
    for i in range(M):
        a = (np.array(Ix(n)) * Fvx[i]/2 + np.array(Iy(n)) * Fvy[i]/2)
        alist.append(a)
    return alist

#平均ハミルトニアン理論を用いて、ラジオ波のユニタリ行列を計算するメソッド
#最終的にU_MU_{M-1} \cdots U_2U_1U_0を計算する
def Ulist1(Hamil):
    Ulist3 = []
    """
    Ulist3には各時間刻みでのユニタリ行列が格納される
    Ulist3[t] = U_tU_{t-1}\cdtos U_2U_1U_0
    """
    for i in range(M):
        # print(i)
        U = -Hamil[i]*1j*dt
        U = expm(U)
        Ulist3.append(U)
        if i >= 1:
            aa = np.dot(Ulist3[i],Ulist3[i-1])
            Ulist3[i] = deepcopy(aa)
    return aa



#ラジオ波のI成分、Q成分を計算
Fvxmy, Fvymy = myFvx1(myvxopt), myFvy1(myvyopt)