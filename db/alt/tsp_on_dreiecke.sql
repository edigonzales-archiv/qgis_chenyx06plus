/*SELECT DISTINCT ON (nummer) ogc_fid, nummer, round(ST_X(the_geom)::numeric, 3) as ycoord, round(ST_Y(the_geom)::numeric, 3) as xcoord
FROM
(
 SELECT 1 as ogc_fid, a.nummer, a.the_geom
 FROM wasseramt.tsp_lv95 as a,
 (
    SELECT (ST_DumpPoints(the_geom_lv95)).geom as the_geom
    FROM wasseramt.dreiecke
 ) as b
 WHERE a.the_geom && b.the_geom
 AND ST_Distance(ST_SnapToGrid(b.the_geom, 0.001), ST_SnapToGrid(a.the_geom, 0.001)) = 0
) as c
WHERE geometrytype(the_geom) = 'POINT'
*/

SELECT ogc_fid, nummer, round(ST_X(the_geom)::numeric, 3) as ycoord, round(ST_Y(the_geom)::numeric, 3) as xcoord, the_geom
FROM
(
 SELECT a.ogc_fid, a.nummer, a.the_geom
 FROM wasseramt.tsp_lv03 as a,
 (
   SELECT ST_GeomFromEWKB(the_wkb) as the_geom
   FROM
   (
    SELECT DISTINCT ST_AsEWKB((ST_DumpPoints(the_geom_lv03)).geom) as the_wkb
    FROM wasseramt.dreiecke
   ) as r
 ) as b
 WHERE a.the_geom && b.the_geom
 AND ST_Intersects(a.the_geom, b.the_geom)
) as c
WHERE geometrytype(the_geom) = 'POINT'
ORDER BY nummer;