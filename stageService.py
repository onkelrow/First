# ---------------------------------------------------------------------------
# stageService.py
# Created on: 2014-10-30 
# Usage: 
# Description: 
# ---------------------------------------------------------------------------

# Set the necessary product code

# Import arcpy module
import arcpy, sys, os, string


def encode(text):
#     """
#     For printing unicode characters to the console.
#     """
    return text.encode('utf-8')

#Arcgisserver Connection file
connectionFilePath = r'C:\Users\administrator\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\arcgis on ripsproc2014_6080 (admin).ags'

# pruefen der Projektdateien
MapPath = []


def stageService():
    try:
        inFolder = raw_input("10.2 Mxd's ")

        MapFolder = os.listdir(inFolder)

        for file in MapFolder:
            processFile(file)

    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
        arcpy.AddError(arcpy.GetMessages(2))
    except Exception as e:
        print e.args[0]
        arcpy.AddError(e.args[0])


def processFile(file):
    try:
        fileExt = os.path.splitext(file)[1]
        if fileExt == ".mxd":
            MapPath = os.path.join(inFolder, file)
            file = MapPath.strip('\'')
            mxd = arcpy.mapping.MapDocument(file)
            base = os.path.basename(file)
            serviceName = base[:-4]
            SDDraft = file[:-4] + ".sddraft"
            sd = file[:-4] + ".sd"

            #erstellen des Servicefiles als sd draft
            print "\n" + "Publishing: " + base

            analysis = arcpy.mapping.CreateMapSDDraft(mxd, SDDraft, serviceName, "FROM_CONNECTION_FILE",
                                                      connectionFilePath, "False", "", "None", "None")
            arcpy.StageService_server(SDDraft, sd)
            #sofern keine fehler beim Ueberpruefen zur bereitstellung erfolgt sind erstelle einen Dienst fuer den mapservice
            arcpy.UploadServiceDefinition_server(sd, connectionFilePath)

    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
        arcpy.AddError(arcpy.GetMessages(2))
    except Exception as e:
        print e.args[0]
        arcpy.AddError(e.args[0])


# This test allows the script to be used from the operating
# system command prompt (stand-alone), in a Python IDE, 
# as a geoprocessing script tool, or as a module imported in
# another script
if __name__ == '__main__':
    # Arguments are optional
    argv = tuple(arcpy.GetParameterAsText(i)
                 for i in range(arcpy.GetArgumentCount()))
    stageService()








