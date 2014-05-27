#!/bin/bash

#sudo su postgres

createdb   chenyx06plus_versioned
createlang plpgsql   chenyx06plus_versioned

psql -d chenyx06plus_versioned   -f /usr/share/postgresql/8.4/contrib/postgis-1.5/postgis.sql
psql -d chenyx06plus_versioned -f /usr/share/postgresql/8.4/contrib/postgis-1.5/spatial_ref_sys.sql


#shp2pgsql -W latin1 -s 21781 -S -I tsp-chenyx06-lv03.shp tsp-lv03 | psql -d chenyx06plus_versioned  
#shp2pgsql -W latin1 -s 2056 -S -I tsp-chenyx06-lv95.shp tsp-lv95 | psql -d chenyx06plus_versioned  


#shp2pgsql -W latin1 -s 21781 -S -I chenyx06-lv03.shp dreiecke_lv03 | psql -d chenyx06plus_versioned  
#shp2pgsql -W latin1 -s 2056 -S -I chenyx06-lv95.shp dreiecke_lv95 | psql -d chenyx06plus_versioned  
