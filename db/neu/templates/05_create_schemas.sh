#!/bin/bash

psql -d DB_NAME -f 03_create_ch_default_schema.sql
psql -d DB_NAME -f 04_create_local_schema.sql
