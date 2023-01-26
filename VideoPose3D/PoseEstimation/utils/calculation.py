import math
import numpy as np


class Calculation:
    vector1 = []
    vector2 = [0,0,1] #vector of z axis

    def __init__(self, load, left_hand, right_hand, left_shoulder, right_shoulder, low_back, upper_torso):
        self.load = load
        self.left_hand = left_hand
        self.right_hand = right_hand
        self.left_shoulder = left_shoulder
        self.right_shoulder = right_shoulder
        self.low_back = low_back
        self.upper_torso = upper_torso

    def dist_from_shoulder_to_hand(self):
        midpoint_of_shoulders = Calculation.midpoint(self.left_shoulder, self.right_shoulder)
        midpoint_of_hands = Calculation.midpoint(self.left_hand, self.right_hand)
        distance = ((midpoint_of_shoulders[0] - midpoint_of_hands[0])**2 + (midpoint_of_shoulders[1] - midpoint_of_hands[1])**2 + \
                    (midpoint_of_shoulders[2] - midpoint_of_hands[2])**2)**0.5

        return distance

    def dist_from_low_back_to_hand(self):
        midpoint_of_hands = Calculation.midpoint(self.left_hand, self.right_hand)
        distance = ((self.low_back[0] - midpoint_of_hands[0])**2 + (self.low_back[1] - midpoint_of_hands[1])**2 + \
                    (self.low_back[2] - midpoint_of_hands[2])**2)**0.5

        return distance

    def dist_from_low_back_to_shoulder(self):
        midpoint_of_shoulders = Calculation.midpoint(self.left_shoulder, self.right_shoulder)
        distance = ((self.low_back[0] - midpoint_of_shoulders[0])**2 + (self.low_back[1] - midpoint_of_shoulders[1])**2 + \
                    (self.low_back[2] - midpoint_of_shoulders[2])**2)**0.5

        return distance

    def trigonometry(self):
        calculation = Calculation(load=self.load, low_back=self.low_back, upper_torso=self.upper_torso, right_shoulder=self.right_shoulder, \
                                  right_hand=self.right_hand, left_shoulder=self.left_shoulder, left_hand=self.left_hand)
        a = calculation.dist_from_low_back_to_shoulder()
        b = calculation.dist_from_low_back_to_hand()
        c = calculation.dist_from_shoulder_to_hand()

        #Angle between b and c
        A = math.acos( (b**2 + c**2 - a**2) / 2*b*c )
        B = math.asin( (b/a) * (math.sin(A)) )
        C = math.pi - A - B

        return [A, B, C]

    def vector_from_low_back_to_upper_torso(self):
        Calculation.vector1 = ((self.upper_torso[0] - self.low_back[0]), (self.upper_torso[1] - self.low_back[1]), \
                               (self.upper_torso[2] - self.low_back[2]))
    
    def angle_between_spine_and_z_axis(self):
        v1 = np.array(Calculation.vector1)
        v2 = np.array(Calculation.vector2)
        v1_mag = Calculation.magnitude(v1)
        v2_mag = Calculation.magnitude(v2)
        dot_product = np.dot(v1, v2)
        theta = math.acos(dot_product/(v1_mag * v2_mag))
        return theta

    def moment(self):
        calculation = Calculation(load=self.load, low_back=self.low_back, upper_torso=self.upper_torso, right_shoulder=self.right_shoulder, \
                                  right_hand=self.right_hand, left_shoulder=self.left_shoulder, left_hand=self.left_hand)
        angles = calculation.trigonometry()
        theta = calculation.angle_between_spine_and_z_axis
        A, B, C = angles
        
        angle_for_low_back = theta + C
        angle_for_shoulder = (theta + C) + A

        low_back_moment = (self.load * math.sin(angle_for_low_back)) * calculation.dist_from_low_back_to_hand()
        shoulder_moment = (self.load * math.sin(angle_for_shoulder)) * calculation.dist_from_shoulder_to_hand()

        return [low_back_moment, shoulder_moment]

    @staticmethod
    def midpoint(left_body_part, right_body_part):
        midpoint_x = (left_body_part[0] + right_body_part[0]) / 2
        midpoint_y = (left_body_part[1] + right_body_part[1]) / 2
        midpoint_z = (left_body_part[2] + right_body_part[2]) / 2

        return [midpoint_x, midpoint_y, midpoint_z]

    @staticmethod
    def magnitude(vector):
        return math.sqrt(sum(pow(element, 2) for element in vector))

    