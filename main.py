
# Date: 11 May 2024
# Program: Central program where user will interact with backend components
#   (the composer/maestro to the programs symphony)



# Define where are the 3x UWB location anchors that are being used 
""" 
Position.set_anchors(position1)
Position.set_anchors(position2)
Position.set_anchors(position3) 
"""

# Define which file names to play, the locations of the sound sources,
# and where the users location is w.r.t. the sounds
""" 
Sound.create_sound_source(filename, positionVectorOfItsLocation)
Sound.create_sound_source(filename, positionVectorOfItsLocation) 
.
.
.
"""

# Start the programs tracking and adjusting audio levels based on it
""" 
while True:
    user_Position = Position.getUserPosition()
    user_Orientation = Orientation.getUserOrientation()

    Sound.output_sound_to_user(desiredOutputDevice, user_Orientation, user_Position) 
"""


