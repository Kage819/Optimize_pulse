"""
ロバストネス最適化パルスの最適化
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm
from copy import deepcopy
from sympy.physics.quantum import TensorProduct
from operator import mul
from scipy.optimize import minimize
import datetime

dt_now = datetime.datetime.now()
print(dt_now)
start_hour = dt_now.hour
start_minute = dt_now.minute

# from Hamiltonian import Ix,Iy,ZZ,YY,XX,XY,XZ,YZ,I,Iz
# from data import Nmine,M,n,d,sf,tlist,dt,sigmaI,sigmax,sigmay,sigmaz,T1
from data import sigmaI,sigmax,sigmay,sigmaz,M,Nmine

#最適化時間の規格化
T1 = 1
#scaling factor
sf = 0.43
#時間刻み
tlist, dt = np.linspace(0,T1,M,retstep = True)
#エラーコスト関数の重み係数
weight = 1/10

# #ランダム生成
vx1 = np.random.randint(-10, 10, (1, Nmine))
vy1 = np.random.randint(-10, 10, (1, Nmine))  # -10以上10未満の整数乱数
vxopt = vx1[0]
vyopt = vy1[0]
#ランダム生成された初期値
initial_v = np.concatenate((vxopt, vyopt))

#パルスのI成分
def Fvx (vx):
    Fvxlist = []
    omega_xlist = np.zeros((Nmine,M))
    for i in range(Nmine):
        omegax_n = vx[i]*np.sin(2*(i+1)*np.pi*tlist/T1)
        omega_xlist[i,:] = omegax_n
    Fvxlist = np.sum(omega_xlist, axis=0)
    return Fvxlist   

#パルスのQ成分
def Fvy (vy):
    Fvylist = []
    omega_ylist = np.zeros((Nmine,M))
    for i in range(Nmine):
        omegay_n = vy[i]*np.sin(2*(i+1)*np.pi*tlist/T1)
        omega_ylist[i,:] = omegay_n
    Fvylist = np.sum(omega_ylist, axis=0)
    return Fvylist


#制御ハミルトニアン
def Hamiltonian(Fvx,Fvy):
    alist = []
    for i in range(M):
        a = (sigmax * Fvx[i]/2 + sigmay * Fvy[i] /2)
        alist.append(a)
    return alist

#ユニタリ発展
def Ulist(Hamil):
    Ulist3 = []
    """
    Ulist3には各時間刻みでのユニタリ行列が格納される
    Ulist3[t] = U_tU_{t-1}\cdtos U_2U_1U_0
    """
    for i in range(M):
        # print(i)
        U = Hamil[i]*1j*dt
        U = expm(U)
        Ulist3.append(U)
        if i >= 1:
            aa = np.dot(Ulist3[i],Ulist3[i-1])
            Ulist3[i] = deepcopy(aa)
    return Ulist3


def Udagger(Ulist):
    Ulist1 = []
    for i in range(M):
        a = Ulist[i].T
        a = np.conj(a)
        Ulist1.append(a)
    return Ulist1  

#system compile matrix
def get_c_list(vx, vy, t_list):
    """
    Args:  
        fx : get_amplitude_x
        fy : get_amplitude_y
        t_list : time list
    Return:
        numpy array of shape (3,3,len(t_list))
    """
    c_list = []
    pauli_list = [sigmax, sigmay, sigmaz]
    URF_list = Ulist(Hamiltonian(Fvx(vx),Fvy(vy)))
    c_list = np.zeros((3,3,len(t_list)), dtype=np.complex128)
    for beta in range(3):
        for alpha in range(3):
            sigma_alpha = pauli_list[alpha]
            sigma_beta = pauli_list[beta]
            for t in range(len(t_list)):
                c_list[beta, alpha, t] = \
                    np.einsum("ij, jk, kl, li",
                              URF_list[t].conj().T, sigma_alpha, URF_list[t], sigma_beta)/(len(sigmaz))
    return c_list



def get_eta(vx, vy, t_list):
    """
    minegishi 修論のetaを計算する関数
    Args:
        Args:  
        fx : get_amplitude_x
        fy : get_amplitude_y
        t_list : time list
    Return:
        eta at time T 
    """
    # t_list, dt = np.linspace(0,T,n_steps,retstep=True)
    c_list = get_c_list(vx, vy, t_list)
    eta = np.zeros((3,3))
    for beta in range(3):
        for gamma in range(3):
            eta[beta, gamma] = np.sum(c_list[beta,2]*c_list[gamma,2] -
                                      c_list[beta,1]*c_list[gamma,1]/2 - 
                                      c_list[beta,0]*c_list[gamma,0]/2)*dt
    return eta


# error cost function
def get_error_part(vx,vy):
    fvx,fvy = Fvx(vx),Fvy(vy)
    C_list = get_c_list(vx,vy,tlist)
    res = []
    for j in range(3):
        res.append(np.abs(np.dot(fvx,C_list[j,0])*dt)**2)
        res.append(np.abs(np.dot(fvx,C_list[j,1])*dt)**2)
        res.append(np.abs(np.dot(fvy,C_list[j,0])*dt)**2)
        res.append(np.abs(np.dot(fvy,C_list[j,1])*dt)**2)
    # print(res)
    return np.array(res)*(weight**2)

cost = np.zeros(9).reshape(3,3)
def target(sf):
    cost[2,2] = sf
    return cost

#generate cost function
def cost_function(paramater):
    vx = paramater[:Nmine]
    vy = paramater[Nmine:]
    e = get_eta(vx,vy,tlist)
    error_part = get_error_part(vx,vy)
    print(e)
    dd = (target(sf)-e)**2 
    dd = np.sum(dd) + np.sum(error_part)
    return dd


#最適化時にコスト関数の値を呼び出し
def callback(param):
    print(cost_function(param))

# #制約を与える
seiyaku = 2*np.pi*220e3
cons=({'type': 'ineq',
       'fun': lambda x: seiyaku - max(np.sqrt(Fvx(x[:Nmine]/60e-6)**2+Fvy(x[Nmine:]/60e-6)**2))})

# #最適化スタート
zz = minimize(cost_function,initial_v, constraints=cons,method = 'SLSQP', callback=callback)
print(zz)