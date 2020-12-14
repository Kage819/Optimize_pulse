import numpy as np
import matplotlib.pyplot as plt
from Hamiltonian import Ix,Iy,ZZ,YY,XX
from scipy.linalg import expm
from copy import deepcopy
from data import M,n


#pi/2パルスの間隔
delta = 3.5e-6

#pi/2パルスの幅
tau_pulse = 1.5e-6
T1 = 12*delta + tau_pulse*12

#立ち上がり時間
tatiagari = 200e-9

#時間刻み
tlist, dt = np.linspace(0,T1,M,retstep = True)
# print(dt)

def get_pulse_amplitude_x_tatiagari(t, delta, tau_pulse):
    """
    Args:  
        delta : free evolution time
        tau_pulse : pi/2 pulse width
        t: time
    Return:
        amplitude of I at time t (np.array) 
    """
    delta_dash = 2*delta + tau_pulse
    amp = 1/(tau_pulse+tatiagari)/4*2*np.pi
    print(amp/2/np.pi)
    while T1 <= t:
        t = t - T1
    if 0 <= t and t <= delta/2-tatiagari:
        return 0

    #tanzaku 1
    if delta/2-tatiagari <= t and t <= delta/2:
        # print(t-(delta/2-tatiagari))
        return amp/tatiagari*(t-(delta/2-tatiagari))
        # return amp*np.cos(k*(t-(delta/2-tatiagari))*1e9+np.pi/2)
    if delta/2 <= t and t <= delta/2+tau_pulse:
        return amp
    if delta/2+tau_pulse <= t and t <= delta/2+tau_pulse+tatiagari:
        # print(t-(delta/2+tau_pulse))
        return -amp/tatiagari*np.cos((t-(delta/2+tau_pulse))-np.pi/2)+amp

    if delta/2+tau_pulse+tatiagari <= t and t <= delta/2+tau_pulse+delta_dash-tatiagari:
        return 0
    
    #tanzaku 2
    if delta/2+tau_pulse+delta_dash-tatiagari<= t and t <= delta/2+tau_pulse+delta_dash: 
        return amp/tatiagari*(t-(delta/2+tau_pulse+delta_dash-tatiagari)) 
    if delta/2+tau_pulse+delta_dash <= t and t <= delta/2+2*tau_pulse+delta_dash: 
        return amp
    if  delta/2+2*tau_pulse+delta_dash <= t and t <= delta/2+2*tau_pulse+delta_dash+tatiagari: 
        return -amp/tatiagari*(t-(delta/2+2*tau_pulse+delta_dash))+amp
    
    if delta/2+2*tau_pulse+delta_dash <= t and t <= delta/2+2*tau_pulse+delta_dash + delta-tatiagari:
        return 0

    #tanzaku 3
    if delta/2+2*tau_pulse+delta_dash + delta-tatiagari <= t and t <= delta/2+2*tau_pulse+delta_dash + delta:
        return amp/tatiagari*(t-(delta/2+2*tau_pulse+delta_dash + delta-tatiagari)) 
    if delta/2+2*tau_pulse+delta_dash + delta <= t and t <= delta/2+3*tau_pulse+delta_dash + delta:
        return amp
    if delta/2+3*tau_pulse+delta_dash + delta <= t and t <= delta/2+3*tau_pulse+delta_dash + delta + tatiagari:
        return -amp/tatiagari*(t-(delta/2+3*tau_pulse+delta_dash + delta))+amp 

    if delta/2+3*tau_pulse+delta_dash + delta <= t and t <= delta/2+3*tau_pulse+2*delta_dash + delta-tatiagari:
        return 0
    
    #tanzaku 4
    if delta/2+3*tau_pulse+2*delta_dash + delta - tatiagari <= t and t<= delta/2+3*tau_pulse+2*delta_dash + delta:
        return amp/tatiagari*(t-(delta/2+3*tau_pulse+2*delta_dash + delta - tatiagari)) 
    if delta/2+3*tau_pulse+2*delta_dash + delta <= t and t<= delta/2+4*tau_pulse+2*delta_dash + delta:
        return amp
    if delta/2+4*tau_pulse+2*delta_dash + delta <= t and t<= delta/2+4*tau_pulse+2*delta_dash + delta + tatiagari:
        return -amp/tatiagari*(t-(delta/2+4*tau_pulse+2*delta_dash + delta))+amp 

    if delta/2+4*tau_pulse+2*delta_dash + delta <= t and t <= delta/2+4*tau_pulse+2*delta_dash + 2*delta - tatiagari:
        return 0
    
    #tanzaku 5
    if delta/2+4*tau_pulse+2*delta_dash + 2*delta-tatiagari <= t and t <= delta/2+4*tau_pulse+2*delta_dash + 2*delta:
        return -amp/tatiagari*(t-(delta/2+4*tau_pulse+2*delta_dash + 2*delta-tatiagari))
    if delta/2+4*tau_pulse+2*delta_dash + 2*delta <= t and t <= delta/2+5*tau_pulse+2*delta_dash + 2*delta:
        return -amp
    if delta/2+5*tau_pulse+2*delta_dash + 2*delta <= t and t <= delta/2+5*tau_pulse+2*delta_dash + 2*delta+tatiagari:
        return amp/tatiagari*(t-(delta/2+5*tau_pulse+2*delta_dash + 2*delta))-amp

    if delta/2+5*tau_pulse+2*delta_dash + 2*delta <= t and t <= delta/2+5*tau_pulse+3*delta_dash + 2*delta-tatiagari:
        return 0
    
    #tanzaku 6
    if delta/2+5*tau_pulse+3*delta_dash + 2*delta-tatiagari <= t and t <= delta/2+5*tau_pulse+3*delta_dash + 2*delta:
        return -amp/tatiagari*(t-(delta/2+5*tau_pulse+3*delta_dash + 2*delta-tatiagari))
    if delta/2+5*tau_pulse+3*delta_dash + 2*delta <= t and t <= delta/2+6*tau_pulse+3*delta_dash + 2*delta:
        return -amp
    if delta/2+6*tau_pulse+3*delta_dash + 2*delta <= t and t <= delta/2+6*tau_pulse+3*delta_dash + 2*delta+tatiagari:
        return amp/tatiagari*(t-(delta/2+6*tau_pulse+3*delta_dash + 2*delta))-amp

    if delta/2+6*tau_pulse+3*delta_dash + 2*delta <= t and t <= delta/2+6*tau_pulse+3*delta_dash + 3*delta-tatiagari:
        return 0
    
    #tanzaku 7
    if delta/2+6*tau_pulse+3*delta_dash + 3*delta-tatiagari <= t and t <= delta/2+6*tau_pulse+3*delta_dash + 3*delta:
        return -amp/tatiagari*(t-(delta/2+6*tau_pulse+3*delta_dash + 3*delta-tatiagari))
    if delta/2+6*tau_pulse+3*delta_dash + 3*delta <= t and t <= delta/2+7*tau_pulse+3*delta_dash + 3*delta:
        return -amp
    if delta/2+7*tau_pulse+3*delta_dash + 3*delta <= t and t <= delta/2+7*tau_pulse+3*delta_dash + 3*delta+tatiagari:
        return amp/tatiagari*(t-(delta/2+7*tau_pulse+3*delta_dash + 3*delta))-amp

    if delta/2+7*tau_pulse+3*delta_dash + 3*delta <= t and t <= delta/2+7*tau_pulse+4*delta_dash + 3*delta-tatiagari:
        return 0

    #tanzaku 8
    if delta/2+7*tau_pulse+4*delta_dash + 3*delta-tatiagari <= t and t <= delta/2+7*tau_pulse+4*delta_dash + 3*delta:
        return -amp/tatiagari*(t-(delta/2+7*tau_pulse+4*delta_dash + 3*delta-tatiagari))
    if delta/2+7*tau_pulse+4*delta_dash + 3*delta <= t and t <= delta/2+8*tau_pulse+4*delta_dash + 3*delta:
        return -amp
    if delta/2+8*tau_pulse+4*delta_dash + 3*delta <= t and t <= delta/2+8*tau_pulse+4*delta_dash + 3*delta+tatiagari:
        return amp/tatiagari*(t-(delta/2+8*tau_pulse+4*delta_dash + 3*delta))-amp
    else:
        return 0



def get_pulse_amplitude_y(t):
    return 0

fvx8 = []
fvy8 = []
for i in range(len(tlist)):
    fvx8.append(get_pulse_amplitude_x_tatiagari(tlist[i],delta,tau_pulse))
    fvy8.append(get_pulse_amplitude_y(tlist[i]))
