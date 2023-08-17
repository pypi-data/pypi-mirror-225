import os
import sys
import platform
import ctypes
import subprocess
import random
import shutil
from PIL import ImageGrab

def pause():
    input("Press Enter to continue...")

def screenshot(filename='screenshot.png'):
    if platform.system() == 'Windows':
        img = ImageGrab.grab()
        img.save(filename)
    else:
        print("Screenshot feature is only supported on Windows.")

def random_number():
    return random.randint(0, 1000000)

def send_file(file_name, new_location):
    try:
        shutil.move(file_name, new_location)
        print(f"File '{file_name}' sent to '{new_location}' successfully.")
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_operating_system():
    return platform.system()

def source_code():
    return "https://github.com/BL1Z33/a4"

def package():
    return "https://pypi.org/project/a4"