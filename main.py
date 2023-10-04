import tkinter.ttk 
from tkinter import PhotoImage 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
     FigureCanvasTkAgg)
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
import subprocess


def IMU(): # function to open a new window for IMU graph
     
    # Toplevel object which will
    # be treated as a new window
    newWindow = tk.Toplevel(master)
    # Initialize Tkinter and Matplotlib Figure
    fig, ax = plt.subplots()
    
    # Create Canvas
    canvas = FigureCanvasTkAgg(fig, master=newWindow)  
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
    # Plot data on Matplotlib Figure
    t = np.arange(0, 2*np.pi, .01)
    ax.plot(t, np.sin(t))
    canvas.draw()
    
                #newWindow.mainloop()
    # sets the title of the
    # Toplevel widget
    newWindow.title("IMU")
 
    # sets the geometry of toplevel
    newWindow.geometry("600x600")
 
    # A Label widget to show in toplevel
    tk.Label(newWindow, text ="IMU").pack()
 
def GPS(): # function to open a new window for GPS data    
    try:
        script_path = 'gpsintkinker.py'
        subprocess.run(['python', script_path])
    except Exception as e:
        print(f"Error executing script: {str(e)}")
     

master = tk.Tk() # creates a Tk() object
master.title("AVIONICA")
  
# sets the geometry of main
# root window
master.geometry("240x240")
label_top = tk.Label(master, text="AVIONICA")
label_top.pack(side="top", pady=10)


 
#Buttons for sensors  
btn_imu = tk.Button(master, text ="IMU",command = IMU)
btn_imu.pack(pady = 10)

btn_gps = tk.Button(master,text ="GPS",command = GPS)
btn_gps.pack(pady = 10)
 
#Image in the bottom right corner
label = tk.Label(master)
label.pack(pady = 10 , side=tkinter.BOTTOM)
image = Image.open("logo.png") # Load your image
image = image.resize((50, 50))
image=ImageTk.PhotoImage(image)
image_label = tk.Label(label, image=image) # Create a Label widget with the resized image
image_label.photo = image # Keep a reference to the PhotoImage to prevent it from being garbage collected
image_label.pack(side= tkinter.BOTTOM) # Position the image label in the window

tk.mainloop() # mainloop, runs infinitely