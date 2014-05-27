# Konsole

# Importieren der Transformationsstützpunkte
shp2pgsql -W latin1 -s 21781 -S -I tsp-chenyx06-lv03.shp tsp-lv03 | psql -d chenyx06plus
shp2pgsql -W latin1 -s 2056 -S -I tsp-chenyx06-lv95.shp tsp-lv95 | psql -d chenyx06plus

# Importieren der Dreiecke
shp2pgsql -W latin1 -s 21781 -S -I chenyx06-lv03.shp dreiecke_lv03 | psql -d chenyx06plus
shp2pgsql -W latin1 -s 2056 -S -I chenyx06-lv95.shp dreiecke_lv95 | psql -d chenyx06plus




