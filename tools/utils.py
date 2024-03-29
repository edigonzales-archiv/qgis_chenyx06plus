# -*- coding: utf8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtXml
from qgis.core import *
from qgis.gui import *

import time

def doShowSimpleLayer( iface, layer, defaultSql, isVisible=False, zoomToExtent=False, showLegend=True, admin=False, addMapLayer=True  ):
    """
    Lädt einen Layer (PostgreSQL, WMS, Raster) in QGIS.
    Zur Zeit noch kein Legenden-Gruppen Support.
    Argumente:
    layer:  Metainformation zum zu ladenden Layer (z.B. Typ, Style etc.) (Python Dictionary)
    defaultSql: Verwendung eines default SQL Strings (nur bei PostgreSQL sinnvoll) (Boolean)
    settings: Settings, z.B. Login und Passwort und Infos zum bearbeitenden Operat. (Python Dictionary)
    """
    settings = getSettings()

    if defaultSql == True:
        fosnr = settings["fosnr"]
        lotnr = settings["lotnr"]
        date = settings["date"]
    
    host = settings["host"]
    database = settings["database"]
    dbschema = settings["schema"]
    port =  settings["port"]
    
    username = settings["username"]
    password = settings["password"]    
    
    if admin == True:
        username = settings["admin"]
        password = settings["adminpassword"]    

    
    # Falls gar kein type vorhanden ist,
    # wird angenommen, dass es sich
    # um einen Postgis-Layer handelt.
    try: 
        layer["type"] == "pg"
    except:
        layer["type"]  = "pg"

    # Postgis-Layer hinzufuegen.
    if layer["type"] == "pg":
        title = layer["title"]
        schema = layer["schema"]
        table = layer["table"]
        geom = layer["geom"]
        sql = ""

        try:
            sql = layer["sql"]
            if sql <> "":
                if defaultSql == True:
                    sql = "(gem_bfs = " + fosnr + " AND los = " + lotnr + " AND lieferdatum = '" + date + "') AND ("+ sql + ")"
            else:
                if defaultSql == True:
                    sql = "gem_bfs = " + fosnr + " AND los = " + lotnr + " AND lieferdatum = '" + date + "'"
        except KeyError:
            if defaultSql == True:
                sql = "gem_bfs = " + fosnr + " AND los = " + lotnr + " AND lieferdatum = '" + date + "'"
               
        # So ists auch möglich NICHT gem_bfs, los und lieferdatum zu requesten.
        try:
            sql_overwrite = layer["sql_overwrite"]
            sql = sql_overwrite
        except:
            pass
                
        try:
            style = layer["style"]
        except:
            style = ""
            print "key error: style"
            
        try:
            group = layer["group"]
        except:
            group = ""
            print "key error: group"
            
        try:
            key = layer["key"]
        except:
            key = ""
            print "key error: key"
    
        if geom == "":
            uri = QgsDataSourceURI("dbname='"+database+"' host="+host+" port="+port+" user='"+username+"' password='"+password+"' table=\""+schema+"\".\""+table+"\" sql="+sql)
        else:
#            uri = QgsDataSourceURI("dbname='"+database+"' host="+host+" port="+port+" user='"+username+"' password='"+password+"' table=\""+schema+"\".\""+table+"\" ("+geom+") sql="+sql)
            uri = QgsDataSourceURI()
            uri.setConnection(host, port, database, username, password)
            uri.setDataSource(schema, table, geom, sql)
            print uri.uri()

            
        if key != "":
            uri.setKeyColumn(key)
                
        layer = QgsVectorLayer(uri.uri(), title, "postgres")
        layer.featureCount() # Sonst funktioniert der featureCount in der virtuellen Maschine nicht. Warum??
    
        ## Apply the style.
        if style <> "":
            qml = QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + '/python/plugins/chenyx06plus/styles/' + style))
            layer.loadNamedStyle(qml)
            
        ## Add layer to the map canvas.
        if not layer.isValid():
            print "Layer failed to load!"        
        else:
            QgsMapLayerRegistry.instance().addMapLayer(layer)
            
        # Zuerst mal alle nicht visible (-> lädt schneller)
        iface.legendInterface().setLayerVisible(layer,  False)      
        iface.mapCanvas().refresh()   
            
        # Legende wegklappen.
        if showLegend == False:
            legendTree = iface.mainWindow().findChild(QDockWidget,"Legend").findChild(QTreeWidget)   
            legendTree.collapseItem(legendTree.currentItem())
            
    # GDAL Raster-Layer hinzufuegen.
    elif layer["type"] == "raster":
        title = layer["title"]
        fileName = layer["file"]
        
        try:
            group = layer["group"]
        except:
            group = ""
            print "key error: group"               
        
        fileInfo = QFileInfo(fileName)
        baseName = fileInfo.baseName()
        layer = QgsRasterLayer(fileName, baseName)
        if not layer.isValid():
            print "Layer failed to load!"
        else:
            QgsMapLayerRegistry.instance().addMapLayer(layer)
    
    # WMS-Layer hinzufuegen.
    elif layer["type"] == "wms":
        url = layer["url"]
        title = layer["title"]
        layers = layer["layers"].split(",") 
        format = layer["format"]
        crs = layer["crs"]
        
        try:
            group = layer["group"]
        except:
            group = ""
            print "key error: group"        

        styles = []
        for i in range(len(layers)):
            styles.append("")

        layer = QgsRasterLayer(0, url, title, "wms", layers, styles, format, crs)
        if not layer.isValid():
            print "Layer failed to load!"        
        else:
            QgsMapLayerRegistry.instance().addMapLayer(layer)

    # WFS Layer hinzufuegen.
    elif layer["type"] == "wfs":
        url = layer["url"]
        title = layer["title"]
        typename = layer["typename"]
        crs = layer["crs"]
        try:
            bbox = layer["bbox"]
        except:
            bbox = ""
            print "key error: bbox"       
        try:
            intersect = layer["intersect"]
        except:
            intersect = ""
        try:
            group = layer["group"]
        except:
            group = ""
            print "key error: group"   
        try:
            style = layer["style"]
        except:
            style = ""
            print "key error: style"

        filter = ""
        if bbox != "":
            filter = ""
            bbox = "&BBOX=" + bbox
            
        if intersect != "":
            bbox = ""
            filter = "&Filter=<Filter><Intersect><PropertyName>"
            filter += str(intersect[0])
            filter += "</PropertyName><gml:Polygon><gml:outerBoundaryIs><gml:LinearRing><gml:coordinates>"
            for coord in intersect[1].asPolygon()[0]:
                filter += coord.toString(5)
                filter += " "
            filter = str(filter).strip()
            filter += "</gml:coordinates></gml:LinearRing></gml:outerBoundaryIs></gml:Polygon></Intersect></Filter>"

        print url

        uri = url + "?SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature" + "&TYPENAME=" + typename + "&SRSNAME=" + crs + bbox + filter
        print uri

        layer = QgsVectorLayer(uri, title, "WFS")
        
        # Apply the style.
        if style <> "":
            qml = QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + '/python/plugins/chenyx06plus/styles/' + style))
            layer.loadNamedStyle(qml)
        
        if not layer.isValid():
            print "VerioSO: WFS layer failed to load!"        
        else:
            if addMapLayer:
                QgsMapLayerRegistry.instance().addMapLayer(layer)


    # Layer einer Gruppe hinzufuegen.
    if group <> "":
        grpList = iface.legendInterface().groups()
        grpIdx = grpList.indexOf(group)
        
        if grpIdx >= 0:
            # Der Gruppenindex wird selber bestimmt,
            # da moveLayer anscheinend der absolute Index 
            # verlangt. Die bestehende Methode aber den
            # relativen Index zurückgibt.
            
            # Bei der Sichtbarkeit gibts ne Fehlueberlegung:
            # So geht das nicht, wird nur der letzte Layer
            # wieder angeschaltet....
            grpIdxAbs = getGroupIndex( iface, group )
            if grpIdxAbs <> 0:
                # Minus 1, weil der neue Layer schon in der Legende ist.
                iface.legendInterface().moveLayer(layer,  grpIdxAbs-1)
#                iface.legendInterface().setLayerVisible(layer,  False)
                iface.legendInterface().setGroupExpanded(grpIdxAbs-2,  False)
#                iface.legendInterface().setGroupVisible(grpIdxAbs-2,  False)                
        else:
            grpIdx = iface.legendInterface().addGroup(group)
            iface.legendInterface().moveLayer(layer, grpIdx)
            
#        iface.legendInterface().setLayerVisible(layer,  False)
        iface.legendInterface().setGroupExpanded(grpIdx,  False)
#        iface.legendInterface().setGroupVisible(grpIdx,  False)
        
        
    if isVisible == True:
        iface.legendInterface().setLayerVisible(layer,  True)      
        iface.mapCanvas().refresh()    
        
    if zoomToExtent == True:
        rect = layer.extent()
        rect.scale(1.2)
        iface.mapCanvas().setExtent( rect )        
        iface.mapCanvas().refresh()            
    
    return layer


# Returns the absolute legend index of
# a group name.
# (c) Stefan Ziegler
def getGroupIndex(iface, groupName):
    relationList = iface.legendInterface().groupLayerRelationship()
    i = 0
    for item in relationList:
        if item[0] == groupName:
            i = i  + 1
            return i
        i = i + 1

    return 0


# Returns some basic settings.
# (c) Stefan Ziegler 
def getSettings( ):
    mySettings = {}

    settings = QSettings("CatAIS","chenyx06+")        
    mySettings["host"] =  settings.value("db/host").toString() 
    mySettings["database"] = settings.value("db/database").toString() 
    mySettings["port"] = settings.value("db/port").toString() 
    mySettings["schema"] = settings.value("db/schema").toString()
    mySettings["username"] = settings.value("db/username").toString() 
    mySettings["password"] = settings.value("db/password").toString()   
    mySettings["admin"] = settings.value("db/admin").toString() 
    mySettings["adminpassword"] = settings.value("db/adminpassword").toString()       
    
    mySettings["fosnr"] = settings.value("core/fosnr").toString()
    mySettings["municipality"] = settings.value("core/municipality").toString()
    mySettings["lotnr"] = settings.value("core/lotnr").toString()      
    mySettings["date"] = settings.value("core/date").toString() 
    
    mySettings["tempdir"] = settings.value("temp/dir").toString()
    
    return mySettings
        

# Returns all baselayers with all the tables from baselayers.xml.
# (c) Stefan Ziegler
def getBaselayers( ):
    
    baselayers = []
        
    filename = QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + "/python/plugins/chenyx06plus/gui/baselayers.xml"))
    try:
        layersfile = open(filename,"r")
        layersxml = layersfile.read()
        
        doc = QtXml.QDomDocument()
        doc.setContent(layersxml,  True)  
        
        root = doc.documentElement()
        if root.tagName() != "baselayers":
            return
            
        node = root.firstChild()
        while not node.isNull():
            if node.toElement() and node.nodeName() == "baselayer":
                baselayer = {}
                id = node.toElement().attribute("id","")
                title = node.toElement().attribute("title",  "")
                type = node.toElement().attribute("type",  "")
                print id,   type
                baselayer["id"] = id
                baselayer["title"] = unicode(title)
                baselayer["type"] = type

                infoNode = node.toElement().firstChild()
                while not infoNode.isNull():
                    print infoNode.nodeName()
                    print infoNode.toElement().text()
                    baselayer[str(infoNode.nodeName())] = infoNode.toElement().text()
                
                    infoNode = infoNode.nextSibling()
            
            baselayers.append(baselayer)
            
            node = node.nextSibling()
            
    except IOError:
        print "error opening baselayers.xml"        
        
    return baselayers



def getCheckTopicsName():
    
    settings = getSettings()
    schema = settings["schema"]
    if schema == "":
        return []    
    
    availableCheckTopics = []

    filename = QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + "/python/plugins/soverify/"+schema+"/gui/checks.xml"))
    try:
        file = open(filename,"r")
        xml = file.read()
        
        doc = QtXml.QDomDocument()
        doc.setContent(xml,  True)  
        
        root = doc.documentElement()
        if root.tagName() != "checks":
            return
            
        node = root.firstChild()
        while not node.isNull():
            if node.toElement() and node.nodeName() == "check":
                topic = node.toElement().attribute("topic",  "")
                availableCheckTopics.append(str(topic))
                
            node = node.nextSibling()
            
    except IOError:
        print "error opening checks.xml"        
        return None
        
    # Doppelte Topics aus Arrray entfernen.
    u = []
    for x in availableCheckTopics:
        if x not in u:
            u.append(x)
            
    return u




# Returns all checks with all the tables from checks.xml.
# (c) Stefan Ziegler
def getChecks( topicName = None):

    settings = getSettings()
    schema = settings["schema"]
    if schema == "":
        return []    

    checks = []

    filename = QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + "/python/plugins/soverify/"+schema+"/gui/checks.xml"))
    try:
        file = open(filename,"r")
        xml = file.read()
        
        doc = QtXml.QDomDocument()
        doc.setContent(xml,  True)  
        
        root = doc.documentElement()
        if root.tagName() != "checks":
            return
            
        node = root.firstChild()
        while not node.isNull():
            if node.toElement() and node.nodeName() == "check":
                check = {}
                id = node.toElement().attribute("id","")
                title = node.toElement().attribute("title",  "")
                group = node.toElement().attribute("group",  "")
                topic = node.toElement().attribute("topic",  "")
                type = node.toElement().attribute("type",  "")                
                check["id"] = id
                check["title"] = unicode(title)
                check["group"] = group
                
                
                check["topic"] = topic
                check["type"] = type
                
#                print "%%%%%%%%%%%%%%%%%%%"
#                print unicode(title)
#                time.sleep(2)                
                
                if topic <> topicName and topicName <> None:
                    node = node.nextSibling()
                    continue
                
                layers = []
                infoNode = node.toElement().firstChild()
                while not infoNode.isNull():
                    if infoNode.toElement() and infoNode.nodeName() == "layer":
                        layer = {}
                        # Da wir die Layer einzeln hinzüfügen und die
                        # normale doShowSimpleLayer-Funktion 
                        # benützen, müssen wir die Gruppe auch den
                        # Layer-Infos hinzufügen.
                        layer["group"] = group
                        layernode = infoNode.toElement().firstChild()
                        while not layernode.isNull():
                            layer[str(layernode.nodeName())] = layernode.toElement().text()
                            layernode = layernode.nextSibling()
                        layers.append( layer )
                        
                    elif infoNode.toElement() and infoNode.nodeName() == "file":
                        complexFile = infoNode.toElement().text()
                        check["file"] = complexFile
                        
                    elif infoNode.toElement() and infoNode.nodeName() == "shortcut":
                        shortcut = infoNode.toElement().text()
                        check["shortcut"] = shortcut
                        
                    infoNode = infoNode.nextSibling()
                if type == "simple":
                    check["layers"] = layers
            
            checks.append( check ) 
            node = node.nextSibling()
            
    except IOError:
        print "error opening checks.xml"        
        return None

    return checks


# Returns all topics with all the tables from topics.xml.
# (c) Stefan Ziegler
def getTopics( ):

    settings = getSettings()
    dbschema = settings["schema"]
    if dbschema == "":
        return []

    topics = []

    filename = QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + "/python/plugins/soverify/"+dbschema+"/gui/topics.xml"))
    try:
        file = open(filename,"r")
        xml = file.read()
        
        doc = QtXml.QDomDocument()
        doc.setContent(xml,  True)  
        
        root = doc.documentElement()
        if root.tagName() != "topics":
            return
            
        node = root.firstChild()
        while not node.isNull():
            if node.toElement() and node.nodeName() == "topic":
                topic = {}
                id = node.toElement().attribute("id","")
                title = node.toElement().attribute("title",  "")
                group = node.toElement().attribute("group",  "")
                topic["id"] = id
                topic["title"] = title
                topic["group"] = group
                
                tables = []
                infoNode = node.toElement().firstChild()
                while not infoNode.isNull():
                    if infoNode.toElement() and infoNode.nodeName() == "table":
                        table = {}
                        tablenode = infoNode.toElement().firstChild()
                        while not tablenode.isNull():
                            table[str(tablenode.nodeName())] = tablenode.toElement().text()
                            tablenode = tablenode.nextSibling()
                        tables.append( table )
                    infoNode = infoNode.nextSibling()
                topic["tables"] = tables
                topics.append(topic)
            node = node.nextSibling()
            
    except IOError:
        print "error opening topics.xml"        
        return None
    
    return topics


# Return QgsVectorLayer from a layer name ( as string )
# (c) Carson Farmer / fTools
def getVectorLayerByName( myName ):
    layermap = QgsMapLayerRegistry.instance().mapLayers()
    for name, layer in layermap.iteritems():
        if layer.type() == QgsMapLayer.VectorLayer and layer.name() == myName:
            if layer.isValid():
                return layer
            else:
                return None    


# Return list of names of all layers in QgsMapLayerRegistry
# (c) Carson Farmer / fTools
# 
def getLayerNames( vTypes,  providerException=None ):
    layermap = QgsMapLayerRegistry.instance().mapLayers()
    layerlist = []
    if vTypes == "all":
        for name, layer in layermap.iteritems():
            provider = layer.dataProvider()
            ## Is this a bug??? I only get "None" as provider for a TIFF....???
            if provider == None:
                layerlist.append( unicode( layer.name() ) )
                continue
            providerName = provider.name()
            if providerName == providerException:
                continue
            else:
                layerlist.append( unicode( layer.name() ) )
    else:
        for name, layer in layermap.iteritems():
            if layer.type() == QgsMapLayer.VectorLayer:
                if layer.geometryType() in vTypes:
                    layerlist.append( unicode( layer.name() ) )
            elif layer.type() == QgsMapLayer.RasterLayer:
                if "Raster" in vTypes:
                    layerlist.append( unicode( layer.name() ) )
    return layerlist
