
dependances : pyside1.X pyOpenGL3 numpy1.X
(eventuellement cx_freeze 4.3.2 pour la compilation)

main : NaoSimulator.py

compile : python setup.py build

installation des dependances pour linux :

sudo apt-get install python-opengl
sudo apt-get install python-numpy

sudo apt-get install python-imaging
sudo apt-get install python-imaging-tk

sudo apt-get install python-pyside

## pour le developpement : (qdesigner, etc.)
##----------------------sudo apt-get install pyside-tools