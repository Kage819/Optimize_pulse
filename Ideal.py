import numpy as np
from data import M,tlist,d,n
from scipy.linalg import expm
from Hamiltonian import XX, YY,dagger
import matplotlib.pyplot as plt

#理想ハミルトニアンの時間発展.照射時間のユニタリ発展を計算するメソッド
def Uideal(Hamil,T):
    rList = []
    tlist2 = np.linspace(0,T,M) 
    for i in range(M):
        kata = -1j * Hamil * tlist2[i]
        rList.append(expm(kata))
    return rList
