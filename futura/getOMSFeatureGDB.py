# coding:utf-8
'''
Created on February 28, 2014
Updated on February 28, 2014
@author: williamg

'''

import datetime
# Obtain current date & time to append to MXD filename
CURRENT_TIME = datetime.datetime.now()
current_time = str(CURRENT_TIME)[:19].replace(' ','_').replace('-','').replace(':','').replace('.','')

def getOMSFeatures(src, dst, symlinks=False, ignore=None):
    import shutil, os
    
    try:
        if os.path.isdir(dst):
            try:
                shutil.rmtree(dst, True)
                shutil.copytree(src, dst, symlinks, ignore)
            except:
                print("Failed to delete existing OMS Features GDB")
    except OSError as e:
        print(e)
        return -1
    return 0

def updateOMSFeaturesSpatRef(wksp=None, spatRef=None):
    """
    updateOMSFeaturesSpatRef(wksp=None, spatRef=None) updates the spatial reference
    of all the features in the OMS_Features.gdb to match the Client's GIS data.
    User will need to either select the spatial reference from the list in the toolbox
    or import the projection for an existing dataset or feature class. 
    """
    import arcpy
    
    #set the oms_features.gdb to the wksp
    #arcpy.env.workspace = wksp
    
    #set the spatial reference to object
    """
    Need more attention here to build the SR onject
    """
    #print("spatRef: " + spatRef)
    try:
        arcpy.env.workspace = spatRef
        sr = arcpy.Describe(spatRef).spatialReference
        sr_str = sr.exportToString()
        #print(sr_str)
    except Exception as e:
        print e.message
        return -1
    
    #get list of all fcs in wksp
    arcpy.env.workspace = wksp
    fcs = arcpy.ListFeatureClasses()
    
    #process each fc
    for fc in fcs:
        #print("Updating SR: " + fc)
        try:
            arcpy.DefineProjection_management(fc, sr_str)
            arcpy.AddMessage("Spatial Projection Updated: " + fc + " (" + sr.name +")")
        except:
            arcpy.AddError("Spatial Projection Update Failed: " + fc)
            return -2
        
    return 1


if __name__ == '__main__':
    try:
        success = getOMSFeatures(r"\\orion\Common\GISServerSetupDVD\OMS\Master_OMS_Features.gdb", r"C:\map_files\OMS_Features.gdb", False, None)
        print("Updated OMS Features.gdb")
    except:
        print("Updated OMS Features.gdb Failed")
    
    if success == 0:
        if updateOMSFeaturesSpatRef(r"C:\map_files\OMS_Features.gdb", r"C:\map_files\OMS_Features.mdb\calls") < 1:
            print("FAILED: Updated SR for OMS_Features.gdb")
        else:
            print("Updated SR for OMS_Features.gdb")
    else:
        print("Update OMS Feautures Spatial Reference could not run to Update OMS Features Failure")
    
    print("Script Completed.")
        