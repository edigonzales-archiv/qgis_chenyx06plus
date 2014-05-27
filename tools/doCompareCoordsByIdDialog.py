# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from Ui_comparecoordsbyid import Ui_CompareCoordsById
import os, sys
import utils
import locale

class CompareCoordsByIdDialog(QDialog, Ui_CompareCoordsById):
  
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)
            
        self.okButton = self.buttonBox.button(QDialogButtonBox.Ok)
        self.connect(self.okButton, SIGNAL("accepted()"), self.accept)


    def initGui(self):
        
        vlayers = utils.getLayerNames([0])
        vlayers.sort(key=locale.strxfrm)
        vlayers.insert(0, "-------------------")
        self.cbLayerA.addItems(vlayers)
        self.cbLayerB.addItems(vlayers)

        self.cbIdA.insertItem( 0,  "--------------------" )
        self.cbIdB.insertItem( 0,  "--------------------" )
        
        
        if len(vlayers) == 0:
            self.okButton.setDisabled (True)
                
        
    @pyqtSignature("on_cbLayerA_currentIndexChanged(QString)")      
    def on_cbLayerA_currentIndexChanged(self):    
        vlayer = utils.getVectorLayerByName(self.cbLayerA.currentText())

        if vlayer == None:
            self.cbIdA.clear()
            self.cbIdA.insertItem( 0,  "--------------------" )            
            return
            
        attrList = []
        
        provider = vlayer.dataProvider()
        fields = provider.fields()

        for i in fields:
            fieldType = fields[i].type()
            if fieldType == 6 or fieldType == 2 or fieldType == 10:
                attrList.append(str(fields[i].name()))
                
        self.cbIdA.clear()
        self.cbIdA.addItems(sorted(attrList))
        self.cbIdA.insertItem( 0,  "--------------------" )
        self.cbIdA.setCurrentIndex(0)        


    @pyqtSignature("on_cbLayerB_currentIndexChanged(QString)")      
    def on_cbLayerB_currentIndexChanged(self):    
        vlayer = utils.getVectorLayerByName(self.cbLayerB.currentText())

        if vlayer == None:
            self.cbIdB.clear()
            self.cbIdB.insertItem( 0,  "--------------------" )            
            return
            
        attrList = []
        
        provider = vlayer.dataProvider()
        fields = provider.fields()

        for i in fields:
            fieldType = fields[i].type()
            if fieldType == 6 or fieldType == 2 or fieldType == 10:
                attrList.append(str(fields[i].name()))
                
        self.cbIdB.clear()
        self.cbIdB.addItems(sorted(attrList))
        self.cbIdB.insertItem( 0,  "--------------------" )
        self.cbIdB.setCurrentIndex(0)        


    def accept(self):

        if self.cbLayerA.currentIndex() == 0:
            QMessageBox.warning( None, "CHENyx06+", "No layer A chosen.")
            return

        elif self.cbLayerB.currentIndex() == 0:
            QMessageBox.warning( None, "CHENyx06+", "No layer B chosen.")
            return

        elif self.cbIdA.currentIndex() == 0:
            QMessageBox.warning( None, "CHENyx06+", "No attribute for layer A chosen.")
            return
            
        elif self.cbIdA.currentIndex() == 0:
            QMessageBox.warning( None, "CHENyx06+", "No attribute for layer B chosen.")
            return   
            
        elif self.cbLayerA.currentIndex() == self.cbLayerB.currentIndex():
            QMessageBox.warning( None, "CHENyx06+", "It's not possible to compare a layer to the same layer.")
            return   

        else:
            self.emit( SIGNAL("okClickedCopyCoordsById(QString, QString, QString, QString,bool)"), self.cbLayerA.currentText(), self.cbLayerB.currentText(), self.cbIdA.currentText(), self.cbIdB.currentText(), self.checkBoxAddLayerToMap.isChecked())

        
