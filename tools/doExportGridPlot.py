from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtXml
from qgis.core import *
from qgis.gui import *
import os, math

from dbTools import DbObj
import utils

class ExportGridPlot( QObject ):
    
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

        self.connected = False
        
        if self.host == "" or self.database == "" or self.port == "" or self.schema == "" or self.admin == "" or self.adminpassword == "":
            QMessageBox.warning( None, "", "No database parameter set.")
        else:
            self.dbobj = DbObj("default", "pg",  self.host,  self.port,  self.database,  self.admin,  self.adminpassword)
            self.connected = self.dbobj.connect()


    def run( self, iface, layerName, createTriangles, createCornerPoints, createGridPoints, gridPointDistance, addLayersToMap ):
        
        srs = iface.mapCanvas().mapRenderer().destinationCrs().authid()
            
        if srs == "EPSG:2056":
            dstEpsgId = 2056
        else:
            dstEpsgId = 21781
        
        if self.connected == False:
            QMessageBox.warning( None, "CHENyx06+", "Could not connect to database." )
            return
        
        player = utils.getVectorLayerByName(layerName)
        if player == None:
            QMessageBox.warning( None, "CHENyx06+", "Perimeter layer not found.")
            return None
        
        xMin = player.extent().xMinimum()
        yMin = player.extent().yMinimum()
        xMax = player.extent().xMaximum()
        yMax = player.extent().yMaximum()
        
        time = QDateTime.currentDateTime()
        shpSuffix = str(time.toString(Qt.ISODate)).replace(":", "").replace("-", "")
        
        # Get the triangles touching the perimeter bounding box.
        fields = { 0 : QgsField("identifier", QVariant.String),
                  1 : QgsField("type", QVariant.Int)}
                  
        shpFilePathTriangles = os.path.join(str(self.tempdir), str("dreiecke_perimeter") + str("_") + shpSuffix + str(".shp"))
        writer = QgsVectorFileWriter(shpFilePathTriangles, "CP1250", fields, QGis.WKBPolygon, QgsCoordinateReferenceSystem(dstEpsgId, QgsCoordinateReferenceSystem().EpsgCrsId))  

        query = "SELECT ogc_fid, nummer, typ, astext(the_geom_lv03) as the_geom FROM " + self.schema + ".dreiecke WHERE the_geom_lv03 && ST_SetSRID(ST_MakeBox2D(ST_Point("+str(xMin)+", "+str(yMin)+"), ST_Point("+str(xMax)+", "+str(yMax)+")), "+str(dstEpsgId)+")"
        self.triangles = self.dbobj.read( query )

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            for i in range(len(self.triangles['OGC_FID'])):
                wkt = self.triangles['THE_GEOM'][i]
                geom = QgsGeometry().fromWkt(wkt)
            
                feat = QgsFeature()
                feat.setGeometry(geom)
                feat.addAttribute(0, QVariant(self.triangles['NUMMER'][i]))
                feat.addAttribute(1, QVariant(self.triangles['TYP'][i]))
                
                writer.addFeature(feat)

        except:
            QApplication.restoreOverrideCursor()            
            del writer   
            QMessageBox.warning( None, "", "Database: Exception.")
            print "Database: Exception."
            return None

        QApplication.restoreOverrideCursor()            
        del writer   
        

        # Get the tsp from the triangles touching the perimeter bounding box.
        fields = { 0 : QgsField("identifier", QVariant.String),
                  1 : QgsField("dy", QVariant.Double), 
                  2 : QgsField("dx", QVariant.Double), 
                  3 : QgsField("fs", QVariant.Double)}
        
        
        shpFilePathTsp = os.path.join(str(self.tempdir), str("tsp_perimeter") + str("_") + shpSuffix + str(".shp"))
        writer = QgsVectorFileWriter(shpFilePathTsp, "CP1250", fields, QGis.WKBPoint, QgsCoordinateReferenceSystem(dstEpsgId, QgsCoordinateReferenceSystem().EpsgCrsId))  

        query = "SELECT d.ogc_fid, d.nummer, d.dy, d.dx, round(sqrt(d.dy*d.dy + d.dx*d.dx),0) as fs, astext(d.the_geom) as the_geom FROM ( SELECT c.ogc_fid, c.nummer, round(((c.ycoord95-2000000)-c.ycoord03)*1000, 0) as dy, round(((c.xcoord95-1000000)-c.xcoord03)*1000, 0) as dx, c.the_geom FROM ( SELECT a.ogc_fid, a.nummer, round(st_x(a.the_geom)::numeric, 3) AS ycoord95, round(st_y(a.the_geom)::numeric, 3) AS xcoord95, round(st_x(b.the_geom)::numeric, 3) AS ycoord03, round(st_y(b.the_geom)::numeric, 3) AS xcoord03, b.the_geom FROM "+self.schema+".tsp_lv95 as a, ( SELECT a.ogc_fid, a.nummer, a.the_geom FROM "+self.schema+".tsp_lv03 a, ( SELECT st_geomfromewkb(r.the_wkb) AS the_geom FROM ( SELECT DISTINCT st_asewkb((st_dumppoints(dreiecke.the_geom_lv03)).geom) AS the_wkb FROM "+self.schema+".dreiecke WHERE the_geom_lv03 && ST_SetSRID(ST_MakeBox2D(ST_Point("+str(xMin)+", "+str(yMin)+"), ST_Point("+str(xMax)+", "+str(yMax)+")), "+str(dstEpsgId)+")) r ) b WHERE a.the_geom && b.the_geom AND st_intersects(st_snaptogrid(a.the_geom, 0.001::double precision), st_snaptogrid(b.the_geom, 0.001::double precision))) as b WHERE a.nummer = b.nummer ) as c ) as d"
        self.tsp = self.dbobj.read( query )

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            for i in range(len(self.tsp['OGC_FID'])):
                wkt = self.tsp['THE_GEOM'][i]
                geom = QgsGeometry().fromWkt(wkt)
            
                feat = QgsFeature()
                feat.setGeometry(geom)
                feat.addAttribute(0, QVariant(self.tsp['NUMMER'][i]))
                feat.addAttribute(1, QVariant(self.tsp['DY'][i]))
                feat.addAttribute(2, QVariant(self.tsp['DX'][i]))
                feat.addAttribute(3, QVariant(self.tsp['FS'][i]))
                
                writer.addFeature(feat)

        except KeyError:
            QApplication.restoreOverrideCursor()            
            del writer   
            QMessageBox.warning( None, "", "Database: Exception.")
            print "Database: Exception."
            return None

        QApplication.restoreOverrideCursor()            
        del writer   

        
        
        

        if addLayersToMap == True:
            vlayer = QgsVectorLayer(shpFilePathTriangles, str("dreiecke_perimeter") + str("__") + shpSuffix, "ogr")                
            qml = QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + '/python/plugins/chenyx06plus/styles/dreiecke/perimeter.qml'))
            vlayer.loadNamedStyle(qml)
        
            if not vlayer.isValid():
                QMessageBox.warning( None, "CHENyx06+", "Layer could not be added." )            
                print "Layer failed to load!"
                return
            else:
                QgsMapLayerRegistry.instance().addMapLayer(vlayer)
                
            vlayer = QgsVectorLayer(shpFilePathTsp, str("tsp_perimeter") + str("__") + shpSuffix, "ogr")                
            qml = QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + '/python/plugins/chenyx06plus/styles/tsp/perimeter.qml'))
            vlayer.loadNamedStyle(qml)
        
            if not vlayer.isValid():
                QMessageBox.warning( None, "CHENyx06+", "Layer could not be added." )            
                print "Layer failed to load!"
                return
            else:
                QgsMapLayerRegistry.instance().addMapLayer(vlayer)
                
                
                
        else:
            QMessageBox.warning( None, "CHENyx06+", "Files created: <br><br><i>" + str(shpFilePathTriangles) + "<br>" +str(shpFilePathTsp) + "</i>" )            

   



