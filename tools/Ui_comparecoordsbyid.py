# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_comparecoordsbyid.ui'
#
# Created: Thu Jul 28 15:43:03 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_CompareCoordsById(object):
    def setupUi(self, CompareCoordsById):
        CompareCoordsById.setObjectName("CompareCoordsById")
        CompareCoordsById.resize(350, 241)
        self.gridLayout_3 = QtGui.QGridLayout(CompareCoordsById)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox = QtGui.QGroupBox(CompareCoordsById)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.cbLayerA = QtGui.QComboBox(self.groupBox)
        self.cbLayerA.setMinimumSize(QtCore.QSize(0, 23))
        self.cbLayerA.setObjectName("cbLayerA")
        self.gridLayout.addWidget(self.cbLayerA, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setMinimumSize(QtCore.QSize(0, 23))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.cbIdA = QtGui.QComboBox(self.groupBox)
        self.cbIdA.setMinimumSize(QtCore.QSize(0, 23))
        self.cbIdA.setObjectName("cbIdA")
        self.gridLayout.addWidget(self.cbIdA, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.cbLayerB = QtGui.QComboBox(self.groupBox)
        self.cbLayerB.setMinimumSize(QtCore.QSize(0, 23))
        self.cbLayerB.setObjectName("cbLayerB")
        self.gridLayout.addWidget(self.cbLayerB, 2, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.cbIdB = QtGui.QComboBox(self.groupBox)
        self.cbIdB.setMinimumSize(QtCore.QSize(0, 23))
        self.cbIdB.setObjectName("cbIdB")
        self.gridLayout.addWidget(self.cbIdB, 3, 1, 1, 1)
        self.checkBoxAddLayerToMap = QtGui.QCheckBox(self.groupBox)
        self.checkBoxAddLayerToMap.setMinimumSize(QtCore.QSize(0, 23))
        self.checkBoxAddLayerToMap.setText("")
        self.checkBoxAddLayerToMap.setObjectName("checkBoxAddLayerToMap")
        self.gridLayout.addWidget(self.checkBoxAddLayerToMap, 4, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(CompareCoordsById)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_3.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(CompareCoordsById)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), CompareCoordsById.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), CompareCoordsById.reject)
        QtCore.QMetaObject.connectSlotsByName(CompareCoordsById)

    def retranslateUi(self, CompareCoordsById):
        CompareCoordsById.setWindowTitle(QtGui.QApplication.translate("CompareCoordsById", "Compare coordinates by identifier", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("CompareCoordsById", "Compare coordinates ", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("CompareCoordsById", "Layer A: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("CompareCoordsById", "Identifier A:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("CompareCoordsById", "Layer B:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("CompareCoordsById", "Identifier B: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("CompareCoordsById", "Add layer to map: ", None, QtGui.QApplication.UnicodeUTF8))

