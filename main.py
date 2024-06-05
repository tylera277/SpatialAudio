
# Date: 11 May 2024
# Program: Central program where user will interact with backend components
#   (the composer/maestro to the programs symphony)

from MainCode.Orientation import Orientation
from MainCode.Sound import Sound

import numpy as np


pico_port = "/dev/cu.usbmodem14101"
#desiredOutputDevice = 3


outputSound1 = "../../Sound_Sources/flowing_stream.wav"
positionOfSound1 = np.zeros((1,3))
positionOfSound1[0,1] = 2

outputSound2 = "../../Sound_Sources/chirping_birds.wav"
positionOfSound2 = np.zeros((1,3))
positionOfSound2[0,1] = -2


# Instantiate each classes object
o = Orientation(pico_port)
s1 = Sound(buffer_size=512, outputDevice=2)
#s2 = Sound(buffer_size=512, outputDevice=2)

# Define where are the 3x UWB location anchors that are being used 
# (will be used for position data eventually)
""" 
Position.set_anchors(position1)
Position.set_anchors(position2)
Position.set_anchors(position3) 
"""

# Define which file names to play, the locations of the sound sources,
# and where the users location is w.r.t. the sounds

s1.create_sound_source(1, outputSound1, positionOfSound1)
#s2.create_sound_source(1, outputSound2, positionOfSound2)
"""
Sound.create_sound_source(filename, positionVectorOfItsLocation) 
.
.
.
"""

s1.preliminary_computes()
#s2.preliminary_computes()
# Start the programs tracking and adjusting audio levels based on it
while True:
    user_Orientation = np.array(o.read())
    s1.output_sound_to_user(user_Orientation) 
    #s2.output_sound_to_user(user_Orientation)
    print(user_Orientation)
