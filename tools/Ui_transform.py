# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_transform.ui'
#
# Created: Tue Jul 26 21:54:44 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Transform(object):
    def setupUi(self, Transform):
        Transform.setObjectName("Transform")
        Transform.resize(400, 170)
        self.gridLayout_2 = QtGui.QGridLayout(Transform)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtGui.QGroupBox(Transform)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.comboBox = QtGui.QComboBox(self.groupBox)
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout.addWidget(self.comboBox)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.useSelected = QtGui.QCheckBox(self.groupBox)
        self.useSelected.setEnabled(True)
        self.useSelected.setObjectName("useSelected")
        self.gridLayout.addWidget(self.useSelected, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Transform)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(Transform)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Transform.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Transform.reject)
        QtCore.QMetaObject.connectSlotsByName(Transform)

    def retranslateUi(self, Transform):
        Transform.setWindowTitle(QtGui.QApplication.translate("Transform", "Transform data", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Transform", "Transformation ", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Transform", "Input layer", None, QtGui.QApplication.UnicodeUTF8))
        self.useSelected.setText(QtGui.QApplication.translate("Transform", "Use only selected features", None, QtGui.QApplication.UnicodeUTF8))

