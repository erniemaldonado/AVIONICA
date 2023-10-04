# %%
import tkinter as tk
import folium
from tkinter import ttk
from tkinter import *
import webbrowser
import os

def display_map():
    
    m = folium.Map(location=[28.702514,-106.139159], zoom_start=14)
    lon,lat=[28.702514,-106.139159] #COORDINATES
    icon_image =  os.path.abspath("D:/Alex/Documentos/TEC/7mo semestre TEC/botrregos/avionica/experimenting/rocketmanbkless.png") 
    icon = folium.CustomIcon(icon_image, icon_size=(38, 95),icon_anchor=(20, 100)) #icon anchor is to center to which point the icon will be relative to even when zooming
    folium.Marker(location=[lon,lat], icon=icon, popup="Aki ando").add_to(m) #Al precionar el cohete que se abra un popup
    m.save("output.html")
    m #desplegar mapa
    # Create a tkinter window
    html_file="output.html"
    webbrowser.open(html_file)

display_map()

# %%
