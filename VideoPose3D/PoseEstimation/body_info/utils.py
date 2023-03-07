import math
import matplotlib.pyplot as plt
import random
from itertools import count

from matplotlib.animation import FuncAnimation


def midpoint(left_body_part, right_body_part):
        midpoint_x = (left_body_part[0] + right_body_part[0]) / 2
        midpoint_y = (left_body_part[1] + right_body_part[1]) / 2
        midpoint_z = (left_body_part[2] + right_body_part[2]) / 2

        return [midpoint_x, midpoint_y, midpoint_z]

def magnitude(vector):
    return math.sqrt(sum(pow(element, 2) for element in vector))

def moment_of_inertia(load, weight, m, k_s, k_t, k_l, L):
    I_xx = (m * weight) * (k_s * L)**2 #moment of inertia about sagittal axis
    I_yy = (m * weight) * (k_l * L)**2 #moment of inertia about longitudinal axis
    I_zz = (m * weight) * (k_t * L)**2 #moment of inertia about longitudinal axis

    return I_xx + I_yy + I_zz

x_values = []
y1_values = []
y2_values = []

def animate(frame, risk_back, accumulated_risk_back):
    x_values.append(frame)
    y1_values.append(risk_back)
    y2_values.append(accumulated_risk_back)

    # clear previous plot
    plt.clf()
    
    # plot new data
    plt.plot(x_values, y1_values, 'go-', linewidth=1, markersize=3)
    plt.plot(x_values, y2_values, 'ro-', linewidth=1, markersize=3)
    
    # add plot decorations (e.g. title, labels)
    plt.title('Ergonomic Risk of Low Back')
    plt.xlabel('Frame')
    plt.ylabel('Risk')
    
    # set axis limits (optional)
    plt.xlim(0, 1000)
    plt.ylim(0, 1)
    
    # pause briefly to allow plot to be displayed
    plt.pause(0.01)
