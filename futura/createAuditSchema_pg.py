'''
Title: Create OMS Audit Schema for In-Depth Troubleshooting
Created: Jun 27, 2013
Modified: Feb 21, 2014

@author: williamg

@version: 0.5

'''

def createAuditSchema(host=None, db=None, user=None, pw=None, auditSchema=None, mainSchema='public', table_list=[]):
    # Check table_list for data; Data validation IS NOT performed at this time.
    if len(table_list) == 0:
        print("Table_List is empty. Creating Audit Table for ALL available OMS tables")
        #return -1
    
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
        conn = psy.connect(conn_string)

        # Create independent cursors
        cursorTbl = conn.cursor()
        cursorCol = conn.cursor()
        cursorExe = conn.cursor()
        cursorFunc = conn.cursor()
        cursorAuditTable = conn.cursor()
        cursorDropFunc = conn.cursor()
        cursorBackupTable = conn.cursor()
        cursorDropTable = conn.cursor()
        cursorCreateTable = conn.cursor()
        cursorCreateFunction = conn.cursor()
        cursorCreateTrigger = conn.cursor()
        
        # Create a timestamp
        curtime = str(dt.datetime.now()).replace(' ','_').replace('-','').replace(':','').replace('.','')
        
    except:
        print("Failed to create connection(s) to database.")
        exit()
            
    # Get list of tables for OMS schema
    sql_omsTables = """SELECT c.relname 
        FROM pg_catalog.pg_class c 
        LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace 
        WHERE n.nspname='""" + mainSchema + """' 
        AND c.relkind IN ('r','') 
        AND n.nspname NOT IN ('pg_catalog', 'pg_toast', 'information_schema') 
        AND c.relname NOT like 'audit_%'
        ORDER BY c.relname ASC"""
    
    # Execute the cursor to obtain the OMS Schema list
    cursorTbl.execute(sql_omsTables)
    availableTables = [tbl[0] for tbl in cursorTbl]
    #print(availableTables)
    #print(table_list)
    
    #determine if all tables or just a selection of table will be audited
    #TODO error trap empty string in other list positions other than index[0]
    process_tables = []
    if len(table_list) > 0 and table_list[0] != '':
        for aTbl in table_list:
            #print(availableTables.index(aTbl))
            if aTbl not in availableTables:
                print('Table "{0}" does not exist in database {1}'.format(aTbl, db))
            else:
                process_tables.append(aTbl)
    else:
        process_tables = availableTables

    counter = 0
    # Loop thru each table and print the table definition in CSV format
    for tbl in process_tables:
        counter += 1
        print("{0}: Processing {1}".format(counter, tbl))
        #===================================================================
        #DROP Trigger IF EXISTS
        #===================================================================
        createTrigger = True
        try:
            sql_audit_trg_exists = "SELECT count(trigger_name) AS trigger_name_count FROM information_schema.triggers WHERE trigger_schema = '" + mainSchema + "' and trigger_name = 'audit_" + tbl + "_trg' GROUP BY trigger_name"
            # Execute sql to obtain the attribute definitions of each table
            cursorExe.execute(sql_audit_trg_exists)
             
            triggers = [foundTRG for foundTRG in cursorExe]
            
            if len(triggers) == 1 and triggers[0][0] == 3:
                # Backup existing audit table
                print("    FOUND: audit_" + tbl + "_trg")
                try:
                    sql_drop_trigger = "DROP TRIGGER audit_" + tbl + "_trg ON " + mainSchema + "." + tbl
                    cursorExe.execute(sql_drop_trigger)
                    conn.commit()
                     
                    print("    DROPPED audit_" + tbl + "_trg")
                except:
                    print("    ERROR: Failed to drop trigger: audit_" + tbl + "_trg")
                    conn.rollback()
                    createTrigger = False
            else:
                print("    WARNING: audit_" + tbl + "_trg NOT FOUND.")
                
        except:
            print("    SQL EXCEPTION: audit_" + tbl + "_trg.")

        #===================================================================
        # DROP Function IF EXISTS
        #===================================================================
        createFunction = True
        try:
            sql_audit_function_exists = "SELECT 1 FROM information_schema.routines WHERE specific_schema = '" + mainSchema + "' and routine_type = 'FUNCTION' and routine_name = 'audit_" + tbl + "'"
            cursorFunc.execute(sql_audit_function_exists)
            
            functions = [foundFUNC for foundFUNC in cursorFunc]
            if len(functions) == 1 and functions[0][0] == 1:
                print("    FOUND: audit_" + tbl + "() function")
                try:
                    sql_drop_function = "DROP FUNCTION " + mainSchema + ".audit_" + tbl + "() CASCADE"
                    cursorDropFunc.execute(sql_drop_function)
                    conn.commit()
                    
                    print("    DROPPED Function: audit_" + tbl + "()")
                except:
                    print("    ERROR: Failed to drop function: audit_" + tbl + "()")
                    conn.rollback()
                    createFunction = False
            else:
                print("    WARNING: Function audit_" + tbl + "() NOT FOUND.")

        except:
            print("    SQL EXCEPTION: Function audit_" + tbl + "()")
            
        #===================================================================
        # Backup then DROP Audit Table IF EXISTS
        #===================================================================
        print("    Backup then DROP Audit Table IF EXISTS")
        createAuditTable = True
        try:
            sql_audit_tbl_exists = "SELECT 1 FROM information_schema.tables WHERE table_schema = '" + auditSchema + "' and table_name = 'audit_" + tbl + "'"
            # Execute sql to obtain the attribute definitions of each table
            cursorAuditTable.execute(sql_audit_tbl_exists)
            auditTables = [auditTable for auditTable in cursorAuditTable]
            if len(auditTables) == 1 and auditTables[0][0] == 1:
                # Backup existing audit table
                print("    FOUND: audit_" + tbl)
                dropAuditTable = False
                try:
                    sql_backup_table = "SELECT * INTO oms_archives.archive_" + curtime + "_audit_" + tbl + " FROM " + auditSchema + ".audit_" + tbl
                    cursorBackupTable.execute(sql_backup_table)
                    conn.commit()
                    dropAuditTable = True
                    print("    audit_" + tbl + " BACKED UP to oms_archives.archive_" + curtime + "_audit_" + tbl)
                    # Drop existing audit table
                except:
                    print("    ERROR: Unable to backup audit_" + tbl)
                    conn.rollback()
                
                if dropAuditTable:
                    try:
                        cursorDropTable.execute("DROP TABLE " + auditSchema + ".audit_" + tbl)
                        conn.commit()
                        print("    audit_" + tbl + ": dropped")
                        
                    except:
                        print("    ERROR: Unable to drop audit table for " + tbl)
                        conn.rollback()
                        createAuditTable = False
                else:
                    createAuditTable = False
            else:
                print("    WARNING: audit_" + tbl + " NOT FOUND.")
                
        except:
            print("    EXCEPTION: audit_" + tbl)
                
    
        #===============================================================
        # Create New Audit Table (from one row of existing OMS table)
        #===============================================================
        
        if createAuditTable:
            print("    Create New Audit Table (from one row of existing OMS table)")
            try:
                sqlCreateTable = "SELECT * INTO " + auditSchema + ".audit_" + tbl + " FROM " + mainSchema + "." + tbl + " LIMIT 0"
                print("    " + sqlCreateTable)
                try:
                    cursorCreateTable.execute(sqlCreateTable)
                    conn.commit()
                    print("    NEW: Created new audit table: audit_" + tbl)
                except:
                    print("    Audit_" + tbl + " creation failed")
                    conn.rollback()
                
                try:
                    # Add Audit Fields to table
                    alterTable1 = "ALTER TABLE " + auditSchema + ".audit_" + tbl + " ADD COLUMN audit_id serial NOT NULL"
                    cursorExe.execute(alterTable1)
                    conn.commit()
                    alterTable2 = "ALTER TABLE " + auditSchema + ".audit_" + tbl + " ADD COLUMN audit_sql_action character(1) NOT NULL"
                    cursorExe.execute(alterTable2)
                    conn.commit()
                    alterTable3 = "ALTER TABLE " + auditSchema + ".audit_" + tbl + " ADD COLUMN audit_stamp timestamp without time zone NOT NULL"
                    cursorExe.execute(alterTable3)
                    conn.commit()
                    alterTable4 = "ALTER TABLE " + auditSchema + ".audit_" + tbl + " ADD COLUMN audit_user_id text NOT NULL"
                    cursorExe.execute(alterTable4)
                    conn.commit()
                    print("    NEW: Audit fields added!")
                except:
                    print("    ERROR: Failed to add audit fields to audit_" + tbl)
                    conn.rollback()

            except:
                print("    ERROR: Could not create audit table for " + tbl)

        #===================================================================
        # Create Function
        #===================================================================
        if createFunction:
            try:
                sql_create_function = """ -- Create function for getting information to be inserted into audit table
                                    CREATE OR REPLACE FUNCTION """ + mainSchema + """.audit_""" + tbl + """() RETURNS TRIGGER AS $usr_audit$
                                        BEGIN
                                            IF (TG_OP = 'DELETE') THEN
                                                INSERT INTO """ + auditSchema + """.audit_""" + tbl + """ VALUES (OLD.*, DEFAULT, 'D', now(), user);
                                                RETURN OLD;
                                            ELSIF (TG_OP = 'UPDATE') THEN
                                                INSERT INTO """ + auditSchema + """.audit_""" + tbl + """ VALUES (NEW.*, DEFAULT, 'U', now(), user);
                                                RETURN NEW;
                                            ELSIF (TG_OP = 'INSERT') THEN
                                                INSERT INTO """ + auditSchema + """.audit_""" + tbl + """ VALUES (NEW.*, DEFAULT, 'I', now(), user);
                                                RETURN NEW;
                                            END IF;
                                            RETURN NULL; -- result is ignored since this is an AFTER trigger
                                        END;
                                    $usr_audit$ LANGUAGE plpgsql;"""
                cursorCreateFunction.execute(sql_create_function)
                conn.commit()
                
                print("    NEW: Created Function audit_" + tbl + "()")
            except:
                print("    ERROR: Failed to create Function audit_" + tbl)
                conn.rollback()
        
        #===================================================================
        # Create Trigger
        #===================================================================
        if createTrigger:
            try:
                sql_create_trigger = """ -- Create Trigger to execute the function for inserting audit information
                                        CREATE TRIGGER audit_""" + tbl + """_trg AFTER INSERT OR UPDATE OR DELETE ON """ + mainSchema + """.""" + tbl + """
                                        FOR EACH ROW EXECUTE PROCEDURE audit_""" + tbl + """();"""
                cursorCreateTrigger.execute(sql_create_trigger)
                conn.commit()
                
                print("    NEW: Created Trigger: audit_" + tbl + "_trg")
            except:
                print("    ERROR: Could not create trigger for " + tbl)
                conn.rollback()

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
    
def moveAuditData(host=None, db=None, user=None, pw=None, srcSchema=None, destSchema=None):
    try:
        import psycopg2 as psy
        #import psycopg2.extras as psyExtras
        import datetime as dt
    except:
        print("Failed to import python-postgresql drivers.")
        exit()
    try:
        # Connection String
        conn_string = "host='{0}' dbname='{1}' user='{2}' password='{3}'".format(host, db, user, pw)
        # Create independent connections
        conn = psy.connect(conn_string)
        # Create independent cursors
        cursorTbl = conn.cursor()
        #Create list of Audit Tables to Move
        cursorTbl.execute("""SELECT c.relname 
        FROM pg_catalog.pg_class c 
        LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace 
        WHERE n.nspname='""" + srcSchema + """' 
        AND c.relkind IN ('r','') 
        AND n.nspname NOT IN ('pg_catalog', 'pg_toast', 'information_schema') 
        AND c.relname like 'audit_%'
        ORDER BY c.relname ASC""")
        auditTables = [tbl[0] for tbl in cursorTbl]
        # Create a timestamp
        curtime = str(dt.datetime.now()).replace(' ','_').replace('-','').replace(':','').replace('.','')
    except:
        print("Failed to create connection(s) to database.")
        exit()
        
    print(curtime)
    for table in auditTables:
        #sql_backup_table = "SELECT * INTO oms_archives.archive_" + curtime + "_audit_" + tbl[0] + " FROM " + auditSchema + ".audit_" + tbl[0]
        sql = "INSERT INTO {0}.{1} SELECT * FROM {2}.{3}".format(destSchema, table, srcSchema, table)
        try:
            cursorTbl.execute(sql)
            cursorTbl.execute("DROP TABLE IF EXISTS {0}.{1} CASCADE".format(srcSchema, table))
            conn.commit()
            print("Audit Data Migrated: {0}".format(table))
        except Exception as e:
            print(table + " errors:")
            conn.rollback()
            print(e)
            #print("Move existing audit data from public to oms_audit schema failed")
    print(curtime)
    del cursorTbl

if __name__ == "__main__":
    host = 'localhost'
    db = 'coweta-fayette'
    user = 'postgres'
    pw = 'usouth'
    srcSchema = 'public'
    destSchema = 'oms_audits'
    
    #moveAuditData(host, db, user, pw, srcSchema, destSchema)
    createAuditSchema(host, db, user, pw, destSchema, srcSchema, [''])
    print("Script Completed")