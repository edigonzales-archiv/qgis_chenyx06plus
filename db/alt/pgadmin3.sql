/*
INSERT INTO bern.tsp (nummer, typ, the_geom_lv03, the_geom_lv95) 
 SELECT a.nom as nummer, 1 as typ, ST_SnapToGrid(a.the_geom, 0.001) as the_geom_lv03, ST_SnapToGrid(b.the_geom, 0.001) as the_geom_lv95
 FROM "tsp-lv03" as a, "tsp-lv95" as b
 WHERE a.nom = b.nom

DELETE   FROM bern.tsp



CREATE TABLE bern.tsp
(
  ogc_fid serial NOT NULL UNIQUE,
  nummer character varying UNIQUE,
  typ integer,
  the_geom_lv03 geometry,
  the_geom_lv95 geometry,  
  CONSTRAINT tsp_pkey PRIMARY KEY (ogc_fid),
  CONSTRAINT enforce_dims_the_geom_lv03 CHECK (st_ndims(the_geom_lv03) = 2),
  CONSTRAINT enforce_geotype_the_geom_lv03 CHECK (geometrytype(the_geom_lv03) = 'POINT'::text OR the_geom_lv03 IS NULL),
  CONSTRAINT enforce_srid_the_geom_lv03 CHECK (st_srid(the_geom_lv03) = 21781),
  CONSTRAINT enforce_dims_the_geom_lv95 CHECK (st_ndims(the_geom_lv95) = 2),
  CONSTRAINT enforce_geotype_the_geom_lv95 CHECK (geometrytype(the_geom_lv95) = 'POINT'::text OR the_geom_lv95 IS NULL),
  CONSTRAINT enforce_srid_the_geom_lv95 CHECK (st_srid(the_geom_lv95) = 2056)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE bern.tsp OWNER TO stefan;


INSERT INTO geometry_columns VALUES ('"', 'bern', 'tsp', 'the_geom_lv03', 2, '21781', 'POINT');
INSERT INTO geometry_columns VALUES ('"', 'bern', 'tsp', 'the_geom_lv95', 2, '2056', 'POINT');


ALTER TABLE dreiecke_lv03  ADD CONSTRAINT enforce_triangle_the_geom CHECK(st_npoints(the_geom)= 4); 

select st_npoints(the_geom),*
from dreiecke_lv03
where st_npoints(the_geom) <> 3
limit 10


SELECT count(*)::integer FROM simon.parcel p WHERE ST_Covers(p.geom,$1);


SELECT astext((ST_DumpPoints(the_geom)).geom)
FROM dreiecke_lv03
WHERE nom = 'BEYYYY'


SELECT CASE WHEN count(*)=3 THEN 1::boolean ELSE 0::boolean END
FROM
(
 SELECT 1 as ogc_fid, ST_Intersection(b.the_geom, a.the_geom_lv03) as the_geom
 FROM bern.tsp as a,
 (
  SELECT ST_Collect(geom) as the_geom
  FROM
  (
   SELECT (ST_DumpPoints(the_geom)).geom
   FROM dreiecke_lv03
   WHERE nom = 'BEYYYY'
  ) as a
 ) as b
 WHERE ST_Intersects(b.the_geom, a.the_geom_lv03)
) as c
WHERE geometrytype(the_geom) = 'POINT'

*/
SELECT count(*)
FROM
(
 SELECT 1 as ogc_fid, ST_Intersection(ST_SnapToGrid(b.the_geom, 0.001), ST_SnapToGrid(a.the_geom_lv03, 0.001)) as the_geom
 FROM bern.tsp as a,
 (
  SELECT ST_Collect(geom) as the_geom
  FROM
  (
   SELECT (ST_DumpPoints(the_geom)).geom
   FROM dreiecke_lv03
   WHERE num = 'AG0001'
  ) as a
 ) as b
 WHERE a.the_geom_lv03 && b.the_geom--ST_Intersects(b.the_geom, ST_Buffer(a.the_geom_lv03, 0.1))
) as c
WHERE geometrytype(the_geom) = 'POINT'


ALTER TABLE dreiecke_lv03 ADD CONSTRAINT enforce_triangle_on_tsp_the_geom CHECK(bern.triangle_on_tsp(the_geom) = 3); 

select bern.triangle_on_tsp(the_geom), num, nom
from dreiecke_lv03
limit 100
