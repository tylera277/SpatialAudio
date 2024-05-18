

import pyaudio
import wave
import threading
import time
import math
import sys

import numpy as np
import matplotlib.pyplot as plt


np.set_printoptions(threshold=sys.maxsize)



pa = pyaudio.PyAudio()

# CERTAIN PARAMETERS FOR THE CALCULATION & STREAM
volume = 0.5
frames_per_buffer = 512
position_of_sound_angle = 3*np.pi/4
position_of_sound_distance = 20

# AUDIO FILES THAT CAN BE PLAYED
wf = wave.open("Sound_Sources/chirping_birds.wav", "rb")
#wf = wave.open("Sound_Sources/flowing_stream.wav", "rb")



def ITD(distance_from_listener, angle_in_rad):
    speed_of_sound = 343
    time = abs(distance_from_listener/speed_of_sound * (angle_in_rad + math.sin(angle_in_rad)))

    return time

def ILD(angle_in_rad):
    return math.cos(angle_in_rad)


# This functionality is still being worked on (18 May 2024)
def intensity_distance_calculator(distance_from_listener):
    rhs = 20 * math.log(1/distance_from_listener)
    return (rhs)


audio_data_l = np.zeros(frames_per_buffer, dtype=np.int16)
audio_data_r = np.zeros(frames_per_buffer, dtype=np.int16)
mix = np.zeros(2*frames_per_buffer, dtype=np.int16)
data_out = np.zeros(2*frames_per_buffer, dtype=np.int16)

start_time = time.time()

time_diff = ITD(position_of_sound_distance, position_of_sound_angle)
print("Diff: ", time_diff)

amp_diff = ILD(position_of_sound_angle)
print("AMP DIFF: ", amp_diff)

    




stream_out = pa.open(
    rate=wf.getframerate(),
    channels=2,
    format=pa.get_format_from_width(wf.getsampwidth()),
    output=True,
    output_device_index=3,
    frames_per_buffer=frames_per_buffer
)

# Calculate the time delay, in term of frames, between sounds reaching each ear
frame_delay = int(time_diff * wf.getframerate())
print("frame delay: ", frame_delay)

# Read the entire .wav file into memory once before the stream
whole_audio_data_source1 = wf.readframes(wf.getnframes())
print("Length: ", len(whole_audio_data_source1))

# Convert the whole file into a workable numpy array
whole_audio_data = np.frombuffer(whole_audio_data_source1, dtype=np.int16)

# Splitting the interleaved file into each channel for (hopefully)
# better independent control of each
whole_audio_data_left = whole_audio_data[0::2]
whole_audio_data_right = whole_audio_data[1::2]

# Start the stream so I can output the buffer to output device and for it to 
# play
stream_out.start_stream()

# Markers for where in the whole array that I am currently reading from
left_channel_current_place = 0
right_channel_current_place = 0

# Setting the starting points for amplitudes of the sounds,
# will be adjusted as the sound position changes
print(intensity_distance_calculator(position_of_sound_distance))
amp_left = intensity_distance_calculator(position_of_sound_distance)
amp_right = intensity_distance_calculator(position_of_sound_distance)

first_time = True
print("Starting to output now!")

while left_channel_current_place < wf.getnframes():
    start_time = time.time()

    
    if(first_time):
        delay = np.zeros((frame_delay))
        if (position_of_sound_angle >= 0) and (position_of_sound_angle < np.pi):
            print("here")
            whole_audio_data_left = np.insert(whole_audio_data_left, 0, delay, axis=0)
            amp_left = (amp_diff * amp_right) + 0.1
        else:
            whole_audio_data_right = np.insert(whole_audio_data_right, 0, delay, axis=0)
            amp_right = (amp_diff * amp_left) + 0.1


    # This needs to be at the end of the execution so it sends the right 
    # format to be played out on the speakers
    mix[0::2] = amp_left * whole_audio_data_left[left_channel_current_place:left_channel_current_place + frames_per_buffer]
    mix[1::2] = amp_right * whole_audio_data_right[right_channel_current_place:right_channel_current_place + frames_per_buffer]
    data_out = np.chararray.tobytes(mix.astype(np.int16))
    stream_out.write(data_out)

    # Moving the markers ahead by a full buffer size
    left_channel_current_place += frames_per_buffer
    right_channel_current_place += frames_per_buffer

    first_time = False


stream_out.stop_stream()
stream_out.close()

pa.terminate()




""" For multi song playing purposes, *MAY* need this later

audio_files = ["Sound_Sources/flowing_stream.wav", "Sound_Sources/chirping_birds.wav"]

threads = []

for file in audio_files:
    thread = threading.Thread(target=play_audio, args=(file, volume))
    threads.append(thread)
    thread.start()


for thread in threads:
    thread.join()

pa.terminate() """