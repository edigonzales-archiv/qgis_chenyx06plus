# Konsole

# Importieren der Transformationsstützpunkte
shp2pgsql -W latin1 -s 21781 -S -I ../../data/shp/tsp-chenyx06-lv03.shp tsp-lv03 | psql -d DB_NAME
shp2pgsql -W latin1 -s 2056 -S -I ../../data/shp/tsp-chenyx06-lv95.shp tsp-lv95 | psql -d DB_NAME

# Importieren der Dreiecke
shp2pgsql -W latin1 -s 21781 -S -I ../../data/shp/chenyx06-lv03.shp dreiecke_lv03 | psql -d DB_NAME
shp2pgsql -W latin1 -s 2056 -S -I ../../data/shp/chenyx06-lv95.shp dreiecke_lv95 | psql -d DB_NAME




