import sys
import os

from cx_Freeze import setup, Executable
import PySide

"""
utiliser : python setup.py build pour compiler.
"""


base = None
if sys.platform == "win32":
    base = "Win32GUI"

importationCode=[]


dependances = ["doc/","dep/","objects/"]

#QWEB
#includefiles = ["rsc_rc.py",(os.path.join(os.path.dirname(PyQt4.uic.__file__),
#"widget-plugins"), "PyQt4.uic.widget-plugins")]+importationCode+dependances
#QWEB!
includefiles = ["rsc_rc.py"]+importationCode+dependances

includes = []#["PyQt4.QtNetwork"]
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
