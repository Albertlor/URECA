import math
import json


def midpoint(left_body_part, right_body_part):
        midpoint_x = (left_body_part[0] + right_body_part[0]) / 2
        midpoint_y = (left_body_part[1] + right_body_part[1]) / 2
        midpoint_z = (left_body_part[2] + right_body_part[2]) / 2

        return [midpoint_x, midpoint_y, midpoint_z]

def magnitude(vector):
    return math.sqrt(sum(pow(element, 2) for element in vector))

def moment_of_inertia(load, weight, m, k_s, k_t, k_l, L):
    I_xx = (m * weight) * (k_s * L)**2 #moment of inertia about sagittal axis
    I_yy = (m * weight) * (k_l * L)**2 #moment of inertia about longitudinal axis
    I_zz = (m * weight) * (k_t * L)**2 #moment of inertia about longitudinal axis

    return I_xx + I_yy + I_zz

