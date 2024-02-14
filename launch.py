import subprocess
import os
import customtkinter
import tkinter as tk
from PIL import Image, ImageTk
import json
import shutil
import urllib.request
import io
import threading

# Initialize the main window
window = customtkinter.CTk()
window.title("MSMP")
window.geometry("399x274")
window.resizable(0, 0)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_rowconfigure(2, weight=1)
window.grid_rowconfigure(3, weight=1)

# Define the image variable
image = None

# Load the image asynchronously
def download_image(url):
    photo = Image.open(io.BytesIO(urllib.request.urlopen(url).read()))
    return ImageTk.PhotoImage(photo)

# URL of the image
image_url = 'https://raw.githubusercontent.com/MaxG7855/ee/main/MSMP-Large.png'

# Assign the image variable
image = download_image(image_url)

# Find the file path of prismlauncher.exe
def find_file_in_all_drives(filename):
    drives = [chr(x) + ":\\" for x in range(65, 91)]
    for drive in drives:
        if os.path.exists(drive):
            for root, dirs, files in os.walk(drive):
                if filename in files:
                    return os.path.join(root, filename)
    return None

filename = "prismlauncher.exe"
file_path = find_file_in_all_drives(filename)
path = file_path.replace(filename, '', 1)

if file_path:
    print(f"File '{filename}' found at: {file_path}")
else:
    print(f"File '{filename}' not found in any drive.")
    exit()

# Import Minecraft instance function
def import_minecraft_instance():
    prism_launcher_path = file_path

    if not os.path.exists(prism_launcher_path):
        print("Error: PrismLauncher executable not found.")
        return

    os.system(prism_launcher_path + f" --import http://maxwellg.pro/MSMP.zip")
    print("Successfully imported Minecraft instance from PrismLauncher.")

# Import button click event handler
def import_btn():
    if os.path.exists(path + 'instances\\MSMP'):
        shutil.rmtree(path + 'instances\\MSMP')
    threading.Thread(target=import_minecraft_instance).start()

# Launch button click event handler
def launch():
    account = accounts_dropdown.get()
    if account != "Select Account":
        threading.Thread(target=lambda: os.system(file_path + f" --launch MSMP -a {account}")).start()
    else:
        threading.Thread(target=lambda: os.system(file_path + f" --launch MSMP")).start()

# Create buttons
button1 = customtkinter.CTkButton(window, text="Import / Update Instance", command=import_btn, fg_color="green")
button1.grid(row=2, column=0, sticky='nsew')  # Adjust column span to center the button

button2 = customtkinter.CTkButton(window, text="Launch Instance", command=launch, fg_color="green")
button2.grid(row=2, column=2, sticky='nsew')  # Adjust column span to center the button

# Create and display the image label
image_label = customtkinter.CTkLabel(window, text=" ", image=image)
image_label.grid(row=1, column=0, columnspan=3, sticky='nsew')  # Adjust column span to center the image label

# Run the application
window.mainloop()
