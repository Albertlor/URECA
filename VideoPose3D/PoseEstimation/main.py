import os
import argparse

from utils.keypoints import Keypoints
from utils.calculation import Calculation
from database.database import Database
from pprint import pprint

ap = argparse.ArgumentParser()
ap.add_argument("-b", "--body_part", type=str, help="body part to study")
ap.add_argument("-e", "--exist", type=int, required=True, help="Read existing json file or Create new json file")
ap.add_argument("-i", "--individual", type=int, required=True, help="Which individual are you specifying")
args = vars(ap.parse_args())


JSON_FILENAME = {
    "LOW_BACK": "low_back_dict_json.json",
    "UPPER_TORSO": "upper_torso_dict_json.json",
    "RIGHT_SHOULDER": "right_shoulder_dict_json.json",
    "RIGHT_HAND": "right_hand_dict_json.json",
    "LEFT_SHOULDER": "left_shoulder_dict_json.json",
    "LEFT_HAND": "left_hand_dict_json.json"
}


"""
The person we want to specify
"""
INDIVIDUAL = args["individual"]
LOAD = 50 #in Newton


"""
Select an option about reading an existing json file from database or create a new one to database
"""
if args["exist"] == 1:
    NEW_KEYPOINTS = False
elif args["exist"] == 0:
    NEW_KEYPOINTS = True
else:
    print('Please enter a valid command')

# If reading an existing json file from database
if NEW_KEYPOINTS == False:
    BODY_PART_LIST = ["LOW_BACK", 
                      "UPPER_TORSO", 
                      "RIGHT_SHOULDER", 
                      "RIGHT_HAND", 
                      "LEFT_SHOULDER", 
                      "LEFT_HAND"]

    JSONFILEPATH_DICT = {}
    for BODY_PART in BODY_PART_LIST:
        JSONFILEPATH = rf"C:\Users\ASUS\Academic\URECA\VideoPose3D\PoseEstimation\database\json_data\Individual_{INDIVIDUAL}\{JSON_FILENAME[BODY_PART]}"
        JSONFILEPATH_DICT[BODY_PART] = JSONFILEPATH

    database = Database(jsonPathDict=JSONFILEPATH_DICT, individual=INDIVIDUAL)

# If creating a new json file to database
else:
    NPYFILEPATH = rf"C:\Users\ASUS\Academic\URECA\VideoPose3D\PoseEstimation\database\npy_data\Individual_{INDIVIDUAL}\Individual_{INDIVIDUAL}_output.npy"
    database = Database(npyPath=NPYFILEPATH, individual=INDIVIDUAL)


"""
Specify the directory where the JSON file has to be written to. 
"""
PARENT_DIRECTORY = r"C:\Users\ASUS\Academic\URECA\VideoPose3D\PoseEstimation\database\json_data"
DIRECTORY = f"Individual_{INDIVIDUAL}"
PATH = os.path.join(PARENT_DIRECTORY, DIRECTORY)


def read_from_database(new_keypoints=True):
    """
    1. Start the entire pipeline by retrieving the dataset from the database
    2. If 'new_keypoints' is specified as 'True', writes the new result to the database
    3. If not, it's just simply reading the existing data
    """
    if new_keypoints == True:
        coordinates = database.read_npy_data()
        try:
            if coordinates.all():
                write_to_database(coordinates)
        except AttributeError:
            pass

    else:
        coordinates = database.read_json_data()
        
        body_part_dict = {}
        coordinates_list = []
        count = 0
        for coordinate in coordinates.values():
            for i in coordinate.values():
                coordinates_list.append(i)
        
            body_part_dict[BODY_PART_LIST[count]] = coordinates_list
            count += 1

        # pprint(body_part_dict, indent=4)
        return body_part_dict
    
def write_to_database(coordinates):
    """
    1. Check if the directory exists or not
    2. Write the JSON file into the database
    """
    create_directory()
    keypoints = Keypoints(coordinates, individual=INDIVIDUAL)
    json_file_dict = {}
    json_file_dict['low_back_dict_json'] = keypoints.low_back_keypoint()
    json_file_dict['upper_torso_dict_json'] = keypoints.upper_torso_keypoint()
    json_file_dict['right_shoulder_dict_json'] = keypoints.right_shoulder_keypoint()
    json_file_dict['right_hand_dict_json'] = keypoints.right_hand_keypoint()
    json_file_dict['left_shoulder_dict_json'] = keypoints.left_shoulder_keypoint()
    json_file_dict['left_hand_dict_json'] = keypoints.left_hand_keypoint()

    for filename, file in json_file_dict.items():
        database.write_json_data(json_file=file, json_filename=filename)

def create_directory():
    """
    Create a new directory for output json file if the directory doesn't exist
    """
    if os.path.isdir(PATH) == False:
        os.mkdir(PATH)
        print(f'Successfully created directory {DIRECTORY}!')  

def main():
    body_part_dict = read_from_database(new_keypoints=NEW_KEYPOINTS)
    
    low_back = body_part_dict['LOW_BACK'][0]
    upper_torso = body_part_dict['UPPER_TORSO'][0]
    right_shoulder = body_part_dict['RIGHT_SHOULDER'][0]
    right_hand = body_part_dict['RIGHT_HAND'][0]
    left_shoulder = body_part_dict['LEFT_SHOULDER'][0]
    left_hand = body_part_dict['LEFT_HAND'][0]

    calculation = Calculation(load=LOAD, low_back=low_back, upper_torso=upper_torso, right_shoulder=right_shoulder, right_hand=right_hand, \
                              left_shoulder=left_shoulder, left_hand=left_hand)
    
    moment = calculation.moment()

    body_part = (args["body_part"]).lower()

    if body_part == 'low_back':
        print(f'Moment about Low Back: {moment[0]}Nm')
    elif body_part == 'shoulder':
        print(f'Moment about Shoulders: {moment[1]}Nm')
    elif body_part == 'all':
        print(f'Moment about Low Back: {moment[0]}Nm')
        print(f'Moment about Shoulders: {moment[1]}Nm')
    else:
        print('Please enter a valid command!')

if __name__ == '__main__':
    main()