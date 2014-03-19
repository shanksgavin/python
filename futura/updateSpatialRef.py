# coding:utf-8
'''
Created on February 28, 2014
Updated on March 3, 2014
@author: williamg

'''

def updateOMSFeaturesSpatRef(wksp=None, spatRef=None):
    """
    updateOMSFeaturesSpatRef(wksp=None, spatRef=None) updates the spatial reference
    of all the features in the OMS_Features.gdb to match the Client's GIS data.
    User will need to either select the spatial reference from the list in the toolbox
    or import the projection for an existing dataset or feature class. 
    """
    import arcpy
    
    try:
        arcpy.env.workspace = spatRef
        sr = arcpy.Describe("calls").spatialReference
        sr_str = sr.exportToString()
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
    import os
    
    oldWKSP = r"C:\map_files\OMS_Features.mdb"
    newWKSP = r"C:\map_files\OMS_Features.gdb"
    
    if os.path.isdir(newWKSP):
        if updateOMSFeaturesSpatRef(wksp=newWKSP, spatRef=oldWKSP) < 1:
            print("FAILED: Updated SR for OMS_Features.gdb")
        else:
            print("Updated SR for OMS_Features.gdb")
    else:
        print("Workspace Not Found: {0}".format(oldWKSP))