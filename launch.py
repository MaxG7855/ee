import subprocess
import os
import customtkinter
import tkinter as tk
from PIL import Image, ImageTk
import json
import io
import urllib.request


window = tk.Tk()  # Create the main window
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

    os.system(prism_launcher_path + " --import " + instance_name)
    print(f"Successfully imported Minecraft instance '{instance_name}' from PrismLauncher.")

def import_btn():
    if os.path.exists(path + 'instances\\MSMP'):
        shutil.rmtree(path + 'instances\\MSMP')
        import_minecraft_instance(instance_name)
    else:
        import_minecraft_instance(instance_name)

def launch():
    os.system(file_path + " --launch " + "MSMP")

def populate_accounts_dropdown():
    try:
        # Path to the accounts.json file
        accounts_json_path = os.path.expanduser("~\\AppData\\PrismLauncher\\accounts.json")

        # Check if Prism Launcher is installed in the default directory
        if not os.path.exists(accounts_json_path):
            # If Prism Launcher is not in the default directory, assume it's in the same directory as prismlauncher.exe
            accounts_json_path = os.path.join(os.path.dirname(file_path), "accounts.json")

        # Read the contents of the accounts.json file
        with open(accounts_json_path, 'r') as f:
            accounts_data = json.load(f)

        # Extract account names from the JSON data
        account_names = [account["name"] for account in accounts_data]

        # Clear any existing options in the dropdown menu
        accounts_menu["menu"].delete(0, "end")

        # Add retrieved account names to the dropdown menu
        for account_name in account_names:
            accounts_menu["menu"].add_command(label=account_name, command=tk._setit(accounts_dropdown, account_name))
    except FileNotFoundError:
        print("Error: accounts.json file not found.")
    except json.JSONDecodeError:
        print("Error: Unable to decode accounts.json file.")

# Create a dropdown list to select the account
accounts_dropdown = tk.StringVar(window)
populate_accounts_dropdown()  # Populate the dropdown with accounts

accounts_menu = tk.OptionMenu(window, accounts_dropdown, *accounts_menu["menu"].commands.keys())
accounts_menu.grid(column=3, row=8)

button1 = customtkinter.CTkButton(window, text="Import / Update Instance", command=import_btn)
button1.grid(column=3, row=10)
button2 = customtkinter.CTkButton(window, text="Launch Instance", command=launch)
button2.grid(column=3, row=11)
image_label = customtkinter.CTkLabel(window, text=" ", image=image)
image_label.grid(column=3, row=9)

window.mainloop()
