import os
import sys
import platform
import ctypes
import subprocess
import random
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
