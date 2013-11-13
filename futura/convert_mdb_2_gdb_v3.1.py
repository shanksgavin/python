# coding:utf-8
'''
Created on May 20, 2013
Updated on Oct 11, 2013
@author: williamg

@todo: add functionality to update layer's definition query

'''

try:
    import arcpy
    arcVersion = '10'
except:
    import arcgisscripting
    gp = arcgisscripting.create(9.3)
    arcVersion = '9.3'


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


# Define Map Document parameter from ArcTool
if arcVersion == '10':
    if arcpy.GetParameterAsText(0) is None or arcpy.GetParameterAsText(0) == '':
        arcpy.AddError("Map Document is required!")
        
    else:
        mapDocument = arcpy.GetParameterAsText(0)
    # Define Logging parameter from ArcTool
    if arcpy.GetParameter(1) is None:
        arcpy.AddError("Logging options needs to be True or False")
        
    else:
        logging = arcpy.GetParameter(1)
    
    # Run Script now that variables are defined
    updateLabelClasses(mapDocument, logging)
    arcpy.AddMessage("Script Completed.")
    
else:
    gp.AddWarning('This script is not capable of successfully running in ArcGIS 9.3')
    