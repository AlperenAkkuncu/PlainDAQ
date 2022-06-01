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

        # Set up plot parameters
        self.ax.set_xlim(-1, 1)
        self.ax.set_ylim(0, 12)
        self.ax.set_xticklabels(labels = "")
        self.ax.set_yticklabels(labels = "")
        self.ax.grid(True)

        # ********************
        # Vertical cursors
        # ********************
        self.cursor_0, = self.ax.plot([], [], 'k-', marker="d",
                                    markersize=10, markerfacecolor='#4169E1',
                                    picker=True, pickradius=5)
        self.cursor_0.set_color( '#041004' )

        self.cursor_1, = self.ax.plot([], [], 'k-', marker="d",
                                    markersize=10, markerfacecolor='#4169E1',
                                    picker=True, pickradius=5)
        self.cursor_1.set_color( '#041004' )
        

        #initialize cursor positions.
        self.cursor_0.set_data( [ self.x[ int(len(self.x)*0.2) ], self.x[ int(len(self.x)*0.2) ] ],[ self.ax.get_ylim()[0],self.ax.get_ylim()[1] ] )
        self.cursor_1.set_data( [ self.x[ int(len(self.x)*0.8) ], self.x[ int(len(self.x)*0.8)  ] ],[ self.ax.get_ylim()[0],self.ax.get_ylim()[1] ] )
        
        self.cursor_0.set(visible = False)
        self.cursor_1.set(visible = False)
        
        #Filling between the cursors
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

        # ********************
        # Text for measurement
        # ********************
        self.text_stats = self.ax.text(-0.95, 11.3, u"\u25B3t : \nrms: \np-to-p",bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   ))
        self.text_stats.set(visible = False)

        self.text_fps = self.ax.text(0.78,11.7,"FPS: ",bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   ))
        self.time_exec = 0
        self.time_start = 0


        #Plot Events
        self.button_press_ID = plt.connect('button_press_event', self.on_click)
        self.button_release_ID = plt.disconnect('button_release_event')
        self.motion_notify_ID = plt.disconnect('motion_notify_event')
        self.motion_notify_ID = plt.connect('resize_event', self.on_resize)
        self.pickevent_ID = plt.disconnect('pick_event')
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
        if self.cursor_0.get_visible():
            _cursor_0_xdata = self.cursor_0.get_xdata()[0]
            _cursor_0_ind  = np.abs(self.x - _cursor_0_xdata).argmin() #closest
            
            _cursor_1_xdata = self.cursor_1.get_xdata()[0]
            _cursor_1_ind = np.abs(self.x - _cursor_1_xdata).argmin()
            
            delta_t = _cursor_0_xdata - _cursor_1_xdata
            if delta_t != 0:
                if _cursor_0_xdata > _cursor_1_xdata:
                    rms = np.sqrt(np.mean(np.square(self.y[_cursor_1_ind:_cursor_0_ind]))) #RMS text
                    p_to_p = np.ptp(self.y[_cursor_1_ind:_cursor_0_ind]) #peak to peak text

                    self.cursor_verts = [   (_cursor_1_xdata,self.ax.get_ylim()[0]), # left, bottom
                                            (_cursor_1_xdata,self.ax.get_ylim()[1]), # left, top
                                            (_cursor_0_xdata,self.ax.get_ylim()[1]), # right, top  
                                            (_cursor_0_xdata,self.ax.get_ylim()[0]), # right, bottom
                                            (0,0), # ignored
                                            ]
                    self.cursor_path = Path(self.cursor_verts, self.cursor_codes)
                    self.cursor_patch.set_path(self.cursor_path)
                    self.cursor_patch.set(visible = True)

                else:
                    rms = np.sqrt(np.mean(np.square(self.y[_cursor_0_ind:_cursor_1_ind]))) #RMS text
                    p_to_p = np.ptp(self.y[_cursor_0_ind:_cursor_1_ind]) #peak to peak text

                    self.cursor_verts = [   (_cursor_0_xdata,self.ax.get_ylim()[0]), # left, bottom
                                            (_cursor_0_xdata,self.ax.get_ylim()[1]), # left, top
                                            (_cursor_1_xdata,self.ax.get_ylim()[1]), # right, top  
                                            (_cursor_1_xdata,self.ax.get_ylim()[0]), # right, bottom
                                            (0,0), # ignored
                                            ]
                    self.cursor_path = Path(self.cursor_verts, self.cursor_codes)
                    self.cursor_patch.set_path(self.cursor_path)
                    self.cursor_patch.set(visible = True)
                
                #Set the position of edge arrows


                self.text_stats.set_text( u"\u25B3t : %1.4f\nrms: %2.4f\np-to-p: %2.4f"%(delta_t,rms,p_to_p) )
                self.text_stats.set(visible = True)
    
    def get_cursor_vis(self):
        return self.cursor_0.get_visible()
    
    def set_cursor_vis(self, val):
        self.cursor_0.set(visible = val)
        self.cursor_1.set(visible = val)
        self.text_stats.set(visible = val)
        self.cursor_patch.set(visible = val)
        
        if(val == True):
            self.pickevent_ID = plt.connect('pick_event', self.on_pick)
        else:
            plt.disconnect(self.pickevent_ID)
                                   

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
                pass

            elif event.button == MouseButton.MIDDLE:
                pass
    
    def on_release(self, event):
        if event.inaxes:
            if event.button == MouseButton.MIDDLE:
                print("Middle released!")
                plt.disconnect(self.motion_notify_ID)
                plt.disconnect(self.button_release_ID)

    def on_resize(self, event):
        pass
        #print(self.fig.get_figheight())
        #print(self.fig.get_figwidth())   

    def on_motion(self, event):
        if event.inaxes:
            pass

    def on_pick(self, event):
        
        if(event.artist == self.cursor_0):
            self.motion_notify_ID = plt.connect('motion_notify_event', self.on_motion_cursor_0)
            self.button_release_ID = plt.connect('button_release_event', self.on_release_cursor_0)

        elif(event.artist == self.cursor_1):
            self.motion_notify_ID = plt.connect('motion_notify_event', self.on_motion_cursor_1)
            self.button_release_ID = plt.connect('button_release_event', self.on_release_cursor_1)

    def on_motion_cursor_0(self, event):
        if event.inaxes:
            self.cursor_0.set_data( [event.xdata,event.xdata],[ self.ax.get_ylim()[0],self.ax.get_ylim()[1] ] )
  
    def on_release_cursor_0(self, event):   
        plt.disconnect(self.button_release_ID)
        plt.disconnect(self.motion_notify_ID)

    def on_motion_cursor_1(self, event):
        if event.inaxes:
            self.cursor_1.set_data( [event.xdata,event.xdata],[ self.ax.get_ylim()[0],self.ax.get_ylim()[1] ] )

    def on_release_cursor_1(self, event):    
        plt.disconnect(self.button_release_ID)
        plt.disconnect(self.motion_notify_ID)

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