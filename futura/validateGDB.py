'''
Title: Validate OMS_Features.gdb against master File Geodatabase
Created: Jun 18, 2013

@author: williamg
'''
import arcpy

# Set Workspace
arcpy.env.workspace = arcpy.GetParameterAsText(0)
#wksp = arcpy.env.workspace
for fc in arcpy.ListFeatureClasses():
    arcpy.AddMessage(fc + " Fields:")
    for field in arcpy.ListFields(fc):
        arcpy.AddMessage(field.name + "\t" + field.type + "\t" + str(field.length) + "\t" + str(field.isNullable))
    arcpy.AddMessage("\n")

# Read the Master File Geodatabase file for comparing

# Describe the Workspace
