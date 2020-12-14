from data import d,sf,n,T1,M,dt,e1,e2,e3,e4,theta
from Hamiltonian import ZZ, XX, YY
from OptPulse import Fvxmy,Fvymy,Ulist1,tHamil,Hamiltonian1
from pulse8 import fvx8,fvy8
from Ideal import Uideal
from Fidelity import Fidelity,Fidelity_for_error
import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import expm
import pylab
import os
from error import pulse_with_error,phase_with_error


# sf = 0.7747747747747749　　#sf of opt_pulse
# sf = 0.7995799579957995 #sf of old_pulse
sf = 0.9993999399939993  # sf of 8pulse

#結合定数のリスト
dlist = [15,20,25]

result_with_error = np.zeros((len(e1),len(theta)))
for j in range(len(dlist)):
    #ダイポール - ダイポールのハミルトニアン
    Hdd = dlist[j]*(2*ZZ(n) - (XX(n) + YY(n)))*1e3

    #理想ハミルトニアン
    Hideal = dlist[j]*(YY(n) - XX(n)) * sf*1e3


    #各時間刻みでの理想ハミルトニアンによるユニタリ発展を計算
    Utarget = Uideal(Hideal,T1)


    result = []
    print(j)
    for i in range(len(e1)):
        fvx_with_error,fvy_with_error = pulse_with_error(fvx8,fvy8,e1[i],e2,e3[i],e4)#パルス強度に関するエラーを与える
        for k in range(len(theta)):
            print(i,k)
            fvx_with_error_, fvy_with_error_ = phase_with_error(fvx_with_error,fvy_with_error,theta[k])#位相に関するエラーを与える
            hamil = Hamiltonian1(fvx_with_error_,fvy_with_error_)
            Hsys = [hamil[n] + Hdd for n in range(M)]
            U = Ulist1(Hsys)
            Result = Fidelity_for_error(U,Utarget)
            result_with_error[i,k] = Result
            print(Result)
    print(result)
    np.save("8pulse_result_with_error_d"+str(dlist[j])+"k_1214.npy",result_with_error)
plt.show()
