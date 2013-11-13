'''
Title: Insert OMS Logs into oms_logging db
Created: May 7, 2013
Modified: October 7, 2013

@author: williamg

@version: 0.29
'''

import sys

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
            sys.exit()
        
        try:
            import datetime as dt
        except:
            print("Failed to import datetime module.")
            sys.exit()
            
        try:
            conn_string = "host='localhost' dbname='"+db+"' user='postgres' password='usouth'"
            conn = psy.connect(conn_string)
            cursor = conn.cursor()
            curtime = dt.datetime.now()
            print(curtime)
            del cursor
            
        except:
            print("Failed to create connection to database.")
            sys.exit()

def backupOMSLogs(host=None, db=None, schema=None, archive=None):
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
        return errors
    else:
        try:
            import psycopg2 as psy
        except:
            print("Failed to import python-postgresql drivers.")
            return -4
        
        try:
            import datetime as dt
        except:
            print("Failed to import datetime module.")
            return -3
            
    try:
        conn_string = "host='" + host + "' dbname='" + db + "' user='postgres' password='usouth'"
        conn = psy.connect(conn_string)
        cursor = conn.cursor()
        curtime = dt.datetime.now()
        backup_tbl = str(curtime).replace(' ','_').replace('-','').replace(':','').replace('.','')
        #truncate = False
        try:
            sql_omslogs = "SELECT * INTO {0}.log_{1}_omslogs from {2}.omslogs;".format(archive, backup_tbl, schema)
            #print(sql)
            cursor.execute(sql_omslogs)
            conn.commit()
            #truncate = True
        except:
            print("Failed to backup oms_logfiles.omslogs")
            return -2
            
        #=======================================================================
        # if truncate:
        #     cursor.execute("TRUNCATE {0}.omslogs;".format(schema))
        #     conn.commit()
        #     return 1
        #=======================================================================
        return 1
    
    except:
        return -1
    

def importLogfiles(host=None, db=None, schema=None, f=None, rename=True):
    """ 
    Parse supplied logfile (f) and insert into provided database (db)
    @var db: the database to insert the logfile contents
    @var f: the file name including the full path to the log file.
    """
    
    import os
    
    try:
        import psycopg2 as psy
        import datetime as dt
    except:
        print("Failed to import python-postgresql drivers.")
        exit()

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
        return errors
    else:
        import re
        conn_string = "host='" + host + "' dbname='" + db + "' user='postgres' password='usouth'"
        conn = psy.connect(conn_string)
        cursor = conn.cursor()
        
        print("Importing " + f)
        fo = open(f, "r")
        last_values = {}
        lineNumber = 0
        for line in fo:
            lineNumber += 1
            if len(line.strip()) == 0 or line == '\n':
                pass
            else:
                matchObj = re.match(r'\d{4}-\d{2}-\d{2}', line[:10], re.U)
                if matchObj:
                    date_ = line[:10]
                    last_values['date_'] = date_
                    time_ = line[11:23]
                    last_values['time_'] = time_
                    if line.find(": ",26) == -1:
                        category = 'unknown'
                        message = line[27:]
                    else:
                        category = line[26:line.find(": ",26)]
                        message = line[line.find(": ",27)+2:].replace('\n', '')
                    try:
                        sqlInsert = u"""INSERT INTO {0}.omslogs (date_, time_, category, message, logfile) VALUES (to_date('{1}', 'YYYY-MM-DD'), to_timestamp('{2}', 'HH24:MI:SS,MS'), '{3}', {4}, {5});\n""".format(schema, date_, time_, category, psy.extensions.QuotedString(message.replace('\n', '')).getquoted(), psy.extensions.QuotedString(f).getquoted())
                        cursor.execute(sqlInsert)
                        cursor.execute('COMMIT;')
                        #cursor.execute("""INSERT INTO omsclient (date_, time_, time_ms, category, message) VALUES (to_date('{0}', 'YYYY-MM-DD'), to_timestamp('{1}', 'HH24:MI:SS'), {2}, '{3}', {4});\n""".format(date_, time_, time_ms, category, psycopg2.extensions.QuotedString(message).getquoted()))
                    except:
                        sqlInsert = u"""INSERT INTO {0}.omslogs (date_, time_, category, message, logfile) VALUES (to_date('{1}', 'YYYY-MM-DD'), to_timestamp('{2}', 'HH24:MI:SS,MS'), '{3}', {4}, {5});\n""".format(schema, last_values['date_'], last_values['time_'], 'issue', psy.extensions.QuotedString(line.replace('\n', '')).getquoted(), psy.extensions.QuotedString(f).getquoted())
                        cursor.execute(sqlInsert)
                        cursor.execute('COMMIT;')
                else:
                    sqlInsert = u"""INSERT INTO {0}.omslogs (date_, time_, category, message, logfile) VALUES (to_date('{1}', 'YYYY-MM-DD'), to_timestamp('{2}', 'HH24:MI:SS,MS'), '{3}', {4}, {5});\n""".format(schema, last_values['date_'], last_values['time_'], 'additional_lines', psy.extensions.QuotedString(line.replace('\n', '')).getquoted(), psy.extensions.QuotedString(f).getquoted())
                    cursor.execute(sqlInsert)
                    cursor.execute('COMMIT;')
            
        fo.close()
        del cursor
        curtime = str(dt.datetime.now()).replace(' ','_').replace('-','').replace(':','').replace('.','')
        try:
            fileinfo = os.path.split(f)
            destination = fileinfo[0] + os.sep + "logged_" + curtime + "_" + fileinfo[1]
            if rename:
                os.rename(f, destination)
                print("    Renamed " + f + " to logged_" + curtime + "_" + fileinfo[1])
        except:
            print("    Could not rename log file: " + f)
            
        return "    Completed file " + f

def importLogs(host=None, db=None, logfile=None, rename=True):
    if logfile is None:
        print("No file was provided. Exiting...")
        exit()
        
    #import needed modules
    import os, glob
    import datetime as dt
    
    #check if base name of file exists
    logfileExists = os.path.isfile(logfile)
    
    if logfileExists == False:
        #print a statement that file path provided is not useful then exit
        print("No files available for import. ")
        return None
    
    #Adding wildcard to path for glob.iglob to find all files with matching basename    
    logfile += "*"
    
    try:
        #create a list of logfiles with base name file provided
        logfiles = [log for log in glob.iglob(logfile)]
        
    except:
        print("Failed to execute finding all files with logfile basename")
        exit()
        
    #begin processing files
    #print("Beginning Import")
    if len(logfiles) > 0:
        for f in logfiles: 
            try:
                objmodel_starttime = dt.datetime.now()
                print(importLogfiles(host, db, 'oms_logfiles', f, rename))
                objectmodel_run_time = dt.datetime.now()
                print("    Imported in " + str(objectmodel_run_time-objmodel_starttime))
            except:
                print("    Couldn't import " + f)
    else:
        print("No new logs to be inserted!")

if __name__ == "__main__":
    # Update the database before running the utility --What does this mean? wg on 2013-09-19
    host = 'omsprod'
    db = 'inland_20130926'
    logfile_schema = 'oms_logfiles'
    archive_schema = 'oms_archives'
    renameFile = True
    
    ### Should be no need to modify anything below this line ###
    import datetime as dt
    starttime = dt.datetime.now()
    print("Started Existing Log Backup Process: " + str(starttime))
    backup = backupOMSLogs(host, db, logfile_schema, archive_schema)
    #print(backup)
    if backup == 1:
        print("Starting Import process: " + str(dt.datetime.now()))
        importLogs(host, db, "\\\\omsprod\\c$\\omsprint\\Logs\\ObjectModel\\objectmodel.log", renameFile)
        importLogs(host, db, "\\\\omsprod\\c$\\omsprint\\Logs\\OMSClient\\omsclient.log", renameFile)
        importLogs(host, db, "\\\\omsprod\\C$\\Program Files (x86)\\Futura Systems\\Futura OMS\\Bin\\SaveData\\Logs\\Savedata\\savedata.log", renameFile)

        
        endtime = dt.datetime.now()
    else:
        if type(backup) is int:
            print("OMS Console Data Backup failed with error code: {0}".format(str(backup)))
        else:
            for err in backup:
                print(err)
        endtime = dt.datetime.now()
    
    print("Total script time: " + str(endtime-starttime))
