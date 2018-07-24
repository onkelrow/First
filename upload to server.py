#import modules
import arcpy, sys, os, string

#specify folder containing MXDs
inFolder = raw_input("Please enter folder containing 10.2 MXDs to Publish to ArcServer: ")

#specify connection File Path
connectionFilePath = r'C:\Users\53_e_rv\AppData\Roaming\ESRI\Desktop10.5\ArcCatalog\arcgis on ripsgdi18.lubw.bwl.de_6080 (admin).ags'

#look in folder for mxds
MapPath= []
MapFolder = os.listdir(inFolder)

for file in MapFolder:
    fileExt = os.path.splitext(file)[1]
    if fileExt == ".mxd":
        MapPath = os.path.join(inFolder, file)
        file = MapPath.strip('\'')
        mxd = arcpy.mapping.MapDocument(file)
        base = os.path.basename(file)
        serviceName = base[:-4]
        SDDraft = file[:-4] + ".sddraft"
        sd = file[:-4] + ".sd"

        #Create Map SD Draft
        print "\n" + "Publishing: " + base
        analysis = arcpy.mapping.CreateMapSDDraft(mxd, SDDraft, serviceName, "FROM_CONNECTION_FILE", connectionFilePath, "False", "wms",  "", "")

        # stage and upload the service if the sddraft analysis did not contain errors
        if analysis['errors'] == {}:
            # Execute StageService
            print "SD vorbereiten"
            arcpy.StageService_server(SDDraft, sd)
            # Execute UploadServiceDefinition
            print "Hochladen Service Definition"
            arcpy.UploadServiceDefinition_server(sd, connectionFilePath)
            print "Erstellen " + base +" geglueckt" + "\n"
        else:
            #pass
            # if the sddraft analysis contained errors, display them
            print analysis['errors']
    #continue
