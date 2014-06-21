# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aPropos.ui'
#
# Created: Sat Jun 21 14:16:49 2014
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_widget(object):
    def setupUi(self, widget):
        widget.setObjectName("widget")
        widget.resize(421, 464)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
        widget.setSizePolicy(sizePolicy)
        widget.setMinimumSize(QtCore.QSize(421, 464))
        widget.setMaximumSize(QtCore.QSize(421, 464))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(206, 213, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(206, 213, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(206, 213, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(206, 213, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        widget.setPalette(palette)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/ico.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        widget.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(widget)
        self.label.setMaximumSize(QtCore.QSize(200, 100))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_3 = QtGui.QLabel(widget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtGui.QLabel(widget)
        self.label_2.setMaximumSize(QtCore.QSize(260, 16777215))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(":/img/LOGOTYPE.png"))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(widget)
        QtCore.QMetaObject.connectSlotsByName(widget)

    def retranslateUi(self, widget):
        widget.setWindowTitle(QtGui.QApplication.translate("widget", "À propos", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("widget", "NAO Simulator 2014\n"
"v.0.9.8 Adrien Vernotte\n"
"juin 2014", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("widget", "NAO Simulator 2014 est un simulateur de robot NAO gratuit destiné à apprendre la programmation en Python dans une interface simple.\n"
"\n"
"Ce simulateur a été développé dans le cadre du projet \"Horizon ENIB\" qui vise à faire découvrir l\'enseignement supérieur et la recherche dans le domaine de l\'informatique, de l\'électronique et de la mécatronique.\n"
"\n"
"Programmé en Python, utilise PyQt4 et l\'API de l\'ENIB.\n"
"Remerciements : Céline Jost", None, QtGui.QApplication.UnicodeUTF8))

import rsc_rc
