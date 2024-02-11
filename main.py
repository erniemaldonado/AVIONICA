import tkinter as tk
from tkinter.ttk import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import threading
from PIL import Image, ImageTk
from tkdial import Meter
from tkinter.messagebox import showinfo
import subprocess
import serial
import time
import datetime
import geopandas as gpd
#receiving "rotX","rotY","rotZ","Temp"
Sensordata={}
rotationsx=[]
rotationsy=[]
rotationsz=[]
times=[]
temps=[]
altitudes=[]
longitudes=[]
latitudes=[]

sensor_data={ #Please enter all sensors that youll be receiving here
     "Time": ["Time"],
      "LAT":["Latitudes"],
      "LONG":["Longitudes"],
      "ALT":["Altitudes"],
      "Temp":["Temperature"],
      "RotX":["Calibrating..."],
      "RotY":["Calibrating..."],
      "RotZ":["Calibrating..."]
}
def read_serial_data():#Read data from the serial port continiously
    global startminute
    port="COM10" #Change to required port
    try:
        ser = serial.Serial(port, baudrate=9600)  
        ser.flushInput()
        time.sleep(1)
        GO=True
        while True:
            # Read data from the serial port
                try:
                    ser.flushInput()
                    cc=(ser.readline().decode().strip()) 
                except UnicodeDecodeError:
                    print("waiting...")
                    time.sleep(0.1)
                    cc=(ser.readline().decode().strip()) 
                    
                if cc[0:4]=="RotX": #waits till data is send properly to store it, substitute for expected first value if necessary
                    if GO:
                        print("Go!")
                        GO=False
                    pairs = cc.split(",") #Split the string into pairs using a comma as the delimiter
                    #print(pairs)
                    #Iterate through the pairs and add them to the dictionary
                    rainau=datetime.datetime.now()
                    times.append(rainau)
                    Sensordata["Time"].append(times)
                    for i in range(0, len(pairs), 2):
                        property_name = pairs[i]
                    property_value = pairs[i + 1]
                    if property_name in sensor_data: 
                            sensor_data[property_name].append(property_value)

                    current_datetime = datetime.datetime.now().minute
                    if current_datetime>(startminute+1)%60: #Every 5 minutes save data to the csv 
                        startminute=current_datetime
                        savingdata()
    except:
             print("Serial port " + port + " not open or currently occupied, please check and run the code again.")  

     
#FUNCTIONS
def savingdata():
    global firsttime
    csv_file = 'cuuheteria.csv'
    df=gpd.GeoDataFrame(sensor_data)
    df.to_csv(csv_file, mode='a', index=False, header=False)
    print(f"Database '{csv_file}' updated successfully.")
    for key in sensor_data:
       sensor_data[key]=[]
    showinfo(message="Data has been saved!")

def battery_level_label():
    return f"Battery is currently at: {pbbat['value']}%"
def GPS(): # function to open a new window for GPS data    
    try:
        script_path = 'gpsintkinker.py'
        subprocess.run(['python', script_path])
    except Exception as e:
        print(f"Error executing script: {str(e)}")

root = tk.Tk()
root.title("AVIONICA")
#IN CASE OF MULTISCREEN MONITOR, UNCOMMENT IN CASE YOU WANT TO OPEN TKINTER IN OTHER SCREEN
# screen_width = root.winfo_screenwidth()-800
# screen_height = root.winfo_screenheight()-500
# x_offset = screen_width+1000
# y_offset = 10
# root.geometry(f"{screen_width}x{screen_height}+{x_offset}+{y_offset}")

root.geometry("1400x900")
frames={}

#Defining which Topic will be in which location of the grid. TOPIC: LOCATION
quadrant_names = {     
 "Temperature": [0,0],
 "Mission state": [0,1],
 "Nose Cone Separation state":[0,2],
 "Battery":[0,3],
 "Save Data":[0,4],
 "Vertical velocity":[1,0],
 "Velocity":[1,1],
 "Humidity":[1,2],
 "Acceleration":[2,0],
 "Altitude":[2,2]
}

# Configure rows and columns for resizing
for r in range(4):
    root.rowconfigure(r, weight=1 if r!=4 else 0)
for c in range(5):
    root.columnconfigure(c, weight=1)

act_height=40
colors=["brown4","black","gray82"]

# Create and label the frames
for r in range(3):
    for c in range(5):
        if r<=2:
            key = [k for k, v in quadrant_names.items() if v == [r,c]]
            if key:
             key = [k for k, v in quadrant_names.items() if v == [r,c]][0]
            else:
             key="test"
        else:
            key="test"
    
        frame = tk.Frame(root, borderwidth=2, relief="ridge",background=colors[r%3])
        frame.grid(row=r, column=c,sticky="nsew")
        frames[key]=frame
        if not(key=="Save Data" or key=="GPS" or key=="Altitude"):
            labele = tk.Label(frame, text=key)
            labele.pack()

        labele.pack()
        label_behind = tk.Label(frame,background=colors[r%3],height=1)
        label_behind.place(anchor="center")
        label_behind.pack()
        if key=="Save Data":
            btn = tk.Button(frame,text =key, height=3,width=7,command=savingdata)
            btn.pack()
            weight = tk.Label(frame,height=1,background=colors[r%3])
            weight.pack()
            btn = tk.Button(frame,text ="GPS", height=3,width=7, command=GPS)
            btn.pack()
            tk.Label(frame,background=colors[r%3],height=3).pack()
        elif key=="Temperature":
                    meter2 = Meter(frame, radius=130, start=-100, end=200, border_width=3,
                    fg="black", text_color="white", start_angle=210, end_angle=-240,
                    text_font="DS-Digital 20", scale_color="black", axis_color="white",
                    needle_color="white")
                    meter2.set_mark(0, 100, "#5052d0")
                    meter2.set_mark(101,200, "#92d050")
                    meter2.set_mark(201,300, "red")
                    meter2.set(10) # set value
                    meter2.pack()


#Altitude section
for widget in frames["Altitude"].winfo_children():
             widget.destroy()

tk.Frame(frames["Altitude"], borderwidth=2, relief="ridge",background="gray82")
# Create a subplot within the figure
figalt = Figure(figsize=(5,5), dpi=80)
figalt.patch.set_facecolor('lightgray')
canvas = FigureCanvasTkAgg(figalt, master=frames["Altitude"])
canvas.get_tk_widget().pack()
axalt = figalt.add_subplot(111)

def altitude_frame(i,dataList,Sensordata):
    axalt.set_title("Altitude (meters)")                        # Set title of figure
    axalt.set_xlabel("Last 50 seconds") 
    axalt.set_ylabel("meters")  
    if len(Sensordata) :
        #print(Sensordata)
        #rotationsx.append(float(Sensordata["RotX"])) # Add to the list holding the fixed number of points to animate    
        altitude = Sensordata["ALT"][-50:] #make sure data is always the most recent 50 values 
        #print(dataList)
        axalt.clear()    
        axalt.set_ylim([0, 3500])   # Set Y axis limit of plot
        axalt.set_title("Altitude (meters)")                        # Set title of figure
        axalt.set_xlabel("Last 50 seconds") 
        axalt.set_ylabel("meters")  
                                    # Clear last data frame
        axalt.plot(altitude,"k")               # Plot new data frame
                            # Set title of y axis 

# 3D VIEW section
def axisrotation_frame():
    merged_frame3d = tk.Frame(root, borderwidth=2, relief="ridge")
    merged_frame3d.grid(row=1, column=3, rowspan=2, columnspan=2, sticky="nsew")
    label = tk.Label(merged_frame3d, text="3D View Simulated")
    label.pack()

#Velocity section
def velocity_frame():
    merged_frame_vel = tk.Frame(root, borderwidth=2, relief="ridge",background="gray82")
    merged_frame_vel.grid(row=1, column=0, rowspan=1, columnspan=2, sticky="nsew")
    figvelocity = Figure(figsize=(6,7), dpi=80)
    figvelocity.patch.set_facecolor('lightgray')
    canvas = FigureCanvasTkAgg(figvelocity, master=merged_frame_vel)
    canvas.get_tk_widget().pack()

    # Create a subplot within the figure
    ax = figvelocity.add_subplot(111)
    # Data for the graph (example data)
    vx = [1, 20, 30, 45, 21]
    vy = [-6, 10, 11, 13, 19]
    vz = [50, 37, 29, 14, 6]
    x = [1, 2, 3, 4, 5]

    # Plot the data

    ax.plot(x,vx,"r", label="X")
    ax.plot(x,vy,"b", label="Y")
    ax.plot(x,vz,"k", label="Z")
    ax.set_xlabel("Last 50 seconds")
    ax.set_ylabel("Velocity")
    ax.set_title("Velocity (m/s)")
    # Add a legend
    ax.legend()

#Acceleration section
merged_frame_acc = tk.Frame(root, borderwidth=2, relief="ridge",background="gray82")
merged_frame_acc.grid(row=2, column=0, rowspan=1, columnspan=2, sticky="nsew")
# Create a subplot within the figure
figacc = Figure(figsize=(6,7), dpi=80)
figacc.patch.set_facecolor('lightgray')
canvas = FigureCanvasTkAgg(figacc, master=merged_frame_acc)
canvas.get_tk_widget().pack()
axacc = figacc.add_subplot(111)
def acceleration_frame(i,dataList,Sensordata):
        # Using the data from Sensor_data to update the plot
    axacc.set_title("Arduino Data (rad/s)")                        # Set title of figure
    axacc.set_xlabel("Last 50 seconds") 
    axacc.set_ylabel("Rad/s")      
    if len(Sensordata) :
        #print(Sensordata)
        #rotationsx.append(float(Sensordata["RotX"])) # Add to the list holding the fixed number of points to animate    
        dataListx = Sensordata["RotX"][-50:] #make sure data is always the most recent 50 values 
        dataListy = Sensordata["RotY"][-50:]#make sure data is always the most recent 50 values 
        dataListz = Sensordata["RotZ"][-50:] #make sure data is always the most recent 50 values 
        #print(dataList)
        axacc.clear()                                          # Clear last data frame
        axacc.plot(dataListx,"r",label="X")               # Plot new data frame
        axacc.plot(dataListy,"b",label="y")               # Plot new data frame
        axacc.plot(dataListz,"k",label="z")               # Plot new data frame
        axacc.set_ylim([-366, 366])                              # Set Y axis limit of plot
        axacc.set_title("Arduino Data (rad/s)")                        # Set title of figure
        axacc.set_xlabel("Last 50 seconds") 
        axacc.set_ylabel("Rad/s")                              # Set title of y axis 
        axacc.legend()
        #print(Sensordata["Temp"])
        meter2.set(Sensordata["Temp"][-1])
    

def battery_frame():
    global pbbat
    pbbat = tk.ttk.Progressbar(
        frames["Battery"],
        orient='horizontal',
        mode='determinate',
        length=120
    )
    pbbat.pack()
    tk.Label(frames["Battery"],height=1,background=colors[0]).pack()
    value_label = tk.Label(frames["Battery"], text=battery_level_label(),background=colors[0])
    value_label.pack()

def humidity_frame():
    frame=frames["Humidity"]
    tk.Label(frame,height=2,background="black").pack()
    meter2 = Meter(frame, radius=130, start=0, end=100, border_width=3,
    fg="black", text_color="white", start_angle=210, end_angle=-240,
    text_font="DS-Digital 20", scale_color="black", axis_color="white",
    needle_color="white",text="%")
    meter2.set_mark(0, 20, "#d6862b")
    meter2.set_mark(21,50, "#d97648")
    meter2.set_mark(51,75, "#92d050")
    meter2.set_mark(76,100, "#175b96")
    meter2.set(10) # set value
    meter2.pack()

#altitude_frame()
humidity_frame()
battery_frame()
axisrotation_frame()
velocity_frame()
#acceleration_frame()
logo_quadrant = tk.Frame(root) #, relief="solid"
logo_quadrant.grid(row=3, column=0, rowspan=1, columnspan=5,sticky="news")

root.rowconfigure(0,weight=1,minsize=200)
root.rowconfigure(3,weight=0,minsize=60)
class Logo(tk.Frame):
    def __init__(self, master, *pargs):
        tk.Frame.__init__(self, master, *pargs) #,background="red"
        self.image =  Image.open("d:\\Alex\\Documentos\\TEC\\7mo semestre TEC\\botrregos\\avionica\\AVIONICA\\images\\logo.png") # Load your image
        self.img_copy= self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = tk.Label(self, image=self.background_image,background="black",height=15)
        self.background.pack(fill=tk.BOTH,expand=tk.YES)
        self.background.bind('<Configure>', self._resize_image)
    def _resize_image(self,event):
        global act_height
        new_height = event.height
        act_height=new_height
        if new_height>85:
            new_height=new_height # 85
            tk.Frame(logo_quadrant,height=15)
        #print(new_height)
        self.image = self.img_copy.resize((new_height,new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image =  self.background_image)

e = Logo(logo_quadrant)
e.pack(fill=tk.BOTH, expand=tk.YES)



serial_thread = threading.Thread(target=read_serial_data)
serial_thread.daemon = True
serial_thread.start()
dataList=[]
#Each moving object inside the code requieres its own animation
ani_rotx = FuncAnimation(figacc, acceleration_frame, fargs=(dataList,Sensordata), interval=1000, frames=10)
ani_altitude=FuncAnimation(figalt, altitude_frame, fargs=(dataList,Sensordata), interval=1000, frames=10)
#ani_roty = F

root.mainloop()