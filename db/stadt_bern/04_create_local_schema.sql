CREATE SCHEMA stadt_bern
  AUTHORIZATION av_chenyx06_stadt_be_admin;

GRANT USAGE ON SCHEMA stadt_bern TO av_chenyx06_stadt_be_user;
GRANT USAGE ON SCHEMA stadt_bern TO av_chenyx06_stadt_be_admin;
GRANT USAGE ON SCHEMA stadt_bern TO av_chenyx06_stadt_be_admin;


CREATE TABLE stadt_bern.tsp_lv03
(
  ogc_fid serial NOT NULL UNIQUE,
  nummer character varying NOT NULL UNIQUE,
  typ integer,
  the_geom geometry,
  CONSTRAINT tsp_lv03_pkey PRIMARY KEY (ogc_fid),
  CONSTRAINT enforce_dims_the_geom CHECK (st_ndims(the_geom) = 2),
  CONSTRAINT enforce_geotype_the_geom CHECK (geometrytype(the_geom) = 'POINT'::text OR the_geom IS NULL),
  CONSTRAINT enforce_srid_the_geom CHECK (st_srid(the_geom) = 21781)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE stadt_bern.tsp_lv03 OWNER TO av_chenyx06_stadt_be_admin;
GRANT SELECT ON stadt_bern.tsp_lv03 TO av_chenyx06_stadt_be_user;

CREATE INDEX tsp_lv03_the_geom_gist
  ON stadt_bern.tsp_lv03
  USING gist
  (the_geom);

CREATE INDEX idx_tsp_lv03_nummer
  ON stadt_bern.tsp_lv03
  USING btree
  (nummer);

INSERT INTO geometry_columns VALUES ('"', 'stadt_bern', 'tsp_lv03', 'the_geom', 2, '21781', 'POINT');


CREATE TABLE stadt_bern.tsp_lv95
(
  ogc_fid serial NOT NULL UNIQUE,
  nummer character varying NOT NULL UNIQUE,
  typ integer,
  the_geom geometry,
  CONSTRAINT tsp_lv95_pkey PRIMARY KEY (ogc_fid),
  CONSTRAINT enforce_dims_the_geom CHECK (st_ndims(the_geom) = 2),
  CONSTRAINT enforce_geotype_the_geom CHECK (geometrytype(the_geom) = 'POINT'::text OR the_geom IS NULL),
  CONSTRAINT enforce_srid_the_geom CHECK (st_srid(the_geom) = 2056)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE stadt_bern.tsp_lv95 OWNER TO av_chenyx06_stadt_be_admin;
GRANT SELECT ON stadt_bern.tsp_lv95 TO av_chenyx06_stadt_be_user;

CREATE INDEX tsp_lv95_the_geom_gist
  ON stadt_bern.tsp_lv95
  USING gist
  (the_geom);

CREATE INDEX idx_tsp_lv95_nummer
  ON stadt_bern.tsp_lv95
  USING btree
  (nummer);

INSERT INTO geometry_columns VALUES ('"', 'stadt_bern', 'tsp_lv95', 'the_geom', 2, '2056', 'POINT');



-- Kopiert TSP von temp. Tabelle in TSP-Tabelle.
INSERT INTO stadt_bern.tsp_lv03 (nummer, typ, the_geom) 
 SELECT a.nom as nummer, 1 as typ, ST_SnapToGrid(a.geom, 0.001) as the_geom
 FROM "tsp-lv03" as a
 ORDER by a.nom;

INSERT INTO stadt_bern.tsp_lv95 (nummer, typ, the_geom) 
 SELECT a.nom as nummer, 1 as typ, ST_SnapToGrid(a.geom, 0.001) as the_geom
 FROM "tsp-lv95" as a
 ORDER by a.nom;




-- Prueft ob Dreieckspunkte auf TSP liegen.
-- Leider noch zwei Funktionen fuer beide
-- Bezugsrahmen. -> SRID kann man aus Geometrie
-- rausholen und dann if/else...
CREATE OR REPLACE FUNCTION stadt_bern.triangle_on_tsp_lv03(triangle geometry) RETURNS integer AS $$
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
   SELECT 1 as ogc_fid, ST_Intersection(ST_SnapToGrid(b.the_geom, 0.001), ST_SnapToGrid(a.the_geom, 0.001)) as the_geom
   FROM stadt_bern.tsp_lv03 as a,
   (
    SELECT ST_Collect(geom) as the_geom
    FROM
    (
     SELECT (ST_DumpPoints(triangle)).geom
    ) as a
   ) as b
    WHERE a.the_geom && b.the_geom
  ) as c
  WHERE geometrytype(the_geom) = 'POINT';
  RETURN count_row.count;
  
 END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION stadt_bern.triangle_on_tsp_lv95(triangle geometry) RETURNS integer AS $$
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
   SELECT 1 as ogc_fid, ST_Intersection(ST_SnapToGrid(b.the_geom, 0.001), ST_SnapToGrid(a.the_geom, 0.001)) as the_geom
   FROM stadt_bern.tsp_lv95 as a,
   (
    SELECT ST_Collect(geom) as the_geom
    FROM
    (
     SELECT (ST_DumpPoints(triangle)).geom
    ) as a
   ) as b
    WHERE a.the_geom && b.the_geom
  ) as c
  WHERE geometrytype(the_geom) = 'POINT';
  RETURN count_row.count;
  
 END IF;
END;
$$ LANGUAGE plpgsql;



-- Dreiecks-Tabelle
CREATE TABLE stadt_bern.dreiecke_lv03_bearbeitung 
(
  ogc_fid serial NOT NULL,
  nummer character varying NOT NULL UNIQUE,
  typ integer,
  the_geom geometry,
  CONSTRAINT dreiecke_lv03_bearbeitung_pkey PRIMARY KEY (ogc_fid),
  CONSTRAINT enforce_dims_the_geom CHECK (st_ndims(the_geom) = 2),
  CONSTRAINT enforce_geotype_the_geom CHECK (geometrytype(the_geom) = 'POLYGON'::text OR the_geom IS NULL),
  CONSTRAINT enforce_srid_the_geom CHECK (st_srid(the_geom) = 21781),
  CONSTRAINT enforce_triangle_the_geom CHECK (st_npoints(the_geom) = 4),
  CONSTRAINT enforce_triangle_on_tsp_the_geom CHECK(stadt_bern.triangle_on_tsp_lv03(the_geom) = 3)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE stadt_bern.dreiecke_lv03_bearbeitung OWNER TO av_chenyx06_stadt_be_admin;
GRANT SELECT ON stadt_bern.dreiecke_lv03_bearbeitung TO av_chenyx06_stadt_be_user;

CREATE INDEX dreiecke_lv03_bearbeitung_the_geom_gist
  ON stadt_bern.dreiecke_lv03_bearbeitung
  USING gist
  (the_geom);

CREATE INDEX idx_dreiecke_lv03_bearbeitung_nummer
  ON stadt_bern.dreiecke_lv03_bearbeitung
  USING btree
  (nummer);

INSERT INTO geometry_columns VALUES ('"', 'stadt_bern', 'dreiecke_lv03_bearbeitung', 'the_geom', 2, '21781', 'POLYGON');

CREATE TABLE stadt_bern.dreiecke_lv95_bearbeitung 
(
  ogc_fid serial NOT NULL,
  nummer character varying NOT NULL UNIQUE,
  typ integer,
  the_geom geometry,
  CONSTRAINT dreiecke_lv95_bearbeitung_pkey PRIMARY KEY (ogc_fid),
  CONSTRAINT enforce_dims_the_geom CHECK (st_ndims(the_geom) = 2),
  CONSTRAINT enforce_geotype_the_geom CHECK (geometrytype(the_geom) = 'POLYGON'::text OR the_geom IS NULL),
  CONSTRAINT enforce_srid_the_geom CHECK (st_srid(the_geom) = 2056),
  CONSTRAINT enforce_triangle_the_geom CHECK (st_npoints(the_geom) = 4),
  CONSTRAINT enforce_triangle_on_tsp_the_geom CHECK(stadt_bern.triangle_on_tsp_lv95(the_geom) = 3)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE stadt_bern.dreiecke_lv95_bearbeitung OWNER TO av_chenyx06_stadt_be_admin;
GRANT SELECT ON stadt_bern.dreiecke_lv95_bearbeitung TO av_chenyx06_stadt_be_user;

CREATE INDEX dreiecke_lv95_bearbeitung_the_geom_gist
  ON stadt_bern.dreiecke_lv95_bearbeitung
  USING gist
  (the_geom);

CREATE INDEX idx_dreiecke_lv95_bearbeitung_nummer
  ON stadt_bern.dreiecke_lv95_bearbeitung
  USING btree
  (nummer);

INSERT INTO geometry_columns VALUES ('"', 'stadt_bern', 'dreiecke_lv95_bearbeitung', 'the_geom', 2, '2056', 'POLYGON');


-- Kopiert Dreiecke von temp. Tabelle in Dreiecks-Tabelle.
INSERT INTO stadt_bern.dreiecke_lv03_bearbeitung (nummer, typ, the_geom) 
 SELECT a.nummer as nummer, 1 as typ, ST_SnapToGrid(a.geom, 0.001) as the_geom
 FROM "dreiecke_lv03" as a
 ORDER BY a.nummer;

INSERT INTO stadt_bern.dreiecke_lv95_bearbeitung (nummer, typ, the_geom) 
 SELECT a.nummer as nummer, 1 as typ, ST_SnapToGrid(a.geom, 0.001) as the_geom
 FROM "dreiecke_lv95" as a
 ORDER BY a.nummer;


-- Trigger den Bearbeitungs-Tabellen hinzufügen
-- Momentan nur LV03.

--DROP TRIGGER update_dreiecke_tsp ON stadt_bern.dreiecke_lv03_bearbeitung;
--DROP FUNCTION stadt_bern.update_dreiecke_tsp();

CREATE OR REPLACE FUNCTION stadt_bern.update_dreiecke_tsp() RETURNS TRIGGER AS $$

BEGIN
 IF(TG_OP='DELETE') 
 THEN
  EXECUTE 'DELETE FROM stadt_bern.dreiecke_tsp WHERE dreieck_nummer = '|| quote_literal(OLD.nummer);
 ELSE
  IF(TG_OP='UPDATE')
  THEN
   IF(NEW.nummer != OLD.nummer)
   THEN
    EXECUTE 'DELETE FROM stadt_bern.dreiecke_tsp WHERE dreieck_nummer = '|| quote_literal(OLD.nummer);
   END IF;
  END IF;

  EXECUTE 'DELETE FROM stadt_bern.dreiecke_tsp WHERE dreieck_nummer = '|| quote_literal(NEW.nummer);
  EXECUTE 'INSERT INTO stadt_bern.dreiecke_tsp (dreieck_nummer, tsp_nummer_1, tsp_nummer_2, tsp_nummer_3)
SELECT c.dreieck_nummer, c.tsp_nummer_1 as tsp_nummer_1, c.tsp_nummer_2 as tsp_nummer_2, d.tsp_nummer as tsp_nummer_3
FROM
(
 SELECT a.dreieck_nummer, a.tsp_nummer as tsp_nummer_1, b.tsp_nummer as tsp_nummer_2
 FROM
 (
  SELECT n.nummer as dreieck_nummer, m.nummer as tsp_nummer 
  FROM stadt_bern.tsp_lv03 m,
  (
   SELECT nummer, ST_PointN(ST_Boundary(ST_Reverse(ST_ForceRHR(the_geom))),1) as the_geom 
   FROM stadt_bern.dreiecke_lv03_bearbeitung WHERE nummer = '|| quote_literal(NEW.nummer) ||' 
  ) n
  WHERE n.the_geom && m.the_geom
  AND ST_Intersects(ST_SnapToGrid(n.the_geom, 0.001), ST_SnapToGrid(m.the_geom, 0.001)) 
 
 ) a
 LEFT OUTER JOIN
 (
  SELECT n.nummer as dreieck_nummer, m.nummer as tsp_nummer 
  FROM stadt_bern.tsp_lv03 m,
  (
   SELECT nummer, ST_PointN(ST_Boundary(ST_Reverse(ST_ForceRHR(the_geom))),2) as the_geom 
   FROM stadt_bern.dreiecke_lv03_bearbeitung WHERE nummer = '|| quote_literal(NEW.nummer) ||' 
  ) n
  WHERE n.the_geom && m.the_geom
  AND ST_Intersects(ST_SnapToGrid(n.the_geom, 0.001), ST_SnapToGrid(m.the_geom, 0.001)) 
 ) b
 ON a.dreieck_nummer = b.dreieck_nummer
) c
LEFT OUTER JOIN
(
  SELECT n.nummer as dreieck_nummer, m.nummer as tsp_nummer 
  FROM stadt_bern.tsp_lv03 m,
  (
   SELECT nummer, ST_PointN(ST_Boundary(ST_Reverse(ST_ForceRHR(the_geom))),3) as the_geom 
   FROM stadt_bern.dreiecke_lv03_bearbeitung WHERE nummer = '|| quote_literal(NEW.nummer) ||' 
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
   AFTER INSERT OR UPDATE OR DELETE ON stadt_bern.dreiecke_lv03_bearbeitung
   FOR EACH ROW
   EXECUTE PROCEDURE stadt_bern.update_dreiecke_tsp();




-- Def. Dreieckstabelle anlegen.
CREATE TABLE stadt_bern.dreiecke 
(
  ogc_fid serial NOT NULL,
  nummer character varying NOT NULL UNIQUE,
  typ integer,
  the_geom_lv03 geometry,
  the_geom_lv95 geometry,
  CONSTRAINT dreiecke_pkey PRIMARY KEY (ogc_fid),
  CONSTRAINT enforce_dims_the_geom_lv03 CHECK (st_ndims(the_geom_lv03) = 2),
  CONSTRAINT enforce_geotype_the_geom_lv03 CHECK (geometrytype(the_geom_lv03) = 'POLYGON'::text OR the_geom_lv03 IS NULL),
  CONSTRAINT enforce_srid_the_geom_lv03 CHECK (st_srid(the_geom_lv03) = 21781),
  CONSTRAINT enforce_dims_the_geom_lv95 CHECK (st_ndims(the_geom_lv95) = 2),
  CONSTRAINT enforce_geotype_the_geom_lv95 CHECK (geometrytype(the_geom_lv95) = 'POLYGON'::text OR the_geom_lv03 IS NULL),
  CONSTRAINT enforce_srid_the_geom_lv95 CHECK (st_srid(the_geom_lv95) = 2056)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE stadt_bern.dreiecke OWNER TO av_chenyx06_stadt_be_admin;
GRANT SELECT ON stadt_bern.dreiecke TO av_chenyx06_stadt_be_user;

CREATE INDEX dreiecke_the_geom_lv03_gist
  ON stadt_bern.dreiecke
  USING gist
  (the_geom_lv03);

CREATE INDEX dreiecke_the_geom_lv95_gist
  ON stadt_bern.dreiecke
  USING gist
  (the_geom_lv95); 

CREATE INDEX idx_dreiecke_nummer
  ON stadt_bern.dreiecke 
  USING btree
  (nummer);  

INSERT INTO geometry_columns VALUES ('"', 'stadt_bern', 'dreiecke', 'the_geom_lv03', 2, '21781', 'POLYGON');
INSERT INTO geometry_columns VALUES ('"', 'stadt_bern', 'dreiecke', 'the_geom_lv95', 2, '2056', 'POLYGON');


-- Dreiecks-Views für WFS (Brauche ich die noch??)
CREATE OR REPLACE VIEW stadt_bern.dreiecke_lv03_v AS 
 SELECT ogc_fid, nummer, typ, the_geom_lv03 as the_geom
   FROM stadt_bern.dreiecke;

ALTER TABLE stadt_bern.dreiecke_lv03_v OWNER TO av_chenyx06_stadt_be_admin;
GRANT SELECT ON TABLE stadt_bern.dreiecke_lv03_v TO av_chenyx06_stadt_be_user;
COMMENT ON VIEW stadt_bern.dreiecke_lv03_v IS 'Def. Dreiecke LV03 fuer WFS).';

INSERT INTO geometry_columns VALUES ('"', 'stadt_bern', 'dreiecke_lv03_v', 'the_geom', 2, '21781', 'POLYGON');

CREATE OR REPLACE VIEW stadt_bern.dreiecke_lv95_v AS 
 SELECT ogc_fid, nummer, typ, the_geom_lv95 as the_geom
   FROM stadt_bern.dreiecke;

ALTER TABLE stadt_bern.dreiecke_lv95_v OWNER TO av_chenyx06_stadt_be_admin;
GRANT SELECT ON TABLE stadt_bern.dreiecke_lv95_v TO av_chenyx06_stadt_be_user;
COMMENT ON VIEW stadt_bern.dreiecke_lv95_v IS 'Def. Dreiecke LV95 fuer WFS).';

INSERT INTO geometry_columns VALUES ('"', 'stadt_bern', 'dreiecke_lv95_v', 'the_geom', 2, '2056', 'POLYGON');


-- Erstmaliges importieren der Dreiecke
INSERT INTO stadt_bern.dreiecke (nummer, typ, the_geom_lv03, the_geom_lv95)
SELECT a.nummer, a.typ, ST_Reverse(ST_ForceRHR(a.the_geom)) as the_geom_lv03, ST_Reverse(ST_ForceRHR(b.the_geom)) as the_geom_lv95 
FROM stadt_bern.dreiecke_lv03_bearbeitung a, stadt_bern.dreiecke_lv95_bearbeitung b
WHERE a.nummer = b.nummer
ORDER BY a.nummer;


-- LookUp Table: Dreiecke-TSP
CREATE TABLE stadt_bern.dreiecke_tsp
(
  ogc_fid serial NOT NULL,
  dreieck_nummer character varying NOT NULL,
  tsp_nummer_1 character varying,
  tsp_nummer_2 character varying,
  tsp_nummer_3 character varying,
  
  CONSTRAINT dreiecke_tsp_pkey PRIMARY KEY (ogc_fid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE stadt_bern.dreiecke_tsp OWNER TO av_chenyx06_stadt_be_admin;
GRANT ALL ON TABLE stadt_bern.dreiecke_tsp TO av_chenyx06_stadt_be_admin;
GRANT SELECT ON TABLE stadt_bern.dreiecke_tsp TO av_chenyx06_stadt_be_user;

CREATE INDEX idx_dreiecke_tsp_dreieck_nummer
  ON stadt_bern.dreiecke_tsp
  USING btree
  (dreieck_nummer);

CREATE INDEX idx_dreiecke_tsp_tsp_nummer_1
  ON stadt_bern.dreiecke_tsp
  USING btree
  (tsp_nummer_1);

CREATE INDEX idx_dreiecke_tsp_tsp_nummer_2
  ON stadt_bern.dreiecke_tsp
  USING btree
  (tsp_nummer_2);

CREATE INDEX idx_dreiecke_tsp_tsp_nummer_3
  ON stadt_bern.dreiecke_tsp
  USING btree
  (tsp_nummer_3);


-- Daten in Lookup-Table schreiben.
INSERT INTO stadt_bern.dreiecke_tsp (dreieck_nummer, tsp_nummer_1)
  SELECT n.nummer as dreieck_nummer, m.nummer as tsp_nummer 
  FROM stadt_bern.tsp_lv03 m,
  (
   SELECT nummer, ST_PointN(ST_Boundary(ST_Reverse(ST_ForceRHR(the_geom))),1) as the_geom 
   FROM stadt_bern.dreiecke_lv03_bearbeitung ORDER BY nummer
  ) n
  WHERE n.the_geom && m.the_geom
  AND ST_Intersects(ST_SnapToGrid(n.the_geom, 0.001), ST_SnapToGrid(m.the_geom, 0.001)); 


UPDATE stadt_bern.dreiecke_tsp
SET tsp_nummer_2 = 
(
  SELECT m.nummer as tsp_nummer 
  FROM stadt_bern.tsp_lv03 m,
  (
   SELECT nummer, ST_PointN(ST_Boundary(ST_Reverse(ST_ForceRHR(the_geom))),2) as the_geom 
   FROM stadt_bern.dreiecke_lv03_bearbeitung 
   WHERE stadt_bern.dreiecke_tsp.dreieck_nummer = stadt_bern.dreiecke_lv03_bearbeitung.nummer   
   ORDER BY nummer
  ) n
  WHERE n.the_geom && m.the_geom
  AND ST_Intersects(ST_SnapToGrid(n.the_geom, 0.001), ST_SnapToGrid(m.the_geom, 0.001)) 
); 


UPDATE stadt_bern.dreiecke_tsp
SET tsp_nummer_3 = 
(
  SELECT m.nummer as tsp_nummer 
  FROM stadt_bern.tsp_lv03 m,
  (
   SELECT nummer, ST_PointN(ST_Boundary(ST_Reverse(ST_ForceRHR(the_geom))),3) as the_geom 
   FROM stadt_bern.dreiecke_lv03_bearbeitung 
   WHERE stadt_bern.dreiecke_tsp.dreieck_nummer = stadt_bern.dreiecke_lv03_bearbeitung.nummer   
   ORDER BY nummer
  ) n
  WHERE n.the_geom && m.the_geom
  AND ST_Intersects(ST_SnapToGrid(n.the_geom, 0.001), ST_SnapToGrid(m.the_geom, 0.001)) 
); 

-- Erst nach dem ersten Import die NOT NULL constraints hinzufügen:
ALTER TABLE stadt_bern.dreiecke_tsp 
ALTER COLUMN tsp_nummer_1 SET NOT NULL,
ALTER COLUMN tsp_nummer_2 SET NOT NULL,
ALTER COLUMN tsp_nummer_3 SET NOT NULL;


-- Trigger zum Nachführen der def. Dreiecke.
--DROP TRIGGER update_dreiecke ON stadt_bern.dreiecke_tsp;
--DROP FUNCTION stadt_bern.update_dreiecke();

CREATE OR REPLACE FUNCTION stadt_bern.update_dreiecke() RETURNS TRIGGER AS $$
BEGIN
 IF(TG_OP='DELETE') 
 THEN
  EXECUTE 'DELETE FROM stadt_bern.dreiecke WHERE nummer = '|| quote_literal(OLD.dreieck_nummer);
 ELSE
  EXECUTE 'DELETE FROM stadt_bern.dreiecke WHERE nummer = '|| quote_literal(NEW.dreieck_nummer);
  EXECUTE 'INSERT INTO stadt_bern.dreiecke (nummer, typ, the_geom_lv03, the_geom_lv95) SELECT h.dreieck_nummer, i.typ, h.the_geom_lv03, h.the_geom_lv95 
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
     FROM stadt_bern.dreiecke_tsp as m, stadt_bern.tsp_lv03 as n
     WHERE dreieck_nummer = '||quote_literal(NEW.dreieck_nummer)||'
     AND m.tsp_nummer_1 = n.nummer
    ) a
    LEFT OUTER JOIN
    (
     SELECT dreieck_nummer, the_geom
     FROM stadt_bern.dreiecke_tsp as m, stadt_bern.tsp_lv03 as n
     WHERE dreieck_nummer = '||quote_literal(NEW.dreieck_nummer)||'
     AND m.tsp_nummer_2 = n.nummer
    ) b
    ON a.dreieck_nummer = b.dreieck_nummer
   ) c
   LEFT OUTER JOIN
   (
    SELECT dreieck_nummer, the_geom
    FROM stadt_bern.dreiecke_tsp as m, stadt_bern.tsp_lv03 as n
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
     FROM stadt_bern.dreiecke_tsp as m, stadt_bern.tsp_lv95 as n
     WHERE dreieck_nummer = '||quote_literal(NEW.dreieck_nummer)||'
     AND m.tsp_nummer_1 = n.nummer
    ) a
    LEFT OUTER JOIN
    (
     SELECT dreieck_nummer, the_geom
     FROM stadt_bern.dreiecke_tsp as m, stadt_bern.tsp_lv95 as n
     WHERE dreieck_nummer = '||quote_literal(NEW.dreieck_nummer)||'
     AND m.tsp_nummer_2 = n.nummer
    ) b
    ON a.dreieck_nummer = b.dreieck_nummer
   ) c
   LEFT OUTER JOIN
   (
    SELECT dreieck_nummer, the_geom
    FROM stadt_bern.dreiecke_tsp as m, stadt_bern.tsp_lv95 as n
    WHERE dreieck_nummer = '||quote_literal(NEW.dreieck_nummer)||'
    AND m.tsp_nummer_3 = n.nummer
   ) d
   ON c.dreieck_nummer = d.dreieck_nummer
  ) e
 ) g
 ON f.dreieck_nummer = g.dreieck_nummer
) h,
stadt_bern.dreiecke_lv03_bearbeitung i
WHERE h.dreieck_nummer = i.nummer';

 END IF;

 RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER update_dreiecke
   AFTER INSERT OR UPDATE OR DELETE ON stadt_bern.dreiecke_tsp
   FOR EACH ROW
   EXECUTE PROCEDURE stadt_bern.update_dreiecke();


-- View für WFS: TSP on dreiecke
CREATE OR REPLACE VIEW stadt_bern.tsp_on_dreiecke_lv03_v AS 
SELECT DISTINCT ogc_fid, nummer, round(ST_X(the_geom)::numeric, 3) as ycoord, round(ST_Y(the_geom)::numeric, 3) as xcoord, the_geom
FROM
(
 SELECT a.ogc_fid, a.nummer, a.the_geom
 FROM stadt_bern.tsp_lv03 as a,
 (
   SELECT ST_GeomFromEWKB(the_wkb) as the_geom
   FROM
   (
    SELECT DISTINCT ST_AsEWKB((ST_DumpPoints(the_geom_lv03)).geom) as the_wkb
    FROM stadt_bern.dreiecke
   ) as r
 ) as b
 WHERE a.the_geom && b.the_geom
 AND st_distance(st_snaptogrid(a.the_geom, 0.0001::double precision), st_snaptogrid(b.the_geom, 0.0001::double precision)) = 0
) as c
WHERE geometrytype(the_geom) = 'POINT'
ORDER BY nummer;

ALTER TABLE stadt_bern.tsp_on_dreiecke_lv03_v OWNER TO av_chenyx06_stadt_be_admin;
GRANT SELECT ON TABLE stadt_bern.tsp_on_dreiecke_lv03_v TO av_chenyx06_stadt_be_user;
COMMENT ON VIEW stadt_bern.tsp_on_dreiecke_lv03_v IS 'TSP on Dreiecke LV03).';

INSERT INTO geometry_columns VALUES ('"', 'stadt_bern', 'tsp_on_dreiecke_lv03_v', 'the_geom', 2, '21781', 'POINT');

CREATE OR REPLACE VIEW stadt_bern.tsp_on_dreiecke_lv95_v AS 
SELECT DISTINCT ogc_fid, nummer, round(ST_X(the_geom)::numeric, 4) as ycoord, round(ST_Y(the_geom)::numeric, 4) as xcoord, the_geom
FROM
(
 SELECT a.ogc_fid, a.nummer, a.the_geom
 FROM stadt_bern.tsp_lv95 as a,
 (
   SELECT ST_GeomFromEWKB(the_wkb) as the_geom
   FROM
   (
    SELECT DISTINCT ST_AsEWKB((ST_DumpPoints(the_geom_lv95)).geom) as the_wkb
    FROM stadt_bern.dreiecke
   ) as r
 ) as b
 WHERE a.the_geom && b.the_geom
 AND st_distance(st_snaptogrid(a.the_geom, 0.0001::double precision), st_snaptogrid(b.the_geom, 0.0001::double precision)) = 0
) as c
WHERE geometrytype(the_geom) = 'POINT'
ORDER BY nummer;

ALTER TABLE stadt_bern.tsp_on_dreiecke_lv95_v OWNER TO av_chenyx06_stadt_be_admin;
GRANT SELECT ON TABLE stadt_bern.tsp_on_dreiecke_lv95_v TO av_chenyx06_stadt_be_user;
COMMENT ON VIEW stadt_bern.tsp_on_dreiecke_lv95_v IS 'TSP on Dreiecke LV95).';

INSERT INTO geometry_columns VALUES ('"', 'stadt_bern', 'tsp_on_dreiecke_lv95_v', 'the_geom', 2, '2056', 'POINT');


-- View fuer Test 'fehlende Tsp'
CREATE OR REPLACE VIEW stadt_bern.missing_tsp_lv95_in_lv03_v AS 
SELECT a.*
FROM stadt_bern.tsp_lv03 as a,
( 
 SELECT nummer FROM stadt_bern.tsp_lv03 EXCEPT SELECT nummer FROM stadt_bern.tsp_lv95
) as b
WHERE a.nummer = b.nummer;

ALTER TABLE stadt_bern.missing_tsp_lv95_in_lv03_v OWNER TO av_chenyx06_stadt_be_admin;
GRANT SELECT ON TABLE stadt_bern.missing_tsp_lv95_in_lv03_v TO av_chenyx06_stadt_be_user;
COMMENT ON VIEW stadt_bern.missing_tsp_lv95_in_lv03_v IS 'fehlende lv95-tsp).';

INSERT INTO geometry_columns VALUES ('"', 'stadt_bern', 'missing_tsp_lv95_in_lv03_v', 'the_geom', 2, '21781', 'POINT');

CREATE OR REPLACE VIEW stadt_bern.missing_tsp_lv03_in_lv95_v AS 
SELECT a.*
FROM stadt_bern.tsp_lv95 as a,
( 
 SELECT nummer FROM stadt_bern.tsp_lv95 EXCEPT SELECT nummer FROM stadt_bern.tsp_lv03
) as b
WHERE a.nummer = b.nummer;

ALTER TABLE stadt_bern.missing_tsp_lv03_in_lv95_v OWNER TO av_chenyx06_stadt_be_admin;
GRANT SELECT ON TABLE stadt_bern.missing_tsp_lv03_in_lv95_v TO av_chenyx06_stadt_be_user;
COMMENT ON VIEW stadt_bern.missing_tsp_lv03_in_lv95_v IS 'fehlende lv03-tsp.';

INSERT INTO geometry_columns VALUES ('"', 'stadt_bern', 'missing_tsp_lv03_in_lv95_v', 'the_geom', 2, '2056', 'POINT');


-- Tabelle fuer Ueberlappung:
-- Table: stadt_bern.triangle_overlap_lv03

-- DROP TABLE stadt_bern.triangle_overlap_lv03;

CREATE TABLE stadt_bern.triangle_overlap_lv03
(
  ogc_fid serial NOT NULL,
  error_type character varying,
  the_geom geometry,
  CONSTRAINT triangle_overlap_lv03_pkey PRIMARY KEY (ogc_fid),
  CONSTRAINT enforce_dims_the_geom CHECK (st_ndims(the_geom) = 2),
  CONSTRAINT enforce_geotype_the_geom CHECK (geometrytype(the_geom) = 'MULTIPOLYGON'::text OR the_geom IS NULL),
  CONSTRAINT enforce_srid_the_geom CHECK (st_srid(the_geom) = 21781)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE stadt_bern.triangle_overlap_lv03 OWNER TO av_chenyx06_stadt_be_admin;
GRANT ALL ON TABLE stadt_bern.triangle_overlap_lv03 TO av_chenyx06_stadt_be_admin;
GRANT SELECT ON TABLE stadt_bern.triangle_overlap_lv03 TO av_chenyx06_stadt_be_user;


INSERT INTO geometry_columns VALUES ('"', 'stadt_bern', 'triangle_overlap_lv03', 'the_geom', 2, '21781', 'MULTIPOLYGON');

-- Tabelle fuer Loecher
-- Table: stadt_bern.triangle_hole_lv03

-- DROP TABLE stadt_bern.triangle_hole_lv03;

CREATE TABLE stadt_bern.triangle_hole_lv03
(
  ogc_fid serial NOT NULL,
  error_type character varying,
  the_geom geometry,
  CONSTRAINT triangle_hole_lv03_pkey PRIMARY KEY (ogc_fid),
  CONSTRAINT enforce_dims_the_geom CHECK (st_ndims(the_geom) = 2),
  CONSTRAINT enforce_geotype_the_geom CHECK (geometrytype(the_geom) = 'MULTIPOLYGON'::text OR the_geom IS NULL),
  CONSTRAINT enforce_srid_the_geom CHECK (st_srid(the_geom) = 21781)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE stadt_bern.triangle_hole_lv03 OWNER TO av_chenyx06_stadt_be_admin;
GRANT ALL ON TABLE stadt_bern.triangle_hole_lv03 TO av_chenyx06_stadt_be_admin;
GRANT SELECT ON TABLE stadt_bern.triangle_hole_lv03 TO av_chenyx06_stadt_be_user;

INSERT INTO geometry_columns VALUES ('"', 'stadt_bern', 'triangle_hole_lv03', 'the_geom', 2, '21781', 'MULTIPOLYGON');
