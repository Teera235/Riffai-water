@echo off
echo Installing PostGIS extension...
echo.

REM Create a temporary SQL file
echo CREATE EXTENSION IF NOT EXISTS postgis; > temp_postgis.sql
echo CREATE EXTENSION IF NOT EXISTS postgis_topology; >> temp_postgis.sql
echo GRANT ALL PRIVILEGES ON DATABASE riffai TO riffai; >> temp_postgis.sql
echo GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO riffai; >> temp_postgis.sql
echo GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO riffai; >> temp_postgis.sql
echo ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO riffai; >> temp_postgis.sql
echo ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO riffai; >> temp_postgis.sql

echo Running SQL commands...
gcloud sql connect riffai-db --user=postgres --database=riffai --project=trim-descent-452802-t2 < temp_postgis.sql

del temp_postgis.sql
echo.
echo Done!
