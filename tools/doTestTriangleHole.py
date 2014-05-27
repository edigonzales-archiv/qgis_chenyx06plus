 # -*- coding: utf8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtXml
from qgis.core import *
from qgis.gui import *

from dbTools import DbObj
import utils

class TestTriangleHole( QObject ):
    
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
            self.dbobj = DbObj("default", "pg", self.host, self.port, self.database, self.admin, self.adminpassword)
            self.connected = self.dbobj.connect()
            
        if self.connected == False:
            QMessageBox.warning( None, "", "Could not connect to database.")
            return

        srs = iface.mapCanvas().mapRenderer().destinationCrs().authid()
        #Fehler in QGIS 1.8?
        srs = "EPSG:21781"
        if srs == "EPSG:21781" or srs == "EPSG:2056":
            pass
        else:
            QMessageBox.warning( None, "", "Wrong CRS: " + srs + "<br>Should be EPSG:21781 or EPSG:2056")
            return
            
            
        query = "BEGIN; "
        query += "DELETE FROM " + self.schema + ".triangle_hole_lv03; "
        query += "INSERT INTO " + self.schema + ".triangle_hole_lv03 (error_type, the_geom) SELECT 'hole':: varchar, ST_Multi(geom) as the_geom FROM ( SELECT (ST_Dump(ST_SymDifference(a.the_geom, b.the_geom))).geom FROM ( SELECT ST_Union(the_geom) as the_geom FROM "+self.schema+".dreiecke_lv03_bearbeitung ) as a, ( SELECT ST_BuildArea(ST_ExteriorRing(ST_Union(the_geom))) as the_geom FROM "+self.schema+".dreiecke_lv03_bearbeitung ) as b ) as a; "
        query += "COMMIT; "
        print query
        
        QApplication.setOverrideCursor(Qt.WaitCursor)                        
        try:
            result = self.dbobj.runError( query )
        except:
            QApplication.restoreOverrideCursor()

        QApplication.restoreOverrideCursor()

        print "****"
        print result
        print "****"

        if str(result).strip() != "":
            QMessageBox.critical( None, "", "Database error: <br>" + result)
            return

        table = {}
        table["type"] = "pg"        
        table["title"] = u"Löcher in Dreiecksvermaschung"
        table["schema"] = self.schema
        table["table"] = "triangle_hole_lv03"
        table["geom"] = "the_geom"
        table["key"] = "ogc_fid"            
        table["sql"] = ""
        table["group"] = ""
        table["style"] = "dreiecke/holes.qml"
        vlayerTriangleHoles = utils.doShowSimpleLayer( iface, table, False, True )

            
            


