# -*- coding: latin1 -*-
"""
/***************************************************************************
Name                 : Chenyx06plus
Description          : ....
Date                 : 2011-05-30
copyright            : (C) 2011 by Stefan Ziegler
email                : stefan.ziegler@bd.so.ch
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries.
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtXml
from qgis.core import *
from qgis.gui import *

#import os, time, shutil
#import xlwt as pycel

#from tools.dbTools import DbObj
import tools.utils


class Chenyx06plus:
    
    def __init__( self, iface, version ):
        self.iface = iface
        self.version = version
        
        # Do some initialisation work.
        srs = QgsCoordinateReferenceSystem()
        srs.createFromSrsId(21781)
        self.canvas = self.iface.mapCanvas()
        self.canvas.setMapUnits(QGis.Meters)
        self.rect = self.canvas.extent()
        mapRender = self.canvas.mapRenderer()
        mapRender.setMapUnits(QGis.Meters)
        mapRender.setDestinationCrs(srs)
        mapRender.setProjectionsEnabled(0)
        QgsProject.instance().writeEntry("MapCanvas","/Units",QString("meters"))
        QgsProject.instance().writeEntry("SpatialRefSys","/ProjectCRSProj4String",srs.toProj4())
#        QgsProject.instance().writeEntry("Digitizing","/TopologicalEditing",1);
#        QgsProject.instance().writeEntry("Digitizing","/AvoidPolygonIntersections",1);
        self.canvas.refresh()
        
        
    def initGui(self):

        self.menu = QMenu()
        self.menu.setTitle( QCoreApplication.translate( "chenyx06+", "CHENyx06+" ) )
        
        self.loadChenyx06 = QAction( QCoreApplication.translate("chenyx06+", "Load CHENyx06 data" ), self.iface.mainWindow() )
        self.changeSettings = QAction( QCoreApplication.translate("chenyx06+", "Settings" ), self.iface.mainWindow() )            
        self.about = QAction( QCoreApplication.translate("chenyx06+", "About" ), self.iface.mainWindow() )
    
        self.transformMenu = QMenu( QCoreApplication.translate( "chenyx06+", "Transform data..." ) )
        self.transformRegular = QAction( QCoreApplication.translate("chenyx06+", "with regular CHENyx06" ), self.iface.mainWindow() )            
        self.transformModified = QAction( QCoreApplication.translate("chenyx06+", "with modified CHENyx06" ), self.iface.mainWindow() )            
        self.transformMenu.addAction( self.transformModified )
        self.transformMenu.addAction( self.transformRegular )
        
        self.compareCoordsMenu = QMenu( QCoreApplication.translate( "chenyx06+", "Compare coordinates..." ) )
        self.compareCoordsById = QAction( QCoreApplication.translate("chenyx06+", "by identifier" ), self.iface.mainWindow() )   
        self.compareCoordsByLocation = QAction( QCoreApplication.translate("chenyx06+", "by location" ), self.iface.mainWindow() )   
        self.compareCoordsMenu.addAction( self.compareCoordsById )
        self.compareCoordsMenu.addAction( self.compareCoordsByLocation )

        self.importMenu = QMenu( QCoreApplication.translate( "chenyx06+", "Import" ) )
        self.importCopyLv03TspData = QAction( QCoreApplication.translate("chenyx06+", "Copy data into LV03-TSP" ), self.iface.mainWindow() )            
        self.importCopyLv95TspData = QAction( QCoreApplication.translate("chenyx06+", "Copy data into LV95-TSP" ), self.iface.mainWindow() )            
        self.importMenu.addAction( self.importCopyLv03TspData )
        self.importMenu.addAction( self.importCopyLv95TspData )
        
        self.exportMenu = QMenu( QCoreApplication.translate( "chenyx06+", "Export" ) )
        self.exportFineltra = QAction( QCoreApplication.translate("chenyx06+", "Export CHENyx06" ), self.iface.mainWindow() )        
        self.exportGridPlot = QAction( QCoreApplication.translate("chenyx06+", "Export regular grid plot" ), self.iface.mainWindow() )        
        self.exportMenu.addAction( self.exportFineltra )
        self.exportMenu.addAction( self.exportGridPlot )        

        self.testsMenu = QMenu( QCoreApplication.translate( "chenyx06+", "Tests" ) )
        self.testMissingTsp = QAction( QCoreApplication.translate("chenyx06+", "Missing TSP" ), self.iface.mainWindow() )            
        self.testTriangleOverlap = QAction( QCoreApplication.translate("chenyx06+", "Triangle overlaps" ), self.iface.mainWindow() )            
        self.testTriangleHoles = QAction( QCoreApplication.translate("chenyx06+", "Triangle holes" ), self.iface.mainWindow() )            
        self.testsMenu.addAction( self.testMissingTsp )       
        self.testsMenu.addAction( self.testTriangleOverlap )        
        self.testsMenu.addAction( self.testTriangleHoles )

        self.baseLayersMenu = QMenu( QCoreApplication.translate( "chenyx06+", "Load baselayer" ) )
        baselayers = tools.utils.getBaselayers()
        for baselayer in baselayers:
            action = QAction( QCoreApplication.translate("chenyx06+", baselayer["title"] ), self.iface.mainWindow() )
            self.baseLayersMenu.addAction( action  )
            QObject.connect( action, SIGNAL( "triggered()" ), lambda layer=baselayer: self.doShowBaseLayer(layer) )        

        self.menu.addAction( self.loadChenyx06 )
        self.menu.addMenu( self.transformMenu )
        self.menu.addMenu( self.compareCoordsMenu )
        self.menu.addSeparator()
        self.menu.addMenu( self.importMenu )
        self.menu.addMenu( self.exportMenu )        
        self.menu.addSeparator()
        self.menu.addMenu( self.testsMenu )
        self.menu.addSeparator()
        self.menu.addMenu( self.baseLayersMenu )
        self.menu.addSeparator()      
        self.menu.addAction( self.changeSettings )
        self.menu.addSeparator()
        self.menu.addAction( self.about )        

        menu_bar = self.iface.mainWindow().menuBar()
        actions = menu_bar.actions()
        lastAction = actions[ len( actions ) - 1 ]
        menu_bar.insertMenu( lastAction, self.menu )
        
        QObject.connect( self.loadChenyx06, SIGNAL( "triggered()" ), self.doLoadChenyx06 )
        QObject.connect( self.transformRegular, SIGNAL( "triggered()" ), lambda type="regular": self.doTransformDataDialog(type) )
        QObject.connect( self.transformModified, SIGNAL( "triggered()" ), lambda type="modified": self.doTransformDataDialog(type) )  
        QObject.connect( self.compareCoordsById, SIGNAL( "triggered()" ), self.doCompareCoordsByIdDialog )    
        QObject.connect( self.compareCoordsByLocation, SIGNAL( "triggered()" ), self.doCompareCoordsByLocationDialog )    
        QObject.connect( self.importCopyLv03TspData, SIGNAL( "triggered()" ), lambda type="lv03": self.doCopyTspDataDialog(type) )          
        QObject.connect( self.importCopyLv95TspData, SIGNAL( "triggered()" ), lambda type="lv95": self.doCopyTspDataDialog(type) )          
        QObject.connect( self.exportFineltra, SIGNAL( "triggered()" ), self.doExportFineltra )    
        QObject.connect( self.exportGridPlot, SIGNAL( "triggered()" ), self.doExportGridPlotDialog )            
        QObject.connect( self.testMissingTsp, SIGNAL( "triggered()" ), self.doTestMissingTsp )        
        QObject.connect( self.testTriangleOverlap, SIGNAL( "triggered()" ), self.doTestTriangleOverlap )        
        QObject.connect( self.testTriangleHoles, SIGNAL( "triggered()" ), self.doTestTriangleHole )        
        QObject.connect( self.changeSettings, SIGNAL( "triggered()" ), self.doChangeSettings )
        QObject.connect( self.about, SIGNAL( "triggered()" ), self.doAbout )        
        
        
    def doLoadChenyx06(self):
        from tools.doLoadChenyx06 import LoadChenyx06
        d = LoadChenyx06()
        d.run(self.iface)


    def doShowBaseLayer( self,  layer ):
        settings = tools.utils.getSettings()
        if settings["host"] == "" or settings["database"] == "" or settings["port"] == "" or settings["schema"] == "" or settings["username"] == "" or settings["password"] == "":
            QMessageBox.warning( None, "CHENyx06+", "No database parameters set.")
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:           
            tools.utils.doShowSimpleLayer( self.iface, layer, False )        
        except:        
            QApplication.restoreOverrideCursor()
        QApplication.restoreOverrideCursor()


    def doApplyModifications(self):
        from tools.doApplyModifications import ApplyModifications
        d = ApplyModifications()
        d.run(self.iface)
        
    
    def doTransformDataDialog(self, type):
        from tools.doTransformDataDialog import TransformDataDialog
        d = TransformDataDialog(self.iface.mainWindow(), type)
        d.initGui()
        d.show()
        QObject.connect( d, SIGNAL( "okClickedTransformData(QString, bool, QString)" ), self.doTransformData )     


    def doTransformData(self, layerName, selectedOnly, type):
        from tools.doTransformData import TransformData
        d = TransformData()
        d.run(self.iface, layerName, selectedOnly, type)
        
    
    def doCompareCoordsByIdDialog(self):
        from tools.doCompareCoordsByIdDialog import CompareCoordsByIdDialog
        d = CompareCoordsByIdDialog(self.iface.mainWindow())
        d.initGui()
        d.show()
        QObject.connect( d, SIGNAL( "okClickedCopyCoordsById(QString, QString, QString, QString, bool)" ), self.doCompareCoordsById )
   

    def doCompareCoordsById(self, layerNameA, layerNameB, idA, idB, addLayerToMap):
        from tools.doCompareCoordsById import CompareCoordsById 
        d = CompareCoordsById()
        d.run(self.iface, layerNameA, layerNameB, idA, idB, addLayerToMap)


    def doCompareCoordsByLocationDialog(self):
        from tools.doCompareCoordsByLocationDialog import CompareCoordsByLocationDialog
        d = CompareCoordsByLocationDialog(self.iface.mainWindow())
        d.initGui()
        d.show()
        QObject.connect( d, SIGNAL( "okClickedCopyCoordsByLocation(QString, QString, QString, QString, double, bool)" ), self.doCompareCoordsByLocation )


    def doCompareCoordsByLocation(self, layerNameA, layerNameB, idA, idB, searchRadius, addLayerToMap):
        from tools.doCompareCoordsByLocation import CompareCoordsByLocation
        d = CompareCoordsByLocation()
        d.run(self.iface, layerNameA, layerNameB, idA, idB, searchRadius, addLayerToMap)


    def doCopyTspDataDialog(self, type):
        from tools.doCopyTspDataDialog import CopyTspDataDialog
        d = CopyTspDataDialog(self.iface.mainWindow(), type)
        result = d.initGui()
        if result != None:
            d.show()
        QObject.connect( d, SIGNAL( "okClickedCopyTspData(QString, QString, QString, QString, bool)" ), self.doCopyTspData )     


    def doCopyTspData(self, layerName, type, numberAttrName, typeAttrName, onlySelected):
        from tools.doCopyTspData import CopyTspData
        d = CopyTspData()
        d.run(self.iface, layerName, numberAttrName, typeAttrName, type,  onlySelected)


    def doExportGridPlotDialog(self):
        from tools.doExportGridPlotDialog import ExportGridPlotDialog
        d = ExportGridPlotDialog(self.iface.mainWindow())
        result = d.initGui()
        if result != None:
            d.show()
        QObject.connect( d, SIGNAL( "okClickedExportGridPlot(QString, bool, bool, bool, float, bool)" ), self.doExportGridPlot )     

    
    def doExportGridPlot(self, layerName, createTriangles, createCornerPoints, createGridPoints, gridPointDistance, addLayersToMap):
        print "layername"
        print layerName
        from tools.doExportGridPlot import ExportGridPlot
        d = ExportGridPlot()
        d.run(self.iface, layerName, createTriangles, createCornerPoints, createGridPoints, gridPointDistance, addLayersToMap)


    def doExportFineltra(self):
        from tools.doExportFineltra import ExportFineltra
        d = ExportFineltra()
        d.run()


    def doTestMissingTsp(self):
        from tools.doTestMissingTsp import TestMissingTsp
        d = TestMissingTsp()
        d.run(self.iface)
        
    
    def doTestTriangleOverlap(self):
        from tools.doTestTriangleOverlap import TestTriangleOverlap
        d = TestTriangleOverlap()
        d.run(self.iface)
        
        
    def doTestTriangleHole(self):
        from tools.doTestTriangleHole import TestTriangleHole
        d = TestTriangleHole()
        d.run(self.iface)        
        

    def doChangeSettings( self ):
        from tools.doChangeSettings import ChangeSettingsDialog
        d = ChangeSettingsDialog( self.iface.mainWindow() )
        d.initGui()
        d.show()
        
        
    def doAbout( self ):
        from tools.doAbout import AboutDialog
        d = AboutDialog( self.iface.mainWindow(),  self.version )
        d.show()                
        

    def unload(self):
        pass



    



        
