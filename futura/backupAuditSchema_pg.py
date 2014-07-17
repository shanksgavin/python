'''
Title: Create OMS Audit Schema for In-Depth Troubleshooting
Created: Jul 9, 2013
Modified: n/a

@author: williamg

@version: 0.1
'''

def backupAuditData(host=None, db=None, user=None, pw=None, srcSchema=None, destSchema=None):
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
        # Create a timestamp
        curtime = str(dt.datetime.now()).replace(' ','_').replace('-','').replace(':','').replace('.','')[:-6]
    except:
        print("Failed to create connection(s) to database.")
        exit()
    print(dt.datetime.now())
    
    # Select all audit tables with data
    # Get list of tables for OMS schema
    sql_omsTables = """SELECT relname
      FROM pg_stat_user_tables 
      WHERE schemaname = '""" + srcSchema + """'
      GROUP BY relname, n_live_tup
      HAVING n_live_tup > 0
      ORDER BY n_live_tup DESC;"""
    
    # Execute the cursor to obtain the OMS Schema list
    cursorTbl.execute(sql_omsTables)
    availableTables = [tbl[0] for tbl in cursorTbl]
    
    counter = 0
    for table in availableTables:
        counter += 1
        #['callbundles','calls','calls_events','case_causes','case_truck_member_history','cases','cases_events','casescustomers','cistoomslog','commonsettings','crew_actions_history','crews','customers','device','export_status','imqueue','interface_errors','interface_errors_mobile','interface_errors_sql','ivrcallerrors','ivrcalls','meterbase','new_export_status','omsnotes','pole','preferences','sections','settings','setup','tag_status','tags','tags_history','truck_members','trucks']:
        
        #sql_backup_table = "SELECT * INTO oms_archives.archive_" + curtime + "_audit_" + tbl[0] + " FROM " + auditSchema + ".audit_" + tbl[0]
        destinationTable = "{0}.archive_{1}_{2}".format(destSchema, curtime, table)
        sql = "SELECT * INTO {0} FROM {1}.{2}".format(destinationTable, srcSchema, table)
        try:
            cursorTbl.execute(sql)
            conn.commit()
            cursorTbl.execute("TRUNCATE " + srcSchema + "." + table)
            print("{0:>3}: Audit Data Archived for {1}".format(str(counter), table))
        except Exception as e:
            print(table + " errors:")
            conn.rollback()
            print(e)
            #print("Move existing audit data from public to oms_audit schema failed")
    print(dt.datetime.now())
    del cursorTbl
            
if __name__ == "__main__":
    host = 'localhost'
    db = 'coweta-fayette'
    user = 'postgres'
    pw = 'usouth'
    srcSchema = 'oms_audits'
    destSchema = 'oms_archives'
    
    backupAuditData(host, db, user, pw, srcSchema, destSchema)
    print("Script Completed")