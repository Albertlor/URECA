import math
import json

CACHE = []

def trigonometry(dist_from_low_back_to_shoulder, dist_from_low_back_to_hand, dist_from_shoulder_to_hand):
        a = dist_from_low_back_to_shoulder
        b = dist_from_low_back_to_hand
        c = dist_from_shoulder_to_hand

        #Angle between b and c
        A = math.acos( (b**2 + c**2 - a**2) / (2*b*c) )
        B = math.asin( (b/a) * (math.sin(A)) )
        C = math.pi - A - B

        return [A, B, C]


def midpoint(left_body_part, right_body_part):
        midpoint_x = (left_body_part[0] + right_body_part[0]) / 2
        midpoint_y = (left_body_part[1] + right_body_part[1]) / 2
        midpoint_z = (left_body_part[2] + right_body_part[2]) / 2

        return [midpoint_x, midpoint_y, midpoint_z]

def magnitude(vector):
    return math.sqrt(sum(pow(element, 2) for element in vector))

def cache():
    with open('config.json') as f:
        config = json.load(f)
        
    LAST_TIME = config["LAST_TIME"]
    TIME = config["TIME"]

    print(LAST_TIME)
    print(TIME)
    print(TIME - LAST_TIME)

    CACHE.append()

def moment_of_inertia(load, weight, m, k_s, k_t, k_l, L):
    I_xx = (m * weight) * (k_s * L)**2 #moment of inertia about sagittal axis
    I_yy = (m * weight) * (k_l * L)**2 #moment of inertia about longitudinal axis
    I_zz = (m * weight) * (k_t * L)**2 #moment of inertia about longitudinal axis

    return I_xx + I_yy + I_zz

