import sys

from cx_Freeze import setup, Executable
import PyQt4
import os
import PyQt4.uic

"""
utiliser : python setup.py build pour compiler.
"""

base = None
if sys.platform == "win32":
    base = "Win32GUI"

importationCode=[]

dependances = ["doc/","dep/","objects/"]

icone = [r"dep/48.ico"]

#QWEB
includefiles = ["rsc_rc.py",(os.path.join(os.path.dirname(PyQt4.uic.__file__),
"widget-plugins"), "PyQt4.uic.widget-plugins")]+importationCode+dependances
#QWEB!

includes = ["PyQt4.QtNetwork", "atexit", "numpy.core._methods", "numpy.lib.format"]
excludes = []
packages = ["encodings",
            "OpenGL",
            "OpenGL.arrays" # or just this one
            ]

setup(
    name = "NAO_Simulator_2014",
    author = "Adrien Vernotte",
    version = "1.0.0",
    description = "Simulateur gratuit de NAO - Adrien Vernotte - LGPL v2.1",
    executables = [Executable("NaoSimulator.py", 
                                base = base,
                                icon = icone[0]
                              )
                   ],
    options = {'build_exe': {'excludes':excludes,
                             'packages':packages,'include_files':includefiles,
                             "includes":includes}}
    )
