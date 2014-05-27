from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtXml
from qgis.core import *
from qgis.gui import *
import os, math

from dbTools import DbObj
import utils

class TransformData( QObject ):
    
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
        self.tlayer = None
        self.tlayerDst = None


    def run( self, iface, layerName, selectedOnly, type ):
        if self.host == "" or self.database == "" or self.port == "" or self.schema == "" or self.user == "" or self.userpassword == "":
            QMessageBox.warning( None, "CHENyx06+", "No database parameter set.")
            return
        else:
            self.dbobj = DbObj("default", "pg",  self.host,  self.port,  self.database,  self.admin,  self.adminpassword)
            self.connected = self.dbobj.connect()
            
        if self.tempdir == "":
            QMessageBox.warning( None, "CHENyx06+", "No output directory set.")
            return

        srs = iface.mapCanvas().mapRenderer().destinationCrs().authid()
        #Fehler in QGIS 1.8??
        srs = "EPSG:21781"
        if srs == "EPSG:21781" or srs == "EPSG:2056":
            pass
        else:
            QMessageBox.warning( None, "", "Wrong CRS: " + srs + "<br>Should be EPSG:21781 or EPSG:2056")
            return
            
        if srs == "EPSG:2056":
            srcFrame = "lv95"
            dstFrame = "lv03"
            dstEpsgId = 21781
        else:
            srcFrame = "lv03"
            dstFrame = "lv95"
            dstEpsgId = 2056

        # Get the layer we wanna transform.
        vlayer = utils.getVectorLayerByName(layerName)
        
        if vlayer == None:
            QMessageBox.warning(None, 'CHENyx06+', "No valid layer.")   
            
        if vlayer.featureCount() == 0:
            QMessageBox.information(None, 'CHENyx06+', "No features found in layer.")   
            return
            
        # Regular or modified chenyx06.
        if type == "regular":
            self.schema = "ch_default"
        
        # Build spatial index.
        uri = QgsDataSourceURI()
        uri.setConnection(self.host, self.port, self.database, self.user, self.userpassword)
        uri.setDataSource(self.schema, "dreiecke", "the_geom_"+str(srcFrame))
        uri.setKeyColumn("ogc_fid")        
        print uri.uri()        
        self.tlayer = QgsVectorLayer(uri.uri(), "dreiecke_"+str(srcFrame), "postgres")
        self.tlayer.select()        

        if not (self.tlayer.isValid()):
            print "Layer failed to load!"
            QMessageBox.information(None, 'CHENyx06+', str("Error while loading transformation file/table."))   
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.index = QgsSpatialIndex()
        feat = QgsFeature()
        for feat in self.tlayer:
            self.index.insertFeature(feat)
        QApplication.restoreOverrideCursor()
        print "CHENyx06+: spatial index built."
        
        
        # We need also a layer with the destination Geometry 
        # since I'm not sure about the accuracy/decimals of
        # the wkt string of the attribute.
        uri = QgsDataSourceURI()
        uri.setConnection(self.host, self.port, self.database, self.user, self.userpassword)
        uri.setDataSource(self.schema, "dreiecke", "the_geom_"+str(dstFrame))
        uri.setKeyColumn("ogc_fid")                
        self.tlayerDst = QgsVectorLayer(uri.uri(), "dreiecke_"+str(dstFrame), "postgres")
        self.tlayerDst.select()    

        # Transform the features of the layer.
        provider = vlayer.dataProvider()
        allAttrs = provider.attributeIndexes()
        provider.select(allAttrs)

        vtype = vlayer.wkbType()
        if vtype == QGis.WKBUnknown:
            QMessageBox.information(None, 'CHENyx06+', str("Unknown geometry type. Data will not be transformed."))   
            return


        # Create a vector writer with destination srs (21781 or 2056)
        # TODO: encoding.... 
        time = QDateTime.currentDateTime()
        shpSuffix = str(time.toString(Qt.ISODate)).replace(":", "").replace("-", "")
        shpFilePath = os.path.join(str(self.tempdir), str(layerName) + str("_") + shpSuffix + str(".shp"))
        writer = QgsVectorFileWriter(shpFilePath, "CP1250", provider.fields(), vtype, QgsCoordinateReferenceSystem(dstEpsgId, QgsCoordinateReferenceSystem().EpsgCrsId))  

        if writer.hasError() != QgsVectorFileWriter.NoError:
            print "Error when creating shapefile: ", writer.hasError()
            QMessageBox.information(None, 'CHENyx06+', str("Error when creating shapefile."))   
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            if selectedOnly == True:
                selectedFeatures = vlayer.selectedFeatures()
                for f in selectedFeatures:
                    g = f.geometry()            
                    fet = QgsFeature()
                    tgeom = self.transformGeometry(g, vtype)
                    if tgeom == None:
                        continue
                    fet.setGeometry(tgeom)
                    fet.setAttributeMap(f.attributeMap())
                    writer.addFeature(fet)

            else:
                f = QgsFeature()
                while provider.nextFeature(f):   
                    g = f.geometry()            
                    fet = QgsFeature()
                    tgeom = self.transformGeometry(g, vtype)
                    if tgeom == None:
                        continue
                    fet.setGeometry(tgeom)
                    fet.setAttributeMap(f.attributeMap())
                    writer.addFeature(fet)
        except:
            QApplication.restoreOverrideCursor()
        QApplication.restoreOverrideCursor()

        del writer
        QMessageBox.information(None, 'CHENyx06+', "Vector dataset transformed: <br><br><i>" + shpFilePath + "</i>" )   


    def transformGeometry(self, g, vtype):
        if vtype == QGis.WKBPoint or vtype == QGis.WKBPoint25D:
            p = self.transformPoint(g.asPoint())
            if p == None:
                return None
            return QgsGeometry().fromPoint(p)

        elif vtype == QGis.WKBLineString or vtype == QGis.WKBLineString25D:
            coords = g.asPolyline()
            coords_transformed = []
            for i in coords:
                p = self.transformPoint(i)
                if p == None:
                    return None
                coords_transformed.append(p)
            return QgsGeometry().fromPolyline(coords_transformed)
        
        elif vtype == QGis.WKBPolygon or vtype == QGis.WKBPolygon25D:
            coords = g.asPolygon()
            coords_transformed = []
            ring = []
            for i in coords:
                for k in i: 
                    p = self.transformPoint(k)
                    if p == None:
                        return None
                    ring.append(p)
                coords_transformed .append(ring)
                ring = []
            return QgsGeometry().fromPolygon(coords_transformed )
                
        elif vtype == QGis.WKBMultiPoint or vtype == QGis.WKBMultiPoint25D:
            coords = g.asMultiPoint()
            coords_transformed = []
            for i in coords:
                p = self.transformPoint(i)
                if p == None:
                    return None                
                coords_transformed.append(p)
            return QgsGeometry().fromMultiPoint(coords_transformed)
            
        elif vtype == QGis.WKBMultiLineString or vtype == QGis.WKBMultiLineString25D:
            coords = g.asMultiPolyline()
            coords_transformed = []
            singleline = [] 
            for i in coords:
                for j in i:
                    p = self.transformPoint(j)
                    if p == None:
                        return None
                    singleline.append(p)
                coords_transformed.append(singleline)
                singleline = []
            return QgsGeometry().fromMultiPolyline(coords_transformed)
                
        elif vtype == QGis.WKBMultiPolygon or vtype == QGis.WKBMultiPolygon25D:
            coords = g.asMultiPolygon()
            coords_transformed = []
            ring = []
            for i in coords:
                for j in i:
                    for k in j:
                        p = self.transformPoint(k)
                        if p == None:
                            return None
                        ring.append(p)
                    coords_transformed.append(ring)
                    ring = []
            return QgsGeometry().fromMultiPolygon([coords_transformed])
            
        else:
            QMessageBox.information(None, 'CHENyx06+', str("Should not reach here..."))  
            return None


    def transformPoint(self, point):
        intersectIds = self.index.intersects(QgsRectangle(point.x(), point.y(), point.x(), point.y()))
    
        for id in intersectIds:
            srcFeat= QgsFeature()
            self.tlayer.featureAtId(int(id), srcFeat, True, True)
            srcGeom03 = srcFeat.geometry() 
#            if srcGeom03.contains(point):
            if srcGeom03.distance(QgsGeometry.fromPoint(point)) == 0:
                
                dstFeat = QgsFeature()
                self.tlayerDst.featureAtId(int(id), dstFeat, True, True)
                
#                print "flaeche src: "
#                print srcFeat.geometry().area()
                
                poly_src = srcFeat.geometry().asPolygon()
                poly_dst = dstFeat.geometry().asPolygon()
                
#                print srcFeat.geometry().exportToWkt()
#                print dstFeat.geometry().exportToWkt()
#
#                print srcFeat.attributeMap()[1].toString()
#                print dstFeat.attributeMap()[1].toString()
#
#                print "========================================"
                
                return self.fineltra(point, poly_src, poly_dst)
                    
        return None


    def fineltra(self, point, poly_src, poly_dst):
        
        x1_src = poly_src[0][0].x()
        y1_src = poly_src[0][0].y()
        x2_src = poly_src[0][1].x()
        y2_src = poly_src[0][1].y()
        x3_src = poly_src[0][2].x()
        y3_src = poly_src[0][2].y()      
   
#        print "src point"
#        print "%12.5f" % x1_src
#        print "%12.5f" % y1_src
#        print "%12.5f" % x2_src
#        print "%12.5f" % y2_src
#        print "%12.5f" % x3_src
#        print "%12.5f" % y3_src

        x1_dst = poly_dst[0][0].x()
        y1_dst = poly_dst[0][0].y()
        x2_dst = poly_dst[0][1].x()
        y2_dst = poly_dst[0][1].y()
        x3_dst = poly_dst[0][2].x()
        y3_dst = poly_dst[0][2].y()                     

#        print "dst point"
#        print "%12.5f" % x1_dst 
#        print "%12.5f" % y1_dst 
#        print "%12.5f" % x2_dst 
#        print "%12.5f" % y2_dst 
#        print "%12.5f" % x3_dst 
#        print "%12.5f"  % y3_dst 

        ## Siehe Fineltra Manual Seiten 4-5
        x0_src = point.x()
        y0_src = point.y()

        P1 = math.fabs( 0.5 * ( x0_src*(y2_src-y3_src) + x2_src*(y3_src-y0_src) + x3_src*(y0_src - y2_src) ) )
        P2 = math.fabs( 0.5 * ( x0_src*(y1_src-y3_src) + x1_src*(y3_src-y0_src) + x3_src*(y0_src - y1_src) ) )                
        P3 = math.fabs( 0.5 * ( x0_src*(y1_src-y2_src) + x1_src*(y2_src-y0_src) + x2_src*(y0_src - y1_src) ) )

#        print "P1: " + str(P1*1000)
#        print "P2: " + str(P2*1000)
#        print "P3: " + str(P3*1000)

        ## vxi und vyi berechnen.
        vx1 = x1_dst - x1_src
        vy1 = y1_dst - y1_src
        vx2 = x2_dst - x2_src
        vy2 = y2_dst - y2_src
        vx3 = x3_dst - x3_src
        vy3 = y3_dst - y3_src        
        
#        print "vx1: " + str(vx1)
#        print "vy1: " + str(vy1)
#        print "vx2: " + str(vx2)
#        print "vy2: " + str(vy2)
#        print "vx3: " + str(vx3)
#        print "vy3: " + str(vy3)

        ## Interpolationsverbesserungen.
        DX = (vx1*P1 + vx2*P2 + vx3*P3) / ( P1 + P2 + P3 )
        DY = (vy1*P1 + vy2*P2 + vy3*P3) / ( P1 + P2 + P3 )
                        
        ## Definitive Koordinaten.
        x0_dst = x0_src + DX
        y0_dst = y0_src + DY
   
        return QgsPoint(x0_dst,  y0_dst)       
