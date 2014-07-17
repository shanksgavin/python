'''
Title: Insert OMS Logs into oms_logging db
Created: May 7, 2013
Modified: June 3, 2014

@author: williamg

@todo: Validate time_ for each line being formatted into SQL; see notes in code
@todo: Add check for file locks in case Integration Service is running during log import
@todo: General Cleanup
@todo: Review entire process for conciseness and bugs
@todo: Make process object oriented 
'''

import sys
import datetime as dt

def createLoggingSchema(d_logs):
    """
    Function to create the schema for importing log files
    """
    errors = tuple()
    if d_logs['db'] is None:
        errors += ("database not supplied",)
    if d_logs['logfile_schema'] is None:
        errors += ("schema not supplied",)
    #test if any errors exist. if any exit function and return errors
    if len(errors) > 0:
        return errors
    else:
        try:
            import psycopg2 as psy
        except:
            print("Failed to import python-postgresql drivers.")
            sys.exit()
        
        try:
            conn_string = "host='{0}' dbname='{1}' user='{2}' password='{3}'".format(d_logs['host'],d_logs['db'],d_logs['u'],d_logs['p'])
            conn = psy.connect(conn_string)
            cursor = conn.cursor()
            curtime = dt.datetime.now()
            print(curtime)
            del cursor
            
        except:
            print("Failed to create connection to database.")
            sys.exit()

def backupOMSLogs(host=None, db=None, u=None, p=None, schema=None, archive=None, truncate=False):
    """
    Function to backup the schema for log files
    
    @var db: database name
    @var schema: source schema
    @var archive: archive schema
    
    """
    errors = tuple()
    if host is None:
        errors += ("Host not supplied",)
    if db is None:
        errors += ("database not supplied",)
    if schema is None:
        errors += ("schema not supplied",)
    if archive is None:
        errors += ("archive schema not supplied",)
        
    #test if any errors exist. if any exit function and return errors
    if len(errors) > 0:
        for e in errors:
            print(e)
        return False
    else:
        try:
            import psycopg2 as psy
        except Exception as e:
            print("Failed to import python-postgresql drivers.")
            print(e)
            return False
            
    try:
        conn_string = "host='{0}' dbname='{1}' user='{2}' password='{3}'".format(host, db, u, p)
        conn = psy.connect(conn_string)
        cursor = conn.cursor()
        curtime = dt.datetime.now()
        backup_tbl = str(curtime).replace(' ','_').replace('-','').replace(':','').replace('.','')
        try:
            sql_omslogs = "SELECT * INTO {0}.log_{1}_pg_logs from {2}.pg_logs;".format(archive, backup_tbl, schema)
            #print(sql)
            cursor.execute(sql_omslogs)
            conn.commit()
            
        except Exception as e:
            print("Failed to backup oms_logfiles.pg_logs")
            print(e)
            return False
            
        # Truncate Table OMS_LOGFILES.OMSLOGS
        if truncate: #Default is False
            try:
                cursor.execute("TRUNCATE {0}.pg_logs;".format(schema))
                conn.commit()
                return True
            except Exception as e:
                print(e)
                return False
        else:
            return True
    
    except Exception as e:
        print(e)
        return False
    
def importLogfiles(host=None, db=None, u=None, p=None, schema=None, f=None):
    """ 
    Parse supplied logfile (f) and insert into provided database (db)
    @var db: the database to insert the logfile contents
    @var f: the file name including the full path to the log file.
    """
    
    try:
        import psycopg2 as psy
        #import datetime as dt
    except Exception as e:
        print("Failed to import python-postgresql drivers.")
        print(e)
        return False

    errors = tuple()
    if host is None:
        errors += ("host not supplied",)
    if db is None:
        errors += ("database not supplied",)
    if f is None:
        errors += ("filename not Supplied",)
    if schema is None:
        errors += ("schema not supplied",)
    #test if any errors exist. if any exit function and return errors
    if len(errors) > 0:
        for e in errors:
            print(e)
        return False
    else:
        # Set values for iterating through file
        #last_values = {}
        lineNumber = 0
        
        try:
            import csv
            conn_string = "host='{0}' dbname='{1}' user='{2}' password='{3}'".format(host, db, u, p)
            conn = psy.connect(conn_string)
            cursor = conn.cursor()

            print("Importing " + f)
            #fo = open(f, "r")
            with open(f, 'rb') as fo:
                reader = csv.reader(fo)

                #Loop through file
                for line in reader:
                    lineNumber += 1
                    timestamp_ = line[0]
                    category = line[7]
                    message = line[13][len('execute <unnamed>: '):]
                    params = line[14]
                    
                    # Need to validate time before moving forward
                    # The logging Config file can display time incorrectly as text
                    # e.g. HH:mm:ss.SSS -> 14:25:36.SSS
                    # Format should be ss.fff in web.config
                    
                    #Assumes Log4j is configured to use [] around log level (category)
                    try:
                        sqlInsert = u"INSERT INTO {0}.pg_logs (timestamp_, category, message, params, logfile) VALUES (to_timestamp('{1}', 'YYYY-MM-DD HH24:MI:SS.MS'), '{2}', {3}, {4}, {5});".format(schema, timestamp_, category, psy.extensions.QuotedString(message.replace('\n', '').strip()).getquoted(), psy.extensions.QuotedString(params).getquoted(), psy.extensions.QuotedString(f).getquoted())
                        cursor.execute(sqlInsert)
                    except:
                        sqlInsert = u"INSERT INTO {0}.pg_logs (timestamp_, category, message, logfile) VALUES (to_timestamp('{1}', 'YYYY-MM-DD HH24:MI:SS.MS'), '{2}', {3}, {4});".format(schema, timestamp_, 'insert_issue at line:' + reader.line_num, psy.extensions.QuotedString(line).getquoted(), psy.extensions.QuotedString(f).getquoted())
                        cursor.execute(sqlInsert)

                    if lineNumber % 5000 == 0:
                        conn.commit()
                        #print(str(lineNumber) + " successfully committed")
                    
                #fo.close()
                    
                del cursor
                
                print("    Import Completed for {0}".format(f))
                return True
        
        except Exception as e:
            print("    Error on line: {0}\nDetails: {1}".format(lineNumber, e))
            return False

def createIndex(host=None, db=None, u=None, p=None, schema=None): # Creates MD5 hash index on message column
    try:
        import psycopg2 as psy
        #import datetime as dt
    except Exception as e:
        print("Failed to import python-postgresql drivers.")
        print(e)
        return False
    
    # Build connection string
    conn_string = "host='{0}' dbname='{1}' user='{2}' password='{3}'".format(host, db, u, p)
    conn = psy.connect(conn_string)
    cursor = conn.cursor()
    
    # Drop Index Before (Re)building
    try:
        sqlDropIndex = u'DROP INDEX IF EXISTS {0}.pg_logs_ndx_message;'.format(schema)
        cursor.execute(sqlDropIndex)
    except Exception as e:
        print(e)
        return False
    
    # Build Index on log table
    try:
        sqlCreateIndex = u'CREATE INDEX pg_logs_ndx_message ON {0}.pg_logs (md5(message));'.format(schema)
        cursor.execute(sqlCreateIndex)
    except Exception as e:
        print(e)
        return False
    
    return True
        
def cleanupLogFile(f=None, rename=True, move=True):
    # Log File Management (Move & Rename)
    if f is None:
        print('File not provided for cleanup.')
        return False
    
    #import required modules
    import os, shutil
    
    #format timestamp for file renaming
    curtime = str(dt.datetime.now()).replace(' ','_').replace('-','').replace(':','').replace('.','')
    
    fileinfo = os.path.split(f)
    d1 = dt.datetime.today().strftime("%Y-%m-%d")
    try: #create new directory based on current date 
        os.makedirs(fileinfo[0]+os.sep+d1)
    except: #path already exists
        pass
    #Build destination path
    if rename: #Rename File
        if move: #And Move File
            try:
                #move file into a folder named based on the day of import
                destination = fileinfo[0] + os.sep + d1 + os.sep + "logged_" + curtime + "_" + fileinfo[1]
                shutil.move(f, destination)
                return True
            except Exception as e:
                print(e)
                return False
        else: #Rename But Do Not Move
            try:
                destination = fileinfo[0] + os.sep + "logged_" + curtime + "_" + fileinfo[1]
                os.rename(f, destination)
                return True
            except Exception as e:
                print(e)
                return False
        
    else: #Do Not Rename
        if move: #But Move
            try:
                #move file into a folder named based on the day of import
                destination = fileinfo[0] + os.sep + d1 + os.sep + fileinfo[1]
                shutil.move(f, destination)
                return True
            except Exception as e:
                print(e)
                return False
        else: #Do Not Rename Or Move
            return True

def findLogFiles(logBasename=None):
    if logBasename is None:
        print('Path not provided.')
        return None
    
    #import modules
    import glob, os
    
    # get basename from path provided
    #print(logBasename)
    bp = os.path.split(logBasename)
    
    try:
        # create list of files with same basepath (bp)
        if bp[1] == '*.csv':
            logfiles = [log for log in glob.iglob(logBasename)]
            return logfiles #returns a list
        else:
            print('No CSV Log Files Found: {0}'.format(bp))
            return None
    except Exception as e:
        print(e)
        return None

def run(d_logs):
    """
    loop over available log paths
    See dictionaries below
    """
    for logfile in d_logs['oms_log_path']:
        logs = findLogFiles(d_logs['oms_log_path'][logfile])
        #print('Logs Returned: {0}'.format(logs))
        if logs is not None:
            for log in logs:
                #print('Import Log: {0}'.format(log))
                #importLogs(d_logs['host'], d_logs['db'], d_logs['u'], d_logs['p'], log, d_logs['logfile_schema'], d_logs['renameFile'])
                starttime = dt.datetime.now()
                result = importLogfiles(d_logs['host'], d_logs['db'], d_logs['u'], d_logs['p'], d_logs['logfile_schema'], log)
                #print(result)
                if result:
                    resultCleanup = cleanupLogFile(log, d_logs['renameFile'], d_logs['moveFile'])
                    if resultCleanup:
                        print("    Cleanup Successful")
                else:
                    print('Import Failed: {0}'.format(log))
                endtime = dt.datetime.now()
                print("    Import Elasped: {0}".format(str(endtime-starttime)))

if __name__ == "__main__":
    #
    # Update the parameters & log file path before running the utility
    #

    d_logs_coweta_fayette = {
        'host'          : 'localhost',
        'db'            : 'coweta-fayette',
        'u'             : 'postgres',
        'p'             : 'usouth',
        'logfile_schema': 'oms_logfiles',
        'archive_schema': 'oms_archives',
        'renameFile'    : False,
        'moveFile'      : True,
        'archive'       : True,
        'truncate'      : True,
        'oms_log_path'  : {'pg_logs':r'C:\Program Files (x86)\PostgreSQL\8.4\data\pg_log\*.csv'
                           }
                    }
    
    
    """
    # assign the active path dictionary before running
    """
    d_logs = d_logs_coweta_fayette
    
    
    ### Should be no need to modify anything below this line ###
    starttime = dt.datetime.now()
    
    if d_logs['archive']:
        print("Started Existing Log Backup Process: " + str(starttime))
        backup = backupOMSLogs(d_logs['host'], d_logs['db'], d_logs['u'], d_logs['p'], d_logs['logfile_schema'], d_logs['archive_schema'], d_logs['truncate'])
        #print(backup)
        if backup:
            print("Starting Import process: " + str(dt.datetime.now()))
            run(d_logs)
            endtime = dt.datetime.now()
        else:
            print("Backup Failed")
            endtime = dt.datetime.now()
    else:
        print("Not Archiving OMSLOGS table prior to this Import process")
        print("Starting Import process: " + str(dt.datetime.now()))
        run(d_logs)
        endtime = dt.datetime.now()
    
    print("Total script time: " + str(endtime-starttime))
