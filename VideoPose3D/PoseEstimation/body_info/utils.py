import math
import matplotlib.pyplot as plt
import numpy as np


def midpoint(left_body_part, right_body_part):
        midpoint_x = (left_body_part[0] + right_body_part[0]) / 2
        midpoint_y = (left_body_part[1] + right_body_part[1]) / 2
        midpoint_z = (left_body_part[2] + right_body_part[2]) / 2

        return [midpoint_x, midpoint_y, midpoint_z]

def magnitude(vector):
    return math.sqrt(sum(pow(element, 2) for element in vector))

def moment_of_inertia(load, mass, m, k_s, k_t, k_l, L):
    I_xx = (m * mass) * (k_s * L)**2 #moment of inertia about sagittal axis
    I_yy = (m * mass) * (k_l * L)**2 #moment of inertia about longitudinal axis
    I_zz = (m * mass) * (k_t * L)**2 #moment of inertia about longitudinal axis

    return I_xx + I_yy + I_zz

x1_values = []
x2_values = []
y1_values = []
y2_values = []

previous_y2 = 0

def cumulative_damage(frame, count_peak, risk_back, accumulated_risk_back):
    x1_values.append(frame)
    y1_values.append(risk_back)

    if frame == 1:
        x2_values.append(count_peak)
        y2_values.append(accumulated_risk_back)
    
    elif accumulated_risk_back != previous_y2 and frame != 1:
        x2_values.append(count_peak)
        y2_values.append(accumulated_risk_back)

    # clear previous plot
    plt.clf()
    
    # plot new data
    plt.plot(x1_values, y1_values, 'go-', linewidth=1, markersize=3)
    plt.plot(x2_values, y2_values, 'ro-', linewidth=1, markersize=3)
    
    # add plot decorations (e.g. title, labels)
    plt.title('Ergonomic Risk of Low Back')
    plt.xlabel('Frame')
    plt.ylabel('Risk')
    
    # set axis limits (optional)
    plt.xlim(0, 2000)
    plt.ylim(0, 1)
    
    # pause briefly to allow plot to be displayed
    plt.pause(0.01)

def non_cumulative_damage(risk_level):
    # Define the center and radius of the semicircle
    center = [0.5, 0.5]
    radius = 0.5

    # Create an array of angles to define the semicircle
    angles = np.linspace(0, np.pi, 100)

    # Create the x and y coordinates of the semicircle
    x = center[0] + radius * np.cos(angles)
    y = center[1] + radius * np.sin(angles)

    # Create a figure and axis object to plot the diagram
    fig, ax = plt.subplots(figsize=(6, 6))

    # Plot the semicircle
    ax.plot(x, y, 'k')

    # Create a list of colors for the different risk levels
    colors = ['g', 'r']

    # Calculate the angle to rotate the pointer based on the risk level
    if risk_level == 'low':
        angle = np.deg2rad(30)
    elif risk_level == 'high':
        angle = np.deg2rad(270)

    # Create the x and y coordinates of the pointer
    pointer_x = [center[0] - radius * 0.05, center[0] + radius * 0.05, center[0] + radius * 0.2 * np.cos(angle)]
    pointer_y = [center[1], center[1], center[1] + radius * 0.2 * np.sin(angle)]

    # Plot the pointer
    ax.fill(pointer_x, pointer_y, 'r')

    # Set the axis limits and remove the ticks
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.set_xticks([])
    ax.set_yticks([])

    # Show the plot
    plt.show()