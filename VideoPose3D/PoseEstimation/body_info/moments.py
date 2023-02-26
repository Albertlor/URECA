import numpy as np
import json

from body_info.acceleration import Acceleration
from body_info.utils import midpoint
from body_info.utils import magnitude
from body_info.utils import trigonometry
from body_info.utils import moment_of_inertia


class Moment:
    with open('config.json') as f:
        config = json.load(f)
    individual = config['Individual']
    load = config['Load']
    weight = config['Weight']
    n = config['Frame']

    g_mag = 9.81 #graity

    m1 = 0.0162 #mass percentage of forearm
    m2 = 0.0271 #mass percentage of upper arm
    m3 = 0.4346 #mass percentage of head
    m4 = 0.4346 #mass percentage of trunk

    rA = [0, 0, 0]
    rB = [0, 0, 0]
    rD = [0, 0, 0]
    rG = [0, 0, 0]
    rI = [0, 0, 0]

    def __init__(self):
        pass

    @classmethod
    def direction_of_gravity(cls):
        with open(f'./database/json_data/Individual_{cls.individual}/left_knee_dict_json.json')as f1:
            left_knee = json.load(f1)
        r_left_knee = left_knee[f'LEFT_KNEE_5'] 

        with open(f'./database/json_data/Individual_{cls.individual}/right_knee_dict_json.json')as f2:
            right_knee = json.load(f2)
        r_right_knee = right_knee[f'RIGHT_KNEE_5'] 
        
        with open(f'./database/json_data/Individual_{cls.individual}/left_foot_dict_json.json')as f3:
            left_foot = json.load(f3)
        r_left_foot = left_foot[f'LEFT_FOOT_5']  

        with open(f'./database/json_data/Individual_{cls.individual}/right_foot_dict_json.json')as f4:
            right_foot = json.load(f4)
        r_right_foot = right_foot[f'RIGHT_FOOT_5']

        g1 = r_left_foot - r_left_knee
        g2 = right_foot - r_right_knee 

        g_dir = midpoint(g1, g2) / magnitude(midpoint(g1, g2))

        return g_dir

    @classmethod
    def trunk(cls):
        k_s = 0.372 #radius of gyration about sagittal axis
        k_t = 0.347 #radius of gyration about transverse axis
        k_l = 0.191 #radius of gyration about longitudinal axis
        L = 0.5319 #length of this body segment in meter

        with open(f'./database/json_data/Individual_{cls.individual}/low_back_dict_json.json')as f1:
            low_back = json.load(f1)
        rA_1 = low_back[f'BOTTOM_TORSO_{cls.n - 3}'] #position vector of the low back at frame n-3
        rA_2 = low_back[f'BOTTOM_TORSO_{cls.n - 2}'] #position vector of the low back at frame n-2
        rA_3 = low_back[f'BOTTOM_TORSO_{cls.n - 1}'] #position vector of the low back at frame n-1
        rA_4 = low_back[f'BOTTOM_TORSO_{cls.n}'] #position vector of the low back at frame n
        cls.rA = [rA_1, rA_2, rA_3, rA_4]

        with open(f'./database/json_data/Individual_{cls.individual}/center_torso_dict_json.json')as f2:
            center_torso = json.load(f2)
        rB_1 = center_torso[f'CENTER_TORSO_{cls.n - 3}'] #position vector of the center torso at frame n-3
        rB_2 = center_torso[f'CENTER_TORSO_{cls.n - 2}'] #position vector of the center torso at frame n-2
        rB_3 = center_torso[f'CENTER_TORSO_{cls.n - 1}'] #position vector of the center torso at frame n-1
        rB_4 = center_torso[f'CENTER_TORSO_{cls.n}'] #position vector of the center torso at frame n
        cls.rB = [rB_1, rB_2, rB_3, rB_4]

        rBA = cls.rB - cls.rA

        acceleration = Acceleration(cls.rB, rBA)
        moment_of_inertia = moment_of_inertia(Moment.load, Moment.weight, cls.m4, k_s, k_t, k_l, L)
        return [acceleration.linear_acceleration, acceleration.angular_acceleration, moment_of_inertia]

    @classmethod
    def head(cls):
        k_s = 0.362 #radius of gyration about sagittal axis
        k_t = 0.376 #radius of gyration about transverse axis
        k_l = 0.312 #radius of gyration about longitudinal axis
        L = 0.2033 #length of this body segment in meter

        with open(f'./database/json_data/Individual_{cls.individual}/upper_torso_dict_json.json')as f1:
            upper_torso = json.load(f1)
        rC_1 = upper_torso[f'UPPER_TORSO_{cls.n - 3}'] #position vector of the upper torso at frame n-3
        rC_2 = upper_torso[f'UPPER_TORSO_{cls.n - 2}'] #position vector of the upper torso at frame n-2
        rC_3 = upper_torso[f'UPPER_TORSO_{cls.n - 1}'] #position vector of the upper torso at frame n-1
        rC_4 = upper_torso[f'UPPER_TORSO_{cls.n}'] #position vector of the upper torso at frame n
        rC = [rC_1, rC_2, rC_3, rC_4]

        with open(f'./database/json_data/Individual_{cls.individual}/center_head_dict_json.json')as f2:
            center_head = json.load(f2)
        rD_1 = center_head[f'CENTER_HEAD_{cls.n - 3}'] #position vector of the center head at frame n-3
        rD_2 = center_head[f'CENTER_HEAD_{cls.n - 2}'] #position vector of the center head at frame n-2
        rD_3 = center_head[f'CENTER_HEAD_{cls.n - 1}'] #position vector of the center head at frame n-1
        rD_4 = center_head[f'CENTER_HEAD_{cls.n}'] #position vector of the center head at frame n
        cls.rD = [rD_1, rD_2, rD_3, rD_4]

        rDC = cls.rD - rC

        acceleration = Acceleration(cls.rD, rDC)
        moment_of_inertia = moment_of_inertia(Moment.load, Moment.weight, cls.m3, k_s, k_t, k_l, L)
        return [acceleration.linear_acceleration, acceleration.angular_acceleration, moment_of_inertia]

    @classmethod
    def upper_arm(cls):
        k_s = 0.285 #radius of gyration about sagittal axis
        k_t = 0.269 #radius of gyration about transverse axis
        k_l = 0.158 #radius of gyration about longitudinal axis
        L = 0.2817 #length of this body segment in meter

        with open(f'./database/json_data/Individual_{cls.individual}/left_shoulder_dict_json.json')as f1:
            left_shoulder = json.load(f1)
        rE_left_1 = left_shoulder[f'LEFT_SHOULDER_{cls.n - 3}'] #position vector of the left shoulder at frame n-3
        rE_left_2 = left_shoulder[f'LEFT_SHOULDER_{cls.n - 2}'] #position vector of the left shoulder at frame n-2
        rE_left_3 = left_shoulder[f'LEFT_SHOULDER_{cls.n - 1}'] #position vector of the left shoulder at frame n-1
        rE_left_4 = left_shoulder[f'LEFT_SHOULDER_{cls.n}'] #position vector of the left shoulder at frame n
        rE_left = [rE_left_1, rE_left_2, rE_left_3, rE_left_4]

        with open(f'./database/json_data/Individual_{cls.individual}/right_shoulder_dict_json.json')as f2:
            right_shoulder = json.load(f2)
        rE_right_1 = right_shoulder[f'RIGHT_SHOULDER_{cls.n - 3}'] #position vector of the right shoulder at frame n-3
        rE_right_2 = right_shoulder[f'RIGHT_SHOULDER_{cls.n - 2}'] #position vector of the right shoulder at frame n-2
        rE_right_3 = right_shoulder[f'RIGHT_SHOULDER_{cls.n - 1}'] #position vector of the right shoulder at frame n-1
        rE_right_4 = right_shoulder[f'RIGHT_SHOULDER_{cls.n}'] #position vector of the right shoulder at frame n
        rE_right = [rE_right_1, rE_right_2, rE_right_3, rE_right_4]

        rE = midpoint(rE_left, rE_right)


        with open(f'./database/json_data/Individual_{cls.individual}/left_elbow_dict_json.json')as f3:
            left_elbow = json.load(f3)
        rG_left_1 = left_elbow[f'LEFT_ELBOW_{cls.n - 3}'] #position vector of the left elbow at frame n-3
        rG_left_2 = left_elbow[f'LEFT_ELBOW_{cls.n - 2}'] #position vector of the left elbow at frame n-2
        rG_left_3 = left_elbow[f'LEFT_ELBOW_{cls.n - 1}'] #position vector of the left elbow at frame n-1
        rG_left_4 = left_elbow[f'LEFT_ELBOW_{cls.n}'] #position vector of the left elbow at frame n
        rG_left = [rG_left_1, rG_left_2, rG_left_3, rG_left_4]

        with open(f'./database/json_data/Individual_{cls.individual}/right_elbow_dict_json.json')as f4:
            right_elbow = json.load(f4)
        rG_right_1 = right_elbow[f'RIGHT_ELBOW_{cls.n - 3}'] #position vector of the right elbow at frame n-3
        rG_right_2 = right_elbow[f'RIGHT_ELBOW_{cls.n - 2}'] #position vector of the right elbow at frame n-2
        rG_right_3 = right_elbow[f'RIGHT_ELBOW_{cls.n - 1}'] #position vector of the right elbow at frame n-1
        rG_right_4 = right_elbow[f'RIGHT_ELBOW_{cls.n}'] #position vector of the right elbow at frame n
        rG_right = [rG_right_1, rG_right_2, rG_right_3, rG_right_4]

        cls.rG = midpoint(rG_left, rG_right)


        rFE = (cls.rG - rE) * 0.5772

        acceleration = Acceleration(cls.rG, rFE) #vF = vG
        moment_of_inertia = moment_of_inertia(Moment.load, Moment.weight, cls.m2, k_s, k_t, k_l, L)
        return [acceleration.linear_acceleration, acceleration.angular_acceleration, moment_of_inertia]

    @classmethod
    def forearm(cls):
        k_s = 0.276 #radius of gyration about sagittal axis
        k_t = 0.265 #radius of gyration about transverse axis
        k_l = 0.121 #radius of gyration about longitudinal axis
        L = 0.2689 #length of this body segment in meter

        with open(f'./database/json_data/Individual_{cls.individual}/left_elbow_dict_json.json')as f3:
            left_elbow = json.load(f3)
        rG_left_1 = left_elbow[f'LEFT_ELBOW_{cls.n - 3}'] #position vector of the left elbow at frame n-3
        rG_left_2 = left_elbow[f'LEFT_ELBOW_{cls.n - 2}'] #position vector of the left elbow at frame n-2
        rG_left_3 = left_elbow[f'LEFT_ELBOW_{cls.n - 1}'] #position vector of the left elbow at frame n-1
        rG_left_4 = left_elbow[f'LEFT_ELBOW_{cls.n}'] #position vector of the left elbow at frame n
        rG_left = [rG_left_1, rG_left_2, rG_left_3, rG_left_4]

        with open(f'./database/json_data/Individual_{cls.individual}/right_elbow_dict_json.json')as f4:
            right_elbow = json.load(f4)
        rG_right_1 = right_elbow[f'RIGHT_ELBOW_{cls.n - 3}'] #position vector of the right elbow at frame n-3
        rG_right_2 = right_elbow[f'RIGHT_ELBOW_{cls.n - 2}'] #position vector of the right elbow at frame n-2
        rG_right_3 = right_elbow[f'RIGHT_ELBOW_{cls.n - 1}'] #position vector of the right elbow at frame n-1
        rG_right_4 = right_elbow[f'RIGHT_ELBOW_{cls.n}'] #position vector of the right elbow at frame n
        rG_right = [rG_right_1, rG_right_2, rG_right_3, rG_right_4]

        rG = midpoint(rG_left, rG_right)


        with open(f'./database/json_data/Individual_{cls.individual}/left_hand_dict_json.json')as f3:
            left_hand = json.load(f3)
        rI_left_1 = left_hand[f'LEFT_HAND_{cls.n - 3}'] #position vector of the left hand at frame n-3
        rI_left_2 = left_hand[f'LEFT_HAND_{cls.n - 2}'] #position vector of the left hand at frame n-2
        rI_left_3 = left_hand[f'LEFT_HAND_{cls.n - 1}'] #position vector of the left hand at frame n-1
        rI_left_4 = left_hand[f'LEFT_HAND_{cls.n}'] #position vector of the left hand at frame n
        rI_left = [rI_left_1, rI_left_2, rI_left_3, rI_left_4]

        with open(f'./database/json_data/Individual_{cls.individual}/right_hand_dict_json.json')as f4:
            right_hand = json.load(f4)
        rI_right_1 = right_hand[f'RIGHT_HAND_{cls.n - 3}'] #position vector of the right hand at frame n-3
        rI_right_2 = right_hand[f'RIGHT_HAND_{cls.n - 2}'] #position vector of the right hand at frame n-2
        rI_right_3 = right_hand[f'RIGHT_HAND_{cls.n - 1}'] #position vector of the right hand at frame n-1
        rI_right_4 = right_hand[f'RIGHT_HAND_{cls.n}'] #position vector of the right hand at frame n
        rI_right = [rI_right_1, rI_right_2, rI_right_3, rI_right_4]

        cls.rI = midpoint(rI_left, rI_right)


        rHG = (cls.rI - rG) * 0.4574

        acceleration = Acceleration(cls.rI, rHG) #vH = vI
        moment_of_inertia = moment_of_inertia(cls.load, cls.weight, cls.m1, k_s, k_t, k_l, L)
        return [acceleration.linear_acceleration, acceleration.angular_acceleration, moment_of_inertia]

    @classmethod
    def moment(cls):
        a_trunk, alpha_trunk, I_trunk = cls.trunk()
        a_head, alpha_head, I_head = cls.head()
        a_upper_arm, alpha_upper_arm, I_upper_arm = cls.upper_arm()
        a_forearm, alpha_forearm, I_forearm = cls.forearm()

        a1 = np.array(a_forearm)
        a2 = np.array(a_upper_arm)
        a3 = np.array(a_head)
        a4 = np.array(a_trunk)

        alpha1 = np.array(alpha_forearm)
        alpha2 = np.array(alpha_upper_arm)
        alpha3 = np.array(alpha_head)
        alpha4 = np.array(alpha_trunk)

        I1 = I_forearm
        I2 = I_upper_arm
        I3 = I_head
        I4 = I_trunk

        r1 = np.array(cls.rI - cls.rA)
        r2 = np.array(cls.rG - cls.rA)
        r3 = np.array(cls.rD - cls.rA)
        r4 = np.array(cls.rB - cls.rA)

        F_L = np.array(cls.load * cls.direction_of_gravity())
        g = np.array(cls.g_mag * cls.direction_of_gravity())

        M = -np.cross(r1, F_L) - [np.cross(r1, cls.m1 * g) + np.cross(r2, cls.m2 * g) + np.cross(r3, cls.m3 * g) + np.cross(r4, cls.m4 * g)] + \
                                 [np.cross(r1, cls.m1 * a1) + np.cross(r2, cls.m2 * a2) + np.cross(r3, cls.m3 * a3) + np.cross(r4, cls.m4 * a4)] + \
                                 [(I1 * alpha1) + (I2 * alpha2) + (I3 * alpha3) + (I4 * alpha4)]

        return M