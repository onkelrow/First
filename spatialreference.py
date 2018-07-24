import arcpy
sr = arcpy.SpatialReference(r"C:\Program Files (x86)\ArcGIS\Desktop10.0\Coordinate Systems\Projected Coordinate Systems\UTM\NAD 1983\NAD 1983 UTM Zone 10N.prj")

mxd = arcpy.mapping.MapDocument("current")
df = arcpy.mapping.ListDataFrames(mxd)[0]
df.spatialReference = sr