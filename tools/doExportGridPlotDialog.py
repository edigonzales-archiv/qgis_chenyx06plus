# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from Ui_exportgridplot import Ui_ExportGridPlot
import os, sys
import utils
import locale

class ExportGridPlotDialog(QDialog, Ui_ExportGridPlot):
  
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self.okButton = self.buttonBox.button(QDialogButtonBox.Ok)
        self.connect(self.okButton, SIGNAL("accepted()"), self.accept)

        locale.setlocale(locale.LC_ALL)
        
    def initGui(self):
        
#        tsplayer = utils.getVectorLayerByName("TSP")
#        if tsplayer == None:
#            QMessageBox.warning( None, "CHENyx06+", "TSP layer not found.")
#            return None

        vlayers = utils.getLayerNames([0, 1, 2])
        vlayers.sort()
        vlayers.insert(0, "-------------------")
        self.cBLayer.addItems(vlayers)
        
        if len(vlayers) == 0:
            self.okButton.setDisabled (True)
        
        return True
        
        
    @pyqtSignature("on_cBGridPoints_clicked()")      
    def on_cBGridPoints_clicked(self):    
        print "CLICKED....."
        
        if self.cBGridPoints.checkState() == Qt.Unchecked:
            self.sBGridDistance.setEnabled(False)
        else:
            self.sBGridDistance.setEnabled(True)


    def accept(self):
        if self.cBLayer.currentIndex() == 0:
            QMessageBox.warning( None, "CHENyx06+", "No layer choosen.")
            return
        else:
            self.emit( SIGNAL("okClickedExportGridPlot(QString, bool, bool, bool, float, bool)"), self.cBLayer.currentText(), self.cBTriangles.isChecked(), self.cBCornerPoints.isChecked(), self.cBGridPoints.isChecked(), self.sBGridDistance.value(),  self.cBAddLayers.isChecked())



#        vlayer = utils.getVectorLayerByName(self.cBLayer.currentText())
        

#    @pyqtSignature("on_cBLayer_currentIndexChanged(QString)")      
#    def on_cBLayer_currentIndexChanged(self):    
#        vlayer = utils.getVectorLayerByName(self.cBLayer.currentText())
#        
#        if vlayer == None:
#            self.cBNumber.clear()
#            self.cBType.clear()
#            self.cBNumber.insertItem( 0,  "--------------------" )
#            self.cBType.insertItem( 0,  "--------------------" )            
#            return
#            
#        numberList = []
#        stringList = []
#        
#        provider = vlayer.dataProvider()
#        fields = provider.fields()
#
#        for i in fields:
#            fieldType = fields[i].type()
#            if fieldType == 6 or fieldType == 2:
#                numberList.append(str(fields[i].name()))
#            elif fieldType == 10:
#                stringList.append(str(fields[i].name()))
#                
#        self.cBNumber.clear()
#        self.cBNumber.addItems(sorted(stringList))
#        self.cBNumber.insertItem( 0,  "--------------------" )
#        self.cBNumber.setCurrentIndex(0)        
#
#        self.cBType.clear()
#        self.cBType.addItems(sorted(numberList))
#        self.cBType.insertItem( 0,  "--------------------" )
#        self.cBType.setCurrentIndex(0)        
#   
#        
#    def accept(self):
#
#        if self.cBLayer.currentIndex() == 0:
#            QMessageBox.warning( None, "CHENyx06+", "No layer choosen.")
#            return
#        elif self.cBNumber.currentIndex() == 0:
#            QMessageBox.warning( None, "CHENyx06+", "No number attribute choosen.")
#            return
#        else:
#            self.emit( SIGNAL("okClickedCopyTspData(QString, QString, QString, QString)"), self.cBLayer.currentText(), self.type, self.cBNumber.currentText(), self.cBType.currentText() )

