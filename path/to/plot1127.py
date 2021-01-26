import numpy as np
from data import tlist,T1,e1,e2,theta
import matplotlib.pyplot as plt
import pylab
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib.colors import Normalize
import os

# d_list = np.arange(1e3,16e3,2e3)
# opt = np.load("d-fidelit_60us_opt_pulse_with_sf_1210.npy")
# old = np.load("d-fidelit_60us_old_pulse_with_sf_1210.npy")
# pul8 = np.load("d-fidelit_60us_8pulse_with_sf_1210.npy")
# plt.scatter(d_list,opt,label='opt')
# plt.scatter(d_list,pul8,label="8pulse")
# plt.scatter(d_list,old,label="old")
# plt.legend()
# plt.show()


# optimize_origin = np.load("opt_pulse_test_result_with_error_d10k_1210.npy")
optimize_origin = np.load(os.getcwd()+"/using npy/"+"opt_pulse_result_with_error_d5k_1214.npy")
optimize_ = np.zeros((len(e1),len(theta)))
for i in range(len(e1)):
    for j in range(len(theta)):
        optimize_[i,j] = optimize_origin[i,j]**(1/0.774)


# test_data = np.load("8pulse_test_result_with_error_d10k_1210.npy")
test_data = np.load(os.getcwd()+"/using npy/"+"8pulse_result_with_error_d5k_1214.npy")


# # old = np.load("old_pulse_result_with_error_d10k_1209.npy")
# old_ = np.zeros((len(e1),len(theta)))
# for i in range(len(e1)):
#     for j in range(len(theta)):
#         old_[i,j] = old[i,j]**(1/0.79)
# # print(old[0])





X, Y = np.meshgrid(e1, theta)
extent=[theta[0],theta[-1],e1[0],e1[-1]]
# extent=[e1[0],e1[-1],-16,16]


vmin = 0.98
vmax = 1
plt.subplot(1,2,1)
m_o = plt.imshow(test_data,aspect="auto",extent=extent,vmin=vmin,vmax=vmax)
plt.xlabel("phase error")
plt.ylabel("amplitude error")
plt.title("8pulse")
plt.subplot(1,2,2)
m_o1 = plt.imshow(optimize_,aspect="auto",extent=extent,vmin=vmin,vmax=vmax)
plt.title("optimize")
plt.tick_params(labelbottom=True,
               labelleft=False,
               labelright=False,
               labeltop=False)
plt.tick_params(bottom=True,
               left=True,
               right=False,
               top=False)
plt.xlabel("phase error")
# plt.subplot(1,3,3)
# plt.imshow(old_,aspect="auto",extent=extent,vmin=vmin,vmax=vmax)
# plt.title("experiment")
# plt.tick_params(labelbottom=True,
#                labelleft=False,
#                labelright=False,
#                labeltop=False)
# plt.tick_params(bottom=True,
#                left=True,
#                right=False,
#                top=False)
# plt.xlabel("phase error")
# plt.ylabel("amplitude error")
pp = plt.colorbar(m_o1)
# pp.set_clim(0.97,1)
pylab.savefig("compare_error2D_heatmap_d15k_60us_1214",bbox_inches="tight")
plt.show()
