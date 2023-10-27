## SET BACKEND A magical trick from """https://stackoverflow.com/questions/47356726/fix-matplotlib-not-installed-as-framework-error-w-out-changing-matplotlib-con"""
import matplotlib as mpl
mpl.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import math
import sys

def X_Rotation(alpha):
    Rxc = math.cos(alpha)
    Rxs = math.sin(alpha)
    Rx = np.matrix([[1, 0, 0], [0, Rxc, Rxs], [0, -Rxs, Rxc]])
    return Rx

def Y_Rotation(beta):
    Ryc = math.cos(beta)
    Rys = math.sin(beta)
    Ry = np.matrix([[Ryc, 0, -Rys], [0, 1, 0], [Rys, 0, Ryc]])
    return Ry

def Z_Rotation(gamma):
    Rzc = math.cos(gamma)
    Rzs = math.sin(gamma)
    Rz = np.matrix([[Rzc, Rzs, 0], [-Rzs, Rzc, 0], [0, 0, 1]])
    return Rz

def dX_Rotation(alpha):
    Rxc = math.cos(alpha)
    Rxs = math.sin(alpha)
    Rdx = np.matrix([[0, 0, 0], [0, -Rxs, Rxc], [0, -Rxc, -Rxs]])
    return Rdx

def dY_Rotation(beta):
    Ryc = math.cos(beta)
    Rys = math.sin(beta)
    Rdy = np.matrix([[-Rys, 0, -Ryc], [0, 0, 0], [Ryc, 0, -Rys]])
    return Rdy

def dZ_Rotation(gamma):
    Rzc = math.cos(gamma)
    Rzs = math.sin(gamma)
    Rdz = np.matrix([[-Rzs, Rzc, 0], [-Rzc, -Rzs, 0], [0, 0, 0]])
    return Rdz
 
def Rotation_matrix(alpha, beta, gamma):
    R = np.matrix(X_Rotation(alpha)*Y_Rotation(beta)*Z_Rotation(gamma))
    return R

def Transformation(T, R, x):
    """3D Helmert transformation with known transformation Key 
    (Rotation matrix parameters and Translation vector)"""
    X = T + R*x
    return X

def Apriori_Rotation(x):
    """ Calculation of Apriori Rotation Matrix. 
    Takes first three measured points"""
    if x.shape < (3,3):
        print('Apriori_Rotation: Not enough points')
        sys.exit()

    x_A = x[0,:]
    for i in range(x.shape[0]-1):
        x_A = np.concatenate((x_A, x[0,:]))
    
    x_red = x-x_A
    g_1 = math.atan2(x_red[1,1], x_red[1,0])
    x_1 = Z_Rotation(g_1)*np.transpose(x_red)
    x_1 = np.transpose(x_1)
    b_2 = math.atan2(x_1[1,0], x_1[1,2])
    x_2 = Y_Rotation(b_2)*np.transpose(x_1)
    x_2 = np.transpose(x_2)
    g_3 = math.atan2(x_2[2,1], x_2[2,0])
    x_3 = Z_Rotation(g_3)*np.transpose(x_2)
    R = Z_Rotation(g_1)*Y_Rotation(b_2)*Z_Rotation(g_3)
    return R

def Helmert_3D(X, x):
    """3D Helmert transformation Key Calculation"""
    """ X is 'FROM' and x is 'TO' """
    # Apriori checks
    if np.shape(X) != np.shape(x):    
        print('Helmert_3D: Size of the source matrices are not the same!')
        sys.exit()
    else: 
        s = np.shape(X)
    
    R = np.matrix(np.transpose(Apriori_Rotation(x))*Apriori_Rotation(X))

    T = np.transpose(X[0,:]) - R*np.transpose(x[0,:])
    
    b = np.transpose(x)
    counter = 0
    while (count < 1000):

        counter += 1
    
    print("Too many iterations, the model doesn't convert.")

    return 0 

x = np.matrix([[3970673.003, 1018563.740, 4870369.178],\
    [3970667.574, 1018565.195, 4870373.010],\
    [3970659.461, 1018571.269, 4870377.881],\
    [3970654.604, 1018577.517, 4870380.020],\
    [3970650.090, 1018580.577, 4870382.774],\
    [3970646.096, 1018581.683, 4870385.620]])
    
X = np.matrix([[744970.551, 1040944.109, 224.592],\
    [744966.969, 1040938.331, 224.390],\
    [744958.051, 1040931.492, 224.057],\
    [744950.344, 1040928.731, 223.676],\
    [744945.677, 1040924.795, 223.472],\
    [744943.006, 1040920.538, 223.352]])

"""
R = np.matrix(np.transpose(Apriori_Rotation(x))*Apriori_Rotation(X))

T_1 = np.transpose(X[0,:]) - R*np.transpose(x[0,:])
#print T_1
v = 10

a = Rotation_matrix(1,2,3)
b = np.average(a[:,1])
c = a.mean(0)
d = np.shape(x)
print(np.shape(c), d[0], d[1])

e = np.transpose(x)
print(e, '\n', x)
if np.shape(a) < (3,3):
    print('Apriori_Rotation: Not enough points')

if np.shape(a) != np.shape(a):
    print("Doesnt have a same shape ")
"""
