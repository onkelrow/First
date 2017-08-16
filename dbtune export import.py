import arcpy
ent_gdb = "C:\\gdbs\\enterprisegdb.sde"
output_file = "C:\\temp\\keyword.txt"
arcpy.ExportGeodatabaseConfigurationKeywords_management(ent_gdb,output_file)
