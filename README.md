# PlainDAQ
PlainDAQ is a module that turns your Raspberry Pi Pico into a simple, precision 4-channel oscilloscope and a single channel function generator. Optionally it can also include a Wi-Fi module to add wireless capability to Raspberry Pi Pico modules.

To put it other words, PlainDAQ is a simple, useful tool to add basic precision analog functionality to your Raspberry Pi Pico board. It has a precision, low-noise, low-drift 12-bit 500kSPS/s ADC, sampling 4-channels and supporting 3 ranges (±1V, ±2V, ±4V). It also has a 10-bit DAC which helps create analog outputs and waveforms and it has a single range of ±4V.

Short List of features:

Analog Inputs:
• 4 Channels (multiplexed)  
• 12-bit resolution, 72dB SNR (11.6 ENOB,4000:1 dynamic range)  
• 500 kS/s sampling rate. 
• ±1V, ±2V, ±4V bipolar ranges.  

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

ESP-WROOM-02D AT-Command Module:
• Simple UART interface to Raspberry Pico
• Wi-Fi connectivity    
• Shipped with ESP AT firmware 


# Here are some nice pictures of PlainDAQ
![PlainDAQ_new_2](https://user-images.githubusercontent.com/95479952/184297031-ced6864b-512b-4424-949a-460321cd55f8.jpg)
![PlainDAQ_new_4](https://user-images.githubusercontent.com/95479952/184297121-dce1050f-0a05-4651-a342-d3f4e03c7a57.jpg)

### Filter! More on that later
![Filters](https://user-images.githubusercontent.com/95479952/184297323-fc78def6-4f7d-4448-9687-f404280a94a9.jpg)

## PlainDAQ Connections
![plaindaq-board-layout-1](https://user-images.githubusercontent.com/95479952/184296437-d4080dc3-fe01-415f-93ca-d07e4d21fa70.png)

## PlainDAQ Components
![plaindaq-board-layout-2](https://user-images.githubusercontent.com/95479952/184296734-acf6f79c-d416-4709-8f75-3d16918f5c03.png)



