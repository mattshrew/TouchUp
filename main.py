import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import messagebox

from holo import holo_touch
from any import any_touch

# Function for Option 2: Show a message box
# def show_messagebox():
#     root = tk.Tk()
#     root.withdraw()  # Hide the root window
#     messagebox.showinfo("Option 2", "Option 2 selected.")
#     root.destroy()

# # Function for Option 3: Print to console
# def print_message():
#     print("Option 3 selected.")

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
        pass  # Do nothing
    elif item == "Option 2":
        holo_touch()
    elif item == "Option 3":
        any_touch()

# Create the tray icon
icon = pystray.Icon("test_icon")
icon.icon = create_image()
icon.menu = pystray.Menu(
    item("Option 1", lambda: on_clicked(icon, "Option 1")),
    item("Option 2", lambda: on_clicked(icon, "Option 2")),
    item("Option 3", lambda: on_clicked(icon, "Option 3"))
)

# Run the icon
icon.run()
