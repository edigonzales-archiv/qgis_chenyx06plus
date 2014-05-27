# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtXml
from qgis.core import *
from qgis.gui import *
import os, math

from dbTools import DbObj
import utils

class CompareCoordsById( QObject ):
    
    def __init__(self):
        
        self.settings = QSettings("CatAIS","chenyx06+")
        self.tempdir = self.settings.value("temp/dir").toString()


    def run( self, iface, layerNameA, layerNameB, identA, identB, addLayerToMap):
        if self.tempdir == "":
            QMessageBox.warning( None, "CHENyx06+", "No output directory set.")
            return

        layerA = utils.getVectorLayerByName(layerNameA)
        if layerA == None:
            QMessageBox.warning( None, "CHENyx06+", "Layer not found: " + layerNameA)
            return  

        layerB = utils.getVectorLayerByName(layerNameB)
        if layerB == None:
            QMessageBox.warning( None, "CHENyx06+", "Layer not found: " + layerNameB )
            return  
            
            
        print layerNameA
        print layerNameB
        
        layerAprovider = layerA.dataProvider()
        featA = QgsFeature()
        allAttrsA = layerAprovider.attributeIndexes()
        layerAprovider.select(allAttrsA)
        
        layerBprovider = layerB.dataProvider()
        featB = QgsFeature()
        allAttrsB = layerBprovider.attributeIndexes()
        layerBprovider.select(allAttrsB)
        
        identAidx = layerAprovider.fieldNameIndex(identA)
        identBidx = layerBprovider.fieldNameIndex(identB)

        if identAidx == -1:
            QMessageBox.warning( None, "CHENyx06+", "Attribute (<i>"+identA+"</i>) in layer A not found." )
            return

        if identBidx == -1:
            QMessageBox.warning( None, "CHENyx06+", "Attribute (<i>"+identB+"</i>) in layer B not found." )
            return
            
        fields = { 0 : QgsField("identifier", QVariant.String),
                  1 : QgsField("y1", QVariant.Double), 
                  2 : QgsField("x1", QVariant.Double), 
                  3 : QgsField("y2", QVariant.Double), 
                  4 : QgsField("x2", QVariant.Double), 
                  5 : QgsField("dy", QVariant.Double), 
                  6 : QgsField("dx", QVariant.Double), 
                  7 : QgsField("fs", QVariant.Double)}

        time = QDateTime.currentDateTime()
        fileSuffix = str(time.toString(Qt.ISODate)).replace(":", "").replace("-", "")
        filePath = os.path.join(str(self.tempdir), str(layerNameA) + str("__") + str(layerNameB) + str("__") + fileSuffix + str(".shp"))

        writer = QgsVectorFileWriter(filePath, "CP1250", fields, QGis.WKBPoint, layerAprovider.crs())

        if writer.hasError() != QgsVectorFileWriter.NoError:
            QMessageBox.warning( None, "CHENyx06+", "Error when creating shapefile: " + str(writer.hasError()) )            
            print "Error when creating shapefile: ", writer.hasError()
            return
        
        QApplication.setOverrideCursor(Qt.WaitCursor)
        while layerAprovider.nextFeature(featA):
            geomA = featA.geometry()
            identAttrA = str(featA.attributeMap()[identAidx].toString()).strip()

            layerBprovider = layerB.dataProvider()
            featB = QgsFeature()
            allAttrsB = layerBprovider.attributeIndexes()
            layerBprovider.select(allAttrsB)
            
            while layerBprovider.nextFeature(featB):
                geomB = featB.geometry()
                identAttrB = str(featB.attributeMap()[identBidx].toString()).strip()

                if identAttrA == identAttrB:
                    print str(identAttrA) + "found."
                    
                    y1 = geomA.asPoint().x()
                    x1 = geomA.asPoint().y()
                    y2 = geomB.asPoint().x()
                    x2 = geomB.asPoint().y()
                    dy = y2 - y1
                    dx = x2 - x1
                    fs = ( dy**2 + dx**2  )**0.5

                    feat = QgsFeature()
                    feat.setGeometry(geomA)
                    feat.addAttribute(0, QVariant(identAttrA))
                    feat.addAttribute(1, QVariant(y1))
                    feat.addAttribute(2, QVariant(x1))
                    feat.addAttribute(3, QVariant(y2))
                    feat.addAttribute(4, QVariant(x2))
                    feat.addAttribute(5, QVariant(dy*1000))
                    feat.addAttribute(6, QVariant(dx*1000))
                    feat.addAttribute(7, QVariant(fs*1000))
                    writer.addFeature(feat)
                    
                    # Doppelte Zuweisungen sind so halt nicht mehr möglich. 
                    # Dafür wirds schneller.
                    break
                    
        QApplication.restoreOverrideCursor()
        del writer     

        if addLayerToMap == True:
            vlayer = QgsVectorLayer(filePath, str(layerNameA) + str("__") + str(layerNameB) + str("__") + fileSuffix, "ogr")                
            qml = QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + '/python/plugins/chenyx06plus/styles/diff/diff1.qml'))
            vlayer.loadNamedStyle(qml)
        
            if not vlayer.isValid():
                QMessageBox.warning( None, "CHENyx06+", "Layer could not be added." )            
                print "Layer failed to load!"
                return
            else:
                QgsMapLayerRegistry.instance().addMapLayer(vlayer)
        else:
            QMessageBox.warning( None, "CHENyx06+", "Layer created: <br><br><i>" + filePath + "</i>" )            


