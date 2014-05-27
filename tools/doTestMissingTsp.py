from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtXml
from qgis.core import *
from qgis.gui import *

from dbTools import DbObj
import utils

class TestMissingTsp( QObject ):
    
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
        


    def run( self, iface ):

        if self.host == "" or self.database == "" or self.port == "" or self.schema == "" or self.admin == "" or self.adminpassword == "":
            QMessageBox.warning( None, "", "No database parameter set.")
            return
        else:
            self.dbobj = DbObj("default", "pg",  self.host,  self.port,  self.database,  self.admin,  self.adminpassword)
            self.connected = self.dbobj.connect()

        srs = iface.mapCanvas().mapRenderer().destinationCrs().authid()
        # Fehler in QGIS 1.8??
        srs = "EPSG:21781" 
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
                    
        table = {}
        table["type"] = "pg"        
        table["title"] = "Fehlende TSP (LV95)"
        table["schema"] = self.schema
        table["table"] = "missing_tsp_lv95_in_lv03_v"
        table["geom"] = "the_geom"
        table["key"] = "ogc_fid"            
        table["sql"] = ""
        table["group"] = ""
        table["style"] = "tsp/tsp_missing.qml"
        vlayerMissingTspLv95 = utils.doShowSimpleLayer( iface, table, False, False, False, True, False )

        
        table = {}
        table["type"] = "pg"        
        table["title"] = "Fehlende TSP (LV03)"
        table["schema"] = self.schema
        table["table"] = "missing_tsp_lv03_in_lv95_v"
        table["geom"] = "the_geom"
        table["key"] = "ogc_fid"            
        table["sql"] = ""
        table["group"] = ""
        table["style"] = "tsp/tsp_missing.qml"
        vlayerMissingTspLv03 = utils.doShowSimpleLayer( iface, table, False, False, False, True, False )

            

