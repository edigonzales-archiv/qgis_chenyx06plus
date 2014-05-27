 # -*- coding: utf8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtXml
from qgis.core import *
from qgis.gui import *

import utils

class LoadChenyx06( QObject ):
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

        if self.host == "" or self.database == "" or self.port == "" or self.schema == "" or self.user == "" or self.userpassword == "" or self.admin == "" or self.adminpassword == "":
            QMessageBox.warning( None, "", "No database parameters set.")
            return
            
        # Ok, at the moment only 21781 is supported for working....
        # It gets trickier with the triggers. It would be possible but 
        # we can mess up everthing. Another approach would be to 
        # have every table for every crs.
        srs = iface.mapCanvas().mapRenderer().destinationCrs().description()
        # QGIS 1.8 liefert mir immer ein nicht-valides CRS zurück.
        # Workaround: manuell auf EPSG:21781 setzen. Spielt glaubs keine Rolle, 
        # da wir nur noch in diesem Rahmen arbeiten.
        print "****"
        print srs
        srs = "EPSG:21781"

#        if srs == "EPSG:21781" or srs == "EPSG:2056":
        if srs == "EPSG:21781":
            pass
        else:
#            QMessageBox.warning( None, "", "Wrong CRS: " + srs + "<br>Should be EPSG:21781 or EPSG:2056")
            QMessageBox.warning( None, "", "Wrong CRS: " + srs + "<br>Should be EPSG:21781.")
            return
            
            
        if srs == "EPSG:2056":
            referenceframe = "lv95"
        else:
            referenceframe = "lv03"
            
        
        group = "CHENyx06+ "+ "(" + str(self.schema) + " / "+srs+")"        
    
        table = {}
        table["type"] = "pg"        
        table["title"] = "Dreiecksvermaschung (Bearbeitung)"
        table["schema"] = self.schema
        table["table"] = "dreiecke_"+referenceframe+"_bearbeitung"
        table["geom"] = "the_geom"
        table["key"] = "ogc_fid"            
        table["sql"] = ""
        table["group"] = group
        table["style"] = "dreiecke/dreiecke.qml"
        vlayerDreieckeLV03 = utils.doShowSimpleLayer( iface, table, False, True, False, True, True )
        vlayerDreieckeLV03.setEditType(0, QgsVectorLayer.Hidden)

        table = {}
        table["type"] = "pg"        
        table["title"] = "TSP"
        table["schema"] = self.schema
        table["table"] = "tsp_"+referenceframe
        table["geom"] = "the_geom"
        table["key"] = "ogc_fid"            
        table["sql"] = ""
        table["group"] = group
        table["style"] = "tsp/tsp.qml"
        vlayerTSPLV03 = utils.doShowSimpleLayer( iface, table, False, True, True, True, True )
        vlayerTSPLV03.setEditType(0, QgsVectorLayer.Hidden)

#def doShowSimpleLayer( iface, layer, defaultSql,  settings,  isVisible=False,  zoomToExtent=False, showLegend=True, addMapLayer=True ):
#def doShowSimpleLayer( iface, layer, defaultSql, isVisible=False,  zoomToExtent=False, showLegend=True, admin=False  ):


#        table = {}
#        table["type"] = "pg"        
#        table["title"] = "Parcelling boundary points"
#        table["schema"] = "public"
#        table["table"] = "mutations_parcelling_boundary_points"
#        table["geom"] = "the_geom"
#        table["key"] = "ogc_fid"            
#        table["sql"] = ""
#        table["group"] = group
#        table["style"] = "mutation/parzellierung_grenzpunkte.qml"
#        vlayerParzellierungGrenzpunkte = utils.doShowSimpleLayer( iface, table, True, True, False)
