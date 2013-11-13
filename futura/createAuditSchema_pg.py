'''
Title: Create OMS Audit Schema for In-Depth Troubleshooting
Created: Jun 27, 2013
Modified: Oct 11, 2013

@author: williamg

@version: 0.5

'''

def createAuditSchema(host=None, db='omsprod', user=None, pw=None, table_list=[]):
    # Check table_list for data; Data validation IS NOT performed at this time.
    if len(table_list) == 0:
        print("Table_List is empty. Must provide at least one table to describe")
        return -1
    
    try:
        import psycopg2 as psy
        #import psycopg2.extras as psyExtras
        import datetime as dt
    except:
        print("Failed to import python-postgresql drivers.")
        exit()
        
    try:
        # Connection String
        conn_string = "host='" + host + "' dbname='" + db + "' user='" + user + "' password='" + pw + "'"
        
        # Create independent connections
        connTbl = psy.connect(conn_string)
        connCol = psy.connect(conn_string)
        connExe = psy.connect(conn_string)
        connFunc = psy.connect(conn_string)
        connAuditTable = psy.connect(conn_string)
        connDropFunc = psy.connect(conn_string)
        connBackupTable = psy.connect(conn_string)
        connDropTable = psy.connect(conn_string)
        connCreateTable = psy.connect(conn_string)
        connTruncateTable = psy.connect(conn_string)
        connCreateFunction = psy.connect(conn_string)
        connCreateTrigger = psy.connect(conn_string)
        
        # Create independent cursors
        cursorTbl = connTbl.cursor()
        cursorCol = connCol.cursor()
        cursorExe = connExe.cursor()
        cursorFunc = connFunc.cursor()
        cursorAuditTable = connAuditTable.cursor()
        cursorDropFunc = connDropFunc.cursor()
        cursorBackupTable = connBackupTable.cursor()
        cursorDropTable = connDropTable.cursor()
        cursorCreateTable = connCreateTable.cursor()
        cursorTruncateTable = connTruncateTable.cursor()
        cursorCreateFunction = connCreateFunction.cursor()
        cursorCreateTrigger = connCreateTrigger.cursor()
        
        # Create a timestamp
        curtime = str(dt.datetime.now()).replace(' ','_').replace('-','').replace(':','').replace('.','')
        
    except:
        print("Failed to create connection(s) to database.")
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
    
    counter = 0
    # Loop thru each table and print the table definition in CSV format
    for tbl in cursorTbl:
        if tbl[0] in table_list:
            counter += 1
            print("{0}: Processing {1}".format(counter, tbl[0]))
            #DROP Trigger IF EXISTS
            createTrigger = True
            try:
                sql_audit_trg_exists = "SELECT count(trigger_name) AS trigger_name_count FROM information_schema.triggers WHERE trigger_schema = 'public' and trigger_name = 'audit_" + tbl[0] + "_trg' GROUP BY trigger_name"
                # Execute sql to obtain the attribute definitions of each table
                cursorExe.execute(sql_audit_trg_exists)
                 
                triggers = [foundTRG for foundTRG in cursorExe]
                #print(triggers)
                if len(triggers) == 1 and triggers[0][0] == 3:
                    # Backup existing audit table
                    print("    FOUND: audit_" + tbl[0] + "_trg")
                    try:
                        sql_drop_trigger = "DROP TRIGGER audit_" + tbl[0] + "_trg ON " + tbl[0]
                        cursorExe.execute(sql_drop_trigger)
                        cursorExe.execute("COMMIT")
                         
                        print("    DROPPED audit_" + tbl[0] + "_trg")
                    except:
                        print("    ERROR: Failed to drop trigger: audit_" + tbl[0] + "_trg")
                        createTrigger = False
                else:
                    print("    WARNING: audit_" + tbl[0] + "_trg NOT FOUND.")
                    
                    #break
            except:
                print("    SQL EXCEPTION: audit_" + tbl[0] + "_trg.")

            #===================================================================
            # DROP Function IF EXISTS
            #===================================================================
            #print("DROP Function IF EXISTS")
            createFunction = True
            try:
                sql_audit_function_exists = "SELECT 1 FROM information_schema.routines WHERE specific_schema = 'public' and routine_type = 'FUNCTION' and routine_name = 'audit_" + tbl[0] + "'"
                cursorFunc.execute(sql_audit_function_exists)
                
                functions = [foundFUNC for foundFUNC in cursorFunc]
                if len(functions) == 1 and functions[0][0] == 1:
                    print("    FOUND: audit_" + tbl[0] + "() function")
                    try:
                        sql_drop_function = "DROP FUNCTION audit_" + tbl[0] + "() CASCADE"
                        cursorDropFunc.execute(sql_drop_function)
                        cursorDropFunc.execute("COMMIT")
                        
                        print("    DROPPED Function: audit_" + tbl[0] + "()")
                    except:
                        print("    ERROR: Failed to drop function: audit_" + tbl[0] + "()")
                        createFunction = False
                else:
                    print("    WARNING: Function audit_" + tbl[0] + "() NOT FOUND.")

            except:
                print("    SQL EXCEPTION: Function audit_" + tbl[0] + "()")
                
            #===================================================================
            # Backup then DROP Audit Table IF EXISTS
            #===================================================================
            print("    Backup then DROP Audit Table IF EXISTS")
            createAuditTable = True
            try:
                sql_audit_tbl_exists = "SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' and table_name = 'audit_" + tbl[0] + "'"
                # Execute sql to obtain the attribute definitions of each table
                #print(sql_audit_tbl_exists)
                cursorAuditTable.execute(sql_audit_tbl_exists)
                #print(cursorAuditTable)
                auditTables = [auditTable for auditTable in cursorAuditTable]
                    #print("auditTable: " + str(auditTable))
                if len(auditTables) == 1 and auditTables[0][0] == 1:
                    # Backup existing audit table
                    print("    FOUND: audit_" + tbl[0])
                    dropAuditTable = False
                    try:
                        sql_backup_table = "SELECT * INTO oms_archives.archive_" + curtime + "_audit_" + tbl[0] + " FROM public.audit_" + tbl[0]
                        cursorBackupTable.execute(sql_backup_table)
                        cursorBackupTable.execute("COMMIT")
                        dropAuditTable = True
                        print("    audit_" + tbl[0] + " BACKED UP to oms_archives.archive_" + curtime + "_audit_" + tbl[0])
                        # Drop existing audit table
                    except:
                        print("    ERROR: Unable to backup audit_" + tbl[0])
                    
                    if dropAuditTable:
                        try:
                            #print("Attempting to drop table audit_" + tbl[0])
                            cursorDropTable.execute("DROP TABLE audit_" + tbl[0])
                            cursorDropTable.execute("COMMIT")
                            print("    audit_" + tbl[0] + ": dropped")
                            
                        except:
                            print("    ERROR: Unable to drop audit table for " + tbl[0])
                            createAuditTable = False
                    else:
                        createAuditTable = False
                else:
                    print("    WARNING: audit_" + tbl[0] + " NOT FOUND.")
                    
            except:
                print("    EXCEPTION: audit_" + tbl[0])
                    
        
            #===============================================================
            # Create New Audit Table (from one row of existing OMS table)
            #===============================================================
            
            if createAuditTable:
                print("    Create New Audit Table (from one row of existing OMS table)")
                try:
                    #print("~~~~Trying to Create table as ...")
                    sqlCreateTable = "SELECT * INTO audit_" + tbl[0] + " FROM " + tbl[0] + " LIMIT 0"
                    print("    " + sqlCreateTable)
                    try:
                        #print("    TRYING...")
                        cursorCreateTable.execute(sqlCreateTable)
                        cursorCreateTable.execute("COMMIT")
                        #print("    @@CREATE Table completed.")
                        print("    NEW: Created new audit table: audit_" + tbl[0])
                    except:
                        print("    Audit_" + tbl[0] + " creation failed")
                    #cursorCreateTable.execute("COMMIT")
                    
                    #===========================================================
                    # try:
                    #     # Clear out (truncate) audit table before using
                    #     print("Truncating...")
                    #     sqlTruncateTable = "TRUNCATE TABLE audit_" + tbl[0]
                    #     cursorTruncateTable.execute(sqlTruncateTable)
                    #     cursorTruncateTable.execute("COMMIT")
                    #     cursorTruncateTable.close()
                    #     print("    TRUNCATED audit_" + tbl[0])
                    #     
                    # except:
                    #     print("    ERROR: Failed to truncate table " + tbl[0])
                    #===========================================================
                
                    try:
                        # Add Audit Fields to table
                        #print("    Adding audit fields to table")
                        alterTable1 = "ALTER TABLE audit_" + tbl[0] + " ADD COLUMN audit_id serial NOT NULL"
                        cursorExe.execute(alterTable1)
                        cursorExe.execute("COMMIT")
                        alterTable2 = "ALTER TABLE audit_" + tbl[0] + " ADD COLUMN audit_sql_action character(1) NOT NULL"
                        cursorExe.execute(alterTable2)
                        cursorExe.execute("COMMIT")
                        alterTable3 = "ALTER TABLE audit_" + tbl[0] + " ADD COLUMN audit_stamp timestamp without time zone NOT NULL"
                        cursorExe.execute(alterTable3)
                        cursorExe.execute("COMMIT")
                        alterTable4 = "ALTER TABLE audit_" + tbl[0] + " ADD COLUMN audit_user_id text NOT NULL"
                        cursorExe.execute(alterTable4)
                        cursorExe.execute("COMMIT")
                        print("    NEW: Audit fields added!")
                    except:
                        print("    ERROR: Failed to add audit fields to audit_" + tbl[0])

                except:
                    print("    ERROR: Could not create audit table for " + tbl[0])

            #===================================================================
            # Create Function
            #===================================================================
            if createFunction:
                try:
                    sql_create_function = """ -- Create function for getting information to be inserted into audit table
                                        CREATE OR REPLACE FUNCTION audit_""" + tbl[0] + """() RETURNS TRIGGER AS $usr_audit$
                                            BEGIN
                                                IF (TG_OP = 'DELETE') THEN
                                                    INSERT INTO audit_""" + tbl[0] + """ VALUES (OLD.*, DEFAULT, 'D', now(), user);
                                                    RETURN OLD;
                                                ELSIF (TG_OP = 'UPDATE') THEN
                                                    INSERT INTO audit_""" + tbl[0] + """ VALUES (NEW.*, DEFAULT, 'U', now(), user);
                                                    RETURN NEW;
                                                ELSIF (TG_OP = 'INSERT') THEN
                                                    INSERT INTO audit_""" + tbl[0] + """ VALUES (NEW.*, DEFAULT, 'I', now(), user);
                                                    RETURN NEW;
                                                END IF;
                                                RETURN NULL; -- result is ignored since this is an AFTER trigger
                                            END;
                                        $usr_audit$ LANGUAGE plpgsql;"""
                    cursorCreateFunction.execute(sql_create_function)
                    cursorCreateFunction.execute("COMMIT")
                    
                    print("    NEW: Created Function audit_" + tbl[0] + "()")
                except:
                    print("    ERROR: Failed to create Function audit_" + tbl[0])
            
            #===================================================================
            # Create Trigger
            #===================================================================
            if createTrigger:
                try:
                    sql_create_trigger = """ -- Create Trigger to execute the function for inserting audit information
                                            CREATE TRIGGER audit_""" + tbl[0] + """_trg AFTER INSERT OR UPDATE OR DELETE ON """ + tbl[0] + """
                                            FOR EACH ROW EXECUTE PROCEDURE audit_""" + tbl[0] + """();"""
                    cursorCreateTrigger.execute(sql_create_trigger)
                    cursorCreateTrigger.execute("COMMIT")
                    
                    print("    NEW: Created Trigger: audit_" + tbl[0] + "_trg")
                except:
                    print("    ERROR: Could not create trigger for " + tbl[0])

    # Cursor Cleanup
    cursorTbl.close()
    cursorCol.close()
    cursorExe.close()
    cursorFunc.close()
    cursorAuditTable.close()
    cursorCreateTrigger.close()
    cursorCreateFunction.close()
    cursorCreateTable.close()
    cursorDropTable.close()
    cursorBackupTable.close()
    cursorDropFunc.close()
    
            
if __name__ == "__main__":
    createAuditSchema('localhost', 'wiregrass_2_2_0_84', 'postgres', 'usouth', ['casescustomers', 'sections', 'pole', 'customers', 'meterbase', 'calls', 'omstocislog', 'calls_events', 'pingdetails', 'cases_events', 'cases', 'device', 'crew_actions_history', 'trucks', 'interface_errors', 'interface_errors_mobile', 'case_truck_member_history', 'omsnotes', 'settings', 'tags_history', 'cistoomslog', 'preferences', 'case_causes', 'interface_errors_sql', 'ivrcalls', 'truck_members', 'tags', 'callbundles', 'commonsettings', 'setup', 'imqueue', 'crews', 'ivrcallerrors', 'scada_device_map', 'tag_status', 'export_status', 'new_export_status'])
    #createAuditSchema('wiregrass_2_2_0_74', ['cases', 'calls'])
    print("Script Completed")