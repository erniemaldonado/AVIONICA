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

global value_label

Sensordata={ # Orden en el que el esp32 enviara las variables
      "RotX":[],
      "RotY":[],
      "RotZ":[],
      "ALT":[],
      "TEMP":[],
      "LAT":[],
      "LONG":[],
  
}
def read_serial_data():#Función para obtener los datos enviados por lora del esp
    global startminute
    global list_size
    list_size=30 #Especifique el numero de puntos que mostraran las graficas 
    save_i=0
    port="COM11" #Cambiarlo al puerto requerido
    ser = serial.Serial(port, baudrate=115200)  #Cambiarlo al baudrate requerido
    ser.flushInput()        
    time.sleep(1)
    GO=True
    while True:
            # Leer data del puerto serial
                try:
                    #ser.flushInput()
                    cc=(ser.readline().decode().strip()) 
                except UnicodeDecodeError:
                    print("waiting...")
                    time.sleep(10)
                    cc=(ser.readline().decode().strip()) 
                if cc[0:4]=="+RCV": #Espera a que la info sea enviada de forma apropiada para guardarla
                    if GO:
                        print("Go!")
                        GO=False
                    cc=cc[11:]
                    pairs = cc.split(",") #Separa el string en pares usando una coma para delimitar
                    i=0
                    for variable in Sensordata:
                        if variable != "Time":
                            Sensordata[variable].append(float(pairs[i]))
                            Sensordata[variable]= Sensordata[variable][-10:]
                            i+=1
                    Sensordata["Time"].append(datetime.datetime.now())
                    print(Sensordata)
                    save_i+=1
                    if save_i == list_size: #Cada que cada miembro de la lista sea nuevo se actualizara la base de datos
                         savingdata()
                         save_i=0

#FUNCTIONS
def savingdata():
    global firsttime
    csv_file = 'cuuheteria.csv'
    df=gpd.GeoDataFrame(Sensordata)
    df.to_csv(csv_file, mode='a', index=False, header=False)
    print(f"Base de Datos '{csv_file}' actualizada.")
    for key in Sensordata:
       Sensordata[key]=[]
    showinfo(message="Los datos han sido guardados!")

def battery_level_label():
    return f"Bateria actualmente al: {pbbat['value']}%"

def GPS(): # function to open a new window for GPS data    
    try:
        script_path = 'gpsintkinker.py'
        subprocess.run(['python', script_path])
        time.sleep(1000)

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

#Definir que estará en que sección del grid. TOPIC: LOCATION
quadrant_names = {     
 "Temperatura": [0,0],
 "Estado de la misión": [0,1],
 "Estado de la separación del cono de nariz":[0,2],
 "Bateria":[0,3],
 "Guardar":[0,4],
 "Vertical velocity":[1,0],
 "Velocity":[1,1],
 "Humedad":[1,2],
 "Acceleration":[2,0],
 "Altitude":[2,2]
}

# Configuración de filas y columnas para ajustar tamaños de los cuadrantes
for r in range(4):
    root.rowconfigure(r, weight=1 if r!=4 else 0)
for c in range(5):
    root.columnconfigure(c, weight=1)

act_height=40
colors=["white","white","white"]
Title_font = tk.font.Font( family = "Amasis MT Pro Black",  
                                 size = 15,  
                                 weight = "bold") 
state_font = tk.font.Font( family = "Lucida Console",  
                                 size = 17,  
                                 ) 

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

        #helv36 = tk.tkFont.Font(family="Helvetica",size=36,weight="bold")
        if not(key=="Guardar" or key=="GPS" or key=="Altitude"): #Add title to labels
            labele = tk.Label(frame, text=key,font=Title_font,background="white")
            labele.pack()

        labele.pack()
        label_behind = tk.Label(frame,background=colors[r%3],height=1)
        label_behind.place(anchor="center")
        label_behind.pack()
        if key=="Guardar":
            btn = tk.Button(frame,text =key, height=3,width=7,command=savingdata)
            btn.pack()
            weight = tk.Label(frame,height=1,background=colors[r%3])
            weight.pack()
            btn = tk.Button(frame,text ="GPS", height=3,width=7, command=GPS)
            btn.pack()
            tk.Label(frame,background=colors[r%3],height=3).pack()      
        elif key=="Temperatura":
                    meter2 = Meter(frame, radius=130, start=-100, end=200, border_width=3,
                    fg="black", text_color="white", start_angle=210, end_angle=-240,
                    text_font="DS-Digital 20", scale_color="black", axis_color="white",
                    needle_color="white")
                    meter2.set_mark(0, 100, "#5052d0")
                    meter2.set_mark(101,200, "#92d050")
                    meter2.set_mark(201,300, "red")
                    try:
                        #meter2.set(int(Sensordata["TEMP"])) # set value
                        print(19)
                    except:        
                           meter2.set(20) # set value
                    meter2.pack()



#Altitude section
for widget in frames["Altitude"].winfo_children():
             widget.destroy()
tk.Frame(frames["Altitude"], borderwidth=2, relief="ridge",background="white")
# Crear un subplot dentro de la figure
figalt = Figure(figsize=(5,5), dpi=80)
figalt.patch.set_facecolor('white')
canvas = FigureCanvasTkAgg(figalt, master=frames["Altitude"])
canvas.get_tk_widget().pack()
axalt = figalt.add_subplot(111)

def altitude_frame(i,dataList,Sensordata):
    axalt.set_title("Altitud (metros)")                        # Set title of figure
    axalt.set_xlabel("Ultimos 50 segundos") 
    axalt.set_ylabel("metros")  
    if len( Sensordata["ALT"]) :
        #print(Sensordata)
        altitude = Sensordata["ALT"] #make sure data is always the most recent 50 values 
        #print(dataList)
        axalt.clear()    
        axalt.set_ylim([0, 1500])   # Set Y axis limit of plot
        axalt.set_title("Altitud (metros)")                        # Set title of figure
        axalt.set_xlabel("Ultimos 50 segundos") 
        axalt.set_ylabel("metros")  
                                    # Clear last data frame
        axalt.plot(altitude,"k")    # Plot new data frame
                                     # Set title of y axis 
                                     
# 3D VIEW section
def axisrotation_frame():
    merged_frame3d = tk.Frame(root, borderwidth=2, relief="ridge")
    merged_frame3d.grid(row=1, column=3, rowspan=2, columnspan=2, sticky="nsew")
    label = tk.Label(merged_frame3d, text="TERMINAL",font=Title_font)
    label.pack()

#Velocity section
def velocity_frame():
    merged_frame_vel = tk.Frame(root, borderwidth=2, relief="ridge",background="white")
    merged_frame_vel.grid(row=1, column=0, rowspan=1, columnspan=2, sticky="nsew")
    figvelocity = Figure(figsize=(6,7), dpi=80)
    figvelocity.patch.set_facecolor('white')
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
    ax.set_xlabel("Ultimos 50 segundos")
    ax.set_ylabel("Velocidad")
    ax.set_title("Velocidad (m/s)")
    # Add a legend
    ax.legend()

#Acceleration section
merged_frame_acc = tk.Frame(root, borderwidth=2, relief="ridge",background="white")
merged_frame_acc.grid(row=2, column=0, rowspan=1, columnspan=2, sticky="nsew")
# Create a subplot within the figure
figacc = Figure(figsize=(6,7), dpi=80)
figacc.patch.set_facecolor('white')
canvas = FigureCanvasTkAgg(figacc, master=merged_frame_acc)
canvas.get_tk_widget().pack()
axacc = figacc.add_subplot(111)
global ibat #test
ibat=0  #test

def acceleration_frame(i,dataList,Sensordata):    # Funcion que usa la info de Sensordata para actualizar la grafica
    
    #Actualización de la bateria
    global ibat
    porcentage=[70,10,31,40,80,70] # Substituir por valor actual de la bateria 
    move=porcentage[ibat%(len(porcentage)-1)]-pbbat['value']
    pbbat.step(move)
    ibat += 1
    value_label.config(text=battery_level_label())

    axacc.set_title("Acceleración rotacional del cohete (rad/s)") # Titulo de la figura Acceleración
    axacc.set_xlabel("Ultimos 50 segundos")  #Ajustar por el cada cuanto se adquiere nueva info
    axacc.set_ylabel("Rad/s")  

    if len(Sensordata["RotX"]) :
        dataListx = Sensordata["RotX"] #Mostrara la lista de valores mas recientes de RotX
        dataListy = Sensordata["RotY"] #Mostrara la lista de valores mas recientes de RotY 
        dataListz = Sensordata["RotZ"] #Mostrara la lista de valores mas recientes de RotZ
        axacc.clear()                 #Limpiar la grafica
        axacc.plot(dataListx,"r",label="X") # Ploteamos cada una de las rotaciones
        axacc.plot(dataListy,"b",label="y")             
        axacc.plot(dataListz,"k",label="z")               
        axacc.set_ylim([-50, 50])                  
        axacc.set_title("Arduino Data (rad/s)")                      
        axacc.set_xlabel("Last 50 seconds") 
        axacc.set_ylabel("Rad/s")  
        axacc.legend()

       # meter2.set(float(Sensordata["TEMP"][-1])) #Ajuste de la temperatura
        
def missionstate_frame():
    tk.Label(frames["Estado de la misión"],height=2,background="white").pack() #Espacio libre
    state_label = tk.Label(frames["Estado de la misión"], text="Previo a despegue", fg="PaleGreen2", background="dark slate gray",font=state_font)
    state_label.pack()

def battery_frame():
    global pbbat
    global value_label
    pbbat = tk.ttk.Progressbar(
        frames["Bateria"],
        orient='horizontal',
        mode='determinate',
        length=120
    )
    pbbat.pack()
    tk.Label(frames["Bateria"],height=1,background=colors[0]).pack()
    value_label = tk.Label(frames["Bateria"], text=battery_level_label(),background=colors[0])
    value_label.pack()

def humidity_frame():
    frame=frames["Humedad"]
    tk.Label(frame,height=2,background="white").pack()
    meter2 = Meter(frame, radius=170, start=0, end=100, border_width=3,
    fg="black", text_color="white", start_angle=210, end_angle=-240,
    text_font="DS-Digital 20", scale_color="black", axis_color="white",
    needle_color="white",text="%")
    meter2.set_mark(0, 20, "#d6862b")
    meter2.set_mark(21,50, "#d97648")
    meter2.set_mark(51,75, "#92d050")
    meter2.set_mark(76,100, "#175b96")
    meter2.set(10)  #Valor default de la humedad
    meter2.pack()

def temperatur_frame():
    frame=frames["Temperatura"]
    tk.Label(frame,height=2,background="white").pack()
    meter2 = Meter(frame, radius=170, start=0, end=100, border_width=3,
    fg="black", text_color="white", start_angle=210, end_angle=-240,
    text_font="DS-Digital 20", scale_color="black", axis_color="white",
    needle_color="white",text="%")
    meter2.set_mark(0, 20, "#d6862b")
    meter2.set_mark(21,50, "#d97648")
    meter2.set_mark(51,75, "#92d050")
    meter2.set_mark(76,100, "#175b96")
    meter2.set(10)  #Valor default de la humedad
    meter2.pack()



missionstate_frame()
humidity_frame()
battery_frame()
axisrotation_frame()
velocity_frame()

#acceleration_frame()
#Se definío la posición del frame de aceleración
logo_quadrant = tk.Frame(root) #, relief="solid"
logo_quadrant.grid(row=3, column=0, rowspan=1, columnspan=5,sticky="news")
root.rowconfigure(0,weight=1,minsize=200)
root.rowconfigure(3,weight=0,minsize=60)

#Logo, en la parte de abajo de la interfaz
class Logo(tk.Frame):
    def __init__(self, master, *pargs):
        tk.Frame.__init__(self, master, *pargs) #,background="red"
        self.image =  Image.open("d:\\Alex\\Documentos\\TEC\\7mo semestre TEC\\botrregos\\avionica\\AVIONICA\\images\\logo.png") # Load your image
        self.img_copy= self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = tk.Label(self, image=self.background_image,background="#580F41",height=15)
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
#Cada figura a plotear requiere su animacion, pero para los casos de variables fijas como temp, humedad, estado del cono, esto 
#se puede hacer en una sola, se uso el acceleration_frame para tambien representar estos parametros
ani_rotx = FuncAnimation(figacc, acceleration_frame, fargs=(dataList,Sensordata), interval=400, frames=10)
ani_altitude=FuncAnimation(figalt, altitude_frame, fargs=(dataList,Sensordata), interval=400, frames=10)

root.mainloop()
root.mainloop()