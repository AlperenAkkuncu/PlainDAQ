
import os
import logging
from plot import Plotter
import tkinter as tk
from tkinter import FLAT, SUNKEN, Frame, ttk
import sys
import ttkthemes
import signal
from PIL import ImageTk, Image



class GUI:
    def __init__(self):
        
        self.GUI_logger = logging.getLogger('example_logger')
        self.GUI_logger.warning('This is a warning')
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        #setting theme
        theme_path = os.path.dirname(__file__) + "/Sun-Valley-ttk-theme-master/sun-valley.tcl"
        self.root.tk.call("source", theme_path)
        self.root.tk.call("set_theme", "light")

        #FONTS
        self.font_big = ("Ubuntu", 20, "bold")
        self.button_font = ("Ubuntu", 10, )
        self.font_header = ("Ubuntu", 12, "bold")
        self.font_normal = ("Ubuntu", 10, )
        #ttk styles
        self.style = ttk.Style()
        self.style.configure('big.TButton', font=("Ubuntu", 10, "bold"))
        self.style.configure('bold.TRadiobutton', font=("Ubuntu", 10, "bold"))

        self.pack_frames()
        self.start_plotter()
        self.start_bottom_frame()
        self.start_left_frame()
        

    def pack_frames(self):
        self.left_frame = ttk.Frame(self.root, relief="sunken", padding=(5,10), width = 220)
        self.left_frame.pack(expand=False, fill = tk.Y, side = tk.LEFT)
        self.bottom_frame = Frame(self.root)
        #self.bottom_frame.pack(expand=False, fill = tk.X, side = tk.BOTTOM )
        self.plotter = Plotter(self.root)
        self.plotter.canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)

    def start_plotter(self):
        self.root.wm_title("PlainDAQ GUI v0.1")
        self.plotter.start_anim(1)

    def start_bottom_frame(self):
        self.PlainDAQ_label = ttk.Label(self.bottom_frame, text = "bottom frame", justify = tk.CENTER)
        self.PlainDAQ_label.pack()
        self.dummy_button = ttk.Button(self.bottom_frame, text = "dummy")
        self.dummy_button.pack()


    def start_left_frame(self):

        #Kuncu teknoloji logo
        _image_label = Image.open("icons/kuncu_logo.png")
        _image_label = _image_label.resize((120,110),Image.ANTIALIAS)
        self.img_logo = ImageTk.PhotoImage(_image_label)    
        self.logo_label = tk.Label(self.left_frame,height = 150, image = self.img_logo)
        self.logo_label.pack(expand = False, side = tk.TOP)

        #Input Channels FrameLabel
        self.channel_ON_OFF_frame_text = ttk.Label(self.left_frame, text="Channels:", font=self.font_header)
        self.channel_ON_OFF_frame = ttk.LabelFrame(self.left_frame, labelwidget=self.channel_ON_OFF_frame_text ,
        width = 150, height = 50, padding = 10)
        
        #Channel ON/OFF buttons
        self.CH1_button_var = tk.IntVar()
        self.CH2_button_var = tk.IntVar()
        self.CH3_button_var = tk.IntVar()
        self.CH4_button_var = tk.IntVar()
        self.CH1_button = ttk.Checkbutton(self.channel_ON_OFF_frame ,text = "CH1",
        width = 4, variable=self.CH1_button_var, onvalue = 1, offvalue = 0)
        self.CH1_button.grid(column=0, row=0, padx=0,ipadx = 0)
        self.CH2_button = ttk.Checkbutton(self.channel_ON_OFF_frame ,text = "CH2",
        width = 4, variable=self.CH2_button_var, onvalue = 1, offvalue = 0)
        self.CH2_button.grid(column=0, row=1, padx=0)
        self.CH3_button = ttk.Checkbutton(self.channel_ON_OFF_frame ,text = "CH3",
        width = 4, variable=self.CH3_button_var, onvalue = 1, offvalue = 0)
        self.CH3_button.grid(column=0, row=2, padx=0)
        self.CH4_button = ttk.Checkbutton(self.channel_ON_OFF_frame ,text = "CH4",
        width = 4, variable=self.CH4_button_var, onvalue = 1, offvalue = 0)
        self.CH4_button.grid(column=0, row=3, padx=0)


        #number of samples Frame Label
        self.numsample_label = ttk.Label(self.left_frame, text="Num. Samples:", font=self.font_header)
        self.numsample_label_frame = ttk.LabelFrame(self.left_frame, labelwidget=self.numsample_label,
        width = 150, height = 50, padding = 10)
        
        #number of samples combobox
        self.numsample_combobox = ttk.Combobox(self.numsample_label_frame, values = ["1000","2000"], width=19)
        self.numsample_combobox.pack()

        #Range select FrameLabel
        self.range_select_frame_text = ttk.Label(self.left_frame, text="Range: ", font=self.font_header)
        self.range_select_frame = ttk.LabelFrame(self.left_frame, labelwidget=self.range_select_frame_text ,
        width = 150, height = 50, padding = 10)
        
        ##RadioButton for range selection
        self.range_sel_radio_var = tk.IntVar()
        self.range_sel_RadioButton_0V5 = ttk.Radiobutton(self.range_select_frame, text = u"\u00B1" + "0.5V",
        style="bold.TRadiobutton", variable=self.range_sel_radio_var, value = 0.5, compound=tk.BOTTOM)
        self.range_sel_RadioButton_0V5.grid(column=0, row=0)
        self.range_sel_RadioButton_1V = ttk.Radiobutton(self.range_select_frame, text = u"\u00B1" + "1V   ",
        style="bold.TRadiobutton", variable=self.range_sel_radio_var, value = 1, compound=tk.BOTTOM)
        self.range_sel_RadioButton_1V.grid(column=0, row=1)
        self.range_sel_RadioButton_2V = ttk.Radiobutton(self.range_select_frame, text = u"\u00B1" + "2V   ",
        style="bold.TRadiobutton", variable=self.range_sel_radio_var, value = 2, compound=tk.BOTTOM)
        self.range_sel_RadioButton_2V.grid(column=0, row=2)
        self.range_sel_RadioButton_4V = ttk.Radiobutton(self.range_select_frame, text = u"\u00B1" + "4V   ",
        style="bold.TRadiobutton", variable=self.range_sel_radio_var, value = 4, compound=tk.BOTTOM)
        self.range_sel_RadioButton_4V.grid(column=0, row=3)
        self.range_sel_RadioButton_0V5.invoke() #pick 0.5V range as default

        #Y-Scale notebook
        self.y_scale_notebook = ttk.Notebook(self.left_frame)
        self.y_scale_CH1_y_scale = ttk.Frame(self.y_scale_notebook, width=150, height=100)
        self.y_scale_CH1_y_scale.pack(fill="both", expand=True)
        self.y_scale_CH2_y_scale = ttk.Frame(self.y_scale_notebook)
        self.y_scale_CH2_y_scale.pack(fill="both", expand=True)
        self.y_scale_CH3_y_scale = ttk.Frame(self.y_scale_notebook)
        self.y_scale_CH3_y_scale.pack(fill="both", expand=True)
        self.y_scale_CH4_y_scale = ttk.Frame(self.y_scale_notebook)
        self.y_scale_CH4_y_scale.pack(fill="both", expand=True)

        self.y_scale_notebook.add(self.y_scale_CH1_y_scale, text="CH1")
        self.y_scale_notebook.add(self.y_scale_CH2_y_scale, text="CH2")
        self.y_scale_notebook.add(self.y_scale_CH3_y_scale, text="CH3")
        self.y_scale_notebook.add(self.y_scale_CH4_y_scale, text="CH4")


        #Trigger Panel
        self.trigger_frame_text = ttk.Label(self.left_frame, text="Trigger", font=self.font_header)
        self.trigger_frame_label = ttk.LabelFrame(self.left_frame, labelwidget=self.trigger_frame_text ,
        width = 150, height = 50, padding = 10)

        #Trigger select checkbuttons
        self.CH1_trig_var = tk.IntVar()
        self.CH2_trig_var = tk.IntVar()
        self.CH3_trig_var = tk.IntVar()
        self.CH4_trig_var = tk.IntVar()
        self.CH1_trig = ttk.Checkbutton(self.trigger_frame_label ,text = "CH1",
        width = 4, variable=self.CH1_trig_var, onvalue = 1, offvalue = 0)
        self.CH1_trig.grid(column=0, row=0, padx=0,ipadx = 0)
        self.CH2_trig = ttk.Checkbutton(self.trigger_frame_label ,text = "CH2",
        width = 4, variable=self.CH2_trig_var, onvalue = 1, offvalue = 0)
        self.CH2_trig.grid(column=0, row=1, padx=0)
        self.CH3_trig = ttk.Checkbutton(self.trigger_frame_label ,text = "CH3",
        width = 4, variable=self.CH3_trig_var, onvalue = 1, offvalue = 0)
        self.CH3_trig.grid(column=0, row=2, padx=0)
        self.CH4_trig = ttk.Checkbutton(self.trigger_frame_label ,text = "CH4",
        width = 4, variable=self.CH4_trig_var, onvalue = 1, offvalue = 0)
        self.CH4_trig.grid(column=0, row=3, padx=0)
        

        self.left_frame_place_widgets()
        

    def left_frame_place_widgets(self):
        #self.input_label_frame.place(x=10, y=30)
        self.logo_label.place(x=50, y=1)
        
        self.range_select_frame.place(x=12, y=150)
        self.channel_ON_OFF_frame.place(x=112, y= 150)
        self.numsample_label_frame.place(x=12, y=310)
        self.trigger_frame_label.place(x=12, y=390)
        
        #self.y_scale_notebook.place(x=10, y=250)

    def on_closing(self):
        if __name__ != "__main__":
            signal.raise_signal(signal.SIGTERM) #signal controller to terminate the program
        else:
            pass
        self.root.destroy()
        sys.exit()

if __name__ == "__main__":
    gui = GUI()
    tk.mainloop()