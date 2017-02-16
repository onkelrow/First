__author__ = '53_e_rv'

# -*- coding: utf-8 -*-
import arcpy

# set the workspace
arcpy.env.workspace = 'Database Connections/Connection sde to sdetest.sde'

# set a variable for the workspace
workspace = arcpy.env.workspace

#ent_gdb = "C:\\gdbs\\enterprisegdb.sde"
output_file = "C:\\keyword.txt"
#arcpy.ExportGeodatabaseConfigurationKeywords_management(ent_gdb,output_file)
arcpy.ExportGeodatabaseConfigurationKeywords_management(workspace,output_file)