
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
     FigureCanvasTkAgg)
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
import subprocess
import os
import csv


current_path = "d:\\Alex\\Documentos\\TEC\\7mo semestre TEC\\botrregos\\avionica\\AVIONICA"
print(current_path)

# Create a 5x4 grid of frames
root = tk.Tk()
root.title("INTERFAZ CEITECH")
root.geometry("1000x800")  # Adjust the size as needed
quadrants = [[tk.Frame(root, borderwidth=2) for _ in range(5)] for _ in range(3)]


def savedata(): # function to open a new window for GPS data    
    with open('data.csv', 'w', newline='') as csvfile:
        fieldnames = ['altitude', 'latitude', 'longitude', 'timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # Write the header row if the file is newly created
        writer.writeheader()
        # Assuming you have lists of data for each column
        altitudes = [100, 200, 300, 400]
        latitudes = [40.0, 40.1, 40.2, 40.3]
        longitudes = [-75.0, -75.1, -75.2, -75.3]
        timestamps = ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04']
        # Loop through the data and write each row to the CSV file
        for i in range(len(altitudes)):
            row = {
                'altitude': altitudes[i],
                'latitude': latitudes[i],
                'longitude': longitudes[i],
                'timestamp': timestamps[i]
            }
            writer.writerow(row)

def create_circle(canvas, x, y, radius, color):
    return canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)

# Create a 4x1 frame for the right two quadrants
combined_quadrant = tk.Frame(root, borderwidth=2)
logo_quadrant = tk.Frame(root, borderwidth=3) #, relief="solid"
mission_quadrant= tk.Frame(root)#background="white"

# Place the 3x5 quadrants
for i in range(3):
    for j in range(5):
        quadrants[i][j].grid(row=i, column=j, padx=5, pady=5, sticky="nsew")

# Place the combined quadrant
combined_quadrant.grid(row=1, column=3, rowspan=3, columnspan=2, padx=5, pady=5, sticky="nsew")
logo_quadrant.grid(row=3, column=0, rowspan=5, columnspan=5, padx=5, pady=1, sticky="nsew")

mission_quadrant.grid(row=0, column=1, rowspan=1, columnspan=1, padx=1, pady=1, sticky="nsew")
tk.Label(mission_quadrant,text="Mission state",font=("Helvetica", 12))
circlecanvas=tk.Canvas(mission_quadrant,bg="blue")
circlecanvas.grid(row=0, column=0, sticky="nsew") 
circle = create_circle(circlecanvas, 200, 26, 10, "green")
circlecanvas.pack()
# Configure grid rows and columns to expand with the window
for i in range(3):
    root.grid_rowconfigure(i, weight=2)
for j in range(5):
        root.grid_columnconfigure(j, weight=2)

title_label = tk.Label(combined_quadrant, text="3D View Simulated", font=("Helvetica", 20))
title_label.pack(pady=10)
tk.Label(quadrants[0][0], text="Temperature", font=("Helvetica", 12)).pack()
tk.Label(quadrants[0][1], text="Mission state",font=("Helvetica", 12)).pack()
# circleCanvas=tk.Canvas(quadrants[0][1])
# circleCanvas.pack()

tk.Label(quadrants[0][2], text="Nose cone separation state", font=("Helvetica", 10), background="green").pack()
tk.Label(quadrants[0][3], text="Battery", font=("Helvetica", 12)).pack()
tk.Label(quadrants[1][0], text="Vertical velocity", font=("Helvetica", 12)).pack()
tk.Label(quadrants[1][1], text="Velocity", font=("Helvetica", 12)).pack()
tk.Label(quadrants[1][2], text="Humidity", font=("Helvetica", 12)).pack()
tk.Label(quadrants[2][0], text="Acceleration", font=("Helvetica", 12)).pack()
tk.Label(quadrants[2][1], text="Altitude", font=("Helvetica", 12)).pack()
#tk.Label(quadrants[2][2], text="DATA", font=("Helvetica", 12)).pack()

store_quadrant=quadrants[0][4]
ojo = tk.Button(store_quadrant,text ="Save data", height=3,width=7,command=savedata)
ojo.pack()

#GPS AND STORE DATA
button_quadrant = quadrants[2][2]
canvas = tk.Canvas(button_quadrant, height=60)
canvas.pack()
btn_gps = tk.Button(button_quadrant,text ="GPS", height=3,width=7)
btn_gps.pack()
canvas = tk.Canvas(button_quadrant, height=40, width=2)
canvas.pack()



#storebutton = tk.Button(button_quadrant, text="Store Data", width=10, height=3)
#storebutton.grid(row=1)  # Centering and adding padding

#Image in the bottom right corner
label = tk.Label(logo_quadrant)
label.pack(pady = 1 , side=tk.BOTTOM)
image = Image.open(os.path.join(current_path,"images", "logo.png")) # Load your image
image = image.resize((70, 70))
image=ImageTk.PhotoImage(image)
image_label = tk.Label(label, image=image) # Create a Label widget with the resized image
image_label.photo = image # Keep a reference to the PhotoImage to prevent it from being garbage collected
image_label.pack(side= tk.BOTTOM) # Position the image label in the window

root.mainloop()