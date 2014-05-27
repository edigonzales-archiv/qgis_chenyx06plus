qgis_chenyx06plus
=================

QGIS-Plugin zum interaktiven Erstellen und Verfeinern einer Dreiecksvermaschung (CHENyx06).

Voraussetzungen
---------------
* QGIS 1.8 (leider...)
* PostgreSQL / Postgis: Getestet mit PostgreSQL 9.1 und Postgis 1.5

Installation
------------
Vom Ordner .qgis/python/plugins/chenyx06plus/db/templates/ alle Dateien ein neues Verzeichnis auf der gleichen Ebene kopieren (z.B. `stadt_bern`). Sowohl die Datei `conf_anpassen.sh` mit den gewünschten Werten anpassen. Anschliessend kann mit dem Skript `dateien_anpassen.sh` sämtliche Shellskripte angepasst werden (`sed`-Befehle). Zu guter Letzt wird der Installationsprozess mit dem Skript `XXX_dateien_ausfuehren.sh` gestartet. 

Falls alles geklappt hat sind jetzt sämtliche Schemen und Tabellen angelegt.


