from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtXml
from qgis.core import *
from qgis.gui import *
import os, math

from dbTools import DbObj
import utils

class CopyTspData( QObject ):
    
    def __init__(self):
        
        self.settings = QSettings("CatAIS","chenyx06+")
        
        self.host =  self.settings.value("db/host").toString() 
        self.database = self.settings.value("db/database").toString() 
        self.port = self.settings.value("db/port").toString() 
        self.schema = self.settings.value("db/schema").toString()
        self.user = self.settings.value("db/username").toString() 
        self.userpassword = self.settings.value("db/password").toString()   
        self.admin = self.settings.value("db/admin").toString() 
        self.adminpassword = self.settings.value("db/adminpassword").toString() 
        self.tempdir = self.settings.value("temp/dir").toString()

        self.tlayer = None
        self.tlayerDst = None


    def run( self, iface, layerName, numberAttrName, typeAttrName, referenceFrame, onlySelected ):
        uri = QgsDataSourceURI()
        uri.setConnection(self.host, self.port, self.database, self.admin, self.adminpassword)
        uri.setDataSource(self.schema, "tsp_"+referenceFrame, "the_geom")
        uri.setKeyColumn("ogc_fid")

        tsplayer = QgsVectorLayer(uri.uri(), "tsp_"+referenceFrame, "postgres")
    
        if not tsplayer.isValid():    
            QMessageBox.warning( None, "CHENyx06+", "Could not copy features." )
            return
            
        print uri.uri()

        tspprovider = tsplayer.dataProvider()
        tspNumberIdx = tspprovider.fieldNameIndex("nummer")
        tspTypeIdx = tspprovider.fieldNameIndex("typ")
        
        if tspNumberIdx == -1 or tspTypeIdx == -1:
            QMessageBox.warning( None, "CHENyx06+", "Attributes (<i>"+numberAttrName+"</i> and/or <i>"+typeAttrName+"</i>) not found." )
            return

        copylayer = utils.getVectorLayerByName(layerName)
        if copylayer == None:
            QMessageBox.warning( None, "CHENyx06+", "Layer not found: " + layerName )
            return  

        copyprovider = copylayer.dataProvider()
        feat = QgsFeature()
        allAttrs = copyprovider.attributeIndexes()
        copyprovider.select(allAttrs)

        copyNumberIdx = copyprovider.fieldNameIndex(numberAttrName)
        copyTypeIdx = copyprovider.fieldNameIndex(typeAttrName)
            
            
        error = 0
        QApplication.setOverrideCursor(Qt.WaitCursor)
        
        if onlySelected == True:
            selectedFeatures = copylayer.selectedFeatures()
            for feat in selectedFeatures:
                geom = feat.geometry()
                
                numberAttr = feat.attributeMap()[copyNumberIdx].toString()
                typeAttr = feat.attributeMap()[copyTypeIdx].toInt()[0]
                
                f = QgsFeature()
                f.setGeometry(geom)
                f.setAttributeMap( { tspNumberIdx : QVariant(str(numberAttr)), tspTypeIdx : QVariant(int(typeAttr)) } )
                result = tspprovider.addFeatures([f])
                if result[0] == False:
                    print numberAttr
                    print result
                    error = error + 1
        else:        
            while copyprovider.nextFeature(feat):
                geom = feat.geometry()
                
                numberAttr = feat.attributeMap()[copyNumberIdx].toString()
                typeAttr = feat.attributeMap()[copyTypeIdx].toInt()[0]
                
                f = QgsFeature()
                f.setGeometry(geom)
                f.setAttributeMap( { tspNumberIdx : QVariant(str(numberAttr)), tspTypeIdx : QVariant(int(typeAttr)) } )
                result = tspprovider.addFeatures([f])
                if result[0] == False:
                    print numberAttr
                    print result
                    error = error + 1
                
        QApplication.restoreOverrideCursor()
        
        if error > 0:
            QMessageBox.warning( None, "CHENyx06+", "Could not copy some feature(s)." )
        else:
            QMessageBox.information( None, "CHENyx06+", "Features were added." )

        del tsplayer



