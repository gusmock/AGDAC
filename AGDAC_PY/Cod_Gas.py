# --------------------
#  AGDAC_Automatic Gas Data Acquisition for Gas Counters 
# --------------------

# Author : Carla Isabel Flores Rodriguez 


# Library definition
# ----------------------
import serial
#import serial_open as puerto
import os
import time as time
import csv
import pandas as pd
import datetime as dt 
from dateutil.relativedelta import relativedelta # Time difference
#from drawnow import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec           # gridspec
import sys

# Set up the serial port
# ----------------------
#arduino_port = puerto.str1
arduino_port = 'COM7'              # UBS port name assignation
baud_rate = 9600                   # Bits transference per second 
arduinoData = serial.Serial(arduino_port, baud_rate)
print(arduino_port,' is open', arduinoData.isOpen())
arduinoData.flushInput()           # Remove junk and noise -> clear the computer's input buffer
auxiliarWaiting = 0

# Data saving variables
# ---------------------
path = os.getcwd()                 # Getting current diretory
root_TemporaryData = path + '\\temporary_measurements\\' # Temporal file directory
root_Data  = path + '\\measurements\\'  # Data file directory
flag = 1                           # Flag for file saving
SavingPeriod = 30                   # Saving period (in minutes)
header = True                      # Name of columns actived

# Data variables
#---------------
temp = 0                           # Reference inicial time
MeasureTime = 2                    # Measurement time period ('period' defined in arduino)
timeHMS_var = []                   # Time in H-M-S array
t_var  = np.array([])              # Time periods array
y0_var = np.array([])              # Voltage array of sensor #1
y1_var = np.array([])              # Voltage array of sensor #2 
y2_var = np.array([])              # Voltage array of sensor #3

# Data recording
# ---------------
while True:
   
     
    while (arduinoData.inWaiting()==0): #  number of bytes in the input buffer
        #print('arduinoData.inWaiting()',arduinoData.inWaiting())   
        #print('kkkk')
        #print('\r', 'isOpen=',arduinoData.isOpen(), 'Heard=',arduinoData.inWaiting(), end='')
        if auxiliarWaiting == 0:
            print('\r', 'Wait ',end='')
            auxiliarWaiting = 1
        #pass        

    auxiliarWaiting = 0

    # Data reading
    ser_bytes = arduinoData.readline()          # read a byte string
    #print('ser_bytes')
    
    # Inicial capture time
    if flag == 1:
        date_inicial = dt.datetime.now()
        flag = 0
    
    # Data read as list
    str_decoded_bytes = ser_bytes.decode()      # decode byte string into Unicode  
    string = str_decoded_bytes.rstrip()         # remove \n and \r
    string = string.split(sep="\t")             # to list
    measurement = [float(i) for i in string]    # from string to float
       
    #print('measurement')
    
    # Capture time of curret measurement
    date = dt.datetime.now()
    timeHMS = date.strftime("%H:%M:%S")
    
    # Relative time
    delta = relativedelta(date,date_inicial)
    # print(delta.minutes)
    
    # Print current measurement in console
    print('\r Heard ',timeHMS,measurement,'                                                              ', end='')
    #time.sleep(2)
        
    # ------------ saving in termporal file-------------------
    with open(root_TemporaryData+"temporal.csv","a") as f:
        writer = csv.writer(f,delimiter=",",lineterminator='\r')
        if header:
            writer.writerow(['Time','Volume1','Volume2','Volume3'])
            header = False 
            writer.writerow([date,measurement[0],measurement[1],measurement[2]])
        else:
            writer.writerow([date,measurement[0],measurement[1],measurement[2]])
    
    # Append measurements (within 'SavingPeriod' minutes)
    timeHMS_var.append(timeHMS)
    t_var = np.append(t_var,timeHMS)
    y0_var = np.append(y0_var,measurement[0])
    y1_var = np.append(y1_var,measurement[1])
    y2_var = np.append(y2_var,measurement[2])
    
    # -----------  saving in memeasurements file ----------
    # Saves the collected data only every 'SavingPeriod' minutes
    if delta.minutes >= SavingPeriod:
        print('\r Heard  Saving data file...                                                                     ', end='')
        #time.sleep(2)
    
        # Save data
        today = date_inicial.strftime('%Y%m%d%H%M')
        df = pd.DataFrame(columns=['Time','Volume1','Volume2','Volume3'])
        df['Time'] = timeHMS_var
        df['Volume1'] = y0_var
        df['Volume2'] = y1_var
        df['Volume3'] = y2_var
        df.to_csv(root_Data + today + '.csv')


        # Variables reset
        timeHMS_var = []
        t_var  = np.array([]) 
        y0_var = np.array([])
        y1_var = np.array([])
        y2_var = np.array([])
        temp = 0
        flag = 1
        
        arduinoData.flushInput() # Clean buffer
        
        os.remove(root_TemporaryData+"temporal.csv")
        header = True
     

        
           



    
   





    


