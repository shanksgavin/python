import arcpy
spatRef = arcpy.GetParameterAsText(0)
#sr = spatRef[spatRef.find("'")+1:spatRef.find("'",spatRef.find("'")+1)]
arcpy.AddMessage('*'*25)
arcpy.AddWarning(spatRef)
arcpy.AddMessage('*'*25)