# coding:utf-8
'''
Created on May 20, 2013
Updated on February 27, 2014
@author: williamg

@todo: add functionality to update layer's definition query
@todo: copy MasterOMSFeatures.gdb then rename to OMS_Features.gdb
@todo: update OMS_Features.gdb FCs to match Client's Spatial Ref
@todo: make sure all current OMS Features are in the map (e.g. tags)

'''

import arcpy
import datetime, os
# Obtain current date & time to append to MXD filename
CURRENT_TIME = datetime.datetime.now()
current_time = str(CURRENT_TIME)[:19].replace(' ','_').replace('-','').replace(':','').replace('.','')

def printMXDLayers(mapDoc=None):
    mxd = arcpy.mapping.MapDocument(mapDoc)
    # Data Frame Name is hard-coded to the Default name: Layers
    for df in arcpy.mapping.ListDataFrames(mxd, "Layers"):
        counter = 1
        for lyr in arcpy.mapping.ListLayers(mxd, "", df): 
            print("{0:2}: {1}".format(str(counter), lyr.name))
            if lyr.supports("LABELCLASSES"):
                for lblClass in lyr.labelClasses:
                    print("    Label Class: {0}".format(lblClass.className))
                    print("    Expression: {0}".format(lblClass.expression))
                    print("    SQL Query: {0}".format(lblClass.SQLQuery))
            counter += 1
    del mxd

def getOMSFeatures(src, dst, symlinks=False, ignore=None, logging=False):
    import shutil
    if logging:
        log = open(mapDocument[:-4] + "_" + current_time + ".log", "w+")
    try:
        shutil.copytree(src, dst, symlinks, ignore)
    except OSError as e:
        if logging:
            log.write(e)
            log.close()
        return -1
    if logging:
        log.close()
    return 0
    
def updateOMSFeaturesSpatRef(wksp=None, spatRef=None, logging=False):
    """
    updateOMSFeaturesSpatRef(wksp=None, spatRef=None) updates the spatial reference
    of all the features in the OMS_Features.gdb to match the Client's GIS data.
    User will need to either select the spatial reference from the list in the toolbox
    or import the projection for an existing dataset or feature class. 
    """
    if logging:
        log = open(mapDocument[:-4] + "_" + current_time + ".log", "w+")
    
    #set the oms_features.gdb to the wksp
    arcpy.env.workspace = wksp
    
    #set the spatial reference to object
    sr = arcpy.SpatialReference(spatRef)
    
    #get list of all fcs in wksp
    fcs = arcpy.ListFeatureClasses()
    
    #process each fc
    for fc in fcs:
        try:
            arcpy.DefineProjection_management(fc, sr)
            arcpy.AddMessage("Spatial Projection Updated: " + fc + " (" + sr +")")
            if logging:
                log.write("Spatial Projection Updated: " + fc + " (" + sr +")")
        except:
            arcpy.AddError("Spatial Projection Update Failed: " + fc)
            if logging:
                log.write("Spatial Projection Update Failed: " + fc)
            return -1
    
    if logging:
        log.close()
        
    return 1

def checkOMSFeaturesGLayer(mapDocument, OMSFeatures, logging):
    if logging:
        log = open(mapDocument[:-4] + "_" + current_time + ".log", "w+")
    
    mxd = arcpy.mapping.MapDocument(mapDocument)
    df  = arcpy.mapping.ListDataFrames(mxd, "")[0]
    targetGroupLayer = arcpy.mapping.ListLayers(mxd, "OMS Features", df)[0]
    omsFeatures = ['calls','cases','custout','tags','notes','switching','trucks']
    
    if logging:
        arcpy.AddMessage("Checking OMS Features Group Layer in {0} data frame of {1}".format(df, mxd))
        log.write("Checking OMS Features Group Layer in {0} data frame of {1}".format(df, mxd))
        
    lyrs = arcpy.mapping.ListLayers(mxd, "", df)
    for lyr in lyrs:
        if 'OMS Features' in lyr.longName and not lyr.isGroupLayer:
            #status = 'Present'
            if lyr.name in omsFeatures:
                omsFeatures.remove(omsFeatures.index(lyr.name))
            else:
                #status = 'Not Present'
                addLayer = arcpy.mapping.Layer(OMSFeatures + os.sep + lyr.name)
                try:
                    arcpy.mapping.AddLayerToGroup(df, targetGroupLayer, addLayer, "BOTTOM")
                except:
                    if logging:
                        log.write("Failed to Add Layer {0} to group layer".format(lyr.name))
                    arcpy.AddError("Failed to Add Layer {0} to group layer".format(lyr.name))
            if logging:
                log.write("Processed Layer: {0}".format(lyr.name))
        elif 'OMS Features' not in lyr.longName and lyr.isGroupLayer:
            if logging:
                log.write("Exiting at Layer: {0}".format(lyr.name))
            return
    
    if logging:
        log.close()
            
def updateLabelClasses(mapDoc=None, mapVersion=None, logging=True):
    # Open log file to create a log of changes
    # Default is True
    if logging:
        log = open(mapDoc[:-4] + "_" + current_time + ".log", "w+")
        
    # Define Map Document for converting SQLQueries from Personal to File Geodatabase friendly
    mxd = arcpy.mapping.MapDocument(mapDoc)
    for df in arcpy.mapping.ListDataFrames(mxd, ""):
        counter = 1
        for lyr in arcpy.mapping.ListLayers(mxd, "", df):
            if logging:
                log.write("{0:2}: {1}\n".format(str(counter), lyr.name))
            if lyr.isBroken:
                log.write("    {0}".format("Layer cannot be found.\n"))
                arcpy.AddWarning("Layer cannot be found.")
                continue
            if lyr.isGroupLayer == False:
                arcpy.AddMessage("{0:2}: {1}".format(str(counter), lyr.name))
                
                # Check for existing definition query that needs to be updated to use gdb
                defQuery_found_open_sq_brackets = False
                defQuery_found_closed_sq_brackets = False
                defQuery_found_wildcard = False
                
                if lyr.supports("DEFINITIONQUERY"):
                    if lyr.definitionQuery.find("[") != -1:
                        defQuery_found_open_sq_brackets = True
                        lyr.definitionQuery = lyr.definitionQuery.replace("[", "\"")
                    if lyr.definitionQuery.find("]") != -1:
                        defQuery_found_closed_sq_brackets = True
                        lyr.definitionQuery = lyr.definitionQuery.replace("]", "\"")
                    if lyr.definitionQuery.find("*") != -1:
                        defQuery_found_wildcard = True
                        lyr.definitionQuery = lyr.definitionQuery.replace("*", "%")
                        
                    if (defQuery_found_open_sq_brackets or defQuery_found_closed_sq_brackets) or defQuery_found_wildcard:
                        if logging:
                            log.write("    Updated definition query: {0}\n".format(lyr.definitionQuery))
                        arcpy.AddMessage("    Updated definition query: {0}".format(lyr.definitionQuery))
                    
                    # Validate Definition Query Fields that are in datasource fields
                    if len(lyr.definitionQuery) > 0:
                        if lyr.supports("DATASOURCE") and logging:
                            results = validateDefinitionQuery(lyr.dataSource, lyr.definitionQuery)
                            if results is not None:
                                for result in results:
                                    log.write("{0}{1}\n".format("        ", result))
                                    arcpy.AddWarning("{0}{1}".format("        ", result))
                
                if lyr.supports("LABELCLASSES"):
                    sub_counter = 1
                    for lblClass in lyr.labelClasses:
                        if logging:
                            log.write("    {0} - Label Class: {1}\n".format(sub_counter,lblClass.className))
                        arcpy.AddMessage("    {0} - Label Class: {1}".format(sub_counter,lblClass.className))
                        sub_counter += 1
                        sql_found_open_sq_brackets = False
                        sql_found_closed_sq_brackets = False
                        sql_found_wildcard = False
                        if lblClass.SQLQuery.find("[") != -1:
                            sql_found_open_sq_brackets = True
                            lblClass.SQLQuery = lblClass.SQLQuery.replace("[", "\"")
                        if lblClass.SQLQuery.find("]") != -1:
                            sql_found_closed_sq_brackets = True
                            lblClass.SQLQuery = lblClass.SQLQuery.replace("]", "\"")
                        if lblClass.SQLQuery.find("*") != -1:
                            sql_found_wildcard = True
                            lblClass.SQLQuery = lblClass.SQLQuery.replace("*", "%")
                        if lblClass.SQLQuery.find("Shape.STLength()") != -1:
                            lblClass.SQLQuery = lblClass.SQLQuery.replace("Shape.STLength()", '"Shape_Length"')
                        if lblClass.expression.find("Shape.STLength()") != -1:
                            lblClass.expression = lblClass.expression.replace("Shape.STLength()", "Shape_Length")
                        
                        if sql_found_open_sq_brackets or sql_found_closed_sq_brackets or sql_found_wildcard:
                            if logging:
                                log.write("        Updated SQL Query: {0}\n".format(lblClass.SQLQuery))
                            arcpy.AddMessage("        Updated SQL Query: {0}".format(lblClass.SQLQuery))

                        # Validate SQL Fields that are in datasource fields
                        if len(lblClass.SQLQuery) > 0:
                            if lyr.supports("DATASOURCE") and logging:
                                results = verifySQLFields(lyr.dataSource, lblClass.SQLQuery)
                                if results is not None:
                                    for result in results:
                                        log.write("{0}{1}\n".format("        ", result))
                                        arcpy.AddWarning("{0}{1}".format("        ", result))
                            else:
                                arcpy.AddWarning("    Layer supports dataSource property: {0}".format(lyr.supports("DATASOURCE")))
                                arcpy.AddWarning("    Logging is set to {0}".format(logging))
                                
                        # Validate Expression Fields that are in datasource fields
                        if len(lblClass.expression) > 0:
                            if lyr.supports("DATASOURCE") and logging:
                                results = validateExpression(lyr.dataSource, lblClass.expression)
                                if results is not None:
                                    for result in results:
                                        log.write("{0}{1}\n".format("        ", result))
                                        arcpy.AddWarning("{0}{1}".format("        ", result))
                            #if logging:
                            #    log.write("        Expression: {0}\n".format(lblClass.expression))
                            #print("        Expression: {0}".format(lblClass.expression))
                
                    
            # counting the feature classes
            counter += 1
                
            
    # Save a copy of the MXD with a DATETIME stamp and default to version of running ArcGIS
    mxd.author = "Futura Systems, Inc."
    mxd.description = "This map was automatically created by a script to make it file geodatabase friendly."
    mxd.relativePaths = False
    newMXD = mapDoc[:-4] + "_" + current_time + ".mxd"
    mxd.saveACopy(newMXD, mapVersion)
    if logging:
        log.write("Saved changes to " + newMXD + "\n")
    arcpy.AddMessage("Saved changes to " + newMXD)
    
    #Close the log file
    if logging:
        log.close()
    
    # Delete mxd object
    del mxd
    
def verifySQLFields(layer, sql):
    sqlquery = sql.split('"')
    results = []
    fieldList = arcpy.ListFields(layer)
    
    for comp in sqlquery[1:]:
        if sqlquery.index(comp)%2 != 0:
            Matched = False
            for field in fieldList:
                if comp.lower() == field.name.lower():
                    Matched = True
                    #results.append([comp, "MATCHED"])
            if Matched == False:
                results.append([comp, field.name, "SQL_FIELDS_NOT_MATCHED"])
    if len(results) == 0:
        results = None
                    
    return results

def validateExpression(layer, exp):
    #arcpy.AddWarning("validateExpression Function params: {0}, {1}".format(layer, exp))
    results = []
    fieldList = arcpy.ListFields(layer)
    
    while len(exp) > 0:
        if exp.find('[') != -1:
            expression_field = exp[exp.find('[')+1:exp.find(']')]
        else:
            break
        
        if exp.find('.') != -1:
            expression_field = expression_field[exp.find('.'):]

        # compare expression_field with fieldList
        Matched = False
        for field in fieldList:
            if expression_field.lower() == field.name.lower():
                Matched = True
            #arcpy.AddWarning("Expression Field: {0} FC Field: {1}".format(expression_field.lower(), field.name.lower()))
        if Matched == False:
            results.append([expression_field, field.name, "EXP_FIELDS_NOT_MATCHED"])
        
        #Slice off the string that has been compared
        if exp.find(']') > 0:
            exp = exp[exp.find(']')+1:].strip()
        else:
            exp = ''
            
    if len(results) == 0:
        results = None
        
    return results

def validateDefinitionQuery(layer, exp):
    #arcpy.AddWarning("validateExpression Function params: {0}, {1}".format(layer, exp))
    results = []
    fieldList = arcpy.ListFields(layer)
    
    while len(exp) > 0:
        if exp.find('[') != -1:
            expression_field = exp[exp.find('[')+1:exp.find(']')]
        else:
            break
        
        if exp.find('.') != -1:
            expression_field = expression_field[exp.find('.'):]

        # compare expression_field with fieldList
        Matched = False
        for field in fieldList:
            if expression_field.lower() == field.name.lower():
                Matched = True
            #arcpy.AddWarning("Expression Field: {0} FC Field: {1}".format(expression_field.lower(), field.name.lower()))
        if Matched == False:
            results.append([expression_field, field.name, "DEFQUERY_FIELDS_NOT_MATCHED"])
        
        #Slice off the string that has been compared
        if exp.find(']') > 0:
            exp = exp[exp.find(']')+1:].strip()
        else:
            exp = ''
            
    if len(results) == 0:
        results = None
        
    return results


# Define Map Document parameter from ArcTool
if arcpy.GetParameterAsText(0) is None or arcpy.GetParameterAsText(0) == '':
    arcpy.AddError("Map Document is required!")
    exit()
else:
    mapDocument = arcpy.GetParameterAsText(0)
# Define Logging parameter from ArcTool
if arcpy.GetParameter(1) is None:
    arcpy.AddError("Logging options needs to be True or False")
    exit()
else:
    logging = arcpy.GetParameter(1)
# Define Map Document Version parameter from ArcTool
if arcpy.GetParameterAsText(2) is None:
    arcpy.AddError("Map Document Version was not set")
    exit()
else:
    mapVersion = arcpy.GetParameterAsText(2)
# # Define Source Path to the Master OMS_Features.gdb
# if arcpy.GetParameterAsText(3) is None or arcpy.GetParameterAsText(3) == '':
#     #r"\\orion\Common\GISServerSetupDVD\OMS\Master_OMS_Features.gdb"
#     arcpy.AddError("Master_OMS_Features.gdb Path is required")
#     exit()
# else:
#     MasterOMSFeatures = arcpy.GetParameterAsText(3)
# # Define Destination Path for the OMS_Features.gdb
# if arcpy.GetParameterAsText(4) is None or arcpy.GetParameterAsText(4) == '':
#     #r"C:\map_files\OMS_Features.gdb"
#     arcpy.AddError("OMS_Features.gdb Path is required")
#     exit()
# else:
#     OMSFeatures = arcpy.GetParameterAsText(4)
# # Define Master Spatial Reference
# if arcpy.GetParameterAsText(5) is None or arcpy.GetParameterAsText(5) == '':
#     #r"C:\map_files\OMS_Features.gdb"
#     arcpy.AddError("Spatial Reference is required")
#     exit()
# else:
#     spatRef = arcpy.GetParameterAsText(5)
        
# Run Script now that variables are defined
#getOMSFeatures(MasterOMSFeatures, OMSFeatures, False, None, logging)
#updateOMSFeaturesSpatRef(OMSFeatures, spatRef, logging)
#checkOMSFeaturesGLayer(mapDocument, OMSFeatures, logging)
updateLabelClasses(mapDocument, mapVersion, logging)
arcpy.AddMessage("Script Completed.")

