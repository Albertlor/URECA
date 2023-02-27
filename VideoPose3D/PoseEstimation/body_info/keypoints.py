import json


#17 Keypoints
BOTTOM_TORSO = 0
RIGHT_HIP = 1
RIGHT_KNEE = 2
RIGHT_FOOT = 3
LEFT_HIP = 4
LEFT_KNEE = 5
LEFT_FOOT = 6
CENTER_TORSO = 7
UPPER_TORSO = 8 #THORAX
NOSE = 9 #NECK BASE
CENTER_HEAD = 10
LEFT_SHOULDER = 11
LEFT_ELBOW = 12
LEFT_HAND = 13 #WRIST
RIGHT_SHOULDER = 14
RIGHT_ELBOW = 15
RIGHT_HAND = 16 #WRIST

KEYPOINTS_NAMELIST = ['BOTTOM_TORSO', 'RIGHT_HIP', 'RIGHT_KNEE', 'RIGHT_FOOT', \
                      'LEFT_HIP', 'LEFT_KNEE', 'LEFT_FOOT', \
                      'CENTER_TORSO', 'UPPER_TORS0', 'NOSE', 'CENTER_HEAD', \
                      'LEFT_SHOULDER', 'LEFT_ELBOW', 'LEFT_HAND', \
                      'RIGHT_SHOULDER', 'RIGHT_ELBOW', 'RIGHT_HAND']

class Keypoints:
    """
    This module has the functionalities as follows:
    1. Obtain the keypoint of low back
    2. Obtain the keypoints of shoulders
    3. Obtain the keypoints of hands
    """
    def __init__(self, coordinates, individual=1):
        self.coordinates = coordinates
        self.individual = individual

    def low_back_keypoint(self):
        count = 1
        low_back_dict = {}
        for coordinate in self.coordinates:
            low_back = coordinate[BOTTOM_TORSO].tolist()
            low_back_dict[f'BOTTOM_TORSO_{count}'] = low_back
            count += 1
        low_back_dict_json = Keypoints.to_json(low_back_dict)

        return low_back_dict_json

    def center_torso_keypoint(self):
        count = 1
        center_torso_dict = {}
        for coordinate in self.coordinates:
            center_torso = coordinate[CENTER_TORSO].tolist()
            center_torso_dict[f'CENTER_TORSO_{count}'] = center_torso
            count += 1
        center_torso_dict_json = Keypoints.to_json(center_torso_dict)

        return center_torso_dict_json

    def upper_torso_keypoint(self):
        count = 1
        upper_torso_dict = {}
        for coordinate in self.coordinates:
            upper_torso = coordinate[UPPER_TORSO].tolist()
            upper_torso_dict[f'UPPER_TORSO_{count}'] = upper_torso
            count += 1
        upper_torso_dict_json = Keypoints.to_json(upper_torso_dict)

        return upper_torso_dict_json

    def center_head_keypoint(self):
        count = 1
        center_head_dict = {}
        for coordinate in self.coordinates:
            center_head = coordinate[CENTER_HEAD].tolist()
            center_head_dict[f'CENTER_HEAD_{count}'] = center_head
            count += 1
        center_head_dict_json = Keypoints.to_json(center_head_dict)

        return center_head_dict_json

    def left_shoulder_keypoint(self):
        count = 1
        left_shoulder_dict = {}
        for coordinate in self.coordinates:
            left_shoulder = coordinate[LEFT_SHOULDER].tolist()
            left_shoulder_dict[f'LEFT_SHOULDER_{count}'] = left_shoulder
            count += 1
        left_shoulder_dict_json = Keypoints.to_json(left_shoulder_dict)

        return left_shoulder_dict_json

    def left_elbow_keypoint(self):
        count = 1
        left_elbow_dict = {}
        for coordinate in self.coordinates:
            left_elbow = coordinate[LEFT_ELBOW].tolist()
            left_elbow_dict[f'LEFT_ELBOW_{count}'] = left_elbow
            count += 1
        left_elbow_dict_json = Keypoints.to_json(left_elbow_dict)

        return left_elbow_dict_json

    def left_hand_keypoint(self):
        count = 1
        left_hand_dict = {}
        for coordinate in self.coordinates:
            left_hand = coordinate[LEFT_HAND].tolist()
            left_hand_dict[f'LEFT_HAND_{count}'] = left_hand
            count += 1
        left_hand_dict_json = Keypoints.to_json(left_hand_dict)

        return left_hand_dict_json

    def right_shoulder_keypoint(self):
        count = 1
        right_shoulder_dict = {}
        for coordinate in self.coordinates:
            right_shoulder = coordinate[RIGHT_SHOULDER].tolist()
            right_shoulder_dict[f'RIGHT_SHOULDER_{count}'] = right_shoulder
            count += 1
        right_shoulder_dict_json = Keypoints.to_json(right_shoulder_dict)

        return right_shoulder_dict_json

    def right_elbow_keypoint(self):
        count = 1
        right_elbow_dict = {}
        for coordinate in self.coordinates:
            right_elbow = coordinate[RIGHT_ELBOW].tolist()
            right_elbow_dict[f'RIGHT_ELBOW_{count}'] = right_elbow
            count += 1
        right_elbow_dict_json = Keypoints.to_json(right_elbow_dict)

        return right_elbow_dict_json

    def right_hand_keypoint(self):
        count = 1
        right_hand_dict = {}
        for coordinate in self.coordinates:
            right_hand = coordinate[RIGHT_HAND].tolist()
            right_hand_dict[f'RIGHT_HAND_{count}'] = right_hand
            count += 1
        right_hand_dict_json = Keypoints.to_json(right_hand_dict)

        return right_hand_dict_json

    @staticmethod
    def to_json(data):
        return json.dumps(data, indent=4)

    # @staticmethod
    # def items_to_json(data):
    #     with open('data.json', 'w') as json_file:
    #         json_file.write('{')
    #         json.dump(data, json_file, separators=(',', ':'))
    #         json_file.write('}')