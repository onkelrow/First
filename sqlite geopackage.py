__author__ = '53_e_rv'
import arcpy

# Set local variables
sqlite_database_path = ‘C:\data\example.gpkg’

# Execute CreateSQLiteDatabase
arcpy.gp.CreateSQLiteDatabase(sqlite_database_path, “GEOPACKAGE”)