import arcpy, time, smtplib

# set the workspace
arcpy.env.workspace = 'Database Connections/admin.sde'

# set a variable for the workspace
workspace = arcpy.env.workspace

# get a list of connected users.
userList = arcpy.ListUsers("Database Connections/admin.sde")

# get a list of usernames of users currently connected and make email addresses
emailList = [u.Name + "@yourcompany.com" for user in arcpy.ListUsers("Database Connections/admin.sde")]

# take the email list and use it to send an email to connected users.
SERVER = "mailserver.yourcompany.com"
FROM = "SDE Admin <python@yourcompany.com>"
TO = emailList
SUBJECT = "Maintenance is about to be performed"
MSG = "Auto generated Message.\n\rServer maintenance will be performed in 15 minutes. Please log off."

# Prepare actual message
MESSAGE = """\
From: {0:s}
To: {1:s}
Subject: {2:s}

{3:s}
""".format(FROM, ", ".join(TO), SUBJECT, MSG)

# Send the mail
server = smtplib.SMTP(SERVER)
server.sendmail(FROM, TO, MESSAGE)
server.quit()

#block new connections to the database.
arcpy.AcceptConnections('Database Connections/admin.sde', False)

# wait 15 minutes
time.sleep(900)

#disconnect all users from the database.
arcpy.DisconnectUser('Database Connections/admin.sde', "ALL")

# Get a list of versions to pass into the ReconcileVersions tool.
versionList = arcpy.ListVersions('Database Connections/admin.sde')

# Execute the ReconcileVersions tool.
arcpy.ReconcileVersions_management('Database Connections/admin.sde', "ALL_VERSIONS", "sde.DEFAULT", versionList, "LOCK_ACQUIRED", "NO_ABORT", "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", "DELETE_VERSION", "c:/temp/reconcilelog.txt")

# Run the compress tool.
arcpy.Compress_management('Database Connections/admin.sde')

#Allow the database to begin accepting connections again
arcpy.AcceptConnections('Database Connections/admin.sde', True)

#Get a list of datasets owned by the admin user

# Get the user name for the workspace
# this assumes you are using database authentication.
# OS authentication connection files do not have a 'user' property.
userName = arcpy.Describe(arcpy.env.workspace).connectionProperties.user

# Get a list of all the datasets the user has access to.
# First, get all the stand alone tables, feature classes and rasters.
dataList = arcpy.ListTables('*.' + userName + '.*') + arcpy.ListFeatureClasses('*.' + userName + '.*') + arcpy.ListRasters('*.' + userName + '.*')

# Next, for feature datasets get all of the featureclasses
# from the list and add them to the master list.
for dataset in arcpy.ListDatasets('*.' + userName + '.*'):
    dataList += arcpy.ListFeatureClasses(feature_dataset=dataset)

# pass in the list of datasets owned by the admin to the rebuild indexes and analyze datasets tools
# Note: to use the "SYSTEM" option the user must be an administrator.
arcpy.RebuildIndexes_management(workspace, "SYSTEM", dataList, "ALL")

arcpy.AnalyzeDatasets_management(workspace, "SYSTEM", dataList, "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")