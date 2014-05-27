psql -d postgres -c "CREATE ROLE av_chenyx06_be_superadmin LOGIN PASSWORD 'chenyx06';"
psql -d postgres -c "CREATE ROLE av_chenyx06_be_admin CREATEDB LOGIN PASSWORD 'chenyx06';"
psql -d postgres -c "CREATE ROLE av_chenyx06_be_user LOGIN PASSWORD 'chenyx06';"

createdb --owner av_chenyx06_be_admin chenyx06plus_be

psql -d chenyx06plus_be -f /usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql
psql -d chenyx06plus_be -f /usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql

psql -d chenyx06plus_be -c "GRANT ALL ON SCHEMA public TO av_chenyx06_be_admin;"
psql -d chenyx06plus_be -c "ALTER TABLE geometry_columns OWNER TO av_chenyx06_be_admin;"
psql -d chenyx06plus_be -c "GRANT ALL ON geometry_columns TO av_chenyx06_be_admin;"
psql -d chenyx06plus_be -c "GRANT ALL ON spatial_ref_sys TO av_chenyx06_be_admin;"
psql -d chenyx06plus_be -c "GRANT ALL ON geography_columns TO av_chenyx06_be_admin;"

psql -d chenyx06plus_be -c "GRANT SELECT ON geometry_columns TO av_chenyx06_be_user;"
psql -d chenyx06plus_be -c "GRANT SELECT ON spatial_ref_sys TO av_chenyx06_be_user;"
psql -d chenyx06plus_be -c "GRANT SELECT ON geography_columns TO av_chenyx06_be_user;"
