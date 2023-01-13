import numpy as np


coordinates = np.load('albert_output.npy')
left_shoulder = coordinates[0][11]
right_shoulder = coordinates[0][14]
distance = ((left_shoulder[0] - right_shoulder[0])**2 + (left_shoulder[1] - right_shoulder[1])**2 + (left_shoulder[2] - right_shoulder[2])**2)**0.5
print(f'Distance between left shoulder and right shoulder: {round(distance*100, 2)}cm')
print(f'My actual shoulder length: 43cm')
print(f'Error: {round(43 - round(distance*100, 2), 2)}cm')
print(f'Number of keypoints: {coordinates[0].size/3}')
