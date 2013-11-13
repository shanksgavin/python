'''
Title: Cleanup Homer Test Data by removing duplicate entries from cases table
Created: Jul 11, 2013
Modified: n/a

@author: williamg

@version: 0.1
'''

def cleanup(db='omsprod'):
    """ 
    Cleanup Homer Test data in omsprod_homer DB on FTA_WilliamG
    
    @var db: The name of the source database to be cleaned
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
        connCases = psy.connect(conn_string)
        connOIDs = psy.connect(conn_string)
        connDeleteOIDs = psy.connect(conn_string)
        
        # Create independent cursors
        cursorCases = connCases.cursor()
        cursorOIDs = connOIDs.cursor()
        cursorDeleteOIDs = connDeleteOIDs.cursor()
        
        # Create a timestamp
        curtime = str(dt.datetime.now()).replace(' ','_').replace('-','').replace(':','').replace('.','')
        
    except:
        print("Failed to create connection(s) to database.")
        exit()
            
    #print(str(curtime))
    
    # Get list of tables for OMS schema
    sql_cases = """
    select distinct(elementid, phase, casenum, datestrt), count(casenum), casenum, elementid
    from cases
    group by elementid, phase, casenum, datestrt
    order by count desc, (elementid, phase, casenum, datestrt) asc
    """
    
    # Execute the cursor to obtain the OMS Schema list
    cursorCases.execute(sql_cases)
    
    # Loop thru each table and print the table definition in CSV format
    counter = 0
    for case in cursorCases:
        if case[1] > 1:
            counter += 1
            rowCounter = case[1]
            print("{0:<5}: Case {1:<14} has {2} entries".format(counter, case[2], case[1]))
            
            sql_oids = "SELECT oid FROM cases WHERE casenum = '" + case[2] + "' AND elementid = '" + case[3] + "'"
            #print(sql_oids)
            cursorOIDs.execute(sql_oids)
            
            for oid in cursorOIDs:
                if rowCounter > 1:
                    rowCounter -= 1
                    #print(str(rowCounter))
                    try:
                        sql_delete = "DELETE FROM cases where oid = " + str(oid[0])
                        cursorDeleteOIDs.execute(sql_delete)
                        cursorDeleteOIDs.execute("COMMIT")
                        print("    Deleted OID: {0} from Case: {1} and Elementid: {2}".format(str(oid[0]), case[2], case[3]))
                    except:
                        print("failure")

    # Cursor Cleanup
    cursorCases.close()
    cursorOIDs.close()
    cursorDeleteOIDs.close()
    
    
            
if __name__ == "__main__":
    cleanup('omsprod_homer')
    print("Script Completed")