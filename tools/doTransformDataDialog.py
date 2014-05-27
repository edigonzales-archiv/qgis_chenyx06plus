# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from Ui_transform import Ui_Transform
import os, sys
import utils
import locale

class TransformDataDialog(QDialog, Ui_Transform):
  
    def __init__(self, parent, type):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self.type = type
    
        self.okButton = self.buttonBox.button(QDialogButtonBox.Ok)
        self.connect(self.okButton, SIGNAL("accepted()"), self.accept)

    def initGui(self):
    
        vlayers = utils.getLayerNames([0, 1, 2])
        vlayers.sort(key=locale.strxfrm)
        self.comboBox.addItems(vlayers)
        
        if len(vlayers) == 0:
            self.okButton.setDisabled (True)
        
        
    def accept(self):
        self.emit( SIGNAL("okClickedTransformData(QString, bool, QString)"), self.comboBox.currentText(), self.useSelected.isChecked(), self.type )

