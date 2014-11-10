# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'colors.ui'
#
# Created: Mon Nov 10 14:59:05 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Personnalisation(object):
    def setupUi(self, Personnalisation):
        Personnalisation.setObjectName("Personnalisation")
        Personnalisation.resize(380, 200)
        Personnalisation.setMinimumSize(QtCore.QSize(380, 200))
        Personnalisation.setMaximumSize(QtCore.QSize(380, 200))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/ico.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Personnalisation.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(Personnalisation)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(Personnalisation)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox = QtGui.QComboBox(Personnalisation)
        self.comboBox.setMaximumSize(QtCore.QSize(200, 16777215))
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)
        self.toolButton = QtGui.QToolButton(Personnalisation)
        self.toolButton.setMinimumSize(QtCore.QSize(40, 0))
        self.toolButton.setText("")
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout.addWidget(self.toolButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(Personnalisation)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Personnalisation)
        QtCore.QMetaObject.connectSlotsByName(Personnalisation)

    def retranslateUi(self, Personnalisation):
        Personnalisation.setWindowTitle(QtGui.QApplication.translate("Personnalisation", "Personnalisation", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Personnalisation", "Vous avez besoin de changer les couleurs pour un article scientifique ?\n"
"Vous aimez le rose fuschia ?\n"
"C\'est ici que vous pouvez personnaliser le simulateur !", None, QtGui.QApplication.UnicodeUTF8))

import rsc_rc
