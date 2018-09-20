# D A T E N E X P O R T  D O B  E T R S 8 9
#
# Autor:        Barbara Herwig
# Erstellt am:  15.08.2018
# Beschreibung:
# Export DOB-Daten von ITZGS2 in ETRS89
#
# letzte Aenderungen am:   03.09.2018
# letzte Aenderungen von:  F.Wagner
# letzte Aenderung: Auslagern der Eingangsparamter AOI und ZIELVERZEICHNIS zum externen Aufruf ueber Batch-Skript, Kombination DOP und DOP_SW
#
# Bsiepielaufruf: Python <Path>SRRM_ETRS89_DOP_DOPSW.py E:\TEMP\aoi.shp F:\gis_data
#
#######################################################################################################################

import sys, os, arcpy, time, shutil
from arcpy import env
from arcpy.sa import *
from shutil import copyfile

arcpy.env.overwriteOutput = True


# in eine LogDatei schreiben und auf der CommandLine ausgeben
#######################################################################################################################
def logIt(myString, myLogPathFile):
    try:
        myLogFile = open(myLogPathFile, "a")
    except IOError:  # EA-Fehler
        print 'Konnte Datei ' + myLogPathFile + ' nicht oeffnen'
    else:
        myLogFile.write(myString + "\n")
        myLogFile.close


def myLogPrint(myString, myLogPathFile):
    print myString
    logIt(myString, myLogPathFile)


# Skript Input Parameter
#######################################################################################################################

# Toolparamater
# Auschneide-geometrie
# AOI = r'D:\DATENABGABE\2018_08_31_Test_Gis_Data_Export\extent.shp'
AOI = sys.argv[1]  # Beispiel E:\TEMP\aoi.shp

# Ablageordner
# ZIELVERZEICHNIS = r'D:\DATENABGABE\2018_08_31_Test_Gis_Data_Export'
ZIELVERZEICHNIS = sys.argv[2]  # Beispiel F:\gis_data

# LogDatei: Wird eine Ebene hoeher als Export-Daten ausgegeben
myLogDatei = os.path.abspath(os.path.join(os.path.dirname(ZIELVERZEICHNIS), '.')) + "\\__loggmich__" + time.strftime(
    "%Y_%m_%d__%H_%M_%S", time.localtime()) + ".txt"

# lokale Variablen...
#######################################################################################################################
myLogPrint("\t Basis Pfade", myLogDatei)
myLogPrint("\t\t Output-Wurzelverzeichnis ist: \t\t" + ZIELVERZEICHNIS, myLogDatei)

# Blattschnitt Kilometerquadrant (Orthophoto)
# temporaere Ablage bis UIS-Update
BS_DOP = r'E:\WIBAS_2018_11\_TOOLS\ErsatzArcView\Daten\Joachim_Nov_2018.gdb\UIS_0100000017200002'
# Blattschnitt fuer AOI
BS_DOB_AOI = ZIELVERZEICHNIS + "\\Dateneingang_ETRS89.gdb\Blattschnitt_Orthobilder"
# DOB auf ITZGS2
ORTHO_ITZGS2 = r'\\itzgs2\gis_data_Auslieferung_ETRS89_November_2018\rips\images\dop'
ORTHO_SW = r'\\itzgs2\gis_data_Auslieferung_ETRS89_November_2018\rips\images\dop_sw'
# Original-Image Catalog landesweit
# Lokale Kopie mit angpassten Pfaden
IMAGE_CATALOG_ORIG = r'E:\WIBAS_2018_11\_TOOLS\ErsatzArcView\Daten\gc_dobco_jpg.dbf'
# IMAGE_CATALOG_ORIG = r'\\itzgs2\gis_data_Auslieferung_ETRS89_November_2018\rips\images\catalog\gc_dobco_jpg.dbf'
# Image Catalog fuer AOI
IMAGE_CATALOG_AOI = ZIELVERZEICHNIS + "\\dop\_ic_dobco_jpg.dbf"

# Ergebnisse...
#######################################################################################################################
OUTPUT = ZIELVERZEICHNIS + "\\dop"
OUTPUT_SW = ZIELVERZEICHNIS + "\\dop_sw"

# Steuerung fuer den Ablauf...
#######################################################################################################################
myLogPrint("\n\n", myLogDatei)
myLogPrint("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++", myLogDatei)
myLogPrint(" Skript zur Ausgabe AAA-Daten fuer SSRM startet: " + time.strftime("%Y_%m_%d__%H_%M_%S", time.localtime()),
           myLogDatei)
myLogPrint("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++", myLogDatei)
myLogPrint("\n", myLogDatei)
myLogPrint("\n\t Steuerung fuer den Ablauf wird initialisiert...", myLogDatei)

doDateneingang = 1  # Pruefen ob FGDB fuer Ausgabe vorhanden ist
doInputCheck = 1  # checken ob alle benoetigten Datensaetze im Inputverzeichnis gefunden werden
doBS = 1  # BS ausschneiden
doAuswahl = 1  # Auswahl nach AOI
doAuswahl_SW = 1  # Auswahl DOP_SW
doIMAGECATALOG = 1  # ImageCatalog erstellen

# Pruefen ob in Zielverzeichnis FGDB Dateneingang vorhanden ist. Falls nicht wird es angelegt
#######################################################################################################################
myLogPrint("\n\n", myLogDatei)
myLogPrint("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++", myLogDatei)
myLogPrint(" Pruefen ob Zielverzeichnis zur Ablage der Ergebnisse vorhanden ist", myLogDatei)
myLogPrint("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++", myLogDatei)

if doDateneingang == 1:

    if arcpy.Exists(OUTPUT):
        myLogPrint(" Ordner fuer Ouput ist vorhanden", myLogDatei)
    else:
        myLogPrint(" Ordner fuer Ouput und wird angelegt", myLogDatei)
        os.makedirs(OUTPUT)

else:
    myLogPrint("\t uebersprungen", myLogDatei)

# Inputdatensaetze suchen
#######################################################################################################################
myLogPrint("\n\n", myLogDatei)
myLogPrint("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++", myLogDatei)
myLogPrint(" Input-Datenquellen werden gesucht", myLogDatei)
myLogPrint("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++", myLogDatei)

if doInputCheck == 1:

    tmp = 1

    # Blattschnitt Kilometerquadrant (Orthophoto)
    myLogPrint("\t\t BS_DOB...", myLogDatei)
    if arcpy.Exists(BS_DOP):
        myLogPrint("\t\t vorhanden", myLogDatei)
    else:
        myLogPrint("\t\t nicht vorhanden " + BS_DOB, myLogDatei)
        tmp = 0

    # Image Catalog
    myLogPrint("\t\t Image Catalog...", myLogDatei)
    if arcpy.Exists(IMAGE_CATALOG_ORIG):
        myLogPrint("\t\t vorhanden", myLogDatei)
    else:
        myLogPrint("\t\t nicht vorhanden " + IMAGE_CATALOG_ORIG, myLogDatei)
        tmp = 0

    if tmp == 0:
        myLogPrint("\n\n   ---> Mindestens ein Datensatz wurde nicht gefunden.", myLogDatei)
        tmp = raw_input("        fortfahren? (j/n): ")
        if tmp != "j":
            sys.exit()
    else:
        myLogPrint("\n\n   Inputdatensatzpruefung ok.", myLogDatei)

else:
    myLogPrint("\t uebersprungen", myLogDatei)

# FGDB erstellen

arcpy.CreateFileGDB_management(ZIELVERZEICHNIS, "Dateneingang_ETRS89.gdb", "CURRENT")

# BS
#######################################################################################################################
myLogPrint("\n\n", myLogDatei)
myLogPrint("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++", myLogDatei)
myLogPrint(" BS ausschneiden", myLogDatei)
myLogPrint("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++", myLogDatei)

if doBS == 1:

    # Blattschnitt Kilometerquadrant (Orthophoto)
    if arcpy.Exists("LAYER"):
        arcpy.gp.delete("LAYER")

    arcpy.MakeFeatureLayer_management(BS_DOP, "LAYER")
    arcpy.SelectLayerByLocation_management("LAYER", "INTERSECT", AOI)
    arcpy.CopyFeatures_management("LAYER", BS_DOB_AOI, "", "0", "0", "0")
    arcpy.SelectLayerByAttribute_management("LAYER", "CLEAR_SELECTION", "")

else:
    myLogPrint("\t uebersprungen", myLogDatei)

# --> Select nur fuer ausgewaehlte Themen
#######################################################################################################################
myLogPrint("\n\n", myLogDatei)
myLogPrint("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++", myLogDatei)
myLogPrint(" Auswahl der Dateien nach AOI", myLogDatei)
arcpy.AddMessage("Auswahl der Dateien nach AOI")
myLogPrint("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++", myLogDatei)

if doAuswahl == 1:

    fields = ['OBJECT_ID', 'KB']
    with arcpy.da.SearchCursor(BS_DOB_AOI, fields) as cursor:
        for row in cursor:
            ORDNER = row[1]

            BS_NR = (str(row[0])[0:-2])
            BS_NR_01 = (str(row[0])[:-6])
            BS_NR_02 = (str(row[0])[5:-2])

            if ORDNER <> None:

                if os.path.exists(OUTPUT + "\\" + ORDNER):
                    print "Gibt es bereits"
                else:
                    os.makedirs(OUTPUT + "\\" + ORDNER)

                ORIGINAL_JPG = ORTHO_ITZGS2 + "\\" + ORDNER + "\\FDOP20_" + BS_NR_01 + "_" + BS_NR_02 + "_rgbi.jpg"
                NEU_JPG = OUTPUT + "\\" + ORDNER + "\\FDOP20_" + BS_NR_01 + "_" + BS_NR_02 + "_rgbi.jpg"

                if os.path.exists(ORIGINAL_JPG):
                    copyfile(ORIGINAL_JPG, NEU_JPG)
                else:
                    print " Fehler bei " + str(BS_NR)

                ORIGINAL_JGW = ORTHO_ITZGS2 + "\\" + ORDNER + "\\FDOP20_" + BS_NR_01 + "_" + BS_NR_02 + "_rgbi.jgw"
                NEU_JGW = OUTPUT + "\\" + ORDNER + "\\FDOP20_" + BS_NR_01 + "_" + BS_NR_02 + "_rgbi.jgw"

                if os.path.exists(ORIGINAL_JGW):
                    copyfile(ORIGINAL_JGW, NEU_JGW)
                else:
                    print " Fehler bei " + str(BS_NR)

else:
    myLogPrint("\t uebersprungen", myLogDatei)

myLogPrint("\t ...beendet", myLogDatei)

# DOP_SW ausschneiden

if doAuswahl_SW == 1:

    fields = ['OBJECT_ID', 'KB']
    with arcpy.da.SearchCursor(BS_DOB_AOI, fields) as cursor:
        for row in cursor:
            ORDNER_SW = row[1]

            BS_NR = (str(row[0])[0:-2])
            BS_NR_01 = (str(row[0])[:-6])
            BS_NR_02 = (str(row[0])[5:-2])

            if ORDNER_SW <> None:

                if os.path.exists(OUTPUT_SW + "\\" + ORDNER_SW):
                    print "Gibt es bereits"
                else:
                    os.makedirs(OUTPUT_SW + "\\" + ORDNER_SW)

                ORIGINAL_JPG_SW = ORTHO_SW + "\\" + ORDNER_SW + "\\FDOP20_" + BS_NR_01 + "_" + BS_NR_02 + "_rgbi.jpg"
                NEU_JPG_SW = OUTPUT_SW + "\\" + ORDNER_SW + "\\FDOP20_" + BS_NR_01 + "_" + BS_NR_02 + "_rgbi.jpg"

                if os.path.exists(ORIGINAL_JPG_SW):
                    copyfile(ORIGINAL_JPG_SW, NEU_JPG_SW)
                else:
                    print " Fehler bei " + str(BS_NR)

                ORIGINAL_JGW_SW = ORTHO_SW + "\\" + ORDNER_SW + "\\FDOP20_" + BS_NR_01 + "_" + BS_NR_02 + "_rgbi.jgw"
                NEU_JGW_SW = OUTPUT_SW + "\\" + ORDNER_SW + "\\FDOP20_" + BS_NR_01 + "_" + BS_NR_02 + "_rgbi.jgw"

                if os.path.exists(ORIGINAL_JGW_SW):
                    copyfile(ORIGINAL_JGW_SW, NEU_JGW_SW)
                else:
                    print " Fehler bei " + str(BS_NR)

else:
    myLogPrint("\t uebersprungen", myLogDatei)

myLogPrint("\t ...beendet", myLogDatei)

#######################################################################################################################
myLogPrint("\n\n", myLogDatei)
myLogPrint("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++", myLogDatei)
myLogPrint(" Image Catalog erstellen", myLogDatei)
arcpy.AddMessage("Image Catalog erstellen")
myLogPrint("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++", myLogDatei)

if doIMAGECATALOG == 1:

    # Kopieren des landesweiten Image Catalogs
    arcpy.CopyRows_management(IMAGE_CATALOG_ORIG, IMAGE_CATALOG_AOI)

    arcpy.AddField_management(IMAGE_CATALOG_AOI, "TMP", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.CalculateField_management(IMAGE_CATALOG_AOI, "TMP", "0", "PYTHON_9.3", "")

    fields01 = ['OBJECT_ID', 'KB']
    with arcpy.da.SearchCursor(BS_DOB_AOI, fields01) as cursor01:
        for row01 in cursor01:
            ORDNER = row01[1]

            BS_NR = (str(row01[0])[0:-2])
            BS_NR_01 = (str(row01[0])[:-6])
            BS_NR_02 = (str(row01[0])[5:-2])

            if ORDNER <> None:

                PATH_ORTHO = ORDNER + "\\FDOP20_" + BS_NR_01 + "_" + BS_NR_02 + "_rgbi.jpg"

                fields02 = ['IMAGE', 'TMP']
                with arcpy.da.UpdateCursor(IMAGE_CATALOG_AOI, fields02) as cursor02:
                    for row02 in cursor02:
                        if row02[0] == PATH_ORTHO:
                            row02[1] = 1
                            cursor02.updateRow(row02)

    fields03 = ['IMAGE', 'TMP']
    with arcpy.da.UpdateCursor(IMAGE_CATALOG_AOI, fields03) as cursor03:
        for row03 in cursor03:
            if row03[1] == 0:
                cursor03.deleteRow()

    arcpy.DeleteField_management(IMAGE_CATALOG_AOI, "TMP")

else:
    myLogPrint("\t uebersprungen", myLogDatei)

myLogPrint("\t ...beendet", myLogDatei)

#######################################################################################################################
myLogPrint("\n\n", myLogDatei)
myLogPrint("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++", myLogDatei)
myLogPrint(" Skript beendet: " + time.strftime("%Y_%m_%d__%H_%M_%S", time.localtime()), myLogDatei)
myLogPrint("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++", myLogDatei)