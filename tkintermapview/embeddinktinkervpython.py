from tkinterweb import HtmlFrame #import the HTML browser

import tkinter as tk #python3

root = tk.Tk() #create the tkinter window
frame = HtmlFrame(root) #create HTML browser

frame.load_website("http://localhost:36170") #load a website
frame.pack(fill="both", expand=True) #attach the HtmlFrame widget to the parent window
root.mainloop()