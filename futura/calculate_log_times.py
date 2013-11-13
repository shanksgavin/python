'''
Title: Calculate the time between logged operations
Created: September 25, 2013
Modified: 

@author: williamg

@version: 0.01
'''

def createLoggingSchema(db=None, schema=None):
    """
    Function to create the schema for importing log files
    """
    errors = tuple()
    if db is None:
        errors += ("database not supplied",)
    if schema is None:
        errors += ("schema not supplied",)
    #test if any errors exist. if any exit function and return errors
    if len(errors) > 0:
        return errors
    else:
        try:
            import psycopg2 as psy
        except:
            print("Failed to import python-postgresql drivers.")
            exit()
        
        try:
            import datetime as dt
            from datetime import date
        except:
            print("Failed to import datetime module.")
            exit()
            
        try:
            conn_string = "host='localhost' dbname='"+db+"' user='postgres' password='usouth'"
            conn = psy.connect(conn_string)
            cursor = conn.cursor()
            curtime = dt.datetime.now()
            print(curtime)
            del cursor
            
        except:
            print("Failed to create connection to database.")
            exit()

def logOperationTime(db=None, schema=None):
    """
    Function to calculate time between operations in log files
    
    @var db: database name
    @var schema: source schema
    
    """
    errors = tuple()
    if db is None:
        errors += ("database not supplied",)
    if schema is None:
        errors += ("schema not supplied",)
        
    #test if any errors exist. if any exit function and return errors
    if len(errors) > 0:
        return errors
    else:
        try:
            import psycopg2 as psy
        except:
            print("Failed to import python-postgresql drivers.")
            exit()
            
    try:
        conn_string = "host='localhost' dbname='" + db + "' user='postgres' password='usouth'"
        conn = psy.connect(conn_string)
        cursor = conn.cursor()
        #truncate = False
        try:
            sql_omslogs = "SELECT oid, time_ from {0}.omslogs order by date_ asc, time_ asc, log_id asc;".format(schema)
            #print(sql_omslogs)
            cursor.execute(sql_omslogs)
            #conn.commit()
            #truncate = True
        except:
            print("Failed to backup oms_logfiles.omslogs")
            return -2
        
        #auditTables = [auditTable for auditTable in cursorAuditTable]
        newOID = 0
        oldOID = 0
        afterFirstCycle = False
        oids = [oid for oid in cursor]
        countDown = len(oids)
        #print(len(oids))
        
        #Establish cursor for use inside of loop
        cursorBeginTime = conn.cursor()
        cursorInsertTime = conn.cursor()
        
        for oid in oids:
            #print('Processing OID: ' + str(oid[0]))
            #print(afterFirstCycle)
            if afterFirstCycle:
                #sqlCursorBeginTime = 'SELECT time_ from {0}.omslogs where oid = {1}'.format(schema, oid[0])
                #print(sqlCursorBeginTime)
                #cursorBeginTime.execute(sqlCursorBeginTime)
                #startTime = [start for start in cursorBeginTime]
                #newOID = startTime[0][0]
                newOID = oid[1]
                
                
                #print(newOID.total_seconds(), oldOID.total_seconds())
                try:
                    tDelta = dt.datetime.combine(dt.date.today(), newOID) - dt.datetime.combine(dt.date.today(), oldOID)
                except Exception as e:
                    print(e)
                    
                #print(tDelta.total_seconds())
                try:
                    sqlInsertTime = 'UPDATE {0}.omslogs SET time_delta = {1} WHERE oid = {2};'.format(schema, tDelta.total_seconds(), oid[0])
                    cursorInsertTime.execute(sqlInsertTime)
                    cursorInsertTime.execute('COMMIT;')
                except:
                    print('failed to insert ' + str(tDelta.total_seconds()))
                #Set new oid as old before moving to the next oid
                oldOID = newOID

                countDown -= 1
                #print(countDown, oid)
                
            else:
                #sqlCursorBeginTime = 'SELECT time_ from {0}.omslogs where oid = {1}'.format(schema, oid[0])
                #print(sqlCursorBeginTime)
                #cursorBeginTime.execute(sqlCursorBeginTime)
                #startTime = [start for start in cursorBeginTime]
                
                #print(startTime)
                #oldOID = startTime[0][0]
                oldOID = oid[1]
                
                try:
                    sqlInsertTime = 'UPDATE {0}.omslogs SET time_delta = {1} WHERE oid = {2};'.format(schema, -999, oid[0])
                    cursorInsertTime.execute(sqlInsertTime)
                    cursorInsertTime.execute('COMMIT;')
                except:
                    print('failed to insert -999')
                #print('-999')
                afterFirstCycle = True
        
        del cursorInsertTime
        del cursorBeginTime
        return 1
    
    except:
        return "Error Code: {0}  Remaining OIDs: {1}  Last oid: {2}".format(-1, countDown, oid[0])
    


if __name__ == "__main__":
    # Update the database before running the utility --What does this mean? wg on 2013-09-19
    db = 'oms_coos_curry'
    logfile_schema = 'oms_logfiles'
    
    ### Should be no need to modify anything below this line ###
    import datetime as dt
    starttime = dt.datetime.now()
    print("Started Calculating Operation Time Deltas: " + str(starttime))
    print(logOperationTime(db, logfile_schema))
    print("Total script time: " + str(dt.datetime.now()-starttime))
