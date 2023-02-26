import math
import json

from body_info.kinematics import Position
from body_info.utils import trigonometry


class Dynamics(Position):
    def __init__(self, load, low_back, center_torso, upper_torso, center_head, left_shoulder, left_elbow, left_hand, \
                 right_shoulder, right_elbow, right_hand):
        super().__init__(load, low_back, center_torso, upper_torso, center_head, left_shoulder, left_elbow, left_hand, \
                         right_shoulder, right_elbow, right_hand)

    def force(self):
        position = Position(load=self.load, low_back=self.low_back, center_torso=self.center_torso, upper_torso=self.upper_torso, \
                            center_head=self.center_head, left_shoulder=self.left_shoulder, left_elbow=self.left_elbow, left_hand=self.left_hand, \
                            right_shoulder=self.right_shoulder, right_elbow=self.right_elbow, right_hand=self.right_hand)

        v1 = position.velocity_from_low_back_to_hand()

    def moment(self):
        position = Position(load=self.load, low_back=self.low_back, center_torso=self.center_torso, upper_torso=self.upper_torso, \
                            center_head=self.center_head, left_shoulder=self.left_shoulder, left_elbow=self.left_elbow, left_hand=self.left_hand, \
                            right_shoulder=self.right_shoulder, right_elbow=self.right_elbow, right_hand=self.right_hand)

        position.position_from_low_back_to_upper_torso()
        angles = trigonometry(position.dist_from_low_back_to_shoulder(), position.dist_from_low_back_to_hand(), position.dist_from_shoulder_to_hand())
        theta = position.angle_between_spine_and_z_axis()
        A, B, C = angles
        
        angle_for_low_back = theta + C
        angle_for_shoulder = (theta + C) + A


        low_back_moment = (self.load * math.sin(angle_for_low_back)) * position.dist_from_low_back_to_hand()
        shoulder_moment = (self.load * math.sin(angle_for_shoulder)) * position.dist_from_shoulder_to_hand()

        

        return [low_back_moment, shoulder_moment, theta]