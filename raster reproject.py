import arcpy, sys

InFolder = sys.argv[1]
OutFolder = sys.argv[2]
OutSR = arcpy.SpatialReference(32750)  # "WGS_1984_UTM_Zone_50S"

arcpy.env.workspace = InFolder

for Ras in arcpy.ListRasters():
    arcpy.AddMessage("Projecting " + Ras)
    arcpy.ProjectRaster_management(InFolder + "\\" + Ras, OutFolder + "\\" + Ras, OutSR)
arcpy.AddMessage("Projecting complete")