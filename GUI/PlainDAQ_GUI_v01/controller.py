from GUI import GUI
from DataAcquisition import DataAcquirer
import tkinter
import signal
import threading
import numpy as np

class Controller:
    def __init__(self, simulate_data = False):
        self.gui = GUI()
        self.model = DataAcquirer(simulate_data)
       
        #tThreads for shutting down the software gracefully
        self.SIGINT_event = threading.Event()
        self.SIGTERM_event = threading.Event()
        signal.signal(signal.SIGINT, self.SIGINT_handler)
        signal.signal(signal.SIGTERM, self.SIGTERM_handler)

        #Measurement data
        self.num_sample = 4000
        self.gui.plotter.set_num_sample(self.num_sample)
        self.time_base = np.linspace(-1, 1, self.num_sample)

        if simulate_data:
            self.gen_fake_data = threading.Timer(1, self.generate_fake_data)
            self.gen_fake_data.start()

    def generate_fake_data(self):
        if self.SIGINT_event.is_set() or self.SIGTERM_event.is_set():
            pass
        else:
            _y = self.model.generate_fake_data(self.time_base,2,7,3.5)   
            self.gui.plotter.set_data(self.time_base, _y)
            self.gen_fake_data = threading.Timer(0.05, self.generate_fake_data)
            self.gen_fake_data.start()
    
    def SIGINT_handler(self, signum, frame):
        print("SIGINT")
        self.SIGINT_event.set()

    def SIGTERM_handler(self,signum, frame):
        print("SIGTERM")
        self.SIGTERM_event.set()
        
if __name__ == "__main__":
    controller = Controller(simulate_data = True)
    tkinter.mainloop()    