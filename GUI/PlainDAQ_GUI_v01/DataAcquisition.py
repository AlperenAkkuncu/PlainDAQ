import usb.core
import usb.util
import numpy as np
import time


class DataAcquirer:
    def __init__(self, simulate_data = False):
        if simulate_data == True:
            self.sampling_rate = 1/500000 #500kHz sampling rate
        else:
            pass

    #Generates a fake sine data.
    #Only for simulation
    def generate_fake_data(self,time_base, freq, amplitude, offset):
        return  offset \
        + amplitude*np.sin(2*np.pi*freq*time_base+np.random.uniform(0,0.1,size=1)*np.pi)  \
        + np.random.normal(0, amplitude/10, len(time_base))
