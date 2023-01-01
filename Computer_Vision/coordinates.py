import numpy as np


coordinates = np.load('testing_output1.gif.npy')
print(coordinates)
print(f'Number of keypoints: {coordinates[0].size/3}')
