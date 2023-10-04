import os
import tkinter
import tkintermapview
from PIL import Image, ImageTk

# create tkinter window
root_tk = tkinter.Tk()
root_tk.geometry(f"{1000}x{700}")
root_tk.title("GPS")

# create map widget
map_widget = tkintermapview.TkinterMapView(root_tk, width=1000, height=700, corner_radius=0)
map_widget.pack(fill="both", expand=True)

# load images
current_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
plane_image = ImageTk.PhotoImage(Image.open(os.path.join(current_path, "images", "rocketman.png")).resize((60, 120)))



def marker_callback(marker):
    print(marker.text)
    marker.delete()


# create markers
marker_1 = map_widget.set_marker(28.702514,-106.139159, text="Cohete", icon=plane_image, command=marker_callback,)

# root_tk.after(3000, lambda: marker_2.change_icon(plane_image))

# set initial position of map widget
map_widget.set_address("UACH Chihuahua")
map_widget.set_zoom(11)

root_tk.mainloop()
