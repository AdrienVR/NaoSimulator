# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'documentation.ui'
#
# Created: Thu Jul 24 16:14:35 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(834, 645)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/ico.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.webView = QtWebKit.QWebView(Form)
        self.webView.setUrl(QtCore.QUrl("about:blank"))
        self.webView.setObjectName("webView")
        self.horizontalLayout.addWidget(self.webView)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Documentation", None, QtGui.QApplication.UnicodeUTF8))

from PySide import QtWebKit
import rsc_rc
