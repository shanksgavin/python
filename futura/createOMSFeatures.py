# coding:utf-8
'''
Created on Aug 23, 2013
Updated on Aug 23, 2013
@author: williamg


'''

import arcpy
import os, sys, shutil

def createOMSFeatures(newGDB="C:\\map_files", newGDBname="OMS_Features.gdb", masterGDB="\\\\orion\\common\\GISServerSetupDVD\\OMS\\Master_OMS_Features.gdb", sr=None):
    '''
    @param newGDB: The folder location of where the new file geodatabase should be copied
    @param newGDBname: The name to be used for renaming the copy of Master_OMS_Features.gdb. Default is OMS_Features.gdb
    @param masterGDB: The location of the Master_OMS_Features.gdb. Default location is on \\Orion\common\GISServerSetupDVD\OMS\Master_OMS_Features.gdb
    
    @todo: If OMS_Features exists or fails to create then test if all features are present and the SR matches to the input
    '''
    
    if sr is None:
        print('Spatial Reference Must be defined.  Exiting...')
        sys.exit()

    wksp = newGDB + os.sep + newGDBname
    masterSR = arcpy.SpatialReference()
    masterSR.loadFromString(sr)
    arcpy.env.workspace = wksp
    if arcpy.Exists(wksp):
        for fc in arcpy.ListFeatureClasses():
            spatialRef = arcpy.Describe(fc).spatialReference
            if spatialRef.name != masterSR.name:
                #arcpy.AddWarning("Spatial References Do Not Match on " + fc)
                try:
                    arcpy.DefineProjection_management(fc, sr)
                    arcpy.AddMessage('    updated spatial reference on ' + fc)
                except:
                    arcpy.AddError('    Failed to define projection on ' + fc)
        arcpy.AddMessage('OMS_Features.gdb exists and is properly projected.')
        
    else:
        try:
            shutil.copytree(masterGDB, newGDB + os.sep + newGDBname)
        except:
            arcpy.AddError('Failed to create: ' + newGDB + os.sep + newGDBname)
            sys.exit()

if __name__ == "__main__":
    # Commencement of script
    # Define Map Document parameter from ArcTool
    
    # Define New OMS_Features Folder parameter from ArcTool
    if arcpy.GetParameterAsText(0) is None:
        arcpy.AddError("New OMS_Features geodatabase folder is not defined.")
        exit()
    else:
        newGDB = arcpy.GetParameterAsText(0)
    # Define New OMS_Features Name parameter from ArcTool
    if arcpy.GetParameterAsText(1) is None:
        arcpy.AddError("New OMS_Features geodatabase name is not defined.")
        exit()
    else:
        newGDBname = arcpy.GetParameterAsText(1)
    # Define Master OMS_Features Workspace parameter from ArcTool
    if arcpy.GetParameterAsText(2) is None:
        arcpy.AddError("Master OMS_Features.gdb is not defined.")
        exit()
    else:
        masterGDB = arcpy.GetParameterAsText(2)
    # Define Spatial Reference parameter from ArcTool
    if arcpy.GetParameterAsText(3) is None:
        arcpy.AddError("Spatial Reference is not defined.")
        exit()
    else:
        sr = arcpy.GetParameterAsText(3)
    
    # Run Script now that variables are defined
    createOMSFeatures(newGDB, newGDBname, masterGDB, sr)
    arcpy.AddMessage("Script Completed.")