# -*- coding: latin1 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from Ui_about import Ui_About
import webbrowser, os

currentPath = os.path.dirname(__file__)

class AboutDialog(QDialog, QObject, Ui_About):
    def __init__(self, iface, version):
        QDialog.__init__(self, iface)
        self.iface = iface
        self.setupUi(self)
        QObject.connect(self.btnWeb, SIGNAL("clicked()"), self.openWeb)
        QObject.connect(self.btnHelp, SIGNAL("clicked()"), self.openHelp)
        self.lblVersion.setText(version)
        self.txtAbout.setText(self.getText())    
    
    def openWeb(self):
        webbrowser.open("http://www.catais.org")

    def openHelp(self):
        webbrowser.open(currentPath + "/help/cadtools_help.html")    
        
    def getText(self):
        return self.tr(""" 
Plugin zum Verdichten des CHENyx06-Datensatzes. 

CHENyx06+ DEVELOPERS:
Stefan Ziegler

ACKNOWLEDGEMENTS:
The following individuals (whether they know it or not) have contributed ideas, help, testing, code, and guidence towards this project, and I thank them.
Niklas Grässle


LICENSING INFORMATION:
CHENyx06+ is copyright (C) 2011 Stefan Ziegler
stefan.ziegler@bd.so.ch

Licensed under the terms of GNU GPL 2
This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
""")

