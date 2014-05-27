# -*- coding: utf-8 -*-

# Import the PyQt and the QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

from Ui_settings import Ui_Settings

class ChangeSettingsDialog(QDialog, Ui_Settings):
  
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self.okButton = self.buttonBox.button(QDialogButtonBox.Ok)
        self.connect(self.okButton, SIGNAL("accepted()"), self.accept)
        
        # Get the settings.
        self.settings = QSettings("CatAIS","chenyx06+")
        self.tempdirpath = self.settings.value("temp/dir")
        

    def initGui(self):
        
#        self.schema = self.settings.value("db/schema").toString()
        self.providerDatabase =  self.settings.value("provider/database").toBool()
        self.providerWfs =  self.settings.value("provider/wfs").toBool()        
        
        if self.providerDatabase == True:
            self.radioButtonProviderDatabase.setChecked( True )
        elif self.providerWfs == True:
            self.radioButtonProviderWfs.setChecked( True )

        self.lineEditDbHost.setText( self.settings.value("db/host").toString() ) 
        self.lineEditDbDatabase.setText( self.settings.value("db/database").toString() ) 
        self.lineEditDbPort.setText( self.settings.value("db/port").toString() ) 
        self.lineEditDbSchema.setText( self.settings.value("db/schema").toString() )         
        self.lineEditDbUsername.setText( self.settings.value("db/username").toString() ) 
        self.lineEditDbPassword.setText( self.settings.value("db/password").toString() )  
        self.lineEditDbAdmin.setText( self.settings.value("db/admin").toString() ) 
        self.lineEditDbAdminPassword.setText( self.settings.value("db/adminpassword").toString() ) 
        
        self.lineEditWfsUrl.setText( self.settings.value("wfs/url").toString() ) 
        self.lineEditWfsNamespace.setText( self.settings.value("wfs/namespace").toString() ) 
        self.lineEditWfsUsername.setText( self.settings.value("wfs/username").toString() ) 
        self.lineEditWfsPassword.setText( self.settings.value("wfs/userpassword").toString() ) 

        self.lineEditTempDir.setText( self.settings.value("temp/dir").toString() ) 
            
        
    @pyqtSignature("on_btnBrowseTempDir_clicked()")    
    def on_btnBrowseTempDir_clicked(self):
        dir= QFileDialog.getExistingDirectory(self, "Choose temp directory",self.tempdirpath.toString())
        dirInfo = QFileInfo(dir)
        self.lineEditTempDir.setText(QString(dirInfo.absoluteFilePath()))
        
#        self.settings.setValue("gui/tempdirpath", QVariant(dirInfo.absoluteFilePath()))        
        
        
    def accept(self):
        if self.radioButtonProviderDatabase.isChecked():
            self.settings.setValue("provider/database", QVariant( True ))
            self.settings.setValue("provider/wfs", QVariant( False ))
            self.settings.setValue("provider/name",  QVariant( "postgres" ))
            
        elif self.radioButtonProviderWfs.isChecked():
            self.settings.setValue("provider/database", QVariant( False ))            
            self.settings.setValue("provider/wfs", QVariant( True ))
            self.settings.setValue("provider/name",  QVariant( "wfs" ))

        self.settings.setValue("db/host", QVariant( self.lineEditDbHost.text() ) )   
        self.settings.setValue("db/database", QVariant( self.lineEditDbDatabase.text() ) )      
        self.settings.setValue("db/port", QVariant( self.lineEditDbPort.text() ) )     
        self.settings.setValue("db/schema", QVariant( self.lineEditDbSchema.text() ) )             
        self.settings.setValue("db/username", QVariant( self.lineEditDbUsername.text() ) ) 
        self.settings.setValue("db/password", QVariant( self.lineEditDbPassword.text() ) ) 
        self.settings.setValue("db/admin", QVariant( self.lineEditDbAdmin.text() ) ) 
        self.settings.setValue("db/adminpassword", QVariant( self.lineEditDbAdminPassword.text() ) ) 
                
        self.settings.setValue("wfs/url",  QVariant( self.lineEditWfsUrl.text() ))
        self.settings.setValue("wfs/namespace",  QVariant( self.lineEditWfsNamespace.text() ))
        self.settings.setValue("wfs/username",  QVariant( self.lineEditWfsUsername.text() ))
        self.settings.setValue("wfs/userpassword",  QVariant( self.lineEditWfsPassword.text() ))
                
        self.settings.setValue("temp/dir",  QVariant( self.lineEditTempDir.text() ) )
        
        
#        Brauch ich das in diesem Plugin?
#        if self.settings.value("db/schema").toString() <> self.schema:
#            self.emit( SIGNAL("schemaHasChanged()") )
        
        self.close()
