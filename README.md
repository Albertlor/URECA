# Undergraduate Research Project
## Monocular Vision-Based 3D Human Pose Estimation and Cumulative Damage Assessment at Industrial Workplaces
### Publication of the paper on IEEE: https://ieeexplore.ieee.org/abstract/document/10406589
### The entire program was designed and created by me when I was an undergraduate student in year 2 while working with Asst Prof Kim Jinwoo.
### This research aims to study how to improve the existing ergonomics risk assessment at industrial workplaces. One of the vulnerable body parts is the lumbar, where this was the body part that we were tackling with. 
## How to run?
### Step 1: Clone the project repo
```
git clone git@github.com:Albertlor/URECA.git
```
### Step 2: Change directory into the project repo
```
cd VideoPose3D/PoseEstimation
```
### Step 3: Render the 3D video using VideoPose3D. Refer to the link below for the details
```
https://github.com/facebookresearch/VideoPose3D/blob/main/INFERENCE.md
```
### Step 4: Run the program using the following command:
```
python3 main.py --body_part low_back --exist 1 --individual 1 --video <actual_video_path>
```
Replace the <actual_video_path> with the path of 3D rendered video using VideoPose3D.
