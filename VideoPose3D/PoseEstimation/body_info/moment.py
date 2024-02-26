import numpy as np
import math
import json
import matplotlib.pyplot as plt

from body_info.acceleration import Acceleration
from body_info.utils import midpoint, magnitude, moment_of_inertia


class Moment:
    g_mag = 9.81 #graity
    g_dir = [0, 0, 0]

    # m1 = 0.0162 #mass percentage of forearm
    # m2 = 0.0271 #mass percentage of upper arm
    # m3 = 0.4346 #mass percentage of head
    # m4 = 0.4346 #mass percentage of trunk

    m1 = 0.0187 #mass percentage of forearm
    m2 = 0.0325 #mass percentage of upper arm
    m3 = 0.0826 #mass percentage of head
    m4 = 0.551 #mass percentage of trunk

    rA = []
    rB = []
    rD = []
    rE = []
    rG = []
    rI = []

    def __init__(self):
        pass

    @classmethod
    def direction_of_gravity(cls, individual):
        with open(f'./database/json_data/Individual_{individual}/low_back_dict_json.json')as f1:
            low_back = json.load(f1)
        rA_5 = low_back[f'BOTTOM_TORSO_5'] 
        rA_6 = low_back[f'BOTTOM_TORSO_6']

        with open(f'./database/json_data/Individual_{individual}/upper_torso_dict_json.json')as f2:
            upper_torso = json.load(f2)
        rC_5 = upper_torso[f'UPPER_TORSO_5'] 
        rC_6 = upper_torso[f'UPPER_TORSO_6']

        g1 = (np.array(rC_5) - np.array(rA_5)).tolist()
        g2 = (np.array(rC_6) - np.array(rA_6)).tolist() 

        cls.g_dir = -np.multiply(np.array(midpoint(g1, g2)), 1/(magnitude(midpoint(g1, g2))))

    @classmethod
    def trunk(cls, individual, load, mass, n):
        k_s = 0.372 #radius of gyration about sagittal axis
        k_t = 0.347 #radius of gyration about transverse axis
        k_l = 0.191 #radius of gyration about longitudinal axis
        L = 0.5319 #length of this body segment in meter

        with open(f'./database/json_data/Individual_{individual}/low_back_dict_json.json')as f1:
            low_back = json.load(f1)
        rA_1 = low_back[f'BOTTOM_TORSO_{n - 3}'] #position vector of the low back at frame n-3
        rA_2 = low_back[f'BOTTOM_TORSO_{n - 2}'] #position vector of the low back at frame n-2
        rA_3 = low_back[f'BOTTOM_TORSO_{n - 1}'] #position vector of the low back at frame n-1
        rA_4 = low_back[f'BOTTOM_TORSO_{n}'] #position vector of the low back at frame n
        cls.rA = [rA_1, rA_2, rA_3, rA_4]

        with open(f'./database/json_data/Individual_{individual}/center_torso_dict_json.json')as f2:
            center_torso = json.load(f2)
        rB_1 = center_torso[f'CENTER_TORSO_{n - 3}'] #position vector of the center torso at frame n-3
        rB_2 = center_torso[f'CENTER_TORSO_{n - 2}'] #position vector of the center torso at frame n-2
        rB_3 = center_torso[f'CENTER_TORSO_{n - 1}'] #position vector of the center torso at frame n-1
        rB_4 = center_torso[f'CENTER_TORSO_{n}'] #position vector of the center torso at frame n
        cls.rB = [rB_1, rB_2, rB_3, rB_4]

        rBA = (np.array(cls.rB) - np.array(cls.rA)).tolist()

        acceleration = Acceleration(cls.rB, rBA)
        I = moment_of_inertia(load, mass, cls.m4, k_s, k_t, k_l, L)
        return [acceleration.linear_acceleration(), acceleration.angular_acceleration(), I]

    @classmethod
    def head(cls, individual, load, mass, n):
        k_s = 0.362 #radius of gyration about sagittal axis
        k_t = 0.376 #radius of gyration about transverse axis
        k_l = 0.312 #radius of gyration about longitudinal axis
        L = 0.2033 #length of this body segment in meter

        with open(f'./database/json_data/Individual_{individual}/upper_torso_dict_json.json')as f1:
            upper_torso = json.load(f1)
        rC_1 = upper_torso[f'UPPER_TORSO_{n - 3}'] #position vector of the upper torso at frame n-3
        rC_2 = upper_torso[f'UPPER_TORSO_{n - 2}'] #position vector of the upper torso at frame n-2
        rC_3 = upper_torso[f'UPPER_TORSO_{n - 1}'] #position vector of the upper torso at frame n-1
        rC_4 = upper_torso[f'UPPER_TORSO_{n}'] #position vector of the upper torso at frame n
        rC = [rC_1, rC_2, rC_3, rC_4]

        with open(f'./database/json_data/Individual_{individual}/center_head_dict_json.json')as f2:
            center_head = json.load(f2)
        rD_1 = center_head[f'CENTER_HEAD_{n - 3}'] #position vector of the center head at frame n-3
        rD_2 = center_head[f'CENTER_HEAD_{n - 2}'] #position vector of the center head at frame n-2
        rD_3 = center_head[f'CENTER_HEAD_{n - 1}'] #position vector of the center head at frame n-1
        rD_4 = center_head[f'CENTER_HEAD_{n}'] #position vector of the center head at frame n
        cls.rD = [rD_1, rD_2, rD_3, rD_4]

        rDC = (np.array(cls.rD) - np.array(rC)).tolist()

        acceleration = Acceleration(cls.rD, rDC)
        I = moment_of_inertia(load, mass, cls.m3, k_s, k_t, k_l, L)
        return [acceleration.linear_acceleration(), acceleration.angular_acceleration(), I]

    @classmethod
    def upper_arm(cls, individual, load, mass, n):
        k_s = 0.285 #radius of gyration about sagittal axis
        k_t = 0.269 #radius of gyration about transverse axis
        k_l = 0.158 #radius of gyration about longitudinal axis
        L = 0.2817 #length of this body segment in meter

        with open(f'./database/json_data/Individual_{individual}/left_shoulder_dict_json.json')as f1:
            left_shoulder = json.load(f1)
        rE_left_1 = left_shoulder[f'LEFT_SHOULDER_{n - 3}'] #position vector of the left shoulder at frame n-3
        rE_left_2 = left_shoulder[f'LEFT_SHOULDER_{n - 2}'] #position vector of the left shoulder at frame n-2
        rE_left_3 = left_shoulder[f'LEFT_SHOULDER_{n - 1}'] #position vector of the left shoulder at frame n-1
        rE_left_4 = left_shoulder[f'LEFT_SHOULDER_{n}'] #position vector of the left shoulder at frame n
        rE_left = [rE_left_1, rE_left_2, rE_left_3, rE_left_4]

        with open(f'./database/json_data/Individual_{individual}/right_shoulder_dict_json.json')as f2:
            right_shoulder = json.load(f2)
        rE_right_1 = right_shoulder[f'RIGHT_SHOULDER_{n - 3}'] #position vector of the right shoulder at frame n-3
        rE_right_2 = right_shoulder[f'RIGHT_SHOULDER_{n - 2}'] #position vector of the right shoulder at frame n-2
        rE_right_3 = right_shoulder[f'RIGHT_SHOULDER_{n - 1}'] #position vector of the right shoulder at frame n-1
        rE_right_4 = right_shoulder[f'RIGHT_SHOULDER_{n}'] #position vector of the right shoulder at frame n
        rE_right = [rE_right_1, rE_right_2, rE_right_3, rE_right_4]

        cls.rE = [
                midpoint(rE_left[0], rE_right[0]),
                midpoint(rE_left[1], rE_right[1]),
                midpoint(rE_left[2], rE_right[2]),
                midpoint(rE_left[3], rE_right[3]),
            ]

        with open(f'./database/json_data/Individual_{individual}/left_elbow_dict_json.json')as f3:
            left_elbow = json.load(f3)
        rG_left_1 = left_elbow[f'LEFT_ELBOW_{n - 3}'] #position vector of the left elbow at frame n-3
        rG_left_2 = left_elbow[f'LEFT_ELBOW_{n - 2}'] #position vector of the left elbow at frame n-2
        rG_left_3 = left_elbow[f'LEFT_ELBOW_{n - 1}'] #position vector of the left elbow at frame n-1
        rG_left_4 = left_elbow[f'LEFT_ELBOW_{n}'] #position vector of the left elbow at frame n
        rG_left = [rG_left_1, rG_left_2, rG_left_3, rG_left_4]

        with open(f'./database/json_data/Individual_{individual}/right_elbow_dict_json.json')as f4:
            right_elbow = json.load(f4)
        rG_right_1 = right_elbow[f'RIGHT_ELBOW_{n - 3}'] #position vector of the right elbow at frame n-3
        rG_right_2 = right_elbow[f'RIGHT_ELBOW_{n - 2}'] #position vector of the right elbow at frame n-2
        rG_right_3 = right_elbow[f'RIGHT_ELBOW_{n - 1}'] #position vector of the right elbow at frame n-1
        rG_right_4 = right_elbow[f'RIGHT_ELBOW_{n}'] #position vector of the right elbow at frame n
        rG_right = [rG_right_1, rG_right_2, rG_right_3, rG_right_4]

        cls.rG = [
                    midpoint(rG_left[0], rG_right[0]),
                    midpoint(rG_left[1], rG_right[1]),
                    midpoint(rG_left[2], rG_right[2]),
                    midpoint(rG_left[3], rG_right[3]),
                ]

        rFE = (np.multiply((np.array(cls.rG) - np.array(cls.rE)), 0.5772)).tolist()

        acceleration = Acceleration(cls.rG, rFE) #vF = vG
        I = moment_of_inertia(load, mass, cls.m2, k_s, k_t, k_l, L)
        return [acceleration.linear_acceleration(), acceleration.angular_acceleration(), I]

    @classmethod
    def forearm(cls, individual, load, mass, n):
        k_s = 0.276 #radius of gyration about sagittal axis
        k_t = 0.265 #radius of gyration about transverse axis
        k_l = 0.121 #radius of gyration about longitudinal axis
        L = 0.2689 #length of this body segment in meter

        with open(f'./database/json_data/Individual_{individual}/left_elbow_dict_json.json')as f1:
            left_elbow = json.load(f1)
        rG_left_1 = left_elbow[f'LEFT_ELBOW_{n - 3}'] #position vector of the left elbow at frame n-3
        rG_left_2 = left_elbow[f'LEFT_ELBOW_{n - 2}'] #position vector of the left elbow at frame n-2
        rG_left_3 = left_elbow[f'LEFT_ELBOW_{n - 1}'] #position vector of the left elbow at frame n-1
        rG_left_4 = left_elbow[f'LEFT_ELBOW_{n}'] #position vector of the left elbow at frame n
        rG_left = [rG_left_1, rG_left_2, rG_left_3, rG_left_4]

        with open(f'./database/json_data/Individual_{individual}/right_elbow_dict_json.json')as f2:
            right_elbow = json.load(f2)
        rG_right_1 = right_elbow[f'RIGHT_ELBOW_{n - 3}'] #position vector of the right elbow at frame n-3
        rG_right_2 = right_elbow[f'RIGHT_ELBOW_{n - 2}'] #position vector of the right elbow at frame n-2
        rG_right_3 = right_elbow[f'RIGHT_ELBOW_{n - 1}'] #position vector of the right elbow at frame n-1
        rG_right_4 = right_elbow[f'RIGHT_ELBOW_{n}'] #position vector of the right elbow at frame n
        rG_right = [rG_right_1, rG_right_2, rG_right_3, rG_right_4]

        rG = [
                midpoint(rG_left[0], rG_right[0]),
                midpoint(rG_left[1], rG_right[1]),
                midpoint(rG_left[2], rG_right[2]),
                midpoint(rG_left[3], rG_right[3]),
            ]


        with open(f'./database/json_data/Individual_{individual}/left_hand_dict_json.json')as f3:
            left_hand = json.load(f3)
        rI_left_1 = left_hand[f'LEFT_HAND_{n - 3}'] #position vector of the left hand at frame n-3
        rI_left_2 = left_hand[f'LEFT_HAND_{n - 2}'] #position vector of the left hand at frame n-2
        rI_left_3 = left_hand[f'LEFT_HAND_{n - 1}'] #position vector of the left hand at frame n-1
        rI_left_4 = left_hand[f'LEFT_HAND_{n}'] #position vector of the left hand at frame n
        rI_left = [rI_left_1, rI_left_2, rI_left_3, rI_left_4]

        with open(f'./database/json_data/Individual_{individual}/right_hand_dict_json.json')as f4:
            right_hand = json.load(f4)
        rI_right_1 = right_hand[f'RIGHT_HAND_{n - 3}'] #position vector of the right hand at frame n-3
        rI_right_2 = right_hand[f'RIGHT_HAND_{n - 2}'] #position vector of the right hand at frame n-2
        rI_right_3 = right_hand[f'RIGHT_HAND_{n - 1}'] #position vector of the right hand at frame n-1
        rI_right_4 = right_hand[f'RIGHT_HAND_{n}'] #position vector of the right hand at frame n
        rI_right = [rI_right_1, rI_right_2, rI_right_3, rI_right_4]

        cls.rI = [
                    midpoint(rI_left[0], rI_right[0]),
                    midpoint(rI_left[1], rI_right[1]),
                    midpoint(rI_left[2], rI_right[2]),
                    midpoint(rI_left[3], rI_right[3]),
                ]


        rHG = (np.multiply((np.array(cls.rI) - np.array(rG)), 0.4574)).tolist()

        acceleration = Acceleration(cls.rI, rHG) #vH = vI
        I = moment_of_inertia(load, mass, cls.m1, k_s, k_t, k_l, L)
        return [acceleration.linear_acceleration(), acceleration.angular_acceleration(), I]

    @classmethod
    def angle_between_spine_and_vertical_plane(cls):
        rBA = np.array(cls.rB[2]) - np.array(cls.rA[2])
        rBA_mag = magnitude(rBA.tolist())
        g_dir_mag = magnitude(cls.g_dir)
        dot_product = np.dot(rBA, cls.g_dir)
        theta = math.acos(dot_product/(rBA_mag * -g_dir_mag))
        return theta
    
    @classmethod
    def angle_between_shoulder_and_horizontal_plane(cls):
        rGE = np.array(cls.rG[2]) - np.array(cls.rE[2])
        rGE_mag = magnitude(rGE.tolist())
        g_dir_mag = magnitude(cls.g_dir)
        dot_product = np.dot(rGE, -cls.g_dir)
        theta = math.acos(dot_product/(rGE_mag * -g_dir_mag))
        return theta

    @classmethod
    def moment(cls):
        try:
            with open('config.json') as f:
                config = json.load(f)
            individual = config['Individual']
            load = config['Load']
            weight = config['Weight']
            n = config['Frame']
            cls.direction_of_gravity(individual)

            mass = weight / cls.g_mag

            a_trunk, alpha_trunk, I_trunk = cls.trunk(individual, load, mass, n)
            a_head, alpha_head, I_head = cls.head(individual, load, mass, n)
            a_upper_arm, alpha_upper_arm, I_upper_arm = cls.upper_arm(individual, load, mass, n)
            a_forearm, alpha_forearm, I_forearm = cls.forearm(individual, load, mass, n)

            a1 = a_forearm
            a2 = a_upper_arm
            a3 = a_head
            a4 = a_trunk

            alpha1 = alpha_forearm
            alpha2 = alpha_upper_arm
            alpha3 = alpha_head
            alpha4 = alpha_trunk

            I1 = I_forearm
            I2 = I_upper_arm
            I3 = I_head
            I4 = I_trunk

            # r1 = (np.array(cls.rI) - np.array(cls.rA))[2]
            # r2 = (np.array(cls.rG) - np.array(cls.rA))[2]
            # r3 = (np.array(cls.rD) - np.array(cls.rA))[2]
            # r4 = (np.array(cls.rB) - np.array(cls.rA))[2]
            # r5 = (np.array(cls.rG) - np.array(cls.rE))[2]
            # r6 = (np.array(cls.rI) - np.array(cls.rE))[2]

            r1 = np.multiply(((np.array(cls.rI) - np.array(cls.rA)) - (np.array(cls.rG) - np.array(cls.rA)))[2], 0.5) + np.array(cls.rA)[2]
            r2 = np.multiply(((np.array(cls.rG) - np.array(cls.rA)) - (np.array(cls.rE) - np.array(cls.rA)))[2], 0.5) + np.array(cls.rA)[2]
            r3 = (np.array(cls.rD) - np.array(cls.rA))[2]
            r4 = (np.array(cls.rB) - np.array(cls.rA))[2]

            F_L = np.multiply(load, cls.g_dir)
            g = np.multiply(cls.g_mag, cls.g_dir)

            theta_back = cls.angle_between_spine_and_vertical_plane()

            M_back = (np.cross(r1, np.multiply(2 * mass * cls.m1, g)) + np.cross(r2, np.multiply(2 * mass * cls.m2, g)) + np.cross(r3, np.multiply(mass * cls.m3, g)) + np.cross(r4, np.multiply(mass * cls.m4, g))) + \
                     (np.cross(r1, np.multiply(2 * mass * cls.m1, a1)) + np.cross(r2, np.multiply(2 * mass * cls.m2, a2)) + np.cross(r3, np.multiply(mass * cls.m3, a3)) + np.cross(r4, np.multiply(mass * cls.m4, a4))) + \
                     (np.multiply(2 * I1, alpha1) + np.multiply(2 * I2, alpha2) + np.multiply(I3, alpha3) + np.multiply(I4, alpha4))
            
            F_back = (np.multiply(2 * mass * cls.m1, g) + np.multiply(2 * mass * cls.m2, g) + np.multiply(mass * cls.m3, g) + np.multiply(mass * cls.m4, g)) + \
                     (np.multiply(2 * mass * cls.m1, a1) + np.multiply(2 * mass * cls.m2, a2) + np.multiply(mass * cls.m3, a3) + np.multiply(mass * cls.m4, a4))
            
            # M_back = -(np.cross(r1, F_L)) - \
            #          (np.cross(r1, np.multiply(2 * mass * cls.m1, g)) + np.cross(r2, np.multiply(2 * mass * cls.m2, g)) + np.cross(r3, np.multiply(mass * cls.m3, g)) + np.cross(r4, np.multiply(mass * cls.m4, g))) + \
            #          (np.cross(r1, np.multiply(2 * mass * cls.m1, a1)) + np.cross(r2, np.multiply(2 * mass * cls.m2, a2)) + np.cross(r3, np.multiply(mass * cls.m3, a3)) + np.cross(r4, np.multiply(mass * cls.m4, a4))) + \
            #          (np.multiply(2 * I1, alpha1) + np.multiply(2 * I2, alpha2) + np.multiply(I3, alpha3) + np.multiply(I4, alpha4))
            
            # F_back_mag = abs( np.dot(( F_L + \
            #                            (np.multiply(2 * mass * cls.m1, g) + np.multiply(2 * mass * cls.m2, g) + np.multiply(mass * cls.m3, g) + np.multiply(mass * cls.m4, g)) + \
            #                            (np.multiply(2 * mass * cls.m1, a1) + np.multiply(2 * mass * cls.m2, a2) + np.multiply(mass * cls.m3, a3) + np.multiply(mass * cls.m4, a4))), np.multiply(r4, 1/magnitude(r4))) )
            
            # gamma = math.acos(np.dot(r1, cls.g_dir) / magnitude(r1))

            # F_back_mag = 0.045*168*weight*math.sin(theta) + 0.5*(magnitude(F_L))*(magnitude(r1))*math.sin(gamma) + 0.4*weight + 0.8*magnitude(F_L)

            M_back_mag = magnitude(M_back.tolist()) + ((load / 10) / 5) * 20
            F_back_mag = magnitude(F_back.tolist()) + ((load / 10) / 5) * 920
            M_back_dir = np.multiply(M_back, 1/M_back_mag)

            return [M_back_mag, F_back_mag, M_back_dir, theta_back]

        except Exception as e:
            import traceback
            print(traceback.format_exc())

if __name__ == '__main__':
    dictionary1 = json.load(open('./spine_angle.json', 'r'))
    xAxis1 = [key for key, value in dictionary1.items() if int(key)%15==0 and int(key)!=0]
    yAxis1 = [value for key, value in dictionary1.items() if int(key)%15==0 and int(key)!=0]

    ## LINE GRAPH ##
    plt.plot(xAxis1,yAxis1, color='maroon', marker='o')
    plt.xlabel('Frame')
    plt.ylabel('Spine Angle (degree)')
        
    plt.show()