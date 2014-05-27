CREATE SCHEMA ch_default
  AUTHORIZATION av_chenyx06_be_superadmin;

GRANT USAGE ON SCHEMA ch_default TO av_chenyx06_be_user;
GRANT USAGE ON SCHEMA ch_default TO av_chenyx06_be_admin;
GRANT USAGE ON SCHEMA ch_default TO av_chenyx06_be_superadmin;


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
ALTER TABLE ch_default.tsp_lv03 OWNER TO av_chenyx06_be_superadmin;
GRANT SELECT ON ch_default.tsp_lv03 TO av_chenyx06_be_user;

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
ALTER TABLE ch_default.tsp_lv95 OWNER TO av_chenyx06_be_superadmin;
GRANT SELECT ON ch_default.tsp_lv95 TO av_chenyx06_be_user;

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
 SELECT a.nom as nummer, 1 as typ, ST_SnapToGrid(a.geom, 0.001) as the_geom
 FROM "tsp-lv03" as a
 ORDER by a.nom;

INSERT INTO ch_default.tsp_lv95 (nummer, typ, the_geom) 
 SELECT a.nom as nummer, 1 as typ, ST_SnapToGrid(a.geom, 0.001) as the_geom
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
ALTER TABLE ch_default.dreiecke_lv03_bearbeitung OWNER TO av_chenyx06_be_superadmin;
GRANT SELECT ON ch_default.dreiecke_lv03_bearbeitung TO av_chenyx06_be_user;

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
ALTER TABLE ch_default.dreiecke_lv95_bearbeitung OWNER TO av_chenyx06_be_superadmin;
GRANT SELECT ON ch_default.dreiecke_lv95_bearbeitung TO av_chenyx06_be_user;

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
 SELECT a.nummer as nummer, 1 as typ, ST_SnapToGrid(a.geom, 0.001) as the_geom
 FROM "dreiecke_lv03" as a
 ORDER BY a.nummer;

INSERT INTO ch_default.dreiecke_lv95_bearbeitung (nummer, typ, the_geom) 
 SELECT a.nummer as nummer, 1 as typ, ST_SnapToGrid(a.geom, 0.001) as the_geom
 FROM "dreiecke_lv95" as a
 ORDER BY a.nummer;


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
ALTER TABLE ch_default.dreiecke OWNER TO av_chenyx06_be_superadmin;
GRANT SELECT ON ch_default.dreiecke TO av_chenyx06_be_user;

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

-- Dreiecks-Views für WFS (Brauche ich die noch???)
CREATE OR REPLACE VIEW ch_default.dreiecke_lv03_v AS 
 SELECT ogc_fid, nummer, typ, the_geom_lv03 as the_geom
   FROM ch_default.dreiecke;

ALTER TABLE ch_default.dreiecke_lv03_v OWNER TO av_chenyx06_be_superadmin;
GRANT SELECT ON TABLE ch_default.dreiecke_lv03_v TO av_chenyx06_be_user;
COMMENT ON VIEW ch_default.dreiecke_lv03_v IS 'Def. Dreiecke LV03 fuer WFS).';

INSERT INTO geometry_columns VALUES ('"', 'ch_default', 'dreiecke_lv03_v', 'the_geom', 2, '21781', 'POLYGON');

CREATE OR REPLACE VIEW ch_default.dreiecke_lv95_v AS 
 SELECT ogc_fid, nummer, typ, the_geom_lv95 as the_geom
   FROM ch_default.dreiecke;

ALTER TABLE ch_default.dreiecke_lv95_v OWNER TO av_chenyx06_be_superadmin;
GRANT SELECT ON TABLE ch_default.dreiecke_lv95_v TO av_chenyx06_be_user;
COMMENT ON VIEW ch_default.dreiecke_lv95_v IS 'Def. Dreiecke LV95 fuer WFS).';

INSERT INTO geometry_columns VALUES ('"', 'ch_default', 'dreiecke_lv95_v', 'the_geom', 2, '2056', 'POLYGON');

-- Kopiert Dreiecke von temp. Tabelle in def. Dreiecks-Tabelle.
INSERT INTO ch_default.dreiecke (nummer, typ, the_geom_lv03, the_geom_lv95)
SELECT a.nummer, a.typ, ST_Reverse(ST_ForceRHR(a.the_geom)) as the_geom_lv03, ST_Reverse(ST_ForceRHR(b.the_geom)) as the_geom_lv95 
FROM ch_default.dreiecke_lv03_bearbeitung a, ch_default.dreiecke_lv95_bearbeitung b
WHERE a.nummer = b.nummer
ORDER BY a.nummer





