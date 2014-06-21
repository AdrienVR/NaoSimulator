from PySide import QtCore

from PySide.QtCore import QObject, QThread
from PySide.QtGui import QApplication
from PySide.QtCore import Qt, SIGNAL

from time import sleep

import sys

def test(a):
    sleep(1)
    print "a"
    
class Object(QObject):
    def emitSignal(self):
        self.emit(SIGNAL("aSignal()"))

class Worker(QObject):
    fonct=None

    #ne fonctionne pour une raison inconnue
##    @staticmethod
##    def aSlot():
##        Worker().fonct()
##        print "a"
        
    def aSlot(self):
        Worker().fonct()

def makeThread(funct):
    app = QApplication(sys.argv)
    Worker.fonct=funct
    worker = Worker()
    obj = Object()

    thread = QThread()
    worker.moveToThread(thread)
    QObject.connect(obj, SIGNAL("aSignal()"), worker.aSlot)

    thread.start()
    obj.emitSignal()
    print "Done"


makeThread(test)
