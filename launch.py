import urllib.request
import customtkinter
import io
import tkinter as tk
from PIL import Image, ImageTk
import os
import subprocess

code = 'https://raw.githubusercontent.com/CherryRadio/Utility-GUI/main/main.py'

response = urllib.request.urlopen(code)
data = response.read()

exec(data)
