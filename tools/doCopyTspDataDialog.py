# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from Ui_copytspdata import Ui_CopyTspData
import os, sys
import utils
import locale

class CopyTspDataDialog(QDialog, Ui_CopyTspData):
  
    def __init__(self, parent, type):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self.type = type
    
        self.okButton = self.buttonBox.button(QDialogButtonBox.Ok)
        self.connect(self.okButton, SIGNAL("accepted()"), self.accept)
        
        title = self.groupBox.title()
        title += " (" + str(type).upper() + ")"
        self.groupBox.setTitle(title)


    def initGui(self):
        
#        tsplayer = utils.getVectorLayerByName("TSP")
#        if tsplayer == None:
#            QMessageBox.warning( None, "CHENyx06+", "TSP layer not found.")
#            return None

        vlayers = utils.getLayerNames([0])
        vlayers.sort()
#        vlayers.sort(key=locale.strxfrm)
        vlayers.insert(0, "-------------------")
        self.cBLayer.addItems(vlayers)
        
        self.cBNumber.insertItem( 0,  "--------------------" )
        self.cBType.insertItem( 0,  "--------------------" )
        
        
        if len(vlayers) == 0:
            self.okButton.setDisabled (True)
        
        return True
        
        
    @pyqtSignature("on_cBLayer_currentIndexChanged(QString)")      
    def on_cBLayer_currentIndexChanged(self):    
        vlayer = utils.getVectorLayerByName(self.cBLayer.currentText())
        
        if vlayer == None:
            self.cBNumber.clear()
            self.cBType.clear()
            self.cBNumber.insertItem( 0,  "--------------------" )
            self.cBType.insertItem( 0,  "--------------------" )            
            return
            
        numberList = []
        stringList = []
        
        provider = vlayer.dataProvider()
        fields = provider.fields()

        for i in fields:
            fieldType = fields[i].type()
            if fieldType == 6 or fieldType == 2:
                numberList.append(str(fields[i].name()))
            elif fieldType == 10:
                stringList.append(str(fields[i].name()))
                
        self.cBNumber.clear()
        self.cBNumber.addItems(sorted(stringList))
        self.cBNumber.insertItem( 0,  "--------------------" )
        self.cBNumber.setCurrentIndex(0)        

        self.cBType.clear()
        self.cBType.addItems(sorted(numberList))
        self.cBType.insertItem( 0,  "--------------------" )
        self.cBType.setCurrentIndex(0)        
   
        
    def accept(self):

        if self.cBLayer.currentIndex() == 0:
            QMessageBox.warning( None, "CHENyx06+", "No layer choosen.")
            return
        elif self.cBNumber.currentIndex() == 0:
            QMessageBox.warning( None, "CHENyx06+", "No number attribute choosen.")
            return
        else:
            self.emit( SIGNAL("okClickedCopyTspData(QString, QString, QString, QString, bool)"), self.cBLayer.currentText(), self.type, self.cBNumber.currentText(), self.cBType.currentText(), self.cBoxSelected.isChecked() )

