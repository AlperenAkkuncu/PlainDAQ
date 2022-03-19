import tkinter
import math
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from  matplotlib.markers import MarkerStyle
import time
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class UpdateWaveform:
    def __init__(self, ax):
        
        #sinewave
        self.line, = ax.plot([], [], 'k-')
        self.line.set_color( '#4169E1' )
        #marker line
        self.marker_line, = ax.plot([], [], 'k-')
        self.marker_line.set_color( '#32CD32' )
        #marker
        self.marker, = ax.plot([], [], 'k-', markersize = 12)
        self.marker_style = MarkerStyle(marker = 'o', fillstyle = 'full' )
        self.marker.set_marker(self.marker_style)
        self.marker.set_color('#FF8C00')

        self.num_sample = 2000
        self.x = np.linspace(0, 1, self.num_sample)
        self.y = 5+2*np.sin(2*np.pi*self.x)
        self.ax = ax

        # Set up plot parameters
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 10)
        self.ax.grid(True)

        self.text_x = self.ax.text(0.02,9,"x: \ny: ",bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   ))
        self.text_fps = self.ax.text(0.8,9.4,"FPS: ",bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   ))
        self.time_exec = 0
        self.time_start = 0
    
    def __call__(self,i):

        self.time_exec = time.perf_counter()- self.time_start
        self.time_start = time.perf_counter()
        
        #Generate Sinewave with random frequeny, amplitude and phase
        amplitude = np.random.randint(3,5,size=1)
        freq = np.random.randint(1,10,size=1)
        phase = np.random.uniform(0,2,size=1)
        self.generate_sinewave(freq,amplitude,phase)
        self.line.set_data(self.x, self.y)

        #Generate a random point in the plot and set the marker to that point
        _rand_sample = np.random.randint(0,self.num_sample,size=1)
        self.marker_line.set_data( [self.x[_rand_sample],0.158] , [self.y[_rand_sample],8.8] )
        
        #set marker pos
        self.marker.set_data([self.x[_rand_sample]],[self.y[_rand_sample]])
        self.marker.set_marker(self.marker_style)
        
        #set text
        self.text_x.set_text( "x: %1.4f\ny: %1.4f"%(self.x[_rand_sample],self.y[_rand_sample]) )
        
        #set FPS text
        fps = 1/self.time_exec
        self.text_fps.set_text( "FPS: %2.1f"%fps ) 
        
        #update graph
        return  self.text_x, self.text_fps, self.line, self.marker_line, self. marker,

    def generate_sinewave(self, freq, amplitude, phase):
        self.y = 5+amplitude*np.sin(2*np.pi*freq*self.x+phase*np.pi)  + np.random.normal(0, 1, self.num_sample)/10
        

def on_closing():
    root.destroy()
    sys.exit()

root = tkinter.Tk()
root.wm_title("Sinewave Stress Test")
root.protocol("WM_DELETE_WINDOW", on_closing)

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=0,row=1)
#canvas.draw()

uw = UpdateWaveform(ax)
anim = FuncAnimation(fig, uw, frames=100, interval=3, blit=True)

tkinter.mainloop()
