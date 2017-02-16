__author__ = 'Administrator'
import arcpy, os#workspace to search for MXDs
Workspace = r"C:\temp"
arcpy.env.workspace = Workspace
#list map documents in folder
mxdList = arcpy.ListFiles("*.mxd")
#set relative path setting for each MXD in list.
for mapdoc in mxdList:
    #set map document to change
    filePath = os.path.join(Workspace, mapdoc)
    mxd = arcpy.mapping.MapDocument(filePath)
    #Get the file name
    basename = mapdoc
    try:
        mxd.findAndReplaceWorkspacePaths(r"C:\Users\Administrator\AppData\Roaming\ESRI\Desktop10.0\ArcCatalog\Connection to Direct_lfu_webview_11g_sde_neu.sde",
                                 r"C:\Users\Administrator\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\Connection to direct_lfu_webview_geodbtemp.sde", False)
    except Exception as e:
        print e.message
    #set relative paths property
    mxd.relativePaths = False
    output = os.path.join(r"C:\temp\neue mxd", basename)
    #save map doucment change
    mxd.saveACopy (output)
    #mxd.saveACopy(r"E:\data\Vicente\Oracle11\Schutzgebiete_kombiniert_neu.mxd")
    del mxd, mapdoc
# import arcpy
# mxd = arcpy.mapping.MapDocument(r"C:\Users\Administrator\Desktop\UIS_0100000005800001_neu.mxd")
# mxd.findAndReplaceWorkspacePaths(r"Database Connections\Connection to direct_geo_sde_db_rac.sde",
#                                 r"Database Connections\Connection to direct_lfu_webview_geodbtemp.sde")
# mxd.saveACopy(r"C:\Users\Administrator\Desktop\UIS_0100000005800001_neu_3.mxd")
# del mxd

#