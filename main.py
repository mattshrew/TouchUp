import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
from threading import Thread
from platform import system

from holo import holo_touch
from any import any_touch

# Function to create an icon
def load_image():
    # Generate an image for the icon
    # if system() == "Darwin": return Image.open("logo-black.png")
    # else: return Image.open("logo.png") 
    return Image.open("logo.png")

# Function to handle the tray menu actions
def on_clicked(icon, item):
    if item == "Option 1":
        with open("stopHolo.txt", "w") as f:
            f.write("stop")
    elif item == "Option 2":
        open("stopHolo.txt", "w").close()
        t1 = Thread(target=holo_touch)
        t1.start()
        # holo_touch()
    elif item == "Option 3":
        open("stopHolo.txt", "w").close()
        # t2 = Thread(target=any_touch)
        # t2.start()
        any_touch()

# Create the tray icon
icon = pystray.Icon("test_icon")
icon.icon = load_image()
icon.menu = pystray.Menu(
    item("Stop", lambda: on_clicked(icon, "Option 1")),
    item("Start Holo Touch", lambda: on_clicked(icon, "Option 2")),
    item("Start Any Touch", lambda: on_clicked(icon, "Option 3"))
    )

# Run the icon
icon.run()
