__author__ = 'Roman'
import arcpy, os

#Remove temporary connection file if it already exists
sdeFile = r"C:\Project\Output\TempSDEConnectionFile.sde"
if os.path.exists(sdeFile):
    os.remove(sdeFile)

#Create temporary connection file in memory
arcpy.CreateArcSDEConnectionFile_management(r"C:\Project\Output", "TempConnection", "myServerName", "5151", "myDatabase", "DATABASE_AUTH", "myUserName", "myPassword", "SAVE_USERNAME", "myUser.DEFAULT", "SAVE_VERSION")

#Export a map document to verify that secured layers are present
mxd = arcpy.mapping.MapDocument(r"C:\Project\SDEdata.mxd")
arcpy.mapping.ExportToPDF(mxd, r"C:\Project\output\SDEdata.pdf")

os.remove(sdeFile)
del mxd__author__ = 'Administrator'
