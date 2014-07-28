import sys
import os



from cx_Freeze import setup, Executable
from PySide.QtCore import *
from PySide.QtGui import *

from PySide.QtUiTools import *
import PySide

"""
utiliser : python setup.py build pour compiler.
"""

base = None
if sys.platform == "win32":
    base = "Win32GUI"

importationCode=[]

dependances = ["doc/","dep/","objects/"]

includefiles = importationCode+dependances

includes = []
excludes = []
packages = ["encodings",
            "OpenGL",
            "OpenGL.arrays"] # or just this one

setup(
    name = "NAO_Simulator",
    version = "0.9",
    description = "Simulateur gratuit de NAO",
    executables = [Executable("NaoSimulator.py", base = base)],
    options = {'build_exe': {'excludes':excludes,"compressed":True,
                             'packages':packages,'include_files':includefiles,
                             "includes":includes}}
     )
