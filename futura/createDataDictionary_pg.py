'''
Title: Create OMS Audit Schema for In-Depth Troubleshooting
Created: Jun 27, 2013
Modified: July 3, 2013

@author: williamg
'''

def createDataDictionary(table_list=[]):
    # Check table_list for data; Data validation IS NOT performed at this time.
    if len(table_list) == 0:
        print("Table_List is empty. Must provide at least one table to describe")
        return -1
    
    try:
        import psycopg2 as psy
        #import psycopg2.extras as psyExtras
        import datetime as dt
        # Create a timestamp
        curtime = str(dt.datetime.now()).replace(' ','_').replace('-','').replace(':','').replace('.','')
    except:
        print("Failed to import python-postgresql drivers.")
        exit()
        
    try:
        conn_string = "host='localhost' dbname='oms_coos_curry' user='postgres' password='usouth'"
        connTbl = psy.connect(conn_string)
        connCol = psy.connect(conn_string)
        connExe = psy.connect(conn_string)
        cursorTbl = connTbl.cursor()
        cursorCol = connCol.cursor()
        cursorExe = connExe.cursor()
        #curtime = str(dt.datetime.now()).replace(' ','_').replace('-','').replace(':','').replace('.','')
        
    except:
        print("Failed to create connection to database.")
        exit()
            
    #print(str(curtime))
    
    # Get list of tables for OMS schema
    sql_omsTables = """SELECT c.relname 
        FROM pg_catalog.pg_class c 
        LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace 
        WHERE n.nspname='public' 
        AND c.relkind IN ('r','') 
        AND n.nspname NOT IN ('pg_catalog', 'pg_toast', 'information_schema') 
        ORDER BY c.relname ASC"""
    
    # Execute the cursor to obtain the OMS Schema list
    cursorTbl.execute(sql_omsTables)
    
    # Loop thru each table and print the table definition in CSV format
    for tbl in cursorTbl:
        if tbl[0] in table_list:
            print("Processing {0}".format(tbl[0].upper()))

            fo = open("\\\\orion\\common\\_Docs\\DesignDocuments\\OMS\\Schemas\\ddl_" + tbl[0] + "_" + curtime + ".csv", "w")
            fo.write("{0}, {1}, {2}, {3}\n".format('COLUMN_NAME', 'DATATYPE', 'IS_NULLABLE', 'DEFAULT_VALUE'))
            
            try:
                sql_tblDefinition = """SELECT column_name, data_type, character_maximum_length, column_default, is_nullable, numeric_precision, numeric_scale, datetime_precision
                 FROM INFORMATION_SCHEMA.COLUMNS
                 WHERE table_name= '""" + tbl[0] + "'"
                # Execute sql to obtain the attribute definitions of each table
                cursorExe.execute(sql_tblDefinition)
                
                #===============================================================
                # alterTable1 = "ALTER TABLE audit_" + tbl[0] + " ADD COLUMN audit_id serial NOT NULL"
                # alterTable2 = "ALTER TABLE audit_" + tbl[0] + " ADD COLUMN audit_sql_action character(1) NOT NULL"
                # alterTable3 = "ALTER TABLE audit_" + tbl[0] + " ADD COLUMN audit_stamp timestamp without time zone NOT NULL"
                # alterTable4 = "ALTER TABLE audit_" + tbl[0] + " ADD COLUMN audit_user_id text NOT NULL"
                #===============================================================
                for found in cursorExe:
                    if found[4] == 'YES':
                        nullable = ''
                    else:
                        nullable = 'NOT NULL'
                        
                    if found[3] == None:
                        default_value = ''
                    else:
                        default_value = found[3]
                        
                    if found[1] == 'character varying':
                        print("{0}, {1}({2}), {3}, {4}".format(found[0], found[1], found[2], nullable, default_value))
                        fo.write("{0}, {1}({2}), {3}, {4}\n".format(found[0], found[1], found[2], nullable, default_value))
                    elif found[1] == 'character':
                        print("{0}, {1}({2}), {3}, {4}".format(found[0], found[1], found[2], nullable, default_value))
                        fo.write("{0}, {1}({2}), {3}, {4}\n".format(found[0], found[1], found[2], nullable, default_value))
                    elif found[1] == 'text':
                        print("{0}, {1}, {2}, {3}".format(found[0], found[1], nullable, default_value))
                        fo.write("{0}, {1}, {2}, {3}\n".format(found[0], found[1], nullable, default_value))
                    elif found[1] == 'integer':
                        print("{0}, {1}, {2}, {3}".format(found[0], found[1], nullable, default_value))
                        fo.write("{0}, {1}, {2}, {3}\n".format(found[0], found[1], nullable, default_value))
                    elif found[1] == 'date':
                        print("{0}, {1}, {2}, {3}".format(found[0], found[1], nullable, default_value))
                        fo.write("{0}, {1}, {2}, {3}\n".format(found[0], found[1], nullable, default_value))
                    elif found[1] == 'boolean':
                        print("{0}, {1}, {2}, {3}".format(found[0], found[1], nullable, default_value))
                        fo.write("{0}, {1}, {2}, {3}\n".format(found[0], found[1], nullable, default_value))
                    elif found[1] == 'double precision':
                        print("{0}, {1}, {2}, {3}".format(found[0], found[1], nullable, default_value))
                        fo.write("{0}, {1}, {2}, {3}\n".format(found[0], found[1], nullable, default_value))
                    elif found[1] == 'time without time zone':
                        print("{0}, {1}, {2}, {3}".format(found[0], found[1], nullable, default_value))
                        fo.write("{0}, {1}, {2}, {3}\n".format(found[0], found[1], nullable, default_value))
                    elif found[1] == 'bigint':
                        print("{0}, {1}, {2}, {3}".format(found[0], found[1], nullable, default_value))
                        fo.write("{0}, {1}, {2}, {3}\n".format(found[0], found[1], nullable, default_value))
                    elif found[1] == 'point':
                        print("{0}, {1}, {2}, {3}".format(found[0], found[1], nullable, default_value))
                        fo.write("{0}, {1}, {2}, {3}\n".format(found[0], found[1], nullable, default_value))
                    elif found[1] == 'polygon':
                        print("{0}, {1}, {2}, {3}".format(found[0], found[1], nullable, default_value))
                        fo.write("{0}, {1}, {2}, {3}\n".format(found[0], found[1], nullable, default_value))
                    elif found[1] == 'ARRAY':
                        print("{0}, text[]".format(found[0]))
                        fo.write("{0}, text[]\n".format(found[0]))
                    elif found[1] == 'timestamp with time zone':
                        print("{0}, {1}, {2}, {3}".format(found[0], found[1], nullable, default_value))
                        fo.write("{0}, {1}, {2}, {3}\n".format(found[0], found[1], nullable, default_value))
                    elif found[1] == 'timestamp without time zone':
                        print("{0}, {1}, {2}, {3}".format(found[0], found[1], nullable, default_value))
                        fo.write("{0}, {1}, {2}, {3}\n".format(found[0], found[1], nullable, default_value))
                    elif found[1] == 'smallint':
                        print("{0}, {1}, {2}, {3}".format(found[0], found[1], nullable, default_value))
                        fo.write("{0}, {1}, {2}, {3}\n".format(found[0], found[1], nullable, default_value))
                    elif found[1] == 'path':
                        print("{0}, {1}, {2}, {3}".format(found[0], found[1], nullable, default_value))
                        fo.write("{0}, {1}, {2}, {3}\n".format(found[0], found[1], nullable, default_value))
                    elif found[1] == 'bytea':
                        print("{0}, {1}, {2}, {3}".format(found[0], found[1], nullable, default_value))
                        fo.write("{0}, {1}, {2}, {3}\n".format(found[0], found[1], nullable, default_value))
                    elif found[1] == 'numeric':
                        print("{0}, {1}, {2}, {3}".format(found[0], found[1], nullable, default_value))
                        fo.write("{0}, {1}, {2}, {3}\n".format(found[0], found[1], nullable, default_value))
                    elif found[1] == 'xml':
                        print("{0}, {1}, {2}, {3}".format(found[0], found[1], nullable, default_value))
                        fo.write("{0}, {1}, {2}, {3}\n".format(found[0], found[1], nullable, default_value))
                    else:
                        print("~~~~Unknown data type " + found[1])
                        fo.write("~~~~Unknown data type \n" + found[1])
            except:
                print("Something Failed in the query.")
                fo.write("Something Failed in the query.\n")
            
            fo.close()
                
    # Cursor Cleanup
    cursorTbl.close()
    cursorCol.close()
    cursorExe.close()
            
if __name__ == "__main__":
    createDataDictionary(['casescustomers', 'sections', 'pole', 'customers', 'meterbase', 'calls', 'omstocislog', 'calls_events', 'pingdetails', 'cases_events', 'cases', 'device', 'crew_actions_history', 'trucks', 'interface_errors', 'interface_errors_mobile', 'case_truck_member_history', 'omsnotes', 'settings', 'tags_history', 'cistoomslog', 'preferences', 'case_causes', 'interface_errors_sql', 'ivrcalls', 'truck_members', 'tags', 'callbundles', 'commonsettings', 'setup', 'imqueue', 'crews', 'ivrcallerrors', 'scada_device_map', 'tag_status'])
    #createDataDictionary(['callbundles'])
    print("Script Completed.")