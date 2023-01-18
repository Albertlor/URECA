import math


class Calculation:
    def __init__(self, load, left_hand, right_hand, left_shoulder, right_shoulder, low_back):
        self.load = load
        self.left_hand = left_hand
        self.right_hand = right_hand
        self.left_shoulder = left_shoulder
        self.right_shoulder = right_shoulder
        self.low_back = low_back

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

    def moment(self):


    @staticmethod
    def midpoint(left_body_part, right_body_part):
        midpoint_x = (left_body_part[0] + right_body_part[0]) / 2
        midpoint_y = (left_body_part[1] + right_body_part[1]) / 2
        midpoint_z = (left_body_part[2] + right_body_part[2]) / 2

        midpoint = [midpoint_x, midpoint_y, midpoint_z]
        return midpoint

    @staticmethod
    def trigonometry():
        a = Calculation.dist_from_low_back_to_shoulder()
        b = Calculation.dist_from_low_back_to_hand()
        c = Calculation.dist_from_shoulder_to_hand()

        #Angle between b and c
        A = math.acos( (b**2 + c**2 - a**2) / 2*b*c )
        B = math.asin( b/a * math.sin(A) )
        C = math.pi - A - B

        angles = [A, B, C]

        return angles

    @staticmethod
    def lever_arm():
        angles = Calculation.trigonometry()
        A, B, C = angles
        
        # shoulder_lever_arm = 

        # low_back_lever_arm = 