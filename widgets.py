# -*- coding: utf-8 -*-

import os, sys

from PyQt4.QtGui import QWidget, QTextBrowser
from PyQt4.QtGui import QFileDialog, QCursor, QToolTip
from PyQt4.QtGui import QWidget,QSplashScreen,QDialog
from PyQt4.QtGui import QColorDialog, QPalette, QColor
from PyQt4.QtGui import QFont
from PyQt4.QtCore import SIGNAL
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic

###### QWEB
path = os.path.join(os.path.dirname(sys.argv[0]), "PyQt4.uic.widget-plugins")
uic.widgetPluginPath.append(path)
from PyQt4.QtWebKit import QWebView
###### QWEB!

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
        self.setText(self.toPlainText()+text)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
    def clearTT(self):
        self.setText(">>>")
    def finish(self):
        self.write("\n>>>")
    # define a slot with the right signature
    @QtCore.pyqtSlot(str)
    def slotMessage(self, message):
        self.write(message)


## Chargement de chaque design de fenetre.
UiMainWindow,  Klass = uic.loadUiType(os.path.join("dep",'simulator.ui'))
aProposWindow, k = uic.loadUiType(os.path.join("dep",'aPropos.ui'))
colorWindow, k = uic.loadUiType(os.path.join("dep",'colors.ui'))
docu, k = uic.loadUiType(os.path.join("dep",'documentation.ui'))
config, k = uic.loadUiType(os.path.join("dep",'config.ui'))

class Configuration(QWidget, config):
    """
    Fenêtre de configuration d'adresse IP du robot
    et de configuration du port.
    """
    def __init__(self, conteneur=None):
        if conteneur is None : conteneur = self
        QWidget.__init__(conteneur)
        config.__init__(conteneur)
        self.setupUi(conteneur)

        self.defaultValueIP=""
        self.defaultValuePort=80
        self.valueIP=""
        self.valuePort=80

        ## Les valeurs du proxy par défaut sont stockés dans ce fichier.
        a=open(os.path.join("dep",'config.txt'))
        b=a.readlines()
        a.close()

        if len(b)>1:
            self.defaultValueIP=b[0].strip()
            self.defaultValuePort=int(b[1].strip())
        self.resetDefaults()
        self.appliquer()

        self.connect(self.buttonBox,  SIGNAL("rejected()"), self.hide)
        self.connect(self.buttonBox,  SIGNAL("accepted()"), self.appliquer)
        self.connect(self.pushButtonResetValues,  SIGNAL("released()"), self.resetDefaults)

    def resetDefaults(self):
        self.lineEditValueIP.setText(self.defaultValueIP)
        self.lineEditValuePort.setText(str(self.defaultValuePort))

    def getProxy(self):
        return self.valueIP, self.valuePort

    def appliquer(self):
        self.valueIP=self.lineEditValueIP.text()
        self.valuePort=int(self.lineEditValuePort.text())
        self.hide()

class Documentation(QWidget, docu):
    ## Elle est initialisée une fois instanciée par MainWindow
    def __init__(self, conteneur=None):
        if conteneur is None : conteneur = self
        QWidget.__init__(conteneur)
        docu.__init__(conteneur)
        self.setupUi(conteneur)

class ApWindow(QDialog, aProposWindow):
    def __init__(self, conteneur=None):
        if conteneur is None : conteneur = self
        QDialog.__init__(conteneur)
        aProposWindow.__init__(conteneur)
        self.setupUi(conteneur)

class ColorWindow(QWidget, colorWindow):
    def __init__(self, conteneur=None):
        if conteneur is None : conteneur = self
        QWidget.__init__(conteneur)
        colorWindow.__init__(conteneur)
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
        self.listColor[self.comboBox.currentIndex()] = QColorDialog.getColor()
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
