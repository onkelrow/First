import arcpy, os, sys, string, codecs

# def encode(text):
#     """
#     For printing unicode characters to the console.
#     """
#     return text.encode('utf-8')

#Remove temporary connection file if it already exists
# sdeFile = r"C:\Project\Output\TempSDEConnectionFile.sde"
# if os.path.exists(sdeFile):
#     os.remove(sdeFile)
#
# #Create temporary connection file in memory
# arcpy.CreateArcSDEConnectionFile_management(r"C:\Project\Output", "TempConnection", "myServerName", "5151", "myDatabase", "DATABASE_AUTH", "myUserName", "myPassword", "SAVE_USERNAME", "myUser.DEFAULT", "SAVE_VERSION")
#u'\xe4'.encode('ascii', 'ignore')
#Report service properties for layers in a map that support SERVICEPROPERTIES
outFile = open(r"E:\Data\check\checklayerdatasources.text", "w")
mxd = arcpy.mapping.MapDocument(r"E:\Data\check\120521_FIS_Deiche_event.mxd")
for lyr in arcpy.mapping.ListLayers(mxd):
    if lyr.supports("SERVICEPROPERTIES"):
    #if lyr.supports("DATASOURCE"):
        servProp = lyr.serviceProperties
        lyrdataProp = lyr.dataSource if lyr.supports("dataSource") else "N/A"
        #print "Layer name:" + lyr.name
        outFile.write ("Layer name:" + lyr.name.encode('utf-8') + "\n")
        outFile.write ("Service Type: " + servProp.get('ServiceType', 'N/A') +"\n")
        #outFile.write ("Layer Datasource:" + lyrdataProp.dataSource + "\n")
        outFile.write (lyrdataProp + "\n")
        #print "-----------------------------------------------------"
        # if lyr.serviceProperties["ServiceType"] != "SDE":
        #     print "Service Type: " + servProp.get('ServiceType', 'N/A')
        #     print "    URL:         " + servProp.get('URL', 'N/A')
        #     print "    Connection:  " + servProp.get('Connection', 'N/A')
        #     print "    Server:      " + servProp.get('Server', 'N/A')
        #     print "    Cache:       " + str(servProp.get('Cache', 'N/A'))
        #     print "    User Name:   " + servProp.get('UserName', 'N/A')
        #     print "    Password:    " + servProp.get('Password', 'N/A')
        #     print ""
    else:
        #     print "Service Type: " + servProp.get('ServiceType', 'N/A')
        #     print "    Database:       " + servProp.get('Database', 'N/A')
        #     print "    Server:         " + servProp.get('Server', 'N/A')
        #     print "    Service:        " + servProp.get('Service', 'N/A')
        #     print "    Version:        " + servProp.get('Version', 'N/A')
        #     print "    User name:      " + servProp.get('UserName', 'N/A')
        #     print "    Authentication: " + servProp.get('AuthenticationMode', 'N/A')
        print ""
#del mxd