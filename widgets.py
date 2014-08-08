# -*- coding: utf-8 -*-

import sys
import os

## QT libs
from PySide.QtGui import QTextBrowser
from PySide.QtGui import QWidget,QSplashScreen,QDialog
from PySide.QtGui import QFont
from PySide.QtCore import SIGNAL
from PySide import QtCore
from PySide import QtGui

QWEB_ENABLE = True
if QWEB_ENABLE:
    from PySide.QtWebKit import QWebView

# UI:
## Chargement de chaque design de fenetre.
from dep.Ui_simulator import Ui_MainWindow
from dep.Ui_aPropos import Ui_widget as Ui_aProposWindow
from dep.Ui_colors import Ui_Personnalisation
from dep.Ui_config import Ui_Configuration
if QWEB_ENABLE:
    from dep.Ui_documentation import Ui_Form as docu

class PyShell(QTextBrowser):
    """
    Permet d'afficher du texte comme dans le Python Shell intégré.
    """
    def __init__(self,  conteneur=None):
        QTextBrowser.__init__(self)
        self.setParent(conteneur)
        self.font=QFont("Courier",12)
        self.setFont(self.font)
        self.clearTT()
    def write(self, text):
        if text.strip()=="":return
        self.setText(self.toPlainText()+text)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
    def clearTT(self):
        self.setText(">>>")
    def finish(self):
        self.write("\n\n>>>")
    # define a slot with the right signature
    @QtCore.Slot(str)
    def slotMessage(self, message="ko"):
        try:
            self.write(message)
        except Exception, e:
            pass
        time.sleep(2)

class Configuration(QWidget, Ui_Configuration):
    """
    Fenêtre de configuration d'adresse IP du robot
    et de configuration du port.
    """
    def __init__(self, conteneur=None):
        if conteneur is None : conteneur = self
        QWidget.__init__(conteneur)
        Ui_Configuration.__init__(conteneur)
        self.setupUi(conteneur)

        self.defaultValueIP=""
        self.defaultValuePort=80
        self.valueIP=""
        self.valuePort=80

        ## Les valeurs du proxy par défaut sont stockés dans ce fichier.

        self.load()
        self.resetDefaults()
        self.appliquer()

        self.connect(self.buttonBox,  SIGNAL("rejected()"), self.hide)
        self.connect(self.buttonBox,  SIGNAL("accepted()"), self.appliquer)
        self.connect(self.pushButtonResetValues,  SIGNAL("released()"), self.resetDefaults)

    def load(self):
        a=open(os.path.join("dep",'config.txt'))
        b=a.readline()
        a.close()

        c=b.split(":")

        if len(c)>1:
            self.defaultValueIP=c[0].strip()
            self.defaultValuePort=int(c[1].strip())

    def save(self):
        a=open(os.path.join("dep",'config.txt'),"w")
        a.write(self.valueIP+":"+str(self.valuePort))
        a.close()

    def resetDefaults(self):
        self.lineEditValueIP.setText(self.defaultValueIP)
        self.lineEditValuePort.setText(str(self.defaultValuePort))

    def getProxy(self):
        return self.valueIP, self.valuePort

    def appliquer(self):
        self.valueIP=self.lineEditValueIP.text()
        self.valuePort=int(self.lineEditValuePort.text())
        self.save()
        self.hide()

if QWEB_ENABLE:
    class Documentation(QWidget, docu):
        ## Elle est initialisée une fois instanciée par MainWindow
        def __init__(self, conteneur=None):
            if conteneur is None : conteneur = self
            QWidget.__init__(conteneur)
            docu.__init__(conteneur)
            self.setupUi(conteneur)

class ApWindow(QDialog, Ui_aProposWindow):
    def __init__(self, conteneur=None):
        if conteneur is None : conteneur = self
        QDialog.__init__(conteneur)
        Ui_aProposWindow.__init__(conteneur)
        self.setupUi(conteneur)


from PySide.QtGui import QColorDialog
from PySide.QtGui import QPalette, QColor

class ColorWindow(QWidget, Ui_Personnalisation):
    def __init__(self, conteneur=None):
        if conteneur is None : conteneur = self
        QWidget.__init__(conteneur)
        Ui_Personnalisation.__init__(conteneur)
        self.setupUi(conteneur)

        self.listColor = []
        self.changers = [u"Fond d'écran 3D",u"Arrière-plan"]
        self.changersVar = ["wallpaper","background"]

        self.changedColor = []

        for a in self.changers:
            self.comboBox.addItem(a)
            self.listColor.append(QColor(255,255,255))
            self.changedColor.append(False)

        self.connect(self.toolButton,  SIGNAL("released()"), self.chooseColor)
        self.connect(self.comboBox,  SIGNAL("currentIndexChanged (int)"), self.changeColor)
        self.connect(self.buttonBox, SIGNAL("accepted ()"), self.apply)
        self.connect(self.buttonBox, SIGNAL("rejected ()"), self.hide)

        self.changeColor()

    def chooseColor(self):
        color = QColorDialog.getColor()
        if color.getRgb() != (0,0,0,255):
            self.listColor[self.comboBox.currentIndex()] = color
            self.changedColor[self.comboBox.currentIndex()] = True
            self.changeColor()

    def changeColor(self):
        pixmap = QtGui.QPixmap(16, 16)
        pixmap.fill(self.listColor[self.comboBox.currentIndex()])
        self.toolButton.setIcon(QtGui.QIcon(pixmap))

    def changeColorN(self, n):
        pixmap = QtGui.QPixmap(16, 16)
        pixmap.fill(self.listColor[n])
        self.toolButton.setIcon(QtGui.QIcon(pixmap))

    def apply(self):
        self.colors_applied = self.listColor[:]
        self.hide()

    def getApplied(self):
        result = {}
        for a in range(len(self.changers)):
            if self.changedColor[a]:
                result[self.changersVar[a]] = self.colors_applied[a]
        return result

    def setColorVar(self, var, color):
        self.listColor[self.changersVar.index(var)]=color
        self.changeColorN(self.changersVar.index(var))


