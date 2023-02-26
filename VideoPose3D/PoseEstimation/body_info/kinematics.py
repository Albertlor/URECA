import math
import numpy as np
import json

from body_info.utils import midpoint, magnitude


class Position:
    vector_y = [0,-1,0] #vector of y axis
    r_1 = [] # position vector from low back to hand
    r_2 = [] # position vector from low back to forearm
    r_3 = [] # position vector from low back to upper arm
    r_4 = [] # position vector from low back to COM of torso
    r_5 = [] # position vector from low back to upper torso
    r_6 = [] # position vector from low back to head

    def __init__(self, load, low_back, center_torso, upper_torso, center_head, left_shoulder, left_elbow, left_hand, 
                 right_shoulder, right_elbow, right_hand):
        self.load = load
        self.low_back = low_back
        self.center_torso = center_torso
        self.upper_torso = upper_torso
        self.center_head = center_head
        self.left_shoulder = left_shoulder
        self.left_elbow = left_elbow
        self.left_hand = left_hand
        self.right_shoulder = right_shoulder
        self.right_elbow = right_elbow
        self.right_hand = right_hand

    """
    Position Vectors
    """
    def position_from_low_back_to_hand(self):
        midpoint_of_hands = midpoint(self.left_hand, self.right_hand)

        Position.r_1 = [(midpoint_of_hands[0] - self.low_back[0]), \
                        (midpoint_of_hands[1] - self.low_back[1]), \
                        (midpoint_of_hands[2] - self.low_back[2])]

    def position_from_low_back_to_forearm(self):
        midpoint_of_hands = midpoint(self.left_hand, self.right_hand)
        midpoint_of_elbows = midpoint(self.left_elbow, self.right_elbow)

        position_from_elbow_to_forearm_COM = [(midpoint_of_hands[0] - midpoint_of_elbows[0]), \
                                              (midpoint_of_hands[1] - midpoint_of_elbows[1]), \
                                              (midpoint_of_hands[2] - midpoint_of_elbows[2])] * 0.4574

        position_from_low_back_to_elbow = [(midpoint_of_elbows[0] - self.low_back[0]), \
                                           (midpoint_of_elbows[1] - self.low_back[1]), \
                                           (midpoint_of_elbows[2] - self.low_back[2])]

        Position.r_2 = [(position_from_elbow_to_forearm_COM[0] + position_from_low_back_to_elbow[0]), \
                        (position_from_elbow_to_forearm_COM[1] + position_from_low_back_to_elbow[1]), \
                        (position_from_elbow_to_forearm_COM[2] + position_from_low_back_to_elbow[2])]

    def position_from_low_back_to_upperarm_COM(self):
        midpoint_of_shoulders = midpoint(self.left_shoulder, self.right_shoulder)
        midpoint_of_elbows = midpoint(self.left_elbow, self.right_elbow)

        position_from_shoulder_to_upperarm_COM = [(midpoint_of_elbows[0] - midpoint_of_shoulders[0]), \
                                                  (midpoint_of_elbows[1] - midpoint_of_shoulders[1]), \
                                                  (midpoint_of_elbows[2] - midpoint_of_shoulders[2])] * 0.5772

        position_from_low_back_to_shoulder = [(midpoint_of_shoulders[0] - self.low_back[0]), \
                                              (midpoint_of_shoulders[1] - self.low_back[1]), \
                                              (midpoint_of_shoulders[2] - self.low_back[2])]

        Position.r_3 = [(position_from_shoulder_to_upperarm_COM[0] + position_from_low_back_to_shoulder[0]), \
                        (position_from_shoulder_to_upperarm_COM[1] + position_from_low_back_to_shoulder[1]), \
                        (position_from_shoulder_to_upperarm_COM[2] + position_from_low_back_to_shoulder[2])]

    def position_from_low_back_to_center_torso(self):
        Position.r_4 = [(self.center_torso[0] - self.low_back[0]), \
                        (self.center_torso[1] - self.low_back[1]), \
                        (self.center_torso[2] - self.low_back[2])]

    def position_from_low_back_to_upper_torso(self):
        Position.r_5 = [(self.upper_torso[0] - self.low_back[0]), \
                        (self.upper_torso[1] - self.low_back[1]), \
                        (self.upper_torso[2] - self.low_back[2])]

    def position_from_low_back_to_head(self):
        Position.r_6 = [(self.center_head[0] - self.low_back[0]), \
                        (self.center_head[1] - self.low_back[1]), \
                        (self.center_head[2] - self.low_back[2])]


    """
    Magnitude of Position Vectors
    """
    def dist_from_shoulder_to_hand(self):
        midpoint_of_shoulders = midpoint(self.left_shoulder, self.right_shoulder)
        midpoint_of_hands = midpoint(self.left_hand, self.right_hand)
        distance = magnitude([(midpoint_of_shoulders[0] - midpoint_of_hands[0]), \
                              (midpoint_of_shoulders[1] - midpoint_of_hands[1]), \
                              (midpoint_of_shoulders[2] - midpoint_of_hands[2])])

        return distance

    def dist_from_low_back_to_hand(self):
        midpoint_of_hands = midpoint(self.left_hand, self.right_hand)
        distance = magnitude([(self.low_back[0] - midpoint_of_hands[0]), \
                              (self.low_back[1] - midpoint_of_hands[1]), \
                              (self.low_back[2] - midpoint_of_hands[2])])

        return distance

    def dist_from_low_back_to_shoulder(self):
        midpoint_of_shoulders = midpoint(self.left_shoulder, self.right_shoulder)
        distance = magnitude([(self.low_back[0] - midpoint_of_shoulders[0]), \
                              (self.low_back[1] - midpoint_of_shoulders[1]), \
                              (self.low_back[2] - midpoint_of_shoulders[2])])

        return distance


    """
    Velocity Vector
    """
    def velocity_from_low_back_to_hand(self):
        pass


    """
    Magnitude of Angular Displacement
    """
    def angle_between_spine_and_z_axis(self):
        v1 = np.array(Position.r_5)
        v2 = np.array(Position.vector_y)
        v1_mag = magnitude(v1)
        v2_mag = magnitude(v2)
        dot_product = np.dot(v1, v2)
        theta = math.acos(dot_product/(v1_mag * v2_mag))
        return theta

    