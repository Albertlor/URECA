# Import the necessary libraries
import numpy as np

# Define the path to the AMC file
amc_file_path = "C:\\Users\\ASUS\\Academic\\URECA\\VideoPose3D\\PoseEstimation\\sandwich002.AMC"

# Define a dictionary to store the joint coordinates
joint_coordinates = {}

# Open the AMC file and read the lines
with open(amc_file_path, 'r') as f:
    lines = f.readlines()

# Loop through the lines and extract the joint coordinates
for line in lines:
    # Check if the line starts with the "root" keyword, indicating the start of a new frame
    if line.startswith('root'):
        # Split the line into words and get the frame number
        words = line.split()
        frame_number = int(words[1])
        
        # Initialize a dictionary to store the joint coordinates for this frame
        joint_coordinates[frame_number] = {}
        
        # Loop through the next lines until the end of the frame is reached
        while True:
            next_line = f.readline()
            
            # Check if the end of the frame has been reached
            if next_line.startswith('}'):
                break
            
            # Split the line into words and get the joint name and coordinates
            words = next_line.split()
            joint_name = words[0]
            coordinates = np.array([float(x) for x in words[1:]])
            
            # Add the joint coordinates to the dictionary
            joint_coordinates[frame_number][joint_name] = coordinates