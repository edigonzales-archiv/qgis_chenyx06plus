psql -d postgres -c "CREATE ROLE SUPERADMIN LOGIN PASSWORD 'chenyx06';"
psql -d postgres -c "CREATE ROLE ADMIN CREATEDB LOGIN PASSWORD 'chenyx06';"
psql -d postgres -c "CREATE ROLE USER LOGIN PASSWORD 'chenyx06';"

createdb --owner ADMIN DB_NAME

psql -d DB_NAME -f /usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql
psql -d DB_NAME -f /usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql

psql -d DB_NAME -c "GRANT ALL ON SCHEMA public TO ADMIN;"
psql -d DB_NAME -c "ALTER TABLE geometry_columns OWNER TO ADMIN;"
psql -d DB_NAME -c "GRANT ALL ON geometry_columns TO ADMIN;"
psql -d DB_NAME -c "GRANT ALL ON spatial_ref_sys TO ADMIN;"
psql -d DB_NAME -c "GRANT ALL ON geography_columns TO ADMIN;"

psql -d DB_NAME -c "GRANT SELECT ON geometry_columns TO USER;"
psql -d DB_NAME -c "GRANT SELECT ON spatial_ref_sys TO USER;"
psql -d DB_NAME -c "GRANT SELECT ON geography_columns TO USER;"
