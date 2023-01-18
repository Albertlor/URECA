import os

from utils.keypoints import Keypoints
from database.database import Database
from pprint import pprint


JSON_FILENAME = {
    "LEFT_HAND": "left_hand_dict_json.json",
    "LEFT_SHOULDER": "left_shoulder_dict_json.json",
    "LOW_BACK": "low_back_dict_json.json",
    "RIGHT_HAND": "right_hand_dict_json.json",
    "RIGHT_SHOULDER": "right_shoulder_dict_json.json"
}


"""
Specify which person we are going to study
"""
while True:
    INDIVIDUAL = input("Which person are you specifying?: ")
    if str(INDIVIDUAL).isdigit() == True:
        break
    else:
        print('Please enter an integer')
        continue


"""
Select an option about reading an existing json file from database or create a new one to database
"""
while True:
    EXIST = input('Read an existing data? (True/False): ')
    if EXIST in ['TRUE', 'True', 'true', 'T', 't']:
        NEW_KEYPOINTS = False
        break
    elif EXIST in ['FALSE', 'False', 'false', 'F', 'f']:
        NEW_KEYPOINTS = True
        break
    else:
        print('Please enter a valid command')
        continue

# If reading an existing json file from database
if NEW_KEYPOINTS == False:
    BODY_PART_LIST = []
    while True:
        BODY_PART = input('Enter a body part of interest: ')
        BODY_PART_LIST.append(BODY_PART)
        answer = input('Any other body part of interest?: ')
        if answer in ['Yes', 'yes', 'Y', 'y']:
            continue
        elif answer in ['No', 'no', 'N', 'n']:
            break
        else:
            print('Please enter a valid command')

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

        pprint(body_part_dict, indent=4)
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
    json_file_dict['left_shoulder_dict_json'] = keypoints.left_shoulder_keypoint()
    json_file_dict['right_shoulder_dict_json'] = keypoints.right_shoulder_keypoint()
    json_file_dict['left_hand_dict_json'] = keypoints.left_hand_keypoint()
    json_file_dict['right_hand_dict_json'] = keypoints.right_hand_keypoint()

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
    read_from_database(new_keypoints=NEW_KEYPOINTS)

if __name__ == '__main__':
    main()