'''
Title: Create Witness Tree Data Dictionary
Created: Jun 27, 2013
Modified: October 10, 2013

@author: williamg
'''

import arcpy
import datetime as dt
import glob, os

# Create a timestamp
curtime = str(dt.datetime.now()).replace(' ','_').replace('-','').replace(':','').replace('.','')
    
def createDataDictionary(workspace=None, table_list=[]):
    # Check table_list for data; Data validation IS NOT performed at this time.
    if workspace is None:
        print("No workspace provided. Exiting")
        return -10
    else:
        # test if path is valid and available
        if not os.path.exists(workspace):
            print("workspace does not exist.")
            return -12
    
    if len(table_list) == 0:
        arcpy.env.workspace = workspace
        arcpy.env.overwriteOutput = True
        wksp = arcpy.env.workspace
        print(wksp)
        print("Create a data dictionary on all feature classes and tables within the geodatabase")
    else:
        print("Creating a data dictionary on ", table_list)
        return -1
        
    # Get list of all shapefiles
    shapefiles = glob.glob(wksp + os.sep + "*.shp")
    #print(shapefiles)
    
    # Loop thru each table and print the table definition in CSV format
    for sf in shapefiles:
        s = os.path.basename(sf)
        print("Processing {0}".format(s.upper()))
        
        #Open CSV file to store data
        #fo = open(os.path.dirname(sf) + os.sep + s[:-4] + "_" + curtime + ".csv", "w")
        fo = open(os.path.dirname(sf) + os.sep + "test" + os.sep + s[:-4] + ".csv", "w")
        fo.write("{0}, {1}, {2}, {3}\n".format('', 'COLUMN_NAME', 'DATATYPE', 'IS_NULLABLE'))
        
        try:
            fieldCounter = 0
            fields = arcpy.ListFields(sf)
            for field in fields:
                if field.name not in ['FID', 'Shape', 'SHAPE_Leng', 'SHAPE_Area']:
                    fieldCounter += 1
                    #print("{0}, {1}, {2}, {3}".format(str(fieldCounter), field.name, field.type, field.isNullable))
                    fo.write("{0}, {1}, {2}, {3}\n".format(str(fieldCounter), field.name, field.type, field.isNullable))
                   
            fieldCounter = 0 
            for field in fields:
                if field.name not in ['FID', 'Shape', 'SHAPE_Leng', 'SHAPE_Area']:
                    fieldCounter += 1
                    #Add a blank line to the CSV file
                    fo.write("{0}, {1}\n".format('DATA STATS', field.name))
                
                    try:
                        stats = {}
                        rows = arcpy.SearchCursor(sf, None, None, field.name)
                        for row in rows:
                            if stats.has_key(row.getValue(field.name)):
                                stats[row.getValue(field.name)] = stats.get(row.getValue(field.name)) + 1
                            else:
                                stats[row.getValue(field.name)] = 1
                            
                        #Print out unique data with count
                        fo.write("{0}, {1}, {2}\n".format('', 'Value', 'Count'))
                        items = stats.items()
                        for item in items:
                            fo.write("{0}, {1}, {2}\n".format(str(fieldCounter), item[0], item[1]))
                            
                    except Exception as e:
                        print("    Failed to calculate stats.\n    " + str(e))
        except:
            print("Failed to read shapefile schema.")
            fo.write("Failed to read shapefile schema.\n")

        fo.close()
            
if __name__ == "__main__":
    workspace = 'C:\\Users\\williamg\\Documents\\School\\Deliverables'
    createDataDictionary(workspace)
    #createDataDictionary(['callbundles'])
    print("Script Completed.")