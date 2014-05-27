# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtXml
from qgis.core import *
from qgis.gui import *
import os

from dbTools import DbObj
import utils

class ExportFineltra( QObject ):
    
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


    def run( self ):

        if self.host == "" or self.database == "" or self.port == "" or self.schema == "" or self.admin == "" or self.adminpassword == "":
            QMessageBox.warning( None, "CHENyx06+", "No database parameter set.")
            return

        if self.tempdir == "":
            QMessageBox.warning( None, "CHENyx06+", "No output directory set.")
            return
            
            
        linesTriangles = []
        linesPoints03 = []
        linesPoints95 =[]
        
        # Dreiecksdefinition
        QApplication.setOverrideCursor(Qt.WaitCursor)
        table = "dreiecke_tsp"
        uri = QgsDataSourceURI()
        uri = QgsDataSourceURI("dbname='"+self.database+"' host="+self.host+" port="+self.port+" user='"+self.user+"' password='"+self.userpassword+"' table=\""+self.schema+"\".\""+table+"\"")
        uri.setKeyColumn("ogc_fid")        
        tlayer = QgsVectorLayer(uri.uri(), table, "postgres")
        tlayer.select()        
                
        if not (tlayer.isValid()):
            QApplication.restoreOverrideCursor()     
            print "Layer failed to load!"
            QMessageBox.information(None, 'CHENyx06+', str("Error while loading table: " + table))   
            return

        tprovider = tlayer.dataProvider()
        tallAttrs = tprovider.attributeIndexes()
        tprovider.enableGeometrylessFeatures (True) 
        tprovider.select(tallAttrs, QgsRectangle(), False, False)

        dreieckNummerIdx = tprovider.fieldNameIndex("dreieck_nummer")
        tsp1Idx = tprovider.fieldNameIndex("tsp_nummer_1")
        tsp2Idx = tprovider.fieldNameIndex("tsp_nummer_2")
        tsp3Idx = tprovider.fieldNameIndex("tsp_nummer_3")

        if dreieckNummerIdx == -1:
            QApplication.restoreOverrideCursor()     
            QMessageBox.warning( None, "CHENyx06+", "Attribut (<i>dreieck_nummer</i>) in layer 'dreiecke_tsp' not found." )
            return

        if tsp1Idx == -1:
            QApplication.restoreOverrideCursor()     
            QMessageBox.warning( None, "CHENyx06+", "Attribut (<i>tsp_nummer_1</i>) in layer 'dreiecke_tsp' not found." )
            return

        if tsp2Idx == -1:
            QApplication.restoreOverrideCursor()     
            QMessageBox.warning( None, "CHENyx06+", "Attribut (<i>tsp_nummer_2</i>) in layer 'dreiecke_tsp' not found." )
            return
            
        if tsp3Idx == -1:
            QApplication.restoreOverrideCursor()     
            QMessageBox.warning( None, "CHENyx06+", "Attribut (<i>tsp_nummer_3</i>) in layer 'dreiecke_tsp' not found." )
            return            

        i = 0
        feat = QgsFeature()
        while tprovider.nextFeature(feat):   
            i = i + 1
            dreieckNummer =  feat.attributeMap()[dreieckNummerIdx].toString()
            tsp1 = feat.attributeMap()[tsp1Idx].toString()
            tsp2 = feat.attributeMap()[tsp2Idx].toString()
            tsp3 = feat.attributeMap()[tsp3Idx].toString()
            
            lineTriangle = str("%-7s") % (dreieckNummer)
            lineTriangle += str("%-15s") % tsp1
            lineTriangle += str("%-15s") % tsp2
            lineTriangle += str("%-25s") % tsp3
            lineTriangle += str("2525")                
            linesTriangles.append(lineTriangle)

        # LV03-TSP
        table = "tsp_on_dreiecke_lv03_v"
        uri = QgsDataSourceURI()
        uri = QgsDataSourceURI("dbname='"+self.database+"' host="+self.host+" port="+self.port+" user='"+self.user+"' password='"+self.userpassword+"' table=\""+self.schema+"\".\""+table+"\"")
        uri.setKeyColumn("ogc_fid")        
        p03layer = QgsVectorLayer(uri.uri(), table, "postgres")
        p03layer.select()        
                
        if not (p03layer.isValid()):
            QApplication.restoreOverrideCursor()     
            print "Layer failed to load!"
            QMessageBox.information(None, 'CHENyx06+', str("Error while loading table: " + table))   
            return

        p03provider = p03layer.dataProvider()
        p03allAttrs = p03provider.attributeIndexes()
        p03provider.enableGeometrylessFeatures (True) 
        p03provider.select(p03allAttrs, QgsRectangle(), False, False)

        nummerIdx = p03provider.fieldNameIndex("nummer")
        ycoordIdx = p03provider.fieldNameIndex("ycoord")
        xcoordIdx = p03provider.fieldNameIndex("xcoord")

        if nummerIdx == -1:
            QApplication.restoreOverrideCursor()     
            QMessageBox.warning( None, "CHENyx06+", "Attribut (<i>nummer</i>) in layer '"+table+"' not found." )
            return
            
        if ycoordIdx == -1:
            QApplication.restoreOverrideCursor()     
            QMessageBox.warning( None, "CHENyx06+", "Attribut (<i>ycoordIdx</i>) in layer '"+table+"' not found." )
            return

        if xcoordIdx == -1:
            QApplication.restoreOverrideCursor()     
            QMessageBox.warning( None, "CHENyx06+", "Attribut (<i>xcoordIdx</i>) in layer '"+table+"' not found." )
            return

        i = 0
        feat = QgsFeature()
        while p03provider.nextFeature(feat):   
            i = i + 1
            nummer = feat.attributeMap()[nummerIdx].toString()
            ycoord = feat.attributeMap()[ycoordIdx].toString()
            xcoord = feat.attributeMap()[xcoordIdx].toString()
            
            linePoint03 = str("%-16s") % nummer
            linePoint03 += str("%-12.3f") % float(ycoord)
            linePoint03 += str("%10.3f") % float(xcoord)
            linesPoints03.append(linePoint03)
            
        # LV95-TSP
        table = "tsp_on_dreiecke_lv95_v"
        uri = QgsDataSourceURI()
        uri = QgsDataSourceURI("dbname='"+self.database+"' host="+self.host+" port="+self.port+" user='"+self.user+"' password='"+self.userpassword+"' table=\""+self.schema+"\".\""+table+"\"")
        uri.setKeyColumn("ogc_fid")        
        p95layer = QgsVectorLayer(uri.uri(), table, "postgres")
        p95layer.select()        
                
        if not (p95layer.isValid()):
            QApplication.restoreOverrideCursor()     
            print "Layer failed to load!"
            QMessageBox.information(None, 'CHENyx06+', str("Error while loading table: " + table))   
            return

        p95provider = p95layer.dataProvider()
        p95allAttrs = p95provider.attributeIndexes()
        p95provider.enableGeometrylessFeatures (True) 
        p95provider.select(p95allAttrs, QgsRectangle(), False, False)

        nummerIdx = p95provider.fieldNameIndex("nummer")
        ycoordIdx = p95provider.fieldNameIndex("ycoord")
        xcoordIdx = p95provider.fieldNameIndex("xcoord")

        if nummerIdx == -1:
            QApplication.restoreOverrideCursor()            
            QMessageBox.warning( None, "CHENyx06+", "Attribut (<i>nummer</i>) in layer '"+table+"' not found." )
            return
            
        if ycoordIdx == -1:
            QApplication.restoreOverrideCursor()     
            QMessageBox.warning( None, "CHENyx06+", "Attribut (<i>ycoordIdx</i>) in layer '"+table+"' not found." )
            return

        if xcoordIdx == -1:
            QApplication.restoreOverrideCursor()     
            QMessageBox.warning( None, "CHENyx06+", "Attribut (<i>xcoordIdx</i>) in layer '"+table+"' not found." )
            return

        i = 0
        feat = QgsFeature()
        while p95provider.nextFeature(feat):   
            i = i + 1
            nummer = feat.attributeMap()[nummerIdx].toString()
            ycoord = feat.attributeMap()[ycoordIdx].toString()
            xcoord = feat.attributeMap()[xcoordIdx].toString()
            
            linePoint95 = str("%-15s") % nummer
            linePoint95 += str("%-12.4f") % float(ycoord)
            linePoint95 += str("%10.4f") % float(xcoord)
            linesPoints95.append(linePoint95)


        # Write everything into the file.
        time = QDateTime.currentDateTime()
        fileSuffix = str(time.toString(Qt.ISODate)).replace(":", "").replace("-", "")
        filePath = os.path.join(str(self.tempdir), str("fineltra") + str("_") + fileSuffix + str(".dat"))

        try:
            fh = open(filePath, "w")
            fh.write("Kanton Bern / Amt fuer Geoinformation - Amtliche Vermessung\n")
            fh.write("Arbeitsdatei fuer die Koordinatentransformation\n")
            fh.write("Dreiecksvermaschungsdefinition fuer: " + self.schema + "\n")
        
            for i in range(len(linesTriangles)):
                fh.write(linesTriangles[i])
                fh.write("\n")
                
            fh.write("-999\n")
            fh.write("$$PK LV03-Koordinaten\n")
            
            for i in range(len(linesPoints03)):
                fh.write(linesPoints03[i])
                fh.write("\n")

            fh.write("-999\n")
            fh.write("$$PK LV95-Koordinaten\n")
            
            for i in range(len(linesPoints95)):
                fh.write(linesPoints95[i])
                fh.write("\n")            
            
        except IOError as detail:
            QApplication.restoreOverrideCursor()            
            QMessageBox.warning( None, "CHENyx06+", "Cannot open file.")
            print "CHENyx06+: IOError Exception."
            print str(detail)
        else:
            fh.close()
            QApplication.restoreOverrideCursor()
            
            count03 = p03layer.featureCount()
            count95 = p95layer.featureCount()
            if (count03 != count95):
                info = "<br><br>But something went wrong: <br>Number of LV03-Points: " + str(count03) + "<br>Number of LV95-Points: " + str(count95) 
            else: 
                info = ""
            
            QMessageBox.information( None, "CHENyx06+", "Fineltra file written:<br><br><i>" + filePath + "</i>" + info)


#        QApplication.setOverrideCursor(Qt.WaitCursor)
#        try:
#            # Get the triangle definition.
#            resultTriangles = self.dbobj.read( "SELECT * FROM "+self.schema+".dreiecke_tsp")
#            if len(resultTriangles['OGC_FID']) % 3 != 0:
#                QMessageBox.warning( None, "CHENyx06+", "Ups, Number of points not divisble by three.")
#                return
#            
#            for i in range(len(resultTriangles['OGC_FID'])/3):
#                lineTriangle = str("%-7s") % (i+1)
#                lineTriangle += str("%-15s") % resultTriangles['TSP_NUMMER'][i*3]
#                lineTriangle += str("%-15s") % resultTriangles['TSP_NUMMER'][i*3+1]
#                lineTriangle += str("%-25s") % resultTriangles['TSP_NUMMER'][i*3+2]
#                lineTriangle += str("2525")                
#                linesTriangles.append(lineTriangle)
#                
#            # Get LV03-Coords.
#            # Komisch: SELECT DISTINCT auf Geometrien macht bei LV95 Probleme, dh. es fehlen 10 Punkte?!?.
#            # -> Query geändert (wird aber langsamer), DISTINCT erst am Ende auf Nummer.
#            # Immerhin könnte man so wahrscheinlich noch ne Toleranz einbauen, da jetzt über Distance 
#            # zugeordnet wird.
#            query = """SELECT DISTINCT ON (nummer) ogc_fid, nummer, round(ST_X(the_geom)::numeric, 3) as ycoord, round(ST_Y(the_geom)::numeric, 3) as xcoord
#FROM
#(
# SELECT 1 as ogc_fid, a.nummer, a.the_geom
# FROM """+self.schema+""".tsp_lv03 as a,
# (
#    SELECT (ST_DumpPoints(the_geom_lv03)).geom as the_geom
#    FROM """+self.schema+""".dreiecke
# ) as b
# WHERE a.the_geom && b.the_geom
# AND ST_Distance(ST_SnapToGrid(b.the_geom, 0.001), ST_SnapToGrid(a.the_geom, 0.001)) = 0
#) as c
#WHERE geometrytype(the_geom) = 'POINT'
#"""
#            
#            resultPoints03 = self.dbobj.read(query)
#
#            for i in range(len(resultPoints03['OGC_FID'])):
#                linePoint03 = str("%-16s") % resultPoints03['NUMMER'][i]
#                linePoint03 += str("%-12.3f") % float(resultPoints03['YCOORD'][i])
#                linePoint03 += str("%10.3f") % float(resultPoints03['XCOORD'][i])
#                linesPoints03.append(linePoint03)
#
#            # Get LV95-Coords.
#            query = """SELECT DISTINCT ON (nummer) ogc_fid, nummer, round(ST_X(the_geom)::numeric, 3) as ycoord, round(ST_Y(the_geom)::numeric, 3) as xcoord
#FROM
#(
# SELECT 1 as ogc_fid, a.nummer, a.the_geom
# FROM """+self.schema+""".tsp_lv95 as a,
# (
#    SELECT (ST_DumpPoints(the_geom_lv95)).geom as the_geom
#    FROM """+self.schema+""".dreiecke
# ) as b
# WHERE a.the_geom && b.the_geom
# AND ST_Distance(ST_SnapToGrid(b.the_geom, 0.001), ST_SnapToGrid(a.the_geom, 0.001)) = 0
#) as c
#WHERE geometrytype(the_geom) = 'POINT'
#"""
#            
#            resultPoints95 = self.dbobj.read(query)
#
#            for i in range(len(resultPoints95['OGC_FID'])):
#                linePoint95 = str("%-15s") % resultPoints95['NUMMER'][i]
#                linePoint95 += str("%-12.3f") % float(resultPoints95['YCOORD'][i])
#                linePoint95 += str("%-12.3f") % float(resultPoints95['XCOORD'][i])
#                linesPoints95.append(linePoint95)
#                
#        except KeyError as detail:
#            QApplication.restoreOverrideCursor()            
#            QMessageBox.warning( None, "CHENyx06+", "Database: KeyError Exception.")
#            print "Database: KeyError Exception."
#            print str(detail)
#            return 
#
#        # Write everything into the file.
#        time = QDateTime.currentDateTime()
#        fileSuffix = str(time.toString(Qt.ISODate)).replace(":", "").replace("-", "")
#        filePath = os.path.join(str(self.tempdir), str("fineltra") + str("_") + fileSuffix + str(".dat"))
#
#        try:
#            fh = open(filePath, "w")
#            fh.write("Kanton Solothurn / Amt fuer Geoinformation - Amtliche Vermessung\n")
#            fh.write("Arbeitsdatei fuer die Koordinatentransformation\n")
#            fh.write("Dreiecksvermaschungsdefinition fuer: " + self.schema + "\n")
#        
#            for i in range(len(linesTriangles)):
#                fh.write(linesTriangles[i])
#                fh.write("\n")
#                
#            fh.write("-999\n")
#            fh.write("$$PK LV03-Koordinaten\n")
#            
#            for i in range(len(linesPoints03)):
#                fh.write(linesPoints03[i])
#                fh.write("\n")
#
#            fh.write("-999\n")
#            fh.write("$$PK LV95-Koordinaten\n")
#            
#            for i in range(len(linesPoints95)):
#                fh.write(linesPoints95[i])
#                fh.write("\n")            
#            
#        except IOError as detail:
#            QApplication.restoreOverrideCursor()            
#            QMessageBox.warning( None, "CHENyx06+", "Cannot open file.")
#            print "CHENyx06+: IOError Exception."
#            print str(detail)
#        else:
#            fh.close()
#            QApplication.restoreOverrideCursor()
#            
#            count03 = len(resultPoints03['OGC_FID'])
#            count95 = len(resultPoints95['OGC_FID'])
#            if (count03 != count95):
#                info = "<br><br>But something went wrong: <br>Number of LV03-Points: " + str(count03) + "<br>Number of LV95-Points: " + str(count95) 
#            else: 
#                info = ""
#            
#            QMessageBox.warning( None, "CHENyx06+", "Fineltra file written:<br><br><i>" + filePath + "</i>" + info)

