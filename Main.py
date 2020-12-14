from data import d,sf,n,T1,M,dt,tlist
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


#ダイポール - ダイポールのハミルトニアン
Hdd = d*(2*ZZ(n) - (XX(n) + YY(n)))


#理想ハミルトニアン
Hideal = d*(YY(n) - XX(n))


#ラジオ波のハミルトニアンを計算
# hamil = Hamiltonian1(Fvxmy,Fvymy)
hamil = Hamiltonian1(fvx8,fvy8)

Hsys = [hamil[i] + Hdd for i in range(M)]

#U_nU_{n-1}･･･U2U1 の計算
U = Ulist1(Hsys)



#各時間刻みでの理想ハミルトニアンによるユニタリ発展を計算
Utarget = Uideal(Hideal,T1)

#Fidelityを計算
Result = Fidelity(U,Utarget)
print(Result)
# np.save("sf-Fidelity_d-100k_opt_pulse_without_error_60us_1202.npy",Result)


ax = plt.gca()
tlist = np.linspace(0,T1,len(Result))
tlist = tlist/T1
print(tlist)
print(tlist[np.argmin(Result)])
print(min(Result))
ax.set_yscale('log')
plt.plot(tlist,Result,label="Fidelity")
plt.legend(bbox_to_anchor=(1.05,1),loc="upper left",borderaxespad=0,fontsize=18)
# pylab.savefig("time-Fidelity_d-100k_opt_pulse_1202",bbox_inches="tight")
plt.show()
