import json
import numpy as np

from body_info.utils import magnitude


class Acceleration:
    # with open('config.json') as f:
    #     config = json.load(f)
    # dt = config['Duration']
    dt = (1/30) * 5 #0.167s

    def __init__(self,
                absolute_vector,
                relative_vector):
        self.absolute_vector = absolute_vector
        self.relative_vector = relative_vector

    def linear_acceleration(self):
        abs_r_1, abs_r_2, abs_r_3, abs_r_4 = self.absolute_vector

        abs_v_2 = np.multiply((np.array(abs_r_3) - np.array(abs_r_1)), 1/(2*Acceleration.dt))
        abs_v_3 = np.multiply((np.array(abs_r_4) - np.array(abs_r_2)), 1/(2*Acceleration.dt))

        abs_a_3 = (np.multiply((abs_v_3 - abs_v_2), 1/Acceleration.dt)).tolist()

        return abs_a_3

    def angular_acceleration(self):
        rel_r_1, rel_r_2, rel_r_3, rel_r_4 = self.relative_vector

        rel_r_2_mag = magnitude(rel_r_2)
        rel_r_3_mag = magnitude(rel_r_3)

        rel_v_2 = np.multiply((np.array(rel_r_3) - np.array(rel_r_1)), 1/(2*Acceleration.dt))
        rel_v_3 = np.multiply((np.array(rel_r_4) - np.array(rel_r_2)), 1/(2*Acceleration.dt))

        rel_v_2_mag = magnitude(rel_v_2.tolist())
        rel_v_3_mag = magnitude(rel_v_3.tolist())

        omega_2_mag = rel_v_2_mag / rel_r_2_mag
        omega_3_mag = rel_v_3_mag / rel_r_3_mag

        R2 = np.cross(np.array(rel_r_1), np.array(rel_r_2))
        R3 = np.cross(np.array(rel_r_2), np.array(rel_r_3))

        omega_2_dir = np.multiply(R2, 1/(magnitude(R2)))
        omega_3_dir = np.multiply(R3, 1/(magnitude(R3)))

        omega_2 = np.multiply(omega_2_mag, omega_2_dir)
        omega_3 = np.multiply(omega_3_mag, omega_3_dir)

        alpha_3 = (np.multiply((omega_3 - omega_2), 1/Acceleration.dt)).tolist()

        return alpha_3


