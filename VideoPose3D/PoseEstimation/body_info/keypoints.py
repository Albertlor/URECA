import json


# #17 Keypoints
# BOTTOM_TORSO = 0
# RIGHT_HIP = 1
# RIGHT_KNEE = 2
# RIGHT_FOOT = 3
# LEFT_HIP = 4
# LEFT_KNEE = 5
# LEFT_FOOT = 6
# CENTER_TORSO = 7
# UPPER_TORSO = 8 #THORAX
# NOSE = 9 #NECK BASE
# CENTER_HEAD = 10
# LEFT_SHOULDER = 11
# LEFT_ELBOW = 12
# LEFT_HAND = 13 #WRIST
# RIGHT_SHOULDER = 14
# RIGHT_ELBOW = 15
# RIGHT_HAND = 16 #WRIST


class Keypoints:
    """
    This module has the functionalities as follows:
    1. Obtain the keypoint of low back
    2. Obtain the keypoints of shoulders
    3. Obtain the keypoints of hands
    """
    KEYPOINTS_NAMELIST = ['BOTTOM_TORSO', 'RIGHT_HIP', 'RIGHT_KNEE', 'RIGHT_FOOT', \
                          'LEFT_HIP', 'LEFT_KNEE', 'LEFT_FOOT', \
                          'CENTER_TORSO', 'UPPER_TORSO', 'NOSE', 'CENTER_HEAD', \
                          'LEFT_SHOULDER', 'LEFT_ELBOW', 'LEFT_HAND', \
                          'RIGHT_SHOULDER', 'RIGHT_ELBOW', 'RIGHT_HAND']
    
    def __init__(self, coordinates, individual=1):
        self.coordinates = coordinates
        self.individual = individual

    def body_part_keypoint(self):
        body_part_dict_json_list = []
        count_body_part = 0
        for BODY_PART in Keypoints.KEYPOINTS_NAMELIST:
            count = 1
            body_part_dict = {}
            for coordinate in self.coordinates:
                body_part = coordinate[count_body_part].tolist()
                body_part_dict[f'{BODY_PART}_{count}'] = body_part
                count += 1
            body_part_dict_json = Keypoints.to_json(body_part_dict)
            body_part_dict_json_list.append(body_part_dict_json)
            count_body_part+=1
        return body_part_dict_json_list

    @staticmethod
    def to_json(data):
        return json.dumps(data, indent=4)