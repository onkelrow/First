# import os
# import csv
# import arcpy
#
# def ListMXDSources(path,extension):
#   list_dir = []
#   CountList = []
#   MapList = []
#   list_dir = os.listdir(path)
#   count = 0
#   for paths, dirctory, files in os.walk(path):
#     for file in files:
#         if file.endswith(extension): # eg: '.mxd'
#           MapList.append(os.path.join(paths, file))
#           print MapList
#           for m in MapList:
#                 count += 1
#                 mxd = arcpy.mapping.MapDocument(m)
#                 ## --------- For each map list layers
#                 for lyr in arcpy.mapping.ListLayers(mxd):
#                     with open("ListOfDataSources.csv", 'wb') as csvfile:
#                         csvwriter = csv.writer(csvfile)
#                         for dirpath, dirnames, filenames in arcpy.da.Walk(MapList):
#                             for filename in filenames:
#                                 desc = arcpy.Describe(os.path.join(dirpath, filename))
#                                 csvwriter.writerow([desc.catalogPath, desc.name, desc.dataType])
#import arcpy, os, csv
import os
import csv
import arcpy

def main(folder, outputfile):
    with open(outputfile, "wb") as f:
        w = csv.writer(f)
        header = ("Map Document", "MXD Path", "DataFrame Name", "DataFrame Description", "Layer name", "Layer Datasource")
        w.writerow(header)
        rows = crawlmxds(folder)
        w.writerows(rows)

def crawlmxds(folder):
    for root, dirs, files in os.walk(folder):
        for f in files:
            if f.lower().endswith(".mxd"):
                mxdName = os.path.splitext(f)[0]
                mxdPath = os.path.join(root, f)
                mxd = arcpy.mapping.MapDocument(mxdPath)
                dataframes = arcpy.mapping.ListDataFrames(mxd)
                for df in dataframes:
                    dfDesc = df.description if df.description != "" else "None"
                    layers = arcpy.mapping.ListLayers(mxd, "", df)
                    for lyr in layers:
                        lyrName = lyr.name
                        lyrDatasource = lyr.dataSource if lyr.supports("dataSource") else "N/A"
                        seq = (mxdName, mxdPath, df.name, dfDesc, lyrName, lyrDatasource);
                        yield seq
                del mxd

if __name__ == "__main__":
    folderPath = r"C:\temp1\test" # or arcpy.GetParameterAsText(0)
    output = r"c:\temp1\mxdcrawler.csv" # or arcpy.GetParameterAsText(1)
    main(folderPath, output)