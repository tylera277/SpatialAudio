
import serial
import numpy as np
import time

class Orientation:
    """
    Class which will house all related materials used in determining a users
    orientation in space
    (Mainly interacting with the "Adafruit BNO055 Absolute Orientation Sensor" module
    that I will be using in order to get this information from/about the user)
    """
    def __init__(self, picoPortString):
        self.port_of_pico_string = picoPortString
        self.ser = serial.Serial("{}".format(self.port_of_pico_string), 115200, 8, "N", 1, timeout=.001)
        self.temp_storage = [0,0,0]




    def clean_up_orientation_vector(self):
        # I will clean up this disgrace of a parser eventually with something that looks more
        # professional

        chunks = self.temp_storage
        chunks = chunks.replace(",", "")
        chunks = chunks.replace("(", "")
        chunks = chunks.replace(")", "")

        return chunks.split()



    def read(self):
        start = time.time()
        line = self.ser.readline()
        #print(line.decode("utf-8"))
        if line:
            #file.write(line.decode("utf-8"))
            self.temp_storage = line.decode("utf-8")

        print("Execution time=", time.time()-start)
        #print("BEEP:", self.temp_storage.split())
        return self.clean_up_orientation_vector()

    
    def getUserOrientation(self):
        orientation = np.array((self.get_phi(), self.get_theta(), self.get_psi()))
        return orientation