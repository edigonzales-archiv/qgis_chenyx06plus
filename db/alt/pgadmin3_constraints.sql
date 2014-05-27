CREATE OR REPLACE FUNCTION bern.triangle_on_tsp(triangle geometry) RETURNS integer AS $$
DECLARE
 count_row RECORD;
BEGIN
 IF triangle IS NULL
 THEN
  RETURN 3;
 ELSE
  SELECT count(*)::integer as count INTO count_row
  FROM
  (
   SELECT 1 as ogc_fid, ST_Intersection(ST_SnapToGrid(b.the_geom, 0.001), ST_SnapToGrid(a.the_geom_lv03, 0.001)) as the_geom
   FROM bern.tsp as a,
   (
    SELECT ST_Collect(geom) as the_geom
    FROM
    (
     SELECT (ST_DumpPoints(triangle)).geom
    ) as a
   ) as b
    WHERE a.the_geom_lv03 && b.the_geom
  ) as c
  WHERE geometrytype(the_geom) = 'POINT';
  RETURN count_row.count;
  
 END IF;
END;
$$ LANGUAGE plpgsql;
  
