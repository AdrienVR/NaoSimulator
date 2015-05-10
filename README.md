NaoSimulator
============
NaoSimulator is a free open source [NAO robot](http://www.aldebaran.com) simulator.  
This tool allows to ease the learning of Python programming with the NAO robot.  

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

### Install them on Windows using pip :   
* With python.exe in system path :  
	
	  
  
		python.exe -m pip install PyOpenGL cx-Freeze  

        try:
                python.exe -m pip install numpy  

        except:
Install the Microsoft Visual C++ Compiler for Python 2.7  http://www.microsoft.com/en-us/download/details.aspx?id=44266
	
                python.exe -m pip install numpy  


### Install them on Linux :


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
The main file is : NaoSimulator.py

| ![Python 2.7](https://www.python.org/static/img/python-logo.png "Python 2.7") | ![Qt4](http://www.fevrierdorian.com/blog/public/logos/Qt_logo002.png "Qt4") |
|:----:|:----:|

## Author

Adrien Vernotte
