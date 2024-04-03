import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# Create a tkinter window
root = tk.Tk()
root.title("Multiple FuncAnimations")

# Create two tkinter frames to hold the Matplotlib figures
frame1 = tk.Frame(root)
frame1.pack(side=tk.LEFT, padx=10)
frame2 = tk.Frame(root)
frame2.pack(side=tk.LEFT, padx=10)

# Create two Matplotlib figures and axes
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()

# Create some initial data
x = np.linspace(0, 2 * np.pi, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Create FuncAnimation for the first figure
def animate1(i):
    #ax1.clear()
    ax1.plot(x, y1 + 0.1 * np.sin(2 * np.pi * 0.1 * i))

ani1 = FuncAnimation(fig1, animate1, frames=1000, repeat=False)

# Create FuncAnimation for the second figure
def animate2(i):
    ax2.clear()
    ax2.plot(x, y2 + 0.1 * np.cos(2 * np.pi * 0.1 * i))

ani2 = FuncAnimation(fig2, animate2, frames=1000, repeat=False)

# Create FigureCanvasTkAgg objects to embed the figures in tkinter frames
canvas1 = FigureCanvasTkAgg(fig1, master=frame1)
canvas1.get_tk_widget().pack()
canvas2 = FigureCanvasTkAgg(fig2, master=frame2)
canvas2.get_tk_widget().pack()

root.mainloop()


