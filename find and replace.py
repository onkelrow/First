# #import arcpy
# import arcpy, os
#
# for root, dirs, files in os.walk(r"C:\Project"):
#
#         for f in files:
#             if f.endswith(".mxd"):
#                 mxd = root + '\\' + f
#                 #analysis = arcpy.mapping.AnalyzeForMSD(mxd)
# #mxd = arcpy.mapping.MapDocument(r"C:\Users\Administrator\Desktop\ripsgdi14\wrrl\automated\wrrl_k_bwp_2_2.mxd")
#                 mxd.findAndReplaceWorkspacePaths(r"\\Itzgs2\WRRL_BW", r"\\ripsagsdata\data\Internet\ripsgdi\wrrl_bw")
# mxd.saveACopy(r"C:\Users\Administrator\Desktop\ripsgdi14\wrrl\automated\wrrl_k_bwp_2_2_neu.mxd")
# del mxd

# import arcpy, os
# from arcpy import env
# arcpy.env.overwriteOutput = True
# ws = r"C:\Users\Administrator\Desktop\ripsgdi14\wrrl"
# #oldpath = r"\\Itzgs2\WRRL_BW"
# #oldbase = r"C:\Base Data"
# #newpath = r"\\ripsagsdata\data\Internet\ripsgdi\wrrl_bw"
# #newbase = r"C:\Users\mittcla\Documents\Base Data"
# for root, dirs, files in os.walk(ws):
#     for f in files:
#         if f.endswith('.mxd'):
#             fullpath = os.path.join(root,f)
#             mxd = arcpy.mapping.MapDocument(fullpath)
#             print "Replacing path for " + f +"..."
#             #mxd.findAndReplaceWorkspacePaths(oldpath, newpath)
#             #mxd.findAndReplaceWorkspacePaths(oldbase, newbase)
#             mxd.findAndReplaceWorkspacePaths(r"\\Itzgs2\WRRL_BW", r"\\ripsagsdata\data\Internet\ripsgdi\wrrl_bw")
#             mxd.saveACopy(r"C:\Users\Administrator\Desktop\ripsgdi14\wrrl\automated")
#             del mxd

__author__ = 'Roman'
import arcpy, os#workspace to search for MXDs
Workspace = r"C:\Users\Administrator\Desktop\ripsgdi14\wrrl"
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
        #mxd.findAndReplaceWorkspacePaths(r"C:\Users\Administrator\AppData\Roaming\ESRI\Desktop10.0\ArcCatalog\Connection to Direct_lfu_webview_11g_sde_neu.sde",
                                 #r"C:\Users\Administrator\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\Connection to direct_lfu_webview_geodbtemp.sde", False)
        mxd.findAndReplaceWorkspacePaths(r"\\Itzgs2\WRRL_BW", r"\\ripsagsdata\data\Internet\ripsgdi\WRRL_BW")
        mxd.findAndReplaceWorkspacePaths(r"\\Itzgs2\fix_data\WRRL_BW", r"\\ripsagsdata\data\fix_data\WRRL_BW")
    except Exception as e:
        print e.message
    #set relative paths property
    mxd.relativePaths = False
    output = os.path.join(r"C:\Users\Administrator\Desktop\ripsgdi14\wrrl\automated", basename)
    #save map doucment change
    mxd.saveACopy (output)
    #mxd.saveACopy(r"E:\data\Vicente\Oracle11\Schutzgebiete_kombiniert_neu.mxd")
    del mxd, mapdoc