# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 16:23:20 2021

@author: jbarker
"""

import numpy as np
import math

def X_Rotation(alpha):
    Rxc = math.cos(alpha)
    Rxs = math.sin(alpha)
    Rx = np.array([[1, 0, 0], [0, Rxc, Rxs], [0, -Rxs, Rxc]])
    return Rx

def Y_Rotation(beta):
    Ryc = math.cos(beta)
    Rys = math.sin(beta)
    Ry = np.array([[Ryc, 0, -Rys], [0, 1, 0], [Rys, 0, Ryc]])
    return Ry

def Z_Rotation(gamma):
    Rzc = math.cos(gamma)
    Rzs = math.sin(gamma)
    Rz = np.array([[Rzc, Rzs, 0], [-Rzs, Rzc, 0], [0, 0, 1]])
    return Rz

def dX_Rotation(alpha):
    Rxc = math.cos(alpha)
    Rxs = math.sin(alpha)
    Rdx = np.array([[0, 0, 0], [0, -Rxs, Rxc], [0, -Rxc, -Rxs]])
    return Rdx

def dY_Rotation(beta):
    Ryc = math.cos(beta)
    Rys = math.sin(beta)
    Rdy = np.array([[-Rys, 0, -Ryc], [0, 0, 0], [Ryc, 0, -Rys]])
    return Rdy

def dZ_Rotation(gamma):
    Rzc = math.cos(gamma)
    Rzs = math.sin(gamma)
    Rdz = np.array([[-Rzs, Rzc, 0], [-Rzc, -Rzs, 0], [0, 0, 0]])
    return Rdz

def Rotation_matrix(angle_tuple):
    R = X_Rotation(angle_tuple[0]) @ Y_Rotation(angle_tuple[1]) \
                                                @ Z_Rotation(angle_tuple[2])
    return R

def Transformation(x, From):
    """3D Helmert transformation with known transformation Key
    From is a dictionary of points
    (Rotation matrix parameters, Translation vector and scale in tuple)"""
    T = np.array(x[0:3])
    q = float(x[3])
    R = Rotation_matrix(x[-3:])
    From_transformed = {}
    for point in From:
        From_transformed[point] = tuple(T + q * R @ np.array(From[point]))
    return From_transformed

def Helmert_aproximate_parameters(From,To):
    identicals = list(set(To.keys()) & set(From.keys()))
    if len(identicals) > 3:
        #MAKE BETTER CHOICE ON POINTS WHEN YOU HAVE TIME, IF YOU WANT... PLEASE
        point1_To = np.array(To[identicals[0]])
        point2_To = np.array(To[identicals[-1]])
        point3_To = np.array(To[identicals[len(identicals)//2]])
        point1_To_original = point1_To.copy().transpose()
        #// truncating division = rounds result to lower int
        point1_From = np.array(From[identicals[0]])
        point2_From = np.array(From[identicals[-1]])
        point3_From = np.array(From[identicals[len(identicals)//2]])
        point1_From_original = point1_From.copy().transpose()
        # Translation of the points to have origin in point 1:
        point2_To = point2_To - point1_To
        point3_To = point3_To - point1_To
        point1_To = (0,0,0)
        point2_From = point2_From - point1_From
        point3_From = point3_From - point1_From
        point1_From = (0,0,0)
        # Calculating the aproximate parameters
        # (based on Angle between planes paper)
        # First rotation angle calculations
        psi_To = math.atan2(point2_To[1],point2_To[0])
        psi_From = math.atan2(point2_From[1],point2_From[0])
        # Applying the calculated angle to point 2 and 3
        FirstZrotation2_To = Z_Rotation(psi_To) @ point2_To.transpose()
        FirstZrotation3_To = Z_Rotation(psi_To) @point3_To.transpose()
        FirstZrotation2_From = Z_Rotation(psi_From) @ point2_To.transpose()
        FirstZrotation3_From = Z_Rotation(psi_From) @ point3_To.transpose()
        # Calculating second rotation angle from the first rotated coordinates
        fi_To = math.atan2(FirstZrotation2_To[1],FirstZrotation2_To[2])
        fi_From = math.atan2(FirstZrotation2_From[1],FirstZrotation2_From[2])
        # Applying the calculated angle to point 3
        SecondYrotation3_To = Y_Rotation(fi_To)@ FirstZrotation3_To.transpose()
        SecondYrotation3_From = Y_Rotation(
                                   fi_From) @ FirstZrotation3_From.transpose()
        # Calculating third rotation angle
        theta_To = math.atan2(SecondYrotation3_To[1],SecondYrotation3_To[0])
        theta_From = math.atan2(SecondYrotation3_From[1],
                                SecondYrotation3_From[0])
        # Using all three angles, the full rotation matrix for From To is made
        R_To = Z_Rotation(theta_To) @ Y_Rotation(fi_To) @ Z_Rotation(psi_To)
        R_From = Z_Rotation(theta_From) @ Y_Rotation(fi_From) @ Z_Rotation(
                                                                      psi_From)
        # The translation vector is calculated by rotating the original
        # point1_From to the "To" coordinate frame. By substracting the rotated
        # point1_From from point1_To we get the translation vector.
        R0 = R_To.transpose() @ R_From
        Translation = tuple(point1_To_original - R0 @ point1_From_original)
        # Euler rotation angles
        alpha = math.atan2(R0[1,2],R0[2,2])
        beta = - math.atan(R0[0,0])
        gamma = math.atan2(R0[0,1],R0[0,0])
        R_angles = (alpha, beta, gamma)
        x0 = Translation + (1.0,) + R_angles
    else:
        print('Not enough identical points for transformation calculations.')
    return R0, x0# RX + T

def Build_TFrom(x,From,identicals):
    """x are the transform parameters T,q,R in a tuple"""
    TFrom = np.array([]) #Transformed "From" coords
    for i in range(len(identicals)):
        PointID = identicals[i] #string
        From_ith = np.asarray(From[PointID]) # array
        R = Rotation_matrix(x[4:])
        T = np.array([x[0:3]])
        TFrom_ith = T + x[3] * R @ From_ith
        TFrom = np.append(TFrom,TFrom_ith)
    return TFrom

def Build_A(x,From,identicals):
    # x (TX,TY,TZ,q,alpha,beta,gamma)
    equation_count = 3 * len(identicals)
    RX = X_Rotation(x[4])
    RY = Y_Rotation(x[5])
    RZ = Z_Rotation(x[6])
    dRX = dX_Rotation(x[4])
    dRY = dY_Rotation(x[5])
    dRZ = dZ_Rotation(x[6])
    R = Rotation_matrix(x[4:7])
    A = np.zeros((equation_count,7))
    for i in range(len(identicals)):
        iii = 3*i
        PointID = identicals[i] #string
        From_ith = np.asarray(From[PointID]) # array
        A[iii,0] = 1
        A[iii+1,1] = 1
        A[iii+2,2] = 1
        D_alpha = dRX @ RY @ RZ @ From_ith
        D_beta = RX @ dRY @ RZ @ From_ith
        D_gamma = RX @ RY @ dRZ @ From_ith
        D_q = R @ From_ith
        A[iii:iii+3,3] = D_q
        A[iii:iii+3,4] = D_alpha
        A[iii:iii+3,5] = D_beta
        A[iii:iii+3,6] = D_gamma
    return A

def Helmert_transform(From,To):
    R0, x0 = Helmert_aproximate_parameters(From,To)
    identicals = list(set(To.keys()) & set(From.keys()))
    equation_count = 3*len(identicals)
    dx = np.zeros(7)
    x = np.array(x0)
    vI = np.empty((equation_count))
    vII = np.empty((equation_count))
    To_array = np.empty(0)
    TFrom = Build_TFrom(x,From,identicals)
    A = Build_A(x,From,identicals)
    for i in range(len(identicals)):
        PointID = identicals[i] #string
        To_ith = To[PointID] #tuple
        To_array = np.concatenate((To_array,np.array(To_ith)),axis = None)
    threshold = 0.000001 #fraction of basic unit
    metric = threshold + 1
    counter = 0
    while (metric > threshold) and (counter < 100):
        l_prime = TFrom - To_array
        dx = -np.linalg.inv(A.transpose() @ A) @ A.transpose() @ l_prime
        x += dx
        vI = A @ dx + l_prime
        TFrom = Build_TFrom(x,From,identicals)
        vII = TFrom - To_array
        v = vI-vII
        metric = max(abs(v))
        counter += 1
        A = Build_A(x,From,identicals)
    if counter == 100:
        print("Too many iterations")
#    Transformed_From = Transformation(x,From)
    return x

# =============================================================================
# Testing data [m]
# =============================================================================
"""
To = {'Point1': (3970673.003, 1018563.740, 4870369.178),
      'Point2': (3970667.574, 1018565.195, 4870373.010),
      'Point3': (3970659.461, 1018571.269, 4870377.881),
      'Point4': (3970654.604, 1018577.517, 4870380.020),
      'Point5': (3970650.090, 1018580.577, 4870382.774),
      'Point6': (3970646.096, 1018581.683, 4870385.620)
      }

From = {'Point1': (744970.551, 1040944.109, 224.592),
        'Point2': (744966.969, 1040938.331, 224.390),
        'Point3': (744958.051, 1040931.492, 224.057),
        'Point4': (744950.344, 1040928.731, 223.676),
        'Point5': (744945.677, 1040924.795, 223.472),
        'Point6': (744943.006, 1040920.538, 223.352)
      }
"""
To = {#'Girder_17': (3580.033, 319.23, -450.0),
#'Girder_15': (3200.305, 319.177, -450.0),
#'Girder_11': (2266.398, 319.081, -450.0),
#'Girder_7': (1606.962, 319.299, -450.0),
#'Girder_3': (702.931, 319.295, -450.0),
#'Girder_1': (323.147, 318.65, -450.0),
#'Girder_2': (323.225, -319.282, -450.0),
#'Girder_4': (702.676, -318.731, -450.0),
#'Girder_8': (1607.732, -319.047, -450.0),
#'Girder_12': (2267.506, -319.204, -450.0),
#'Girder_16': (3200.582, -318.769, -450.0),
#'Girder_18': (3580.677, -318.683, -450.0),
#'Girder_13': (2744.555, 319.123, -259.682),
#'Girder_5': (1169.555, 319.067, -259.725),
#'Girder_6': (1169.555, -318.987, -259.516),
#'Girder_14': (2744.555, -318.886, -259.257),
#'Girder_10': (1932.286, -318.933, -445.804),
#'Girder_9': (1931.985, 319.004, -446.523),
'PQK36_1': (3580.129, 319.168, -259.561), 'PQK36_2': (3580.392, 319.0, 260.176), 'PQK36_3': (3580.851, 190.734, 381.651), 'PQK36_4': (3580.31, -189.781, 381.618), 'PQK36_5': (3579.981, -319.023, 260.177), 'PQK36_6': (3580.49, -318.774, -258.959), 'PQK36_7': (3200.33, 319.143, -259.602), 'PQK36_8': (3200.397, 319.051, 260.128), 'PQK36_9': (3200.797, 190.148, 381.562), 'PQK36_10': (3200.68, -190.38, 381.225), 'PQK36_11': (3199.917, -319.228, 259.852), 'PQK36_12': (3200.404, -318.892, -259.514), 'PQK62_1': (703.196, 319.314, -260.024), 'PQK62_2': (703.923, 319.366, 260.716), 'PQK62_3': (703.392, 189.911, 381.514), 'PQK62_4': (702.991, -189.47, 381.848), 'PQK62_5': (703.82, -318.919, 260.03), 'PQK62_6': (702.983, -318.782, -259.336), 'PQK62_7': (323.31, 318.828, -259.505), 'PQK62_8': (323.754, 319.315, 260.722), 'PQK62_9': (322.645, 190.05, 381.429), 'PQK62_10': (322.986, -190.123, 381.216), 'PQK62_11': (323.408, -319.094, 260.357), 'PQK62_12': (323.274, -319.232, -259.953), 'PQL6_1': (2266.658, 319.01, -260.071), 'PQL6_2': (2267.37, 318.814, 260.553), 'PQL6_3': (2267.308, 189.988, 381.281), 'PQL6_4': (2267.461, -189.958, 381.464), 'PQL6_5': (2267.16, -318.638, 260.34), 'PQL6_6': (2267.413, -319.052, -259.248), 'PQL6_7': (1607.165, 319.106, -259.459), 'PQL6_8': (1607.718, 318.579, 260.443), 'PQL6_9': (1607.669, 189.952, 381.423), 'PQL6_10': (1607.666, -190.164, 381.566), 'PQL6_11': (1607.678, -318.455, 259.748), 'PQL6_12': (1607.717, -318.888, -259.318)}
From = {'PQK36_4': (-1864.7391985337786, -1412.5845681076676, 337.5129251994295),
'PQL6_6': (-563.6822583192709, -1636.9194273603023, -301.1856214205907),
'PQK62_11': (1308.9304639165696, -2155.815215165814, 221.20123913470763),
'PQK62_5': (942.252947958758, -2054.6074218479876, 220.31446634117754),
'PQK62_6': (944.0385231639474, -2054.147867656249, -299.0300855126724),
'PQK62_12': (1310.1064657966838, -2154.92028065426, -299.11910328778254),
'PQK62_10': (1274.7635284591167, -2280.4113882071556, 341.7819795813937),
'PQK62_4': (908.3305069086985, -2179.7601403242315, 341.860375875407),
'PQK62_3': (806.830912644317, -2545.2781093678836, 340.7679868916535),
'Girder_5': (334.5118195376464, -2547.217877625032, -304.03077270736935),
'Girder_6': (503.3121340146122, -1930.035362377214, -304.746965806248),
'PQL6_10': (36.58919024011306, -1937.9792688962732, 340.28757472149886),
'PQL6_11': (71.00914002153476, -1814.131411508509, 218.73670545097795),
'PQL6_12': (72.07039018287901, -1812.8993074333082, -300.3212318963134),
'Girder_10': (-238.6981197284123, -1726.0549631030801, -496.83050346103494),
'PQL6_4': (-599.375734960091, -1762.3231107437275, 339.2348623602857),
'PQL6_5': (-564.5588090963123, -1638.1859087703535, 218.3813577277245),
'Girder_14': (-1012.5429340518019, -1513.040647466852, -304.6923997474439),
'Girder_13': (-1185.3143477882425, -2129.7260215327265, -307.6879265322543),
'PQK36_12': (-1462.966608342805, -1388.3937374205786, -302.7876084225827),
'PQK36_10': (-1498.7070188344346, -1513.1937054501027, 337.667227498598),
'PQK36_5': (-1829.7463318971477, -1287.92193683412, 216.33985656689072),
'PQK36_6': (-1829.3170688530968, -1287.21589756316, -302.8024710258846),
'PQK36_9': (-1600.2496449549192, -1879.9153371503346, 337.20649843174596),
'Girder_18': (-1829.3398830901938, -1283.5020424633437, -489.94690957692603),
'Girder_12': (-563.2926950899798, -1635.8549201831534, -491.1499923606186),
'Girder_8': (71.84568961356774, -1813.5629650638004, -489.42774964436546),
'Girder_4': (944.1641588237248, -2056.1063581024837, -488.9871486370865),
'Girder_2': (1308.93177535996, -2158.246795570055, -488.08931509879767)}

x = Helmert_transform(From,To)
print(x)
Transformed = Transformation(x,From)
print(Transformed)
# =============================================================================
# Testing data - Results
# ============================================================================
'''
T:   2.98027817e+06   1.37948616e+06   5.59696765e+06 [m]
q:   1.00016673
Rot: 0.204758250  -0.670278274   1.11095571 [rad]

{'Point1': (3970673.003288134, 1018563.7398536116, 4870369.178586198),
'Point2': (3970667.5735479398, 1018565.1948317708, 4870373.0091473022),
'Point3': (3970659.461105776, 1018571.2697034873, 4870377.8815089483),
'Point4': (3970654.6043181177, 1018577.5169809447, 4870380.0196550041),
'Point5': (3970650.0896756388, 1018580.5766302142, 4870382.7734877616),
'Point6': (3970646.09606406, 1018581.6829998301, 4870385.6206144663)}'''
