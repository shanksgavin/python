# coding:utf-8
'''
Created on May 20, 2013
Updated on Aug 23, 2013
@author: williamg

@todo: Copy/Paste/Rename Master_OMS_Features.gdb
@todo: Redefine Spatial Reference of ALL feature Classes to match the active client's SR
@todo: Create (Save) Layer Properties for ALL Trace layers in OMS_Features
@todo: Add Tag feature class to the OMS Features group layer
@todo: Add all trace_tables to map
@todo: Create join between trace layers and tables
@todo: Reapply symbology to ALL trace layers
@todo: Update/Correct Label SQL, Definition, Expression Queries


'''

import arcpy
import os, sys, shutil, string

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
    
    if arcpy.Exists(wksp):
        arcpy.env.workspace = wksp
        for fc in arcpy.ListFeatureClasses():
            spatialRef = arcpy.Describe(fc).spatialReference
            if spatialRef.name != masterSR.name:
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
        
        
def defineSR(newGDB='C:\\map_files', newGDBname='OMS_Features.gdb', sr=None):
    '''
    @param newGDB: The folder location of where the new file geodatabase should be copied
    @param newGDBname: The name to be used for renaming the copy of Master_OMS_Features.gdb. Default is OMS_Features.gdb
    @param sr: The Spatial Reference to be applied to the OMS_Features Trace feature classes
    
    @todo: Make this work on a single feature class instead of entire workspace then this can be called from the createOMSFeatures()
    '''
    if sr is None:
        print('Spatial Reference Must be defined.  Exiting...')
        sys.exit()
    
    arcpy.env.workspace = newGDB + os.sep + newGDBname
    masterSR = arcpy.SpatialReference()
    masterSR.loadFromString(sr)
    
    for fc in arcpy.ListFeatureClasses():
        spatialRef = arcpy.Describe(fc).spatialReference
        if spatialRef.name != masterSR.name:
            try:
                arcpy.DefineProjection_management(fc, sr)
                arcpy.AddMessage(fc + ' updated spatial reference.')
            except:
                arcpy.AddError('Failed to define projection on ' + fc)
            

def saveLyrProps():
    pass

def addTagsFC(mxd, newGDB, newGDBname, groupLayer='OMS_Features'):
    '''
    @param mapDocument: The Map document that will be updated
    @param groupLayer: The group layer name that will contain the added layer
    @param newGDB: The OMS_Features geodatabase folder location
    @param newGDBname: The OMS_Features geodatabase name
    '''
    
    df = arcpy.mapping.ListDataFrames(mxd)[0]
    targetGroupLayer = arcpy.mapping.ListLayers(mxd, groupLayer, df)[0]
    tagsLayer = arcpy.mapping.Layer(newGDB+os.sep+newGDBname+os.sep+'tags')
    arcpy.AddMessage('    Tags Layer Created')
    arcpy.mapping.AddLayerToGroup(df, targetGroupLayer, tagsLayer, "BOTTOM")
    arcpy.AddMessage('    Tags Layer Added to ' + mxd.filePath)
    #if os.path.exists(newGDB + os.sep + 'test_map.mxd'):
        #os.remove(newGDB + os.sep + 'test_map.mxd')
        #arcpy.AddMessage("test_map.mxd has been deleted.")
    #mxd.saveACopy(newGDB + os.sep + 'test_map.mxd')
    #arcpy.AddMessage("test_map.mxd has been saved.")

def addTraceTbls(mxd, newGDB, newGDBname, groupLayer='trace_layers'):
    df = arcpy.mapping.ListDataFrames(mxd)[0]
    Recloser_Table = arcpy.mapping.TableView(newGDB+os.sep+newGDBname+os.sep+'recloserbank_table')
    Fuse_Table = arcpy.mapping.TableView(newGDB+os.sep+newGDBname+os.sep+'fusebank_table')
    Switching_Table = arcpy.mapping.TableView(newGDB+os.sep+newGDBname+os.sep+'switchbank_table')
    Sectionalizer_Table = arcpy.mapping.TableView(newGDB+os.sep+newGDBname+os.sep+'sectionalizerbank_table')
    Primary_Table = arcpy.mapping.TableView(newGDB+os.sep+newGDBname+os.sep+'primaryconductor_table')
    Secondary_Table = arcpy.mapping.TableView(newGDB+os.sep+newGDBname+os.sep+'secondaryconductor_table')
    arcpy.mapping.AddTableView(df, Recloser_Table)
    arcpy.AddMessage('    Added Table: recloserbank_table')
    arcpy.mapping.AddTableView(df, Fuse_Table)
    arcpy.AddMessage('    Added Table: fusebank_table')
    arcpy.mapping.AddTableView(df, Switching_Table)
    arcpy.AddMessage('    Added Table: switchbank_table')
    arcpy.mapping.AddTableView(df, Sectionalizer_Table)
    arcpy.AddMessage('    Added Table: sectionalizerbank_table')
    arcpy.mapping.AddTableView(df, Primary_Table)
    arcpy.AddMessage('    Added Table: primaryconductor_table')
    arcpy.mapping.AddTableView(df, Secondary_Table)
    arcpy.AddMessage('    Added Table: secondaryconductor_table')
    

def createTraceJoins(mxd, newGDB, newGDBname, groupLayer='trace_layers'):
    #import string
    
    wksp = newGDB + os.sep + newGDBname
    arcpy.env.workspace = wksp
    arcpy.env.qualifiedFieldNames = False
    
    joinFieldFC = 'OBJECTID'
    joinFieldTbl = 'object_id'
    joinType = 0 #boolean value but not sure which to use 1 or 0
    
    df = arcpy.mapping.ListDataFrames(mxd)[0]
    targetGroupLayer = arcpy.mapping.ListLayers(mxd, '*_trace', df)
    """
    @attention: pick up at this point
    @bug: string comparison is failing because fc.name does not have a method '.lower()'
    """
    for fc in targetGroupLayer:
        if fc.name.lower() == 'recloserbank_trace':
            arcpy.AddJoin_management(fc, joinFieldFC, 'recloserbank_table', joinFieldTbl, joinType)
        elif fc.name.lower() == 'fusebank_table':
            arcpy.AddJoin_management(fc, joinFieldFC, 'fusebank_table', joinFieldTbl, joinType)
        elif fc.name.lower() == 'switchbank_table':
            arcpy.AddJoin_management(fc, joinFieldFC, 'switchbank_table', joinFieldTbl, joinType)
        elif fc.name.lower() == 'sectionalizerbank_table':
            arcpy.AddJoin_management(fc, joinFieldFC, 'sectionalizerbank_table', joinFieldTbl, joinType)
        elif fc.name.lower() == 'primaryconductor_table':
            arcpy.AddJoin_management(fc, joinFieldFC, 'primaryconductor_table', joinFieldTbl, joinType)
        elif fc.name.lower() == 'secondaryconductor_table':
            arcpy.AddJoin_management(fc, joinFieldFC, 'secondaryconductor_table', joinFieldTbl, joinType)
        else:
            arcpy.AddError('Something is amiss in the trace join creation on fc: ' + fc)

def updateLyrProps():
    pass

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

def updateLabelClasses(mapDoc=None, logging=True):
    import datetime
    # Obtain current date & time to append to MXD filename
    CURRENT_TIME = datetime.datetime.now()
    current_time = str(CURRENT_TIME)[:19].replace(' ','_').replace('-','').replace(':','').replace('.','')
    
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
    mxd.saveACopy(newMXD)
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


if __name__ == "__main__":
    # Commencement of script
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
    # Define New OMS_Features Folder parameter from ArcTool
    if arcpy.GetParameterAsText(2) is None:
        arcpy.AddError("New OMS_Features geodatabase folder is not defined.")
        exit()
    else:
        newGDB = arcpy.GetParameterAsText(2)
    # Define New OMS_Features Name parameter from ArcTool
    if arcpy.GetParameterAsText(3) is None:
        arcpy.AddError("New OMS_Features geodatabase name is not defined.")
        exit()
    else:
        newGDBname = arcpy.GetParameterAsText(3)
    # Define Master OMS_Features Workspace parameter from ArcTool
    if arcpy.GetParameterAsText(4) is None:
        arcpy.AddError("Master OMS_Features.gdb is not defined.")
        exit()
    else:
        masterGDB = arcpy.GetParameterAsText(4)
    # Define Spatial Reference parameter from ArcTool
    if arcpy.GetParameterAsText(5) is None:
        arcpy.AddError("Spatial Reference is not defined.")
        exit()
    else:
        sr = arcpy.GetParameterAsText(5)
    
    # Run Script now that variables are defined
    mxd = arcpy.mapping.MapDocument(mapDocument)
    createOMSFeatures(newGDB, newGDBname, masterGDB)
    defineSR(newGDB, newGDBname, sr)
    addTagsFC(mxd, newGDB, newGDBname, 'OMS_Features')
    addTraceTbls(mxd, newGDB, newGDBname, 'trace_layers')
    createTraceJoins(mxd, newGDB, newGDBname, 'trace_layers')
    #updateLabelClasses(mapDocument, logging)
    arcpy.AddMessage("Script Completed.")