# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_about.ui'
#
# Created: Mon Jul 25 16:41:46 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_About(object):
    def setupUi(self, About):
        About.setObjectName("About")
        About.resize(285, 333)
        self.gridlayout = QtGui.QGridLayout(About)
        self.gridlayout.setObjectName("gridlayout")
        self.txtAbout = QtGui.QTextEdit(About)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.txtAbout.setPalette(palette)
        self.txtAbout.setAutoFillBackground(True)
        self.txtAbout.setFrameShape(QtGui.QFrame.NoFrame)
        self.txtAbout.setFrameShadow(QtGui.QFrame.Plain)
        self.txtAbout.setReadOnly(True)
        self.txtAbout.setObjectName("txtAbout")
        self.gridlayout.addWidget(self.txtAbout, 2, 0, 1, 3)
        self.btnHelp = QtGui.QPushButton(About)
        self.btnHelp.setEnabled(False)
        self.btnHelp.setObjectName("btnHelp")
        self.gridlayout.addWidget(self.btnHelp, 3, 0, 1, 1)
        self.btnClose = QtGui.QPushButton(About)
        self.btnClose.setObjectName("btnClose")
        self.gridlayout.addWidget(self.btnClose, 3, 2, 1, 1)
        self.btnWeb = QtGui.QPushButton(About)
        self.btnWeb.setEnabled(False)
        self.btnWeb.setObjectName("btnWeb")
        self.gridlayout.addWidget(self.btnWeb, 3, 1, 1, 1)
        self.lblVersion = QtGui.QLabel(About)
        self.lblVersion.setObjectName("lblVersion")
        self.gridlayout.addWidget(self.lblVersion, 1, 0, 1, 2)
        self.lblTitle = QtGui.QLabel(About)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setWeight(75)
        font.setBold(True)
        self.lblTitle.setFont(font)
        self.lblTitle.setTextFormat(QtCore.Qt.RichText)
        self.lblTitle.setObjectName("lblTitle")
        self.gridlayout.addWidget(self.lblTitle, 0, 0, 1, 2)

        self.retranslateUi(About)
        QtCore.QObject.connect(self.btnClose, QtCore.SIGNAL("clicked()"), About.reject)
        QtCore.QMetaObject.connectSlotsByName(About)

    def retranslateUi(self, About):
        About.setWindowTitle(QtGui.QApplication.translate("About", "CHENyx06+ About", None, QtGui.QApplication.UnicodeUTF8))
        self.txtAbout.setHtml(QtGui.QApplication.translate("About", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans Serif\'; font-size:9pt;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.btnHelp.setText(QtGui.QApplication.translate("About", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.btnClose.setText(QtGui.QApplication.translate("About", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.btnWeb.setText(QtGui.QApplication.translate("About", "Web", None, QtGui.QApplication.UnicodeUTF8))
        self.lblVersion.setText(QtGui.QApplication.translate("About", "Version x.x-xxxxxx", None, QtGui.QApplication.UnicodeUTF8))
        self.lblTitle.setText(QtGui.QApplication.translate("About", "CHENyx06+", None, QtGui.QApplication.UnicodeUTF8))

