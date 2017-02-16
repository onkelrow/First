import arcpy

users = arcpy.ListUsers("Database Connections/Connection to sde_sde_db_rac.sde")
# for user in users:
#     print("Username: {0}, Connected at: {1}".format(
#         user.Name, user.ConnectionTime))


# import arcpy

# Set the admistrative workspace connection
# arcpy.env.workspace = "Database Connections/tenone@sde.sde"

# Create a list of users
'''
NOTE: When the arcpy.env.workspace environment is set, a workspace
does not need to be provided to the function.
'''
# users = arcpy.ListUsers()

# Create a list of SDE ID's.
# Use a list comprehension to get the ID values in a new list.
id_users = [user.ID for user in users]
print(id_users)

# import arcpy

arcpy.DisconnectUser("Database Connections/Connection to sde_sde_db_rac.sde", "ALL")