print "service definition draft created"  
    arcpy.AddMessage("service definition draft created")  
  
    # Set local variables  
    inSdFile = sd  
    con = "GIS Servers/arcgis on HPWS32_6080 (admin)"  
    inServer = con  
    inServiceName = 'districtwise' 
	inServiceName = InSdFile 	
    inCluster = "default"  
    inFolderType = "EXISTING"  
    inFolder = "weather"  
    inStartup = "STARTED"  
    inOverride = "OVERRIDE_DEFINITION"  
    inMyContents = "NO_SHARE_ONLINE"  
    inPublic = "PRIVATE"  
    inOrganization = "NO_SHARE_ORGANIZATION"  
    inGroups = ""  
  
    print "publishing local variables defined"  
    arcpy.AddMessage("publishing local variables defined")  
  
    # stage and upload the service if the sddraft analysis did not contain errors  
    if analysis['errors'] == {}:  
        # Execute StageService  
        arcpy.StageService_server(sddraft, sd)  
        print "StageService_server created"  
        arcpy.AddMessage("StageService_server created")  
        # Execute UploadServiceDefinition  
        arcpy.UploadServiceDefinition_server(inSdFile, inServer, inServiceName,   
                                     inCluster, inFolderType, inFolder,   
                                     inStartup, inOverride, inMyContents,   
                                     inPublic, inOrganization, inGroups)  
        print "Uploaded..."  
        arcpy.AddMessage("Uploaded..")  
  
    else:   
        # if the sddraft analysis contained errors, display them  
        print analysis['errors']  