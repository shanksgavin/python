'''
Title: Create OMS Audit Schema for In-Depth Troubleshooting
Created: Jul 9, 2013
Modified: n/a

@author: williamg

@version: 0.1
'''

def backupAuditSchema(db='omsprod'):
    """ 
    Back up Audit Tables into the Archive DB on FTA_WilliamG
    
    @var db: The name of the source database to be archived
    """ 
    try:
        import psycopg2 as psy
        #import psycopg2.extras as psyExtras
        import datetime as dt
    except:
        print("Failed to import python-postgresql drivers.")
        exit()
        
    try:
        # Connection String
        conn_string = "host='localhost' dbname='" + db + "' user='postgres' password='usouth'"
        
        # Create independent connections
        connTbl = psy.connect(conn_string)
        connBackupTable = psy.connect(conn_string)
        connTruncateTable = psy.connect(conn_string)
        
        # Create independent cursors
        cursorTbl = connTbl.cursor()
        cursorBackupTable = connBackupTable.cursor()
        cursorTruncateTable = connTruncateTable.cursor()
        
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
        AND c.relname ilike 'audit_%' 
        ORDER BY c.relname ASC"""
    
    # Execute the cursor to obtain the OMS Schema list
    cursorTbl.execute(sql_omsTables)
    
    # Loop thru each table and print the table definition in CSV format
    for tbl in cursorTbl:
        print("Backup {0}".format(tbl[0]))
        
        #===================================================================
        # Backup Audit Table
        #===================================================================
        truncate = True
        try:
            sql_backup_table = "SELECT * INTO oms_archives.archive_" + curtime + "_" + tbl[0] + " FROM public." + tbl[0]
            cursorBackupTable.execute(sql_backup_table)
            cursorBackupTable.execute("COMMIT")
            print("    public." + tbl[0] + " BACKED UP to oms_archives.archives_" + curtime + "_" + tbl[0])
            
        except:
            print("    ERROR: Unable to backup existing audit table: " + tbl[0]) 
            truncate = False
            
        #===================================================================
        # Truncate Audit Table
        #===================================================================
        if truncate:
            try:
                sql_truncate_table = "TRUNCATE public." + tbl[0]
                cursorTruncateTable.execute(sql_truncate_table)
                cursorTruncateTable.execute("COMMIT")
                print("    " + tbl[0] + " TRUNCATED.")
            except:
                print("    ERROR: Failed to Truncate table: " + tbl[0])
                
    # Cursor Cleanup
    cursorTbl.close()
    cursorBackupTable.close()
    cursorTruncateTable.close()
    
    
            
if __name__ == "__main__":
    backupAuditSchema('wiregrass_2_2_0_84')
    print("Script Completed")