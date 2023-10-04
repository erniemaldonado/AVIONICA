# %%
from tkinterhtml import HtmlFrame
import tkinter as tk
import urllib.request

root = tk.Tk()
frame = HtmlFrame(root, horizontal_scrollbar="auto")


frame.set_content(urllib.request.urlopen("https://duckduckgo.com").read().decode())
root.mainloop()
# %%
