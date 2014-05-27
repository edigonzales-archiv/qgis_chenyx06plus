# Makefile for a PyQGIS plugin 
UI_FILES = Ui_exportgridplot.py Ui_settings.py Ui_about.py Ui_transform.py Ui_copytspdata.py Ui_comparecoordsbyid.py Ui_comparecoordsbylocation.py 

default: compile
	
compile: $(UI_FILES) 


%.py : %.ui
	pyuic4 -o $@ $<

