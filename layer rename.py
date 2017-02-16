__author__ = 'Administrator'
import arcpy
import os

#mxd = arcpy.mapping.MapDocument(r"C:\Users\Administrator\Desktop\ripsgdi14\wrrl\automated\layerrenamed\wrrl_k13_3.mxd")
mxd = arcpy.mapping.MapDocument(r"C:\Users\Administrator\Desktop\ripsgdi14\wrrl\automated\layerrenamed\wrrl_k13_3.mxd")
#mxd = arcpy.mapping.MapDocument("CURRENT")
for lyr in arcpy.mapping.ListLayers(mxd):
    if lyr.supports("DATASOURCE"):
        arcpy.AddMessage("Layer: " + lyr.name + "  Source: " + lyr.dataSource)

for lyr in arcpy.mapping.ListLayers(mxd):
    #lyrname = str(lyr.name)
    print lyrname
    #if lyrname == " ":
    #    lyrname_replaced = lyrname.replace(" ","1")
    #    lyr.name = lyrname_replaced
     #   arcpy.AddMessage(lyrname_replaced)

#mxd.save()

#arcpy.RefreshTOC()

for lyr in arcpy.mapping.ListLayers(mxd):
    if lyr.supports("DATASOURCE"):
        arcpy.AddMessage("Layer: " + lyr.name + "  Source: " + lyr.dataSource)

for lyr in arcpy.mapping.ListLayers(mxd):
    lyrname = str(lyr.name)
    print lyrname
    if lyrname == " ":
        lyrname_replaced = lyrname.replace(" ","1")
        lyr.name = lyrname_replaced
        arcpy.AddMessage(lyrname_replaced)

mxd.save()

arcpy.RefreshTOC()


