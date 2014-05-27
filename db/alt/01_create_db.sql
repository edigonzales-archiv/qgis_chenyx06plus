-- pgadmin3

CREATE ROLE av_chenyx06superadmin LOGIN PASSWORD 'chenyx06';
CREATE ROLE av_chenyx06admin CREATEDB LOGIN PASSWORD 'chenyx06';
CREATE ROLE av_chenyx06user LOGIN PASSWORD 'chenyx06';


# Konsole

sudo su postgres

createdb --owner av_chenyx06admin chenyx06plus
createlang plpgsql chenyx06plus

psql -d chenyx06plus -f /usr/share/postgresql/8.4/contrib/postgis-1.5/postgis.sql
psql -d chenyx06plus -f /usr/share/postgresql/8.4/contrib/postgis-1.5/spatial_ref_sys.sql



-- pgadmin3

GRANT ALL ON SCHEMA public TO av_chenyx06admin;

GRANT SELECT ON geometry_columns TO mspublic;
GRANT SELECT ON spatial_ref_sys TO mspublic;
GRANT SELECT ON geography_columns TO mspublic;
ALTER TABLE geometry_columns OWNER TO av_chenyx06admin;
GRANT SELECT ON spatial_ref_sys TO av_chenyx06admin;
GRANT SELECT ON geography_columns TO av_chenyx06admin;
GRANT SELECT ON geometry_columns TO av_chenyx06user;
GRANT SELECT ON spatial_ref_sys TO av_chenyx06user;
GRANT SELECT ON geography_columns TO av_chenyx06user;
