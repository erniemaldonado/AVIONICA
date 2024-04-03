import tkinter as tk
from tkdial import Dial
from tkdial import Meter
app = tk.Tk()

# some color combinations
color_combinations = [("yellow", "red"), ("white", "cyan"), ("red", "pink"), ("black", "green"),
                    ("white", "black"), ("blue", "blue"), ("green", "green"), ("white", "pink"),
                    ("red", "black"), ("green", "cyan"), ("cyan","black"), ("pink", "blue")]

# for i in range (12):
#     dial = Dial(master=app, color_gradient=color_combinations[i],
#                 unit_length=10, radius=40, needle_color=color_combinations[i][1])
#     dial.set(23)
#     if i<6:
#         dial.grid(row=1, padx=10, pady=10, column=i)
#     else:
#         dial.grid(row=2, padx=10, pady=10, column=11-i)

state=0
moving=[-50,10,20,30,40,50,100]
def update_dial() :
        for widget in app.winfo_children():
             widget.destroy()
        global state
        meter2 = Meter(app, radius=260, start=-100, end=200, border_width=5,
                    fg="black", text_color="white", start_angle=210, end_angle=-240,
                    text_font="DS-Digital 30", scale_color="black", axis_color="white",
                    needle_color="white")
        meter2.set_mark(0, 100, "#5052d0")
        meter2.set_mark(101,200, "#92d050")
        meter2.set_mark(201,300, "red")
        meter2.set(moving[state]) # set value
        meter2.pack()

        state +=1
        app.after(1000,update_dial)

update_dial()
app.mainloop()
