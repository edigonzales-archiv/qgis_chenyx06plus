DROP TRIGGER update_dreiecke ON wasseramt.dreiecke_tsp;
DROP FUNCTION wasseramt.update_dreiecke();

CREATE OR REPLACE FUNCTION wasseramt.update_dreiecke() RETURNS TRIGGER AS $$
BEGIN
 IF(TG_OP='DELETE') 
 THEN
  EXECUTE 'DELETE FROM wasseramt.dreiecke WHERE nummer = '|| quote_literal(OLD.dreieck_nummer);
 ELSE
  EXECUTE 'DELETE FROM wasseramt.dreiecke WHERE nummer = '|| quote_literal(NEW.dreieck_nummer);
  EXECUTE 'INSERT INTO wasseramt.dreiecke (nummer, typ, the_geom_lv03, the_geom_lv95) SELECT h.dreieck_nummer, i.typ, h.the_geom_lv03, h.the_geom_lv95 
FROM
(
 SELECT f.dreieck_nummer, f.the_geom_lv03, g.the_geom_lv95
 FROM
 (
  SELECT e.dreieck_nummer, ST_PolygonFromText(''POLYGON((''||ST_X(the_geom_1)||'' ''||ST_Y(the_geom_1)||'', ''||ST_X(the_geom_2)||'' ''||ST_Y(the_geom_2)||'', ''||ST_X(the_geom_3)||'' ''||ST_Y(the_geom_3)||'', ''||ST_X(the_geom_1)||'' ''||ST_Y(the_geom_1)||''))'', 21781) as the_geom_lv03
  FROM
  (
   SELECT c.dreieck_nummer, c.the_geom_1 as the_geom_1, c.the_geom_2 as the_geom_2, d.the_geom as the_geom_3
   FROM
   (
    SELECT a.dreieck_nummer, a.the_geom as the_geom_1, b.the_geom as the_geom_2
    FROM
    (
     SELECT dreieck_nummer, the_geom
     FROM wasseramt.dreiecke_tsp as m, wasseramt.tsp_lv03 as n
     WHERE dreieck_nummer = '||quote_literal(NEW.dreieck_nummer)||'
     AND m.tsp_nummer_1 = n.nummer
    ) a
    LEFT OUTER JOIN
    (
     SELECT dreieck_nummer, the_geom
     FROM wasseramt.dreiecke_tsp as m, wasseramt.tsp_lv03 as n
     WHERE dreieck_nummer = '||quote_literal(NEW.dreieck_nummer)||'
     AND m.tsp_nummer_2 = n.nummer
    ) b
    ON a.dreieck_nummer = b.dreieck_nummer
   ) c
   LEFT OUTER JOIN
   (
    SELECT dreieck_nummer, the_geom
    FROM wasseramt.dreiecke_tsp as m, wasseramt.tsp_lv03 as n
    WHERE dreieck_nummer = '||quote_literal(NEW.dreieck_nummer)||'
    AND m.tsp_nummer_3 = n.nummer
   ) d
   ON c.dreieck_nummer = d.dreieck_nummer
  ) e
 ) f
 LEFT OUTER JOIN
 (
  SELECT e.dreieck_nummer, ST_PolygonFromText(''POLYGON((''||ST_X(the_geom_1)||'' ''||ST_Y(the_geom_1)||'', ''||ST_X(the_geom_2)||'' ''||ST_Y(the_geom_2)||'', ''||ST_X(the_geom_3)||'' ''||ST_Y(the_geom_3)||'', ''||ST_X(the_geom_1)||'' ''||ST_Y(the_geom_1)||''))'', 2056) as the_geom_lv95
  FROM
  (
   SELECT c.dreieck_nummer, c.the_geom_1 as the_geom_1, c.the_geom_2 as the_geom_2, d.the_geom as the_geom_3
   FROM
   (
    SELECT a.dreieck_nummer, a.the_geom as the_geom_1, b.the_geom as the_geom_2
    FROM
    (
     SELECT dreieck_nummer, the_geom
     FROM wasseramt.dreiecke_tsp as m, wasseramt.tsp_lv95 as n
     WHERE dreieck_nummer = '||quote_literal(NEW.dreieck_nummer)||'
     AND m.tsp_nummer_1 = n.nummer
    ) a
    LEFT OUTER JOIN
    (
     SELECT dreieck_nummer, the_geom
     FROM wasseramt.dreiecke_tsp as m, wasseramt.tsp_lv95 as n
     WHERE dreieck_nummer = '||quote_literal(NEW.dreieck_nummer)||'
     AND m.tsp_nummer_2 = n.nummer
    ) b
    ON a.dreieck_nummer = b.dreieck_nummer
   ) c
   LEFT OUTER JOIN
   (
    SELECT dreieck_nummer, the_geom
    FROM wasseramt.dreiecke_tsp as m, wasseramt.tsp_lv95 as n
    WHERE dreieck_nummer = '||quote_literal(NEW.dreieck_nummer)||'
    AND m.tsp_nummer_3 = n.nummer
   ) d
   ON c.dreieck_nummer = d.dreieck_nummer
  ) e
 ) g
 ON f.dreieck_nummer = g.dreieck_nummer
) h,
wasseramt.dreiecke_lv03_bearbeitung i
WHERE h.dreieck_nummer = i.nummer';

 END IF;

 RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER update_dreiecke
   AFTER INSERT OR UPDATE OR DELETE ON wasseramt.dreiecke_tsp
   FOR EACH ROW
   EXECUTE PROCEDURE wasseramt.update_dreiecke();



SELECT h.dreieck_nummer, i.typ, h.the_geom_lv03, h.the_geom_lv95 
FROM
(
 SELECT f.dreieck_nummer, f.the_geom_lv03, g.the_geom_lv95
 FROM
 (
  SELECT e.dreieck_nummer, ST_PolygonFromText('POLYGON(('||ST_X(the_geom_1)||' '||ST_Y(the_geom_1)||', '||ST_X(the_geom_2)||' '||ST_Y(the_geom_2)||', '||ST_X(the_geom_3)||' '||ST_Y(the_geom_3)||', '||ST_X(the_geom_1)||' '||ST_Y(the_geom_1)||'))', 21781) as the_geom_lv03
  FROM
  (
   SELECT c.dreieck_nummer, c.the_geom_1 as the_geom_1, c.the_geom_2 as the_geom_2, d.the_geom as the_geom_3
   FROM
   (
    SELECT a.dreieck_nummer, a.the_geom as the_geom_1, b.the_geom as the_geom_2
    FROM
    (
     SELECT dreieck_nummer, the_geom
     FROM wasseramt.dreiecke_tsp as m, wasseramt.tsp_lv03 as n
     WHERE dreieck_nummer = 'AG0005'
     AND m.tsp_nummer_1 = n.nummer
    ) a
    LEFT OUTER JOIN
    (
     SELECT dreieck_nummer, the_geom
     FROM wasseramt.dreiecke_tsp as m, wasseramt.tsp_lv03 as n
     WHERE dreieck_nummer = 'AG0005'
     AND m.tsp_nummer_2 = n.nummer
    ) b
    ON a.dreieck_nummer = b.dreieck_nummer
   ) c
   LEFT OUTER JOIN
   (
    SELECT dreieck_nummer, the_geom
    FROM wasseramt.dreiecke_tsp as m, wasseramt.tsp_lv03 as n
    WHERE dreieck_nummer = 'AG0005'
    AND m.tsp_nummer_3 = n.nummer
   ) d
   ON c.dreieck_nummer = d.dreieck_nummer
  ) e
 ) f
 LEFT OUTER JOIN
 (
  SELECT e.dreieck_nummer, ST_PolygonFromText('POLYGON(('||ST_X(the_geom_1)||' '||ST_Y(the_geom_1)||', '||ST_X(the_geom_2)||' '||ST_Y(the_geom_2)||', '||ST_X(the_geom_3)||' '||ST_Y(the_geom_3)||', '||ST_X(the_geom_1)||' '||ST_Y(the_geom_1)||'))', 2056) as the_geom_lv95
  FROM
  (
   SELECT c.dreieck_nummer, c.the_geom_1 as the_geom_1, c.the_geom_2 as the_geom_2, d.the_geom as the_geom_3
   FROM
   (
    SELECT a.dreieck_nummer, a.the_geom as the_geom_1, b.the_geom as the_geom_2
    FROM
    (
     SELECT dreieck_nummer, the_geom
     FROM wasseramt.dreiecke_tsp as m, wasseramt.tsp_lv95 as n
     WHERE dreieck_nummer = 'AG0005'
     AND m.tsp_nummer_1 = n.nummer
    ) a
    LEFT OUTER JOIN
    (
     SELECT dreieck_nummer, the_geom
     FROM wasseramt.dreiecke_tsp as m, wasseramt.tsp_lv95 as n
     WHERE dreieck_nummer = 'AG0005'
     AND m.tsp_nummer_2 = n.nummer
    ) b
    ON a.dreieck_nummer = b.dreieck_nummer
   ) c
   LEFT OUTER JOIN
   (
    SELECT dreieck_nummer, the_geom
    FROM wasseramt.dreiecke_tsp as m, wasseramt.tsp_lv95 as n
    WHERE dreieck_nummer = 'AG0005'
    AND m.tsp_nummer_3 = n.nummer
   ) d
   ON c.dreieck_nummer = d.dreieck_nummer
  ) e
 ) g
 ON f.dreieck_nummer = g.dreieck_nummer
) h,
wasseramt.dreiecke_lv03_bearbeitung i
WHERE h.dreieck_nummer = i.nummer