# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'config.ui'
#
# Created: Fri Jul 25 20:22:20 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Configuration(object):
    def setupUi(self, Configuration):
        Configuration.setObjectName("Configuration")
        Configuration.resize(450, 250)
        Configuration.setMinimumSize(QtCore.QSize(450, 250))
        Configuration.setMaximumSize(QtCore.QSize(450, 250))
        self.verticalLayout = QtGui.QVBoxLayout(Configuration)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtGui.QLabel(Configuration)
        self.label.setMinimumSize(QtCore.QSize(150, 0))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.lineEditValueIP = QtGui.QLineEdit(Configuration)
        self.lineEditValueIP.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lineEditValueIP.setMaxLength(16)
        self.lineEditValueIP.setObjectName("lineEditValueIP")
        self.horizontalLayout_2.addWidget(self.lineEditValueIP)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtGui.QLabel(Configuration)
        self.label_2.setMinimumSize(QtCore.QSize(150, 0))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEditValuePort = QtGui.QLineEdit(Configuration)
        self.lineEditValuePort.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lineEditValuePort.setMaxLength(4)
        self.lineEditValuePort.setObjectName("lineEditValuePort")
        self.horizontalLayout.addWidget(self.lineEditValuePort)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButtonResetValues = QtGui.QPushButton(Configuration)
        self.pushButtonResetValues.setMinimumSize(QtCore.QSize(300, 0))
        self.pushButtonResetValues.setMaximumSize(QtCore.QSize(150, 16777215))
        self.pushButtonResetValues.setObjectName("pushButtonResetValues")
        self.horizontalLayout_3.addWidget(self.pushButtonResetValues)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.buttonBox = QtGui.QDialogButtonBox(Configuration)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Configuration)
        QtCore.QMetaObject.connectSlotsByName(Configuration)

    def retranslateUi(self, Configuration):
        Configuration.setWindowTitle(QtGui.QApplication.translate("Configuration", "Configuration des paramètres réseau", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Configuration", "Adresse IP du robot", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Configuration", "Port", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonResetValues.setText(QtGui.QApplication.translate("Configuration", "Restaurer valeurs par défaut", None, QtGui.QApplication.UnicodeUTF8))

