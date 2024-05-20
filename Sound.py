


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

    def __init__(self):

        sound_source_1 = None
        sound_source_2 = None
        sound_source_3 = None

    def create_sound_source(self, sound_source_number, file_path, source_position_vector):
        pass
    

    def compute(self, users_orientation_vector, users_position_vector):
        pass


    def output_sound_to_user(self):
        pass
