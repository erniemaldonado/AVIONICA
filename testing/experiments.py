import tkinter as tk
from tkdial import Dial

app = tk.Tk()

# some color combinations
color_combinations = [("yellow", "red"), ("white", "cyan"), ("red", "pink"), ("black", "green"),
                    ("white", "black"), ("blue", "blue"), ("green", "green"), ("white", "pink"),
                    ("red", "black"), ("green", "cyan"), ("cyan","black"), ("pink", "blue")]

for i in range (12):
    dial = Dial(master=app, color_gradient=color_combinations[i],
                unit_length=10, radius=40, needle_color=color_combinations[i][1])
    dial.set(23)
    if i<6:
        dial.grid(row=1, padx=10, pady=10, column=i)
    else:
        dial.grid(row=2, padx=10, pady=10, column=11-i)

state=0
moving=[10,20,30,40,50,60]
def update_dial() :
        dial=Dial(master=app)
        dial.grid(row=1,column=2)
        global state
        dial.set(moving[state])
        state +=1
        app.after(1000,update_dial)

update_dial()
app.mainloop()
