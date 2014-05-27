/*
SELECT tsp_nummer, dreieck_nummer
FROM
(
 SELECT a.nummer as tsp_nummer, b.nummer as dreieck_nummer
 FROM wasseramt.tsp_lv03 as a,
 (
   SELECT nummer, (ST_DumpPoints(the_geom)).geom as the_geom
   FROM
   (
     SELECT nummer, ST_RemovePoint(ST_Boundary(ST_Reverse(ST_ForceRHR(the_geom))),3) as the_geom 
     FROM wasseramt.dreiecke_lv03_bearbeitung  ORDER BY nummer 
   ) as c
 ) as b
 WHERE a.the_geom && b.the_geom
 AND ST_Intersects(ST_SnapToGrid(a.the_geom, 0.001), ST_SnapToGrid(b.the_geom, 0.001)) 
) as d;
*/


/*
INSERT INTO wasseramt.dreiecke_tsp_v2 (dreieck_nummer, tsp_nummer_1, tsp_nummer_2, tsp_nummer_3)
SELECT c.dreieck_nummer, c.tsp_nummer_1 as tsp_nummer_1, c.tsp_nummer_2 as tsp_nummer_2, d.tsp_nummer as tsp_nummer_3
FROM
(
 SELECT a.dreieck_nummer, a.tsp_nummer as tsp_nummer_1, b.tsp_nummer as tsp_nummer_2
 FROM
 (
  SELECT n.nummer as dreieck_nummer, m.nummer as tsp_nummer 
  FROM wasseramt.tsp_lv03 m,
  (
   SELECT nummer, ST_PointN(ST_Boundary(ST_Reverse(ST_ForceRHR(the_geom))),1) as the_geom 
   FROM wasseramt.dreiecke_lv03_bearbeitung WHERE nummer = 'AG0001' 
  ) n
  WHERE n.the_geom && m.the_geom
  AND ST_Intersects(ST_SnapToGrid(n.the_geom, 0.001), ST_SnapToGrid(m.the_geom, 0.001)) 
 
 ) a
 LEFT OUTER JOIN
 (
  SELECT n.nummer as dreieck_nummer, m.nummer as tsp_nummer 
  FROM wasseramt.tsp_lv03 m,
  (
   SELECT nummer, ST_PointN(ST_Boundary(ST_Reverse(ST_ForceRHR(the_geom))),2) as the_geom 
   FROM wasseramt.dreiecke_lv03_bearbeitung WHERE nummer = 'AG0001' 
  ) n
  WHERE n.the_geom && m.the_geom
  AND ST_Intersects(ST_SnapToGrid(n.the_geom, 0.001), ST_SnapToGrid(m.the_geom, 0.001)) 
 ) b
 ON a.dreieck_nummer = b.dreieck_nummer
) c
LEFT OUTER JOIN
(
  SELECT n.nummer as dreieck_nummer, m.nummer as tsp_nummer 
  FROM wasseramt.tsp_lv03 m,
  (
   SELECT nummer, ST_PointN(ST_Boundary(ST_Reverse(ST_ForceRHR(the_geom))),3) as the_geom 
   FROM wasseramt.dreiecke_lv03_bearbeitung WHERE nummer = 'AG0001' 
  ) n
  WHERE n.the_geom && m.the_geom
  AND ST_Intersects(ST_SnapToGrid(n.the_geom, 0.001), ST_SnapToGrid(m.the_geom, 0.001)) 
) d
ON c.dreieck_nummer = d.dreieck_nummer
*/

/*
DELETE FROM wasseramt.dreiecek_tsp_v2;

-- fuer einmal alles importieren:
INSERT INTO wasseramt.dreiecke_tsp_v2 (dreieck_nummer, tsp_nummer_1)
  SELECT n.nummer as dreieck_nummer, m.nummer as tsp_nummer 
  FROM wasseramt.tsp_lv03 m,
  (
   SELECT nummer, ST_PointN(ST_Boundary(ST_Reverse(ST_ForceRHR(the_geom))),1) as the_geom 
   FROM wasseramt.dreiecke_lv03_bearbeitung ORDER BY nummer
  ) n
  WHERE n.the_geom && m.the_geom
  AND ST_Intersects(ST_SnapToGrid(n.the_geom, 0.001), ST_SnapToGrid(m.the_geom, 0.001)) 


UPDATE wasseramt.dreiecke_tsp_v2 
SET tsp_nummer_2 = 
(
  SELECT m.nummer as tsp_nummer 
  FROM wasseramt.tsp_lv03 m,
  (
   SELECT nummer, ST_PointN(ST_Boundary(ST_Reverse(ST_ForceRHR(the_geom))),2) as the_geom 
   FROM wasseramt.dreiecke_lv03_bearbeitung 
   WHERE wasseramt.dreiecke_tsp_v2.dreieck_nummer = wasseramt.dreiecke_lv03_bearbeitung.nummer   
   ORDER BY nummer
  ) n
  WHERE n.the_geom && m.the_geom
  AND ST_Intersects(ST_SnapToGrid(n.the_geom, 0.001), ST_SnapToGrid(m.the_geom, 0.001)) 
); 


UPDATE wasseramt.dreiecke_tsp_v2 
SET tsp_nummer_3 = 
(
  SELECT m.nummer as tsp_nummer 
  FROM wasseramt.tsp_lv03 m,
  (
   SELECT nummer, ST_PointN(ST_Boundary(ST_Reverse(ST_ForceRHR(the_geom))),3) as the_geom 
   FROM wasseramt.dreiecke_lv03_bearbeitung 
   WHERE wasseramt.dreiecke_tsp_v2.dreieck_nummer = wasseramt.dreiecke_lv03_bearbeitung.nummer   
   ORDER BY nummer
  ) n
  WHERE n.the_geom && m.the_geom
  AND ST_Intersects(ST_SnapToGrid(n.the_geom, 0.001), ST_SnapToGrid(m.the_geom, 0.001)) 
); 

ALTER TABLE wasseramt.dreiecke_tsp_v2
ALTER COLUMN tsp_nummer_1 SET NOT NULL,
ALTER COLUMN tsp_nummer_2 SET NOT NULL,
ALTER COLUMN tsp_nummer_3 SET NOT NULL;
*/
/*
SELECT c.dreieck_nummer, c.tsp_nummer_1 as tsp_nummer_1, c.tsp_nummer_2 as tsp_nummer_2, d.tsp_nummer as tsp_nummer_3
FROM
(
 SELECT a.dreieck_nummer, a.tsp_nummer as tsp_nummer_1, b.tsp_nummer as tsp_nummer_2
 FROM
 (
  SELECT n.nummer as dreieck_nummer, m.nummer as tsp_nummer 
  FROM wasseramt.tsp_lv03 m,
  (
   SELECT nummer, ST_PointN(ST_Boundary(ST_Reverse(ST_ForceRHR(the_geom))),1) as the_geom 
   FROM wasseramt.dreiecke_lv03_bearbeitung ORDER BY nummer
  ) n
  WHERE n.the_geom && m.the_geom
  AND ST_Intersects(ST_SnapToGrid(n.the_geom, 0.001), ST_SnapToGrid(m.the_geom, 0.001)) 
 
 ) a
 LEFT OUTER JOIN
 (
  SELECT n.nummer as dreieck_nummer, m.nummer as tsp_nummer 
  FROM wasseramt.tsp_lv03 m,
  (
   SELECT nummer, ST_PointN(ST_Boundary(ST_Reverse(ST_ForceRHR(the_geom))),2) as the_geom 
   FROM wasseramt.dreiecke_lv03_bearbeitung ORDER BY nummer
  ) n
  WHERE n.the_geom && m.the_geom
  AND ST_Intersects(ST_SnapToGrid(n.the_geom, 0.001), ST_SnapToGrid(m.the_geom, 0.001)) 
 ) b
 ON a.dreieck_nummer = b.dreieck_nummer
) c
LEFT OUTER JOIN
(
  SELECT n.nummer as dreieck_nummer, m.nummer as tsp_nummer 
  FROM wasseramt.tsp_lv03 m,
  (
   SELECT nummer, ST_PointN(ST_Boundary(ST_Reverse(ST_ForceRHR(the_geom))),3) as the_geom 
   FROM wasseramt.dreiecke_lv03_bearbeitung ORDER BY nummer
  ) n
  WHERE n.the_geom && m.the_geom
  AND ST_Intersects(ST_SnapToGrid(n.the_geom, 0.001), ST_SnapToGrid(m.the_geom, 0.001)) 
) d
ON c.dreieck_nummer = d.dreieck_nummer
*/


DROP TRIGGER update_dreiecke_tsp ON wasseramt.dreiecke_lv03_bearbeitung;
DROP FUNCTION wasseramt.update_dreiecke_tsp();

CREATE OR REPLACE FUNCTION wasseramt.update_dreiecke_tsp() RETURNS TRIGGER AS $$

BEGIN
 IF(TG_OP='DELETE') 
 THEN
  EXECUTE 'DELETE FROM wasseramt.dreiecke_tsp_v2 WHERE dreieck_nummer = '|| quote_literal(OLD.nummer);
 ELSE
  EXECUTE 'DELETE FROM wasseramt.dreiecke_tsp_v2 WHERE dreieck_nummer = '|| quote_literal(NEW.nummer);
  EXECUTE 'INSERT INTO wasseramt.dreiecke_tsp_v2 (dreieck_nummer, tsp_nummer_1, tsp_nummer_2, tsp_nummer_3)
SELECT c.dreieck_nummer, c.tsp_nummer_1 as tsp_nummer_1, c.tsp_nummer_2 as tsp_nummer_2, d.tsp_nummer as tsp_nummer_3
FROM
(
 SELECT a.dreieck_nummer, a.tsp_nummer as tsp_nummer_1, b.tsp_nummer as tsp_nummer_2
 FROM
 (
  SELECT n.nummer as dreieck_nummer, m.nummer as tsp_nummer 
  FROM wasseramt.tsp_lv03 m,
  (
   SELECT nummer, ST_PointN(ST_Boundary(ST_Reverse(ST_ForceRHR(the_geom))),1) as the_geom 
   FROM wasseramt.dreiecke_lv03_bearbeitung WHERE nummer = '|| quote_literal(NEW.nummer) ||' 
  ) n
  WHERE n.the_geom && m.the_geom
  AND ST_Intersects(ST_SnapToGrid(n.the_geom, 0.001), ST_SnapToGrid(m.the_geom, 0.001)) 
 
 ) a
 LEFT OUTER JOIN
 (
  SELECT n.nummer as dreieck_nummer, m.nummer as tsp_nummer 
  FROM wasseramt.tsp_lv03 m,
  (
   SELECT nummer, ST_PointN(ST_Boundary(ST_Reverse(ST_ForceRHR(the_geom))),2) as the_geom 
   FROM wasseramt.dreiecke_lv03_bearbeitung WHERE nummer = '|| quote_literal(NEW.nummer) ||' 
  ) n
  WHERE n.the_geom && m.the_geom
  AND ST_Intersects(ST_SnapToGrid(n.the_geom, 0.001), ST_SnapToGrid(m.the_geom, 0.001)) 
 ) b
 ON a.dreieck_nummer = b.dreieck_nummer
) c
LEFT OUTER JOIN
(
  SELECT n.nummer as dreieck_nummer, m.nummer as tsp_nummer 
  FROM wasseramt.tsp_lv03 m,
  (
   SELECT nummer, ST_PointN(ST_Boundary(ST_Reverse(ST_ForceRHR(the_geom))),3) as the_geom 
   FROM wasseramt.dreiecke_lv03_bearbeitung WHERE nummer = '|| quote_literal(NEW.nummer) ||' 
  ) n
  WHERE n.the_geom && m.the_geom
  AND ST_Intersects(ST_SnapToGrid(n.the_geom, 0.001), ST_SnapToGrid(m.the_geom, 0.001)) 
) d
ON c.dreieck_nummer = d.dreieck_nummer';
 END IF;

 RETURN NEW;

END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER update_dreiecke_tsp
   AFTER INSERT OR UPDATE OR DELETE ON wasseramt.dreiecke_lv03_bearbeitung
   FOR EACH ROW
   EXECUTE PROCEDURE wasseramt.update_dreiecke_tsp();