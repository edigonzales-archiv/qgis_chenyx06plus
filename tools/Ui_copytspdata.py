# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_copytspdata.ui'
#
# Created: Sat Feb 16 15:40:56 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_CopyTspData(object):
    def setupUi(self, CopyTspData):
        CopyTspData.setObjectName(_fromUtf8("CopyTspData"))
        CopyTspData.resize(349, 204)
        self.gridLayout_3 = QtGui.QGridLayout(CopyTspData)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.groupBox = QtGui.QGroupBox(CopyTspData)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cBLayer = QtGui.QComboBox(self.groupBox)
        self.cBLayer.setMinimumSize(QtCore.QSize(0, 23))
        self.cBLayer.setObjectName(_fromUtf8("cBLayer"))
        self.gridLayout.addWidget(self.cBLayer, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.cBNumber = QtGui.QComboBox(self.groupBox)
        self.cBNumber.setMinimumSize(QtCore.QSize(0, 23))
        self.cBNumber.setObjectName(_fromUtf8("cBNumber"))
        self.gridLayout.addWidget(self.cBNumber, 1, 1, 1, 1)
        self.cBType = QtGui.QComboBox(self.groupBox)
        self.cBType.setMinimumSize(QtCore.QSize(0, 23))
        self.cBType.setObjectName(_fromUtf8("cBType"))
        self.gridLayout.addWidget(self.cBType, 2, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.cBoxSelected = QtGui.QCheckBox(self.groupBox)
        self.cBoxSelected.setObjectName(_fromUtf8("cBoxSelected"))
        self.gridLayout_2.addWidget(self.cBoxSelected, 1, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(CopyTspData)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_3.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(CopyTspData)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), CopyTspData.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), CopyTspData.reject)
        QtCore.QMetaObject.connectSlotsByName(CopyTspData)

    def retranslateUi(self, CopyTspData):
        CopyTspData.setWindowTitle(QtGui.QApplication.translate("CopyTspData", "Import TSP", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("CopyTspData", "Points to import ", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("CopyTspData", "Layer: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("CopyTspData", "Number: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("CopyTspData", "Type: ", None, QtGui.QApplication.UnicodeUTF8))
        self.cBoxSelected.setText(QtGui.QApplication.translate("CopyTspData", "Import only selected features", None, QtGui.QApplication.UnicodeUTF8))

