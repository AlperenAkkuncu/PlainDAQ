# PlainDAQ
An Open Source DAQ module for Raspberry Pi Pico

PlainDAQ is a simple, yet useful DAQ module for your Raspberry Pi Pico. It's got 4 analog inputs, a single analog output channel. It can also output ±5V to power external curcuitry that needs symetrical power supply. It optionally includes a simple UART-to-BLE module for wireless connectivity.

Short List of features:

Analog Inputs:
• 4 Channels (multiplexed)  
• 12-bit resolution, 72dB SNR (11.6 ENOB,4000:1 dynamic range)  
• 500 kS/s sampling rate. 
• ±0.5V, ±1V, ±2V, ±4V bipolar ranges.  
• Auto-off calibration. 

Analog Output:  
• 10-bit resolution.  
• 50 kS/s sampling rate.  
• ±4V bipolar range.  

Voltage Reference:
• 2.5V, 20ppm/°C (Typical) Drift  
• Calibrate to 0.05%, Stored in as ROM as calibration data. 

Bipolar Voltage Supply: 
• ±5V power output.   
• ±100mA current rating.    

BLE Module:   
• RAYTAC MDBT42T-AT   
• Bluetooth v5.1    
• Simple UART interface to Raspberry Pico   

Some preliminary pics of the 2D and 3D model of PlainDAQ:
![image](https://user-images.githubusercontent.com/95479952/150742505-596f1a6b-7473-4fc2-9701-bc9f864f2c53.png)
![image](https://user-images.githubusercontent.com/95479952/150743290-590c0edf-d1c8-4169-84f5-43aeb313c938.png)

Here is a hand assembled PlainDAQ, doesn't it look pretty? 😀
![PlainDAQ-angle-02](https://user-images.githubusercontent.com/95479952/150743679-856e5686-c5f7-48ab-8af0-7fbeebe9454c.jpg)


