NaoSimulator
============
NaoSimulator is a free open source [NAO robot](https://www.softbankrobotics.com/emea/en/nao) simulator.  
This tool is made to help students to learn Python programming with the NAO robot.  
Feel free to [submit issues](https://github.com/AdrienVR/NaoSimulator/issues) or even better: [Pull requests](https://gist.github.com/Chaser324/ce0505fbed06b947d962#creating-a-fork)!

| ![NaoSimulator](https://raw.githubusercontent.com/AdrienVR/NaoSimulator/master/ns1.jpg "NaoSimulator") |
|:----:|

## Download Windows Binary

* [NS 1.0.0 zip : 26 mo](https://drive.google.com/uc?export=download&id=0B2xlFxzCEekzbWxFMm56ajJ1UTg)  
* [NS 1.0.0 7z : 18 mo](https://drive.google.com/uc?export=download&id=0B2xlFxzCEekzbExqOGtra244Yms)  
	
## Python Dependencies (non-compiled version)

* [Python 2.7](https://www.python.org/download/releases/2.7.8/)  
* [PyQt4](http://www.riverbankcomputing.co.uk/software/pyqt/download)
* [pyOpenGL3](https://pypi.python.org/pypi/PyOpenGL/3.1.0)
* [numpy1.X](https://pypi.python.org/pypi/numpy)
* (optional) [cx_freeze 4](https://pypi.python.org/pypi/cx_Freeze) **to enable compilation**

### Install them on Windows using pip (make sure to start in Administrator mode):   
* With [python.exe in system path](https://superuser.com/questions/143119/how-do-i-add-python-to-the-windows-path):  

      python -m pip install PyOpenGL cx-Freeze  
      python -m pip install numpy  
     In case it doesn't work, install the [Microsoft Visual C++ Compiler for Python 2.7](http://www.microsoft.com/en-us/download/details.aspx?id=44266), then retry:
     
      python -m pip install numpy  
				
* [How to install PyQt4 on Windows using pip?](https://stackoverflow.com/a/48078369)  

	Download the appropriate version (32bits Python 2.7) of the PyQt4 from here: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4  
	From the download repository:
	
       pip install PyQt4-4.11.4-cp27-cp27m-win32.whl
	
	To execute all functionalities you will also need [PIL](https://stackoverflow.com/a/20061019) (Pillow) and [pynaoqi](https://community.ald.softbankrobotics.com/en/dl/ZmllbGRfY29sbGVjdGlvbl9pdGVtLTc4OC1maWVsZF9zb2Z0X2RsX2V4dGVybmFsX2xpbmstMC0yOGE5Zjk%3D?width=500&height=auto) (run installer in admin mode)
	
       pip install Pillow

### Install them on Linux:


	sudo apt-get install python-qt4 python-qt4-gl python-numpy python-imaging python-imaging-tk  
	(optional) sudo apt-get install cx-freeze  
	
or
	
	sudo apt-get install python-qt4  
	sudo apt-get install python-qt4-gl  
	sudo apt-get install python-opengl  
	sudo apt-get install python-numpy  
	sudo apt-get install python-imaging  
	sudo apt-get install python-imaging-tk  
	(optional) sudo apt-get install cx-freeze  

## Instructions

This is the PyQt4 branch (stable).   
The main file is NaoSimulator.py
You can use Visual Studio 2017 for development and open NaoSimulator.sln
You can build by launching build.bat

| ![Python 2.7](https://www.python.org/static/img/python-logo.png "Python 2.7") | ![Qt4](http://www.fevrierdorian.com/blog/public/logos/Qt_logo002.png "Qt4") |
|:----:|:----:|

## Author

Adrien Vernotte
