import subprocess
import os
import customtkinter
import tkinter as tk
from PIL import Image, ImageTk
import urllib.request
import io
import platform
import shutil
import threading  # Import the threading module

if platform.system() == "Windows":
    window = customtkinter.CTk()
    window.title("MSMP")
    window.geometry("280x174")
    window.resizable(0, 0)

    def download_image():
        photo = Image.open(io.BytesIO(urllib.request.urlopen('https://raw.githubusercontent.com/MaxG7855/ee/main/MSMP-Large.png').read()))
        return ImageTk.PhotoImage(photo)

    # Load the image asynchronously
    image = download_image()

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

    def import_minecraft_instance(instance_name):
        prism_launcher_path = file_path

        if not os.path.exists(prism_launcher_path):
            print("Error: PrismLauncher executable not found.")
            return

        try:
            subprocess.run([prism_launcher_path, "--import", instance_name], check=True)
            print(f"Successfully imported Minecraft instance '{instance_name}' from PrismLauncher.")
        except subprocess.CalledProcessError as e:
            print(f"Error: Failed to import Minecraft instance '{instance_name}' from PrismLauncher.")
            print(e)

    instance_name = "http://maxwellg.pro:25599/MSMP.zip"

    def import_btn():
        if os.path.exists(path + 'instances\\MSMP'):
            shutil.rmtree(path + 'instances\\MSMP')
            import_minecraft_instance(instance_name)
        else:
            import_minecraft_instance(instance_name)

    def launch():
        subprocess.run([file_path, "--launch", "MSMP"], check=True)

    button1 = customtkinter.CTkButton(window, text="Import / Update Instance", command=import_btn)
    button1.grid(column=3, row=10)
    button2 = customtkinter.CTkButton(window, text="Launch Instance", command=launch)
    button2.grid(column=3, row=11)
    image_label = customtkinter.CTkLabel(window, text=" ", image=image)
    image_label.grid(column=3, row=9)

    window.mainloop()
