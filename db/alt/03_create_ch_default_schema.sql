CREATE SCHEMA ch_default
  AUTHORIZATION av_chenyx06superadmin;

GRANT USAGE ON SCHEMA ch_default TO av_chenyx06user;
GRANT USAGE ON SCHEMA ch_default TO av_chenyx06admin;
GRANT USAGE ON SCHEMA ch_default TO av_chenyx06superadmin;


CREATE TABLE ch_default.tsp_lv03
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
ALTER TABLE ch_default.tsp_lv03 OWNER TO av_chenyx06superadmin;
GRANT SELECT ON ch_default.tsp_lv03 TO av_chenyx06user;

CREATE INDEX tsp_lv03_the_geom_gist
  ON ch_default.tsp_lv03
  USING gist
  (the_geom);

CREATE INDEX idx_tsp_lv03_nummer
  ON ch_default.tsp_lv03
  USING btree
  (nummer);

INSERT INTO geometry_columns VALUES ('"', 'ch_default', 'tsp_lv03', 'the_geom', 2, '21781', 'POINT');


CREATE TABLE ch_default.tsp_lv95
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
ALTER TABLE ch_default.tsp_lv95 OWNER TO av_chenyx06superadmin;
GRANT SELECT ON ch_default.tsp_lv95 TO av_chenyx06user;

CREATE INDEX tsp_lv95_the_geom_gist
  ON ch_default.tsp_lv95
  USING gist
  (the_geom);

CREATE INDEX idx_tsp_lv95_nummer
  ON ch_default.tsp_lv95
  USING btree
  (nummer);

INSERT INTO geometry_columns VALUES ('"', 'ch_default', 'tsp_lv95', 'the_geom', 2, '2056', 'POINT');



-- Kopiert TSP von temp. Tabelle in TSP-Tabelle.
INSERT INTO ch_default.tsp_lv03 (nummer, typ, the_geom) 
 SELECT a.nom as nummer, 1 as typ, ST_SnapToGrid(a.the_geom, 0.001) as the_geom
 FROM "tsp-lv03" as a
 ORDER by a.nom;

INSERT INTO ch_default.tsp_lv95 (nummer, typ, the_geom) 
 SELECT a.nom as nummer, 1 as typ, ST_SnapToGrid(a.the_geom, 0.001) as the_geom
 FROM "tsp-lv95" as a
 ORDER by a.nom;




-- Prueft ob Dreieckspunkte auf TSP liegen.
-- Leider noch zwei Funktionen fuer beide
-- Bezugsrahmen. -> SRID kann man aus Geometrie
-- rausholen und dann if/else...
CREATE OR REPLACE FUNCTION ch_default.triangle_on_tsp_lv03(triangle geometry) RETURNS integer AS $$
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
   FROM ch_default.tsp_lv03 as a,
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

CREATE OR REPLACE FUNCTION ch_default.triangle_on_tsp_lv95(triangle geometry) RETURNS integer AS $$
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
   FROM ch_default.tsp_lv95 as a,
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
CREATE TABLE ch_default.dreiecke_lv03_bearbeitung 
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
  CONSTRAINT enforce_triangle_on_tsp_the_geom CHECK(ch_default.triangle_on_tsp_lv03(the_geom) = 3)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE ch_default.dreiecke_lv03_bearbeitung OWNER TO av_chenyx06superadmin;
GRANT SELECT ON ch_default.dreiecke_lv03_bearbeitung TO av_chenyx06user;

CREATE INDEX dreiecke_lv03_bearbeitung_the_geom_gist
  ON ch_default.dreiecke_lv03_bearbeitung
  USING gist
  (the_geom);

CREATE INDEX idx_dreiecke_lv03_bearbeitung_nummer
  ON ch_default.dreiecke_lv03_bearbeitung
  USING btree
  (nummer);

INSERT INTO geometry_columns VALUES ('"', 'ch_default', 'dreiecke_lv03_bearbeitung', 'the_geom', 2, '21781', 'POLYGON');

CREATE TABLE ch_default.dreiecke_lv95_bearbeitung 
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
  CONSTRAINT enforce_triangle_on_tsp_the_geom CHECK(ch_default.triangle_on_tsp_lv95(the_geom) = 3)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE ch_default.dreiecke_lv95_bearbeitung OWNER TO av_chenyx06superadmin;
GRANT SELECT ON ch_default.dreiecke_lv95_bearbeitung TO av_chenyx06user;

CREATE INDEX dreiecke_lv95_bearbeitung_the_geom_gist
  ON ch_default.dreiecke_lv95_bearbeitung
  USING gist
  (the_geom);

CREATE INDEX idx_dreiecke_lv95_bearbeitung_nummer
  ON ch_default.dreiecke_lv95_bearbeitung
  USING btree
  (nummer);

INSERT INTO geometry_columns VALUES ('"', 'ch_default', 'dreiecke_lv95_bearbeitung', 'the_geom', 2, '2056', 'POLYGON');


-- Kopiert Dreiecke von temp. Tabelle in Dreiecks-Tabelle.
INSERT INTO ch_default.dreiecke_lv03_bearbeitung (nummer, typ, the_geom) 
 SELECT a.num as nummer, 1 as typ, ST_SnapToGrid(a.the_geom, 0.001) as the_geom
 FROM "dreiecke_lv03" as a
 ORDER BY a.num;

INSERT INTO ch_default.dreiecke_lv95_bearbeitung (nummer, typ, the_geom) 
 SELECT a.num as nummer, 1 as typ, ST_SnapToGrid(a.the_geom, 0.001) as the_geom
 FROM "dreiecke_lv95" as a
 ORDER BY a.num;


-- Dreieckstabelle anlegen.
CREATE TABLE ch_default.dreiecke 
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
ALTER TABLE ch_default.dreiecke OWNER TO av_chenyx06superadmin;
GRANT SELECT ON ch_default.dreiecke TO av_chenyx06user;

CREATE INDEX dreiecke_the_geom_lv03_gist
  ON ch_default.dreiecke
  USING gist
  (the_geom_lv03);

CREATE INDEX dreiecke_the_geom_lv95_gist
  ON ch_default.dreiecke
  USING gist
  (the_geom_lv95); 

CREATE INDEX idx_dreiecke_nummer
  ON ch_default.dreiecke 
  USING btree
  (nummer);  

INSERT INTO geometry_columns VALUES ('"', 'ch_default', 'dreiecke', 'the_geom_lv03', 2, '21781', 'POLYGON');
INSERT INTO geometry_columns VALUES ('"', 'ch_default', 'dreiecke', 'the_geom_lv95', 2, '2056', 'POLYGON');



-- LookUp Table: Dreiecke-TSP
CREATE TABLE ch_default.dreiecke_tsp
(
  ogc_fid serial NOT NULL,
  tsp_nummer character varying NOT NULL,
  dreieck_nummer character varying NOT NULL,
  CONSTRAINT dreiecke_tsp_pkey PRIMARY KEY (ogc_fid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE ch_default.dreiecke_tsp OWNER TO av_chenyx06superadmin;
GRANT ALL ON TABLE ch_default.dreiecke_tsp TO av_chenyx06superadmin;
GRANT SELECT ON TABLE ch_default.dreiecke_tsp TO av_chenyx06user;

CREATE INDEX idx_dreiecke_tsp_dreieck_nummer
  ON ch_default.dreiecke_tsp
  USING btree
  (dreieck_nummer);

CREATE INDEX idx_dreiecke_tsp_tsp_nummer
  ON ch_default.dreiecke_tsp
  USING btree
  (tsp_nummer);




-- Das ist nur für ch_default: Kann/muss ja
-- dann jeweils auf Knopfdruck nachgeführt werden.
-- Ob LV03/LV95 ist eigentlich Wurst resp.
-- kann angepasst werden.


-- Daten in Lookup-Table schreiben.
INSERT INTO ch_default.dreiecke_tsp (tsp_nummer, dreieck_nummer) 
SELECT tsp_nummer, dreieck_nummer
FROM
(
 SELECT a.nummer as tsp_nummer, b.nummer as dreieck_nummer
 FROM ch_default.tsp_lv03 as a,
 (
   SELECT nummer, (ST_DumpPoints(the_geom)).geom as the_geom
   FROM
   (
     SELECT nummer, ST_RemovePoint(ST_Boundary(ST_Reverse(ST_ForceRHR(the_geom))),3) as the_geom 
     FROM ch_default.dreiecke_lv03_bearbeitung  ORDER BY nummer 
   ) as c
 ) as b
 WHERE a.the_geom && b.the_geom
 AND ST_Intersects(ST_SnapToGrid(a.the_geom, 0.001), ST_SnapToGrid(b.the_geom, 0.001)) 
) as d;



-- Daten Dreieckstabelle schreiben.
-- So *sollten* sie gleich definiert sein (also Punkt-
-- reihenfolge), da gleich berechnet (aber das ja eigentlich
-- noch keine Garantie ist...).
INSERT INTO ch_default.dreiecke (nummer, typ, the_geom_lv03, the_geom_lv95)

SELECT a.dreieck_nummer as nummer, a.typ, ST_SnapToGrid(a.the_geom, 0.001) as the_geom_lv03, ST_SnapToGrid(b.the_geom, 0.001) as the_geom_lv95
FROM
(
 SELECT dreieck_nummer, typ, ST_Reverse(ST_ForceRHR(ST_BuildArea(the_geom))) as the_geom 
 FROM
 (
  SELECT dreieck_nummer, typ, ST_AddPoint(the_geom, ST_PointN(the_geom,1)) as the_geom
  FROM
  (
   SELECT dreieck_nummer, typ, ST_LineFromMultiPoint(ST_Collect(the_geom)) as the_geom
   FROM
   (
    SELECT dreieck_nummer, typ, the_geom as the_geom
    FROM ch_default.tsp_lv03 as a,
    (
     SELECT *
     FROM ch_default.dreiecke_tsp
    ) as b
    WHERE b.tsp_nummer = a.nummer
   ) as c
   GROUP BY dreieck_nummer, typ
  ) as d
 ) as e
) as a,
(
 SELECT dreieck_nummer, typ, ST_Reverse(ST_ForceRHR(ST_BuildArea(the_geom))) as the_geom 
 FROM
 (
  SELECT dreieck_nummer, typ, ST_AddPoint(the_geom, ST_PointN(the_geom,1)) as the_geom
  FROM
  (
   SELECT dreieck_nummer, typ, ST_LineFromMultiPoint(ST_Collect(the_geom)) as the_geom
   FROM
   (
    SELECT dreieck_nummer, typ, the_geom as the_geom
    FROM ch_default.tsp_lv95 as a,
    (
     SELECT *
     FROM ch_default.dreiecke_tsp
    ) as b
    WHERE b.tsp_nummer = a.nummer
   ) as c
   GROUP BY dreieck_nummer, typ
  ) as d
 ) as e
) as b
WHERE a.dreieck_nummer = b.dreieck_nummer
ORDER BY a.dreieck_nummer;

