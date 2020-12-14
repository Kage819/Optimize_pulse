import numpy as np

#結合定数
d = 5e+3
#1周期パルス照射時間
T1 = 60e-6
#計算格子数(Hrfの計算に使用)
M = 10000
#パルス繰り返し回数
N = 1
#スピン数
n = 4

#sf
sf = 1
#時間刻み
tlist, dt = np.linspace(0,T1,M,retstep = True)

#パウリ演算子
sigmax = np.array([[0,1],[1,0]])
sigmay = np.array([[0,-1j],[1j,0]])
sigmaz = np.array([[1,0],[0,-1]])
sigmaI = np.array([[1,0],[0,1]])

#位相直交性エラーを計算する際の角度.theta1は度数であり、thetaで[rad]に変換
theta1 = np.linspace(-8,8,17)
theta = []
for i in range(len(theta1)):
    theta.append(np.deg2rad(theta1[i]))

#振幅エラーの値
e1 = np.linspace(-0.1,0.1,11)
e3 = e1
e2 = 0
e4 = 0