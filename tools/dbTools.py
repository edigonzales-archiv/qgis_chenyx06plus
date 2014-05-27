# -*- coding: utf-8 -*-
"""
/***************************************************************************
Tools for Database Management
------------------------------------------------------------------------------------------------------------------
begin                 : 2010-07-31
copyright           : (C) 2010 by Dr. Horst Duester
email                 :  horst.duester@kappasys.ch
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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
#from qgis.gui import *
#from qgis.core import *
import time,  os,  sys

class DbObj:
    MSG_BOX_TITLE = "Class dbObj"

    ## Konstruktor 
    # @param pluginname string PlugIn-Name des PlugIns in welchem die DB-Verbindung hergestellt wird (default default)
    # @param typ string Datenbank Typ (pg||oracle) (default pg)
    # @param hostname string Hostname Name des db Hosts (default srsofaioi4531)
    # @param port string Port Name des db Ports (default 5432)
    # @param dbname string dbname Name der DB (default sogis)
    # @param username string Username Name des users (default mspublic)
    # @param passwort string Passwort
    def __init__(self,pluginname="default",typ="pg", hostname="localhost",port="5432",dbname="soverify",username="mspublic", passwort=""):
        self.errorDB = ""
        self.errorDriver = ""
        self.typ = typ
        self.hostName = hostname
        self.databaseName = dbname
        self.userName = username
        self.port = port
        self.passwort = passwort
        self.pluginName = pluginname


  # Mit Datenbank verbinden.
    def connect(self):
        # Mit PostGres verbinden
        if self.typ == "pg":
          self.db = QSqlDatabase.addDatabase("QPSQL", self.pluginName)
          print "***"
          print self.db
          print self.hostName
          print self.databaseName
          print self.userName
          print self.port
          print self.passwort

        # Mit Oracle verbinden
        if self.typ == "oracle":
          self.db = QSqlDatabase.addDatabase("QOCI")
   
        self.db.setHostName(self.hostName)
        self.db.setDatabaseName(self.databaseName)
        self.db.setUserName(self.userName)
        self.db.setPassword(self.passwort)
        try:
            self.db.setPort(int(self.port))
        except ValueError:
            return False
        self.db.open()

        # Wenn Fehler bei der DB-Verbindung
        if self.db.open() == False:
          self.errorDriver = str(self.db.lastError().driverText())
          QMessageBox.warning(None, self.MSG_BOX_TITLE, ("Fehlermeldung:' "+unicode(self.errorDriver,'latin1')+".' Es kann keine Verbindung zur Datenbank aufgebaut werden! Einige Funktionen des PlugIn "+unicode(self.pluginName,'latin1')+" funktionieren deshalb nicht!"), QMessageBox.Ok, QMessageBox.Ok)
          return False
    
        return True
      
      
    ## Rckgabe des QSqlDatabase Objektes
    # @return self.db QSqlDatabase
    def dbObj(self):
        return self.db
  
    ## Lesen des Ergebnisses in ein Dictionary ["FELDNAME"][RecNo]. Jedem Key des Dictionary wird eine list zugeordnet.
    # @param abfrage string gewnschte SQL-Query
    # @return datensatz dictionary  Dictionary ["FELDNAME"][RecNo]
    def read(self, abfrage):
        sql = abfrage
    
        query = QSqlQuery(sql,self.db)
        success = query.next()
        print unicode( query.lastError().text() )
        datensatz = {}
        i = 0
        while i < query.record().count():
            result = []
            query.first()
            j = 0
            while j < query.size():
                result.append(query.value(i).toString())
                j = j + 1
                query.next()
            datensatz.update({str(query.record().fieldName(i)).upper(): result})
            i = i + 1
        return datensatz


    ## Schliesst die DB-Verbindung
    def close(self):
        self.db.close()


    ## Ausfuehren einer Query ohne Rckgabeergebnis
    # @param abfrage string gewnschte SQL-Query
    def run(self, abfrage):
        sql = abfrage
        self.db.exec_(sql)


    ## Gibt die Spalten eines Abfrageergebnisses zurck
    # @param abfrage string gewnschte SQL-Query
    # @return result array 1-Dim Array der Spaltennamen
    def cols(self, abfrage):
    
        sql = abfrage
        query = QSqlQuery(sql,self.db)
        query.next()
        result = []
        i = 0
        while i < query.record().count():
      
            result.append(str(query.record().fieldName(i)).upper())
            i = i + 1
        return result


    ## Gibt die Datentypen der Spalten eines Abfrageergebnisses zurck
    # @param abfrage string gewnschte SQL-Query
    # @return datensatz dictionary Dictionary ["FELDNAME"][DatenTyp]
    def colType(self, abfrage):
    
        sql = abfrage
        query = QSqlQuery(sql,self.db)
        query.next()
        datensatz = {}
        i = 0
        while i < query.record().count():
      
            fieldType = query.record().field(i).type()
            datensatz.update({str(query.record().fieldName(i)).upper(): query.record().field(i).value().typeToName(fieldType)})
            i = i + 1
        return datensatz

    ## Ausfuehren einer Query ohne Rckgabeergebnis aber mit Ausgabe einer Fehlermeldung
    # @param abfrage string gewnschte SQL-Query
    # @return lastError string PostgreSQL Fehlermeldung
    # @todo Momentan liefert lediglich der Driver eine Angabe, ob die Abfrage ausgefhrt wurde oder nicht. Der Datenbanktext wird leider nicht angezeigt.
    def runError(self, abfrage):
        driver = self.db.driver()
        sql = abfrage
        self.db.exec_(sql)
        lastError = self.db.lastError().text()
        print unicode( lastError )
        return lastError


    ## Ausfuehren einer Query ohne Rckgabeergebnis aber mit Ausgabe einer Notice
    # @param abfrage string gewnschte SQL-Query
    # @return notice string PostgreSQL Notice
    # @todo zur Zeit ist diese Ausgabe nicht mï¿½lich
    def runNotice(self, abfrage):
        pass


    ## Ausfuehren einer Query ohne Rckgabeergebnis aber mit Ausgabe einer Notice
    # @param abfrage string gewnschte SQL-Query
    # @return notice string PostgreSQL Notice
    # @todo zur Zeit ist diese Ausgabe nicht mï¿½lich
    def readNotice(self, abfrage):
        pass


    ## Prueft, ob ein Objekt vom Typ objtyp (table||view) in der Datenbank existiert 
    # @param objTyp String (table||view)
    # @param name String  Name des Objektes
    # @return Boolean
    def exists(self, objTyp, name):
        tmp_arr = name.split(".");
        if (len(tmp_arr) == 1):
            schema = "public"
        elif (len(tmp_arr) == 2):
            schema = tmp_arr[0]
            name = tmp_arr[1]
    
        if (objTyp == "table"):
            objTyp = "BASE TABLE"
        elif (objTyp == "view"):
            objTyp = "VIEW"
        else:
            QMessageBox.warning(None, "Error", ("Error: Only objects table or view can be checked"), QMessageBox.Ok, QMessageBox.Ok)
            return
        abfrage = "select count(table_name) as count from information_schema.tables where table_schema='"+schema+"' and table_name='"+name+"' and table_type='"+objTyp+"'"
        result = self.read(abfrage)
        if (result["COUNT"][0] == '0'):
            return False
        else:
            return True
      
        self.errorDB = ""
        self.errorDriver = ""
        self.hostName = hostname
        self.databaseName = dbname
        self.userName = username
        self.port = port
        self.passwort = passwort
   
   
    def dbHost(self):
        return self.hostName
  
  
    def dbName(self):
        return self.databaseName


    def dbUser(self):
        return self.userName


    def dbPort(self):
        return self.port


    def dbPasswd(self):
        return self.passwort



