import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import messagebox
import threading

from holo import holo_touch
from any import any_touch

# Function to create an icon
def create_image():
    # Generate an image for the icon
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), "black")
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 4, height // 4, width * 3 // 4, height * 3 // 4),
        fill="white")
    return image

# Function to handle the tray menu actions
def on_clicked(icon, item):
    if item == "Option 1":
        with open("stopHolo.txt", "w") as f:
            f.write("stop")
    elif item == "Option 2":
        open("stopHolo.txt", "w").close()
        t1 = threading.Thread(target=holo_touch)
        t1.start()
        # holo_touch()
    elif item == "Option 3":
        any_touch()

# Create the tray icon
icon = pystray.Icon("test_icon")
icon.icon = create_image()
icon.menu = pystray.Menu(
    item("Stop", lambda: on_clicked(icon, "Option 1")),
    item("Start Holo Touch", lambda: on_clicked(icon, "Option 2")),
    item("Start Any Touch", lambda: on_clicked(icon, "Option 3"))
)

# Run the icon
icon.run()
