
# Date: 11 May 2024
# Program: Central program where user will interact with backend components
#   (the composer/maestro to the programs symphony)

from Orientation import Orientation
from Sound import Sound

import numpy as np


pico_port = "/dev/cu.usbmodem14101"
desiredOutputDevice = 3


outputSound1 = "Sound_Sources/flowing_stream.wav"
#outputSound1 = "Sound_Sources/chirping_birds.wav"
positionOfSound1 = np.zeros((1,3))
positionOfSound1[0,0] = 1

# Instantiate each classes object
o = Orientation(pico_port)
s = Sound(buffer_size=512, outputDevice=3)

# Define where are the 3x UWB location anchors that are being used 
# (will be used for position data eventually)
""" 
Position.set_anchors(position1)
Position.set_anchors(position2)
Position.set_anchors(position3) 
"""

# Define which file names to play, the locations of the sound sources,
# and where the users location is w.r.t. the sounds

s.create_sound_source(1, outputSound1, positionOfSound1)

"""
Sound.create_sound_source(filename, positionVectorOfItsLocation) 
.
.
.
"""

s.preliminary_computes()

# Start the programs tracking and adjusting audio levels based on it
while True:
    user_Orientation = np.array(o.read())
    print("USER:", user_Orientation)
    s.output_sound_to_user(user_Orientation) 
    #print("---------------")


