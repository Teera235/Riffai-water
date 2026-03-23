@echo off
echo Installing PostGIS on Cloud SQL...
echo.
echo When prompted for password, enter: riffai123
echo Then paste this SQL command:
echo.
echo CREATE EXTENSION IF NOT EXISTS postgis CASCADE;
echo CREATE EXTENSION IF NOT EXISTS postgis_topology;
echo \q
echo.
pause
gcloud sql connect riffai-db --user=postgres --database=riffai --project=trim-descent-452802-t2
