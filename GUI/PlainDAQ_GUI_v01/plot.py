from tkinter import ttk
import tkinter
import gc
import math
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backend_bases import MouseButton
from  matplotlib.markers import MarkerStyle
from matplotlib.path import Path
import matplotlib.patches as patches
import time
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Plotter:
    def __init__(self, root):

        self.root = root
        self.fig, self.ax = plt.subplots(layout = "tight")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.ax.set_facecolor("#fafafa")
        self.fig.set_facecolor("#fafafa")
        # ********************
        # Generate data
        # ********************
        self.num_sample = 3000
        self.timestep = 1/self.num_sample
        self.x = np.linspace(0, 1, self.num_sample)
        self.y = 5+2*np.sin(2*np.pi*self.x)
        #self.ax.tick_params('y',labelsize = 1)
        #sinewave
        self.waveform, = self.ax.plot([], [], 'k-', alpha = 0.9)
        self.waveform.set_color( '#4169E1' )

        # ********************
        # Vertical cursors
        # ********************
        self._is_cursor_visible = False
        self.cursor_0, = self.ax.plot([], [], 'k-')
        self.cursor_0.set_color( '#041004' )
        self.cursor_1, = self.ax.plot([], [], 'k-')
        self.cursor_1.set_color( '#041004' )
        
        self.cursor_ind_0 = 0   #cursor_0's index
        self.cursor_ind_1 = 0   #cursor_1's index

        self.cursor_verts = [(0,0), # left, bottom
                            (0,0),  # left, top
                            (0,0),  # right, top
                            (0,0),  # right, bottom
                            (0,0),  # ignored
                            ]
        self.cursor_codes = [   Path.MOVETO,
                                Path.LINETO,
                                Path.LINETO,
                                Path.LINETO,
                                Path.CLOSEPOLY,]
        self.cursor_path = Path(self.cursor_verts, self.cursor_codes)
        self.cursor_patch = patches.PathPatch(self.cursor_path, facecolor='Blue', lw=1, alpha = 0.2, hatch = '///' )
        self.cursor_patch.set(visible = False)
        self.ax.add_patch(self.cursor_patch)


        # Set up plot parameters
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 10)
        self.ax.grid(True)

        # ********************
        # Text for measurement
        # ********************
        self.text_stats = self.ax.text(0.02,8.5,u"\u25B3t : \nrms: \np-to-p",bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   ))
        self.text_stats.set(visible = False)

        self.text_fps = self.ax.text(0.8,9.4,"FPS: ",bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   ))
        self.time_exec = 0
        self.time_start = 0



        self.button_press_ID = plt.connect('button_press_event', self.on_click)
        self.button_release_ID = plt.disconnect('button_release_event')
        self.motion_notify_ID = plt.disconnect('motion_notify_event')

    """
    Called by controller to update the measurement data
    """
    def set_y_data(self, y_data):
        self.y = y_data
    """
    Called by controller to update the time base
    """
    def set_x_data(self, x_data):
        self.x = x_data

    def set_data(self, x_data, y_data):
        self.x = x_data
        self.y = y_data
        self.waveform.set_data(self.x ,self.y )

    def set_num_sample(self, num_samples):
        self.num_sample = num_samples
        self.timestep = 1/self.num_sample

    def update_vertical_cursors(self):
        if self._is_cursor_visible:
            delta_t = self.x[self.cursor_ind_1] - self.x[self.cursor_ind_0]
            if self.cursor_ind_0 != self.cursor_ind_1:
                if self.cursor_ind_0 > self.cursor_ind_1:
                    rms = np.sqrt(np.mean(np.square(self.y[self.cursor_ind_1:self.cursor_ind_0]))) #RMS text
                    p_to_p = np.ptp(self.y[self.cursor_ind_1:self.cursor_ind_0]) #peak to peak text

                    self.cursor_verts = [   (self.x[self.cursor_ind_1],self.ax.get_ylim()[0]), # left, bottom
                                            (self.x[self.cursor_ind_1],self.ax.get_ylim()[1]), # left, top
                                            (self.x[self.cursor_ind_0],self.ax.get_ylim()[1]), # right, top  
                                            (self.x[self.cursor_ind_0],self.ax.get_ylim()[0]), # right, bottom
                                            (0,0), # ignored
                                            ]
                    self.cursor_path = Path(self.cursor_verts, self.cursor_codes)
                    self.cursor_patch.set_path(self.cursor_path)
                    self.cursor_patch.set(visible = True)

                else:
                    rms = np.sqrt(np.mean(np.square(self.y[self.cursor_ind_0:self.cursor_ind_1]))) #RMS text
                    p_to_p = np.ptp(self.y[self.cursor_ind_0:self.cursor_ind_1]) #peak to peak text

                    self.cursor_verts = [   (self.x[self.cursor_ind_0],self.ax.get_ylim()[0]), # left, bottom
                                            (self.x[self.cursor_ind_0],self.ax.get_ylim()[1]), # left, top
                                            (self.x[self.cursor_ind_1],self.ax.get_ylim()[1]), # right, top  
                                            (self.x[self.cursor_ind_1],self.ax.get_ylim()[0]), # right, bottom
                                            (0,0), # ignored
                                            ]
                    self.cursor_path = Path(self.cursor_verts, self.cursor_codes)
                    self.cursor_patch.set_path(self.cursor_path)
                    self.cursor_patch.set(visible = True)
                
                self.text_stats.set_text( u"\u25B3t : %1.4f\nrms: %2.4f\np-to-p: %2.4f"%(delta_t,rms,p_to_p) )
                self.text_stats.set(visible = True)
    
    def __call__(self,i):

        self.time_exec = time.perf_counter()- self.time_start
        self.time_start = time.perf_counter()
        
        if __name__ == "__main__":
            #Generate Sinewave with random frequeny, amplitude and phase
            amplitude = np.random.randint(3,4,size=1)
            freq = 4
            phase = np.random.uniform(0,0.1,size=1)
            self.generate_sinewave(freq,amplitude,phase)
            self.waveform.set_data(self.x, self.y)
        
        #set text
        self.update_vertical_cursors()
        
        #set FPS text
        fps = 1/self.time_exec
        self.text_fps.set_text( "FPS: %2.1f"%fps ) 
       
        #update graph
        return  self.text_stats, self.text_fps, self.waveform, \
                self.cursor_0, self.cursor_1, self.cursor_patch,

    def generate_sinewave(self, freq, amplitude, phase):
        self.y = 5+amplitude*np.sin(2*np.pi*freq*self.x+phase*np.pi) + np.random.normal(0, 1, self.num_sample)/10
        
    def on_click(self, event):
        if event.inaxes:
            if event.button == MouseButton.LEFT:
                print("Left pressed!")
                print("Deleting Cursors")
                if len(self.cursor_0.get_data()[0]) != 0:
                    self._is_cursor_visible = False
                    self.cursor_0.set(visible = False)
                    self.cursor_1.set(visible = False)
                    self.text_stats.set(visible = False)
                    self.cursor_patch.set(visible = False)
                                   

            elif event.button == MouseButton.MIDDLE:
                print("Middle pressed!")
                print("Filling!")
                self._is_cursor_visible = True
                self.cursor_0.set(visible = True)
                self.cursor_1.set(visible = True)
                self.cursor_0.set_data( [event.xdata,event.xdata],[ self.ax.get_ylim()[0],self.ax.get_ylim()[1] ] )
                self.cursor_1.set_data( [event.xdata,event.xdata],[ self.ax.get_ylim()[0],self.ax.get_ylim()[1] ] )
                self.cursor_ind_0 = int(event.xdata/self.timestep)
                self.button_release_ID = plt.connect('button_release_event', self.on_release)
                self.motion_notify_ID = plt.connect('motion_notify_event', self.on_motion)
    
    def on_release(self, event):
        if event.inaxes:
            if event.button == MouseButton.MIDDLE:
                print("Middle released!")
                plt.disconnect(self.motion_notify_ID)
                plt.disconnect(self.button_release_ID)
            

    def on_motion(self, event):
        if event.inaxes:
            self.cursor_1.set_data( [event.xdata,event.xdata],[ self.ax.get_ylim()[0],self.ax.get_ylim()[1] ] )
            self.cursor_ind_1 = int(event.xdata/self.timestep)

    def start_anim(self, interval):
        self.anim = FuncAnimation(self.fig, self, frames = 100, interval = interval, blit=True)

    

if __name__ == "__main__":

    def on_closing():
        root.destroy()
        sys.exit()
       

    root = tkinter.Tk()
    plotter = Plotter(root)
    plotter.canvas.get_tk_widget().pack(expand=True, fill=tkinter.BOTH)

    root.wm_title("Sinewave Stress Test")
    root.protocol("WM_DELETE_WINDOW", on_closing)

    anim = FuncAnimation(plotter.fig, plotter, frames=100, interval=1, blit=True)

    tkinter.mainloop()