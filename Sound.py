
import math
import pyaudio
import wave
import time

import numpy as np

from SoundSource import SoundSource


class Sound:
    """ 
    Housing all of the sound related components to the project,
    including:
        - Placing sound sources at locations and specifying which files to play
        - Calculating users position relative to those sound sources
        - Adjusting volume level and for which channel the sounds go to
        - Outputting these final calculation results to the users specified earbuds/headphones
        - Doing all of it quick enough so as to not cause too much latency or in other words,
        for the sound not to be laggy and cause a poor/unpleasant experience.
    """

    def __init__(self, buffer_size, outputDevice):

        self.buffer_size = buffer_size
        self.outputDevice = outputDevice

        sound_source_1 = None
        sound_source_2 = None
        sound_source_3 = None

        self.SPEED_OF_SOUND = 343
        self.mix = np.zeros(2*self.buffer_size, dtype=np.int16)
        self.data_out = np.zeros(2*self.buffer_size, dtype=np.int16)
        self.left_channel_current_place = 0
        self.right_channel_current_place = 0
        self.amp_left = 1
        self.amp_right = 1
        self.angle = 0
        
        self.wf = wave.open("Sound_Sources/flowing_stream.wav", "rb")
        self.pa = pyaudio.PyAudio()
        
        self.stream_out = self.pa.open(
            rate=self.wf.getframerate(),
            channels=2,
            format=self.pa.get_format_from_width(self.wf.getsampwidth()),
            output=True,
            output_device_index=3,
            frames_per_buffer=self.buffer_size
        )
        

        # Read the entire .wav file into memory once before the stream
        whole_audio_data_source1 = self.wf.readframes(self.wf.getnframes())
        print("Length: ", len(whole_audio_data_source1))

        # Convert the whole file into a workable numpy array
        whole_audio_data = np.frombuffer(whole_audio_data_source1, dtype=np.int16)

        # Splitting the interleaved file into each channel for (hopefully)
        # better independent control of each
        self.whole_audio_data_left = whole_audio_data[0::2]
        self.whole_audio_data_right = whole_audio_data[1::2]

    def create_sound_source(self, sound_source_number, file_path, source_position_vector):

        # Only doing one sound at the moment
        if(sound_source_number == 1):
            sound_source_1 = SoundSource(file_path, source_position_vector)
    

    def ITD(self, distance_from_listener, angle_in_rad):
        time = abs(distance_from_listener/self.SPEED_OF_SOUND * (angle_in_rad + math.sin(angle_in_rad)))

        return time

    def ILD(self, angle_in_rad):
        return math.cos(angle_in_rad)


    def compute(self, users_orientation_vector):
        start_time = time.time()
        first_time = True
        print("Meow:", users_orientation_vector[0])

        position_of_sound_angle = float(users_orientation_vector[0])

        frame_delay = int(self.ITD(1, position_of_sound_angle))
        amp_diff = self.ILD(position_of_sound_angle)

        if(first_time):
            delay = np.zeros((frame_delay))
            if (position_of_sound_angle >= 0) and (position_of_sound_angle < np.pi):
                self.whole_audio_data_left = np.insert(self.whole_audio_data_left, 0, delay, axis=0)
                self.amp_left = (amp_diff * self.amp_right) + 0.1
            else:
                self.whole_audio_data_right = np.insert(self.whole_audio_data_right, 0, delay, axis=0)
                self.amp_right = (amp_diff * self.amp_left) + 0.1


        # This needs to be at the end of the execution so it sends the right 
        # format to be played out on the speakers
        self.mix[0::2] = self.amp_left * self.whole_audio_data_left[self.left_channel_current_place:self.left_channel_current_place + self.buffer_size]
        self.mix[1::2] = self.amp_right * self.whole_audio_data_right[self.right_channel_current_place:self.right_channel_current_place + self.buffer_size]
        data_out = np.chararray.tobytes(self.mix.astype(np.int16))
        self.stream_out.write(data_out)

        # Moving the markers ahead by a full buffer size
        self.left_channel_current_place += self.buffer_size
        self.right_channel_current_place += self.buffer_size



    def output_sound_to_user(self, orientationVector):
        self.compute(orientationVector)        
