
import math

import numpy as np


class Math:

    def __init__(self):
        pass


    def ITD(self, speed_of_sound, distance_from_listener, angle_in_rad):

        time = abs(distance_from_listener/speed_of_sound * (angle_in_rad + math.sin(angle_in_rad)))

        return time

    def ILD(self, angle_in_rad):
        return math.cos(angle_in_rad)

    def roll_rotation(self, angle):
        rotation_matrix = np.array((1, 0,              0            ),
                                   (0, np.cos(angle), -np.sin(angle)),
                                   (0, np.sin(angle),  np.cos(angle)))

        return rotation_matrix
    
    def pitch_rotation(self, angle):
        rotation_matrix = np.array((np.cos(angle), 0, np.sin(angle)),
                                   (0, 1, 0),
                                   (-np.sin(angle), 0,  np.cos(angle)))

        return rotation_matrix

    def yaw_rotation(self, angle):
        rotation_matrix = np.array(((np.cos(angle), -np.sin(angle), 0),
                                   (np.sin(angle), np.cos(angle), 0),
                                   (0, 0,  1)))

        return rotation_matrix    

    def angle_compute(self, sound_position_vector, orientationVector, soundSourceNumber=1):
        position_wrt_fixed_ref_frame = sound_position_vector

        yaw_angle = np.radians(float(orientationVector[0]))
        #print("eep:", position_wrt_fixed_ref_frame)
        #print("HMM1:", position_wrt_fixed_ref_frame)

        position_wrt_moving_ref_frame = np.matmul(position_wrt_fixed_ref_frame, self.yaw_rotation(yaw_angle))

        #print("HMM: ", position_wrt_moving_ref_frame)

        angle_top = np.dot(position_wrt_fixed_ref_frame[0], position_wrt_moving_ref_frame[0])
        angle_bot = (np.linalg.norm(position_wrt_fixed_ref_frame) * np.linalg.norm(position_wrt_moving_ref_frame)) + 0.001
        #print("top: ", angle_top)
        #print("bottom: ", angle_bot)
        return np.arccos(angle_top/angle_bot)