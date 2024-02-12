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

# Load the image asynchronously
def download_image():
    photo = Image.open(io.BytesIO(urllib.request.urlopen('https://raw.githubusercontent.com/MaxG7855/ee/main/MSMP-Large.png').read()))
    return ImageTk.PhotoImage(photo)

image = download_image()

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
def import_minecraft_instance(instance_name):
    prism_launcher_path = file_path

    if not os.path.exists(prism_launcher_path):
        print("Error: PrismLauncher executable not found.")
        return

    os.system(prism_launcher_path + f" --import {instance_name}")
    print(f"Successfully imported Minecraft instance '{instance_name}' from PrismLauncher.")

# Import button click event handler
def import_btn():
    if os.path.exists(path + 'instances\\MSMP'):
        shutil.rmtree(path + 'instances\\MSMP')
    threading.Thread(target=import_minecraft_instance, args=(accounts_dropdown.get(),)).start()

# Launch button click event handler
def launch():
    account = accounts_dropdown.get()
    if account != "Select Account":
        threading.Thread(target=lambda: os.system(file_path + f" --launch MSMP -a {account}")).start()
    else:
        threading.Thread(target=lambda: os.system(file_path + f" --launch MSMP")).start()

# Populate accounts dropdown with account names
def populate_accounts_dropdown():
    global accounts_menu  # Define accounts_menu as global variable
    # Path to the accounts.json file
    accounts_json_path = os.path.expanduser("~\\AppData\\Roaming\\PrismLauncher\\accounts.json")

    # Check if Prism Launcher is installed in the default directory
    if not os.path.exists(accounts_json_path):
        # If Prism Launcher is not in the default directory, assume it's in the same directory as prismlauncher.exe
        accounts_json_path = os.path.join(os.path.dirname(file_path), "accounts.json")

    # Read the contents of the accounts.json file
    with open(accounts_json_path, 'r') as f:
        data = json.load(f)

    if "accounts" in data:
        accounts_data = data["accounts"]
        # Extract account names from the JSON data
        account_names = [account_data.get("profile", {}).get("name", "Unnamed") for account_data in accounts_data]

        # Clear any existing options in the dropdown menu
        accounts_menu = customtkinter.CTkComboBox(master=window, variable=accounts_dropdown, values=account_names, state="readonly")
        accounts_menu.grid(row=0, column=0, columnspan=3, sticky='nw')  # Place the accounts menu in the top-left corner and span all columns

    else:
        print("Error: 'accounts' key not found in accounts.json file.")

# Create a StringVar to control the dropdown menu
accounts_dropdown = tk.StringVar(value="Select Account")

# Create buttons
button1 = customtkinter.CTkButton(window, text="Import / Update Instance", command=import_btn, fg_color="green")
button1.grid(row=2, column=0, sticky='nsew')  # Adjust column span to center the button

button2 = customtkinter.CTkButton(window, text="Launch Instance", command=launch, fg_color="green")
button2.grid(row=2, column=2, sticky='nsew')  # Adjust column span to center the button

# Create and display the image label
image_label = customtkinter.CTkLabel(window, text=" ", image=image)
image_label.grid(row=1, column=0, columnspan=3, sticky='nsew')  # Adjust column span to center the image label

# Initialize accounts_menu as None
accounts_menu = None

# Populate the dropdown with account names
populate_accounts_dropdown()

# Run the application
window.mainloop()
