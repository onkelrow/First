import arcpy
import xml.dom.minidom as DOM

#define local variables
# wrkspc        mxd document directory
# mxdName       mxd document name
# con           ArcGIS Server Catalog path
# service       service name (include service direcotry)
# summary       service summary
# tags          services tags

wrkspc = 'C:/test/'
mxdName = 'sample.mxd'
con = 'GIS Servers/arcgis on localhost_6080 (admin)' 
service = 'MyMapService'
summary = 'Population Density by County'
tags = 'county, counties, population, density, census'

mapDoc = arcpy.mapping.MapDocument(wrkspc + mxdName)
sddraft = wrkspc + service + '.sddraft'
sd = wrkspc + service + '.sd'

# create service definition draft
analysis = arcpy.mapping.CreateMapSDDraft(mapDoc, sddraft, service, 'ARCGIS_SERVER', 
                                          con, True, None, summary, tags)

# set service type to esriServiceDefinitionType_Replacement
newType = 'esriServiceDefinitionType_Replacement'
xml = sddraft
doc = DOM.parse(xml)
descriptions = doc.getElementsByTagName('Type')
for desc in descriptions:
    if desc.parentNode.tagName == 'SVCManifest':
        if desc.hasChildNodes():
            desc.firstChild.data = newType
outXml = xml    
f = open(outXml, 'w')     
doc.writexml( f )     
f.close()

# stage and upload the service if the sddraft analysis did not contain errors
if analysis['errors'] == {}:
    # Execute StageService
    arcpy.StageService_server(sddraft, sd)
    # Execute UploadServiceDefinition
    arcpy.UploadServiceDefinition_server(sd, con)
else: 
    # if the sddraft analysis contained errors, display them
    print analysis['errors']