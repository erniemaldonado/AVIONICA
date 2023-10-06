# %%
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import serial
import threading
import time
# Global data structure to store serial data
serial_data = []

# Function to read data from the serial port in a loop
def read_serial_data():
    ser = serial.Serial('COM10', baudrate=38400)  # Replace 'COM10' with your serial port
    while True:
        # Read data from the serial port
            cc=(ser.readline().decode().strip()) 
            time.sleep(.5)  
            input_string = cc 
            pairs = input_string.split(",") #Split the string into pairs using a comma as the delimiter
            #print(pairs)

            #Iterate through the pairs and add them to the dictionary
            for i in range(0, len(pairs), 2):
                property_name = pairs[i]
                property_value = pairs[i + 1]
                Sensordata[property_name] = property_value
            #print(Sensordata)
            
# Function to update the plot using data from the global data structure
def update_animation(i,dataList,Sensordata):
    # Use the data from serial_data to update the plot
    # Replace this with your data processing and plotting logic
    # For example, you can plot the last N data points.
    if len(Sensordata) :
        print(Sensordata)
        dataList.append(float(Sensordata["LAT"])) # Add to the list holding the fixed number of points to animate    
        dataList = dataList[-50:] #make sure data is always the most recent 50 values 
        print(dataList)
        ax.clear()                                          # Clear last data frame
        ax.plot(dataList)                                # Plot new data frame
        ax.set_ylim([0, 100])                              # Set Y axis limit of plot
        ax.set_title("Arduino Data")                        # Set title of figure
        ax.set_ylabel("LAT")                              # Set title of y axis 

fig = plt.figure()   # Create Matplotlib plots fig is the 'higher level' plot window
ax = fig.add_subplot(111)  # Add subplot to main fig window

dataList = []  
# Start reading data from the serial port in the background
global Sensordata
Sensordata = {} 
serial_thread = threading.Thread(target=read_serial_data)
serial_thread.daemon = True
serial_thread.start()


# Create FuncAnimation to update the plot
ani = FuncAnimation(fig, update_animation, fargs=(dataList,Sensordata), interval=1000)

plt.show()
# %%
