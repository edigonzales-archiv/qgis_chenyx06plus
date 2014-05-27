#!/bin/bash
source conf_anpassen.sh

sed -i "s/SUPERADMIN/$SUPERADMIN/" 01_create_db.sh
sed -i "s/ADMIN/$ADMIN/" 01_create_db.sh
sed -i "s/USER/$USER/" 01_create_db.sh
sed -i "s/DB_NAME/$DB_NAME/" 01_create_db.sh

sed -i "s/DB_NAME/$DB_NAME/" 02_import_tmp_data.sh

sed -i "s/SUPERADMIN/$SUPERADMIN/" 03_create_ch_default_schema.sql
sed -i "s/ADMIN/$ADMIN/" 03_create_ch_default_schema.sql
sed -i "s/USER/$USER/" 03_create_ch_default_schema.sql

sed -i "s/SUPERADMIN/$SUPERADMIN/" 04_create_local_schema.sql
sed -i "s/ADMIN/$ADMIN/" 04_create_local_schema.sql
sed -i "s/USER/$USER/" 04_create_local_schema.sql
sed -i "s/LOCAL_SCHEMA/$LOCAL_SCHEMA/g" 04_create_local_schema.sql

sed -i "s/DB_NAME/$DB_NAME/" 05_create_schemas.sh
