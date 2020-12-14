from data import d,sf,n,T1,M,dt
from Hamiltonian import ZZ, XX, YY
from OptPulse import Fvxmy,Fvymy,Ulist1,tHamil,Hamiltonian1
from pulse8 import fvx8,fvy8
from Ideal import Uideal
from Fidelity import Fidelity_for_error
import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import expm
import pylab
import os
d_list = np.arange(1e3,16e3,2e3)
print(d_list)

# sf = 0.7747747747747749　　#sf of opt_pulse
# sf = 0.7995799579957995 #sf of old_pulse
sf = 0.9993999399939993  # sf of 8pulse

#ダイポール - ダイポールのハミルトニアン
Hdd = (2*ZZ(n) - (XX(n) + YY(n))) 
#理想ハミルトニアン
Hideal = (YY(n) - XX(n)) * sf

#ラジオ波のハミルトニアンを計算
hamil = Hamiltonian1(Fvxmy,Fvymy)
# hamil = Hamiltonian1(fvx8,fvy8)

result = []
for i in range(len(d_list)):
    print(d_list[i])
    Hdd_ = Hdd * d_list[i]
    Hsys = [hamil[i] + Hdd_ for i in range(M)]
    U = Ulist1(Hsys)
    Hideal_ = d_list[i] * Hideal
    Utarget = Uideal(Hideal_,T1)
    Result = Fidelity_for_error(U,Utarget)
    print(Result)
    result.append(Result)
print(result)
np.save("d-fidelit_60us_opt_pulse_with_sf_1211.npy",result)
plt.scatter(d_list,result)
plt.show()
