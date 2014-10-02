
dépendances : pyqt4 pyOpenGL3 numpy1.X
(éventuellement cx_freeze 4.3.2 pour la compilation)
(ou aucune dépendance si utilisation de la version compilée)

main : NaoSimulator.py

compiler : python setup.py build

installation des dépendances sous Linux :

sudo apt-get install python-qt4
sudo apt-get install python-opengl
sudo apt-get install python-qt4-gl
sudo apt-get install python-numpy

sudo apt-get install python-imaging
sudo apt-get install python-imaging-tk