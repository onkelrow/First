import arcpy, time, smtplib

#workspace definieren
arcpy.env.workspace = 'database Connections/connection to geo.sde'

#workspace in variable überführen
workspace = arcpy.env.workspace

# Liste der angemeldeten Geodatabase_user
userList = arcpy.ListUsers("Database Connections/admin.sde")

# Liste aller angemeldeten User aus array ziehen
emailList = [u.Name + "@lubw.bwl.de" for user in arcpy.ListUser("Database Connections/admin.sde")]

# Email über stmplib an User schicken
Server = "mailserver"






#blockieren von neuen Verbindungen zum Schema
arcpy.AcceptConnections('Database Connections/admin.sde', False)

# abwarten für 5 Minuten
time.sleep(300)

#alle user abmelden
arcpy.disconnectUser()