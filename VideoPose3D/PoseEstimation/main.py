#python main.py -b 'low_back' -e 1 -i 1 -v "C:\Users\Albertlor\Academic\URECA\VideoPose3D\PoseEstimation\database\video_data\Individual_1\Individual_1_output.mp4"

import os
import argparse
import math
import time
import cv2
import json
import numpy as np
import matplotlib.pyplot as plt

from body_info.keypoints import Keypoints
from body_info.moment import Moment
from body_info.risk_possibility import Risk
from database.database import Database

ap = argparse.ArgumentParser()
ap.add_argument("-b", "--body_part", type=str, help="body part to study")
ap.add_argument("-e", "--exist", type=int, required=True, help="Read existing json file or Create new json file")
ap.add_argument("-i", "--individual", type=int, required=True, help="Which individual are you specifying")
ap.add_argument("-v", "--video", type=str, help="path to the input video")
args = vars(ap.parse_args())


BODY_PART_LIST = ['LOW_BACK', 'RIGHT_HIP', 'RIGHT_KNEE', 'RIGHT_FOOT', \
                  'LEFT_HIP', 'LEFT_KNEE', 'LEFT_FOOT', \
                  'CENTER_TORSO', 'UPPER_TORSO', 'NOSE', 'CENTER_HEAD', \
                  'LEFT_SHOULDER', 'LEFT_ELBOW', 'LEFT_HAND', \
                  'RIGHT_SHOULDER', 'RIGHT_ELBOW', 'RIGHT_HAND']

"""
The information of the person whom we want to specify
"""
INDIVIDUAL = args["individual"]
LOAD = 230 #in Newton
WEIGHT = 600 #in Newton
ACTION_LIMIT = 3433 #in Newton
A = 5


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
    JSONFILEPATH_DICT = {}
    for BODY_PART in BODY_PART_LIST:
        JSONFILEPATH = rf"C:\Users\Albertlor\Academic\URECA\VideoPose3D\PoseEstimation\database\json_data\Individual_{INDIVIDUAL}\{BODY_PART.lower()}_dict_json.json"
        JSONFILEPATH_DICT[BODY_PART] = JSONFILEPATH

    database = Database(jsonPathDict=JSONFILEPATH_DICT, individual=INDIVIDUAL)

# If creating a new json file to database
else:
    NPYFILEPATH = rf"C:\Users\Albertlor\Academic\URECA\VideoPose3D\PoseEstimation\database\npy_data\Individual_{INDIVIDUAL}\Individual_{INDIVIDUAL}_output.npy"
    database = Database(npyPath=NPYFILEPATH, individual=INDIVIDUAL)


"""
Specify the directory where the JSON file has to be written to. 
"""
PARENT_DIRECTORY = rf"C:\Users\Albertlor\Academic\URECA\VideoPose3D\PoseEstimation\database\json_data"
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
        count = 0
        for coordinate in list(coordinates.values()):
            coordinates_list = []
            for i in list(coordinate.values()):
                
                coordinates_list.append(i)
        
            body_part_dict[BODY_PART_LIST[count]] = coordinates_list
            count += 1
        
        return body_part_dict
    
def write_to_database(coordinates):
    """
    1. Check if the directory exists or not
    2. Write the JSON file into the database
    """
    create_directory()
    keypoints = Keypoints(coordinates, individual=INDIVIDUAL)
    json_file_dict = {}
    body_part_dict_json_list = keypoints.body_part_keypoint()
    count_body_part = 0
    for BODY_PART in BODY_PART_LIST:
        json_file_dict[f'{BODY_PART.lower()}_dict_json'] = body_part_dict_json_list[count_body_part]
        count_body_part+=1

    for filename, file in json_file_dict.items():
        database.write_json_data(json_file=file, json_filename=filename)

def create_directory():
    """
    Create a new directory for output json file if the directory doesn't exist
    """
    if os.path.isdir(PATH) == False:
        os.mkdir(PATH)
        print(f'Successfully created directory {DIRECTORY}!')  


video = cv2.VideoCapture(args["video"])
count_frame = 0
replay = 0
last_time = time.time()

frame_num = 0
count_peak = 0
num_repetition = 0
current_num_repetition = 0
hold = 0 #to hold the repetition to avoid keep adding when the angle is 45 degrees
risk_back_list = []
risk_shoulder_list = []
peak_risk_back = 0
peak_risk_shoulder = 0

fig, ax = plt.subplots()
ax2 = ax.twinx()
x1_values = []
x2_values = []
y1_values = []
y2_values = []

previous_y2 = 0

set_threshold = 0
def cumulative_damage(frame_num, count_peak, force, accumulated_risk_back, risk_threshold):
    """
    Plot the graph to visualize the cumulative damage and compressive force
    """
    global set_threshold

    x1_values.append(frame_num)
    y1_values.append(force)

    if frame_num == 1:
        x2_values.append(count_peak)
        y2_values.append(accumulated_risk_back)
    
    elif accumulated_risk_back != previous_y2 and frame_num != 1:
        x2_values.append(count_peak)
        y2_values.append(accumulated_risk_back)

    # clear previous plot
    ax.cla()
    ax2.cla()
    
    # plot new data
    orange_line = ax.axhline(y=3433, linestyle='--', color='orange')
    blue_line = ax2.axhline(y=risk_threshold, linestyle='--', color='blue')
    green_line, = ax.plot(x1_values, y1_values, 'go-', linewidth=1, markersize=1)
    red_line, = ax2.plot(x2_values, y2_values, 'ro-', linewidth=1, markersize=1)
    handles = [orange_line, green_line, blue_line, red_line]
    
    # add plot decorations (e.g. title, labels)
    plt.title('Ergonomic Risk of Low Back')
    ax.set_xlabel('Frame')
    ax.set_ylabel('Force')
    ax2.set_ylabel('Risk')
    ax2.yaxis.set_label_coords(1.1, 0.5)
    
    # set axis limits (optional)
    ax.set_xlim(0, 2000)
    ax.set_ylim(0, 6000)
    ax2.set_ylim(0, 1)

    # add legend
    ax.legend(handles=handles, loc='upper right', labels=['Action Limit', 'Force', 'Risk Threshold', 'Risk'], facecolor='white', edgecolor='black')
    
    # pause briefly to allow plot to be displayed
    plt.pause(0.01)
    
while True:
    count_frame += 1
    frame_num += 1
    if video.get(cv2.CAP_PROP_FRAME_COUNT) == count_frame:
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        count_frame = 1
        replay = 1

    ret, frame = video.read()
    duration = time.time() - last_time

    last_time = time.time()
    time.sleep(0.000000001)
    fps = str(round((1/duration), 2))

    if ret and (count_frame%5==0):
        #frame = imutils.resize(frame, width=800, inter=cv2.INTER_LINEAR)
        cv2.putText(frame, "fps: " + fps, (50, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

        body_part_dict = read_from_database(new_keypoints=NEW_KEYPOINTS)
        
        try:
            # low_back = body_part_dict['LOW_BACK'][count_frame]
            # center_torso = body_part_dict['CENTER_TORSO'][count_frame]
            # upper_torso = body_part_dict['UPPER_TORSO'][count_frame]
            # center_head = body_part_dict['CENTER_HEAD'][count_frame]
            # left_shoulder = body_part_dict['LEFT_SHOULDER'][count_frame]
            # left_elbow = body_part_dict['LEFT_ELBOW'][count_frame]
            # left_hand = body_part_dict['LEFT_HAND'][count_frame]
            # right_shoulder = body_part_dict['RIGHT_SHOULDER'][count_frame]
            # right_elbow = body_part_dict['RIGHT_ELBOW'][count_frame]
            # right_hand = body_part_dict['RIGHT_HAND'][count_frame]

            with open('config.json', 'w') as f:
                json.dump({"Individual": INDIVIDUAL,
                        "Load": LOAD,
                        "Weight": WEIGHT,
                        "Duration": duration,
                        "Frame": count_frame 
                        }, f, indent=4)

            if video.get(cv2.CAP_PROP_POS_FRAMES) >= 4:
                moment = Moment()
                M = moment.moment()

                if (M[3] * 180 / math.pi) >= 45 and hold == 0:
                    current_num_repetition = num_repetition + 1
                    hold = 1
                elif (M[3] * 180 / math.pi) < 45:
                    hold = 0

                risk = Risk(M[0], M[1], num_repetition, A)
                
                risk_back, compressive_force_back, risk_threshold = risk.risk()

                if current_num_repetition != num_repetition:
                    if risk_back_list is not None:
                        peak_risk_back = max(risk_back_list)
                        count_peak = frame_num
                    risk_back_list = []

                if current_num_repetition == num_repetition:
                    risk_back_list.append(risk_back)
                
                num_repetition = current_num_repetition #update the number of repetition to the current number of repetition

                if replay != 1:
                    with open('moment_back.json') as f1:
                        config1 = json.load(f1)

                    config1[f"Moment_Back_{count_frame}"] = M[0]

                    with open('moment_back.json', 'w') as f1:
                        json.dump(config1, f1, indent=4)

                    with open('force_back.json') as f2:
                        config2 = json.load(f2)

                    config2[f"Force_Back_{count_frame}"] = compressive_force_back

                    with open('force_back.json', 'w') as f2:
                        json.dump(config2, f2, indent=4)

                body_part = (args["body_part"]).lower()

                if body_part == 'low_back':
                    cumulative_damage(frame_num, count_peak, compressive_force_back, peak_risk_back, risk_threshold)
                    print(f'frame: {count_frame}')
                    print(f'Moment about Low Back: {M[0]}Nm')
                    print(f'Low Back Compression Force: {compressive_force_back}N')
                    print(f'Spine Flexion Angle: {M[3] * 180 / math.pi}deg')
                    print(f'Repetition: {num_repetition}')
                    print(f'Accumulated Risk Probability of Low Back: {risk_back}')
                
                    cv2.putText(frame, f'Moment about Low Back: {round(M[0], 3)}Nm', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 193, 0), 1, cv2.LINE_AA)
                    cv2.putText(frame, f'Low Back Compression Force: {round(compressive_force_back, 3)}N', (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 193, 0), 1, cv2.LINE_AA)
                    cv2.putText(frame, f'Spine Flexion Angle:   {round((M[3] * 180 / math.pi), 3)}deg', (50, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 193, 0), 1, cv2.LINE_AA)
                    cv2.putText(frame, f'Repetition: {num_repetition}', (50, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 193, 0), 1, cv2.LINE_AA)

                    if risk_back <= risk_threshold:
                        cv2.putText(frame, f'Risk:   {round((risk_back * 100), 3)}%', (50, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 193, 0), 1, cv2.LINE_AA)
                    if risk_back > risk_threshold:
                        cv2.putText(frame, f'Risk:   {round((risk_back * 100), 3)}%', (50, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1, cv2.LINE_AA)
                else:
                    print('Please enter a valid command!')

            cv2.imshow("Frames", frame)

        except TypeError as e:
            print(e)
            break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break