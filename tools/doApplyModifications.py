# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtXml
from qgis.core import *
from qgis.gui import *

from dbTools import DbObj
import utils

class ApplyModifications( QObject ):
    
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
        
        self.connected = False


    def run( self, iface ):

        if self.host == "" or self.database == "" or self.port == "" or self.schema == "" or self.admin == "" or self.adminpassword == "":
            QMessageBox.warning( None, "", "No database parameter set.")
            return
        else:
            self.dbobj = DbObj("default", "pg",  self.host,  self.port,  self.database,  self.admin,  self.adminpassword)
            self.connected = self.dbobj.connect()

        srs = iface.mapCanvas().mapRenderer().destinationCrs().authid()
        if srs == "EPSG:21781" or srs == "EPSG:2056":
            pass
        else:
            QMessageBox.warning( None, "", "Wrong CRS: " + srs + "<br>Should be EPSG:21781 or EPSG:2056")
            return
            
        if srs == "EPSG:2056":
            referenceFrame = "lv95"
            deleteReferenceFrame = "lv03"
        else:
            referenceFrame = "lv03"
            deleteReferenceFrame = "lv95"
            
        if self.connected == True:
            query = "BEGIN; "
            query += "DELETE FROM " + self.schema + ".dreiecke_" + deleteReferenceFrame + "_bearbeitung; "            
            query += "DELETE FROM " + self.schema + ".dreiecke_tsp; "
            query += "DELETE FROM " + self.schema + ".dreiecke; "            
#            query += """INSERT INTO """ + self.schema + """.dreiecke_tsp (tsp_nummer, dreieck_nummer) 
#SELECT tsp_nummer, dreieck_nummer
#FROM
#(
# SELECT a.nummer as tsp_nummer, b.nummer as dreieck_nummer, ST_Intersection(ST_SnapToGrid(b.the_geom, 0.001), ST_SnapToGrid(a.the_geom, 0.001)) as the_geom
# FROM """+self.schema+""".tsp_"""+referenceFrame+""" as a,
# (
#   SELECT nummer, (ST_DumpPoints(the_geom)).geom as the_geom
#   FROM
#   (
#     SELECT nummer, ST_RemovePoint(ST_Boundary(ST_Reverse(ST_ForceRHR(the_geom))),3) as the_geom FROM """+self.schema+""".dreiecke_"""+referenceFrame+"""_bearbeitung ORDER BY nummer 
#   ) as c
# ) as b
# WHERE a.the_geom && b.the_geom
#) as d;"""
            
            query += """INSERT INTO """ + self.schema + """.dreiecke_tsp (tsp_nummer, dreieck_nummer) 
SELECT tsp_nummer, dreieck_nummer
FROM
(
 SELECT a.nummer as tsp_nummer, b.nummer as dreieck_nummer
 FROM """+self.schema+""".tsp_"""+referenceFrame+""" as a,
 (
   SELECT nummer, (ST_DumpPoints(the_geom)).geom as the_geom
   FROM
   (
     SELECT nummer, ST_RemovePoint(ST_Boundary(ST_Reverse(ST_ForceRHR(the_geom))),3) as the_geom 
     FROM """+self.schema+""".dreiecke_"""+referenceFrame+"""_bearbeitung  ORDER BY nummer 
   ) as c
 ) as b
 WHERE a.the_geom && b.the_geom
 AND ST_Intersects(ST_SnapToGrid(a.the_geom, 0.001), ST_SnapToGrid(b.the_geom, 0.001)) 
) as d;"""
            
            
            query += """INSERT INTO """ + self.schema + """.dreiecke_""" + deleteReferenceFrame + """_bearbeitung (nummer, typ, the_geom) 
SELECT dreieck_nummer, typ, ST_Reverse(ST_ForceRHR(ST_BuildArea(the_geom))) as the_geom 
FROM
(
 SELECT dreieck_nummer, typ, ST_AddPoint(the_geom, ST_PointN(the_geom,1)) as the_geom
 FROM
 (
  SELECT dreieck_nummer, typ, ST_LineFromMultiPoint(ST_Collect(the_geom)) as the_geom
  FROM
  (
   SELECT dreieck_nummer, typ, the_geom as the_geom
   FROM """ + self.schema + """.tsp_""" + deleteReferenceFrame + """ as a,
   ( 
    SELECT *
    FROM """ + self.schema + """.dreiecke_tsp
   ) as b
   WHERE b.tsp_nummer = a.nummer
  ) as c
  GROUP BY dreieck_nummer, typ
 ) as d
) as e
ORDER BY dreieck_nummer; """            
            
            query += """INSERT INTO """+self.schema+""".dreiecke (nummer, typ, the_geom_lv03, the_geom_lv95)

SELECT a.dreieck_nummer as nummer, a.typ, ST_SnapToGrid(a.the_geom, 0.001) as the_geom_lv03, ST_SnapToGrid(b.the_geom, 0.001) as the_geom_lv95
FROM
(
 SELECT dreieck_nummer, typ, ST_Reverse(ST_ForceRHR(ST_BuildArea(the_geom))) as the_geom 
 FROM
 (
  SELECT dreieck_nummer, typ, ST_AddPoint(the_geom, ST_PointN(the_geom,1)) as the_geom
  FROM
  (
   SELECT dreieck_nummer, typ, ST_LineFromMultiPoint(ST_Collect(the_geom)) as the_geom
   FROM
   (
    SELECT dreieck_nummer, typ, the_geom as the_geom
    FROM """+self.schema+""".tsp_lv03 as a,
    (
     SELECT *
     FROM """+self.schema+""".dreiecke_tsp
    ) as b
    WHERE b.tsp_nummer = a.nummer
   ) as c
   GROUP BY dreieck_nummer, typ
  ) as d
 ) as e
) as a,
(
 SELECT dreieck_nummer, typ, ST_Reverse(ST_ForceRHR(ST_BuildArea(the_geom))) as the_geom 
 FROM
 (
  SELECT dreieck_nummer, typ, ST_AddPoint(the_geom, ST_PointN(the_geom,1)) as the_geom
  FROM
  (
   SELECT dreieck_nummer, typ, ST_LineFromMultiPoint(ST_Collect(the_geom)) as the_geom
   FROM
   (
    SELECT dreieck_nummer, typ, the_geom as the_geom
    FROM """+self.schema+""".tsp_lv95 as a,
    (
     SELECT *
     FROM """+self.schema+""".dreiecke_tsp
    ) as b
    WHERE b.tsp_nummer = a.nummer
   ) as c
   GROUP BY dreieck_nummer, typ
  ) as d
 ) as e
) as b
WHERE a.dreieck_nummer = b.dreieck_nummer
ORDER BY a.dreieck_nummer;"""

            query += "COMMIT; "
            print query
            
            QApplication.setOverrideCursor(Qt.WaitCursor)
            result = self.dbobj.runError( query )
            QApplication.restoreOverrideCursor()

            if str(result).strip() != "":
                QMessageBox.critical( None, "CHENyx06+", "Modifications NOT applied. Database error: <br>" + result)
                
            else:
                
                countDreiecke = 0
                countDreieckeLV03 = 0
                countDreieckeLV95 = 0

                result1 = self.dbobj.read( "SELECT count(*) FROM "+ self.schema + ".dreiecke" )
                result2 = self.dbobj.read( "SELECT count(*) FROM "+ self.schema + ".dreiecke_lv03_bearbeitung" )
                result3 = self.dbobj.read( "SELECT count(*) FROM "+ self.schema + ".dreiecke_lv95_bearbeitung" )                
                try:
                    countDreiecke = result1['COUNT'][0]
                    countDreieckeLV03 = result2['COUNT'][0]
                    countDreieckeLV95 = result3['COUNT'][0]
                    
                except KeyError:
                    QMessageBox.warning( None, "", "Database: KeyError Exception.")
                    print "Database: KeyError Exception."
                    return None


                QMessageBox.information( None, "CHENyx06+", "Modifications applied. <br><br> Number of triangles in tables:<table><tr><td><i>dreiecke</i></td><td>&nbsp;&nbsp;&nbsp;</td><td><b>"+countDreiecke+"</b></td></tr><tr><td><i>dreiecke_lv03_bearbeitung</i></td><td>&nbsp;&nbsp;&nbsp;</td><td><b>"+countDreieckeLV03+"</b></td></tr><tr><td><i>dreiecke_lv95_bearbeitung</i></td><td>&nbsp;&nbsp;&nbsp;</td><td><b>"+countDreieckeLV95+"</b></td></tr></table>")
