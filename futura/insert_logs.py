'''
Title: Insert OMS Logs into oms_logging db
Created: May 7, 2013
Modified: October 7, 2013

@author: williamg

@version: 0.29
'''

import sys

def createLoggingSchema(db=None, schema=None, u=None, p=None):
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
            conn_string = "host='" + host + "' dbname='" + db + "' user='" + u + "' password='" + p + "'"
            conn = psy.connect(conn_string)
            cursor = conn.cursor()
            curtime = dt.datetime.now()
            print(curtime)
            del cursor
            
        except:
            print("Failed to create connection to database.")
            sys.exit()

def backupOMSLogs(host=None, db=None, u=None, p=None, schema=None, archive=None):
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
        conn_string = "host='" + host + "' dbname='" + db + "' user='" + u + "' password='" + p + "'"
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
        except Exception as e:
            print("Failed to backup oms_logfiles.omslogs")
            print(e)
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
    

def importLogfiles(host=None, db=None, u=None, p=None, schema=None, f=None, rename=True):
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
        conn_string = "host='" + host + "' dbname='" + db + "' user='" + u + "' password='" + p + "'"
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
                if re.match(r'\d{4}-\d{2}-\d{2}', line[:10], re.U):
                    date_ = line[:10]
                elif re.match(r'\d{2}-\d{2}-\d{4}', line[:10], re.U):
                    date_ = "{0}-{1}".format(line[6:10], line[:5])
                else:
                    date_ = None
                    
                if date_ <> None:
                    #date_ = line[:10]
                    last_values['date_'] = date_
                    endTime = line.find(' ',11)
                    time_ = line[11:endTime]
                    last_values['time_'] = time_
                    
                    #Assumes Log4j is configured to use [] around log level (category)
                    beginCategory = line.find("[",0,30)
                    if beginCategory == -1:
                        category = 'No Category'
                        message = line[24:]
                    else:
                        endCategory = line.find("]",beginCategory)+1
                        category = line[beginCategory:endCategory]
                        message = line[endCategory:].replace('\n', '')
                    try:
                        sqlInsert = u"""INSERT INTO {0}.omslogs (date_, time_, category, message, logfile) VALUES (to_date('{1}', 'YYYY-MM-DD'), to_timestamp('{2}', 'HH24:MI:SS,MS'), '{3}', {4}, {5});\n""".format(schema, date_, time_, category, psy.extensions.QuotedString(message.replace('\n', '')).getquoted(), psy.extensions.QuotedString(f).getquoted())
                        cursor.execute(sqlInsert)
                        #conn.commit()
                        #cursor.execute("""INSERT INTO omsclient (date_, time_, time_ms, category, message) VALUES (to_date('{0}', 'YYYY-MM-DD'), to_timestamp('{1}', 'HH24:MI:SS'), {2}, '{3}', {4});\n""".format(date_, time_, time_ms, category, psycopg2.extensions.QuotedString(message).getquoted()))
                    except:
                        sqlInsert = u"""INSERT INTO {0}.omslogs (date_, time_, category, message, logfile) VALUES (to_date('{1}', 'YYYY-MM-DD'), to_timestamp('{2}', 'HH24:MI:SS,MS'), '{3}', {4}, {5});\n""".format(schema, last_values['date_'], last_values['time_'], 'insert_issue', psy.extensions.QuotedString(line.replace('\n', '')).getquoted(), psy.extensions.QuotedString(f).getquoted())
                        cursor.execute(sqlInsert)
                        #conn.commit()
                else:
                    sqlInsert = u"""INSERT INTO {0}.omslogs (date_, time_, category, message, logfile) VALUES (to_date('{1}', 'YYYY-MM-DD'), to_timestamp('{2}', 'HH24:MI:SS,MS'), '{3}', {4}, {5});\n""".format(schema, last_values['date_'], last_values['time_'], 'additional_lines', psy.extensions.QuotedString(line.replace('\n', '')).getquoted(), psy.extensions.QuotedString(f).getquoted())
                    cursor.execute(sqlInsert)
                    #conn.commit()
            if lineNumber % 2500 == 0:
                conn.commit()
                #print(str(lineNumber) + " successfully committed")
            
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

def importLogs(host=None, db=None, u=None, p=None, logfile=None, rename=True):
    if logfile is None:
        print("No file was provided. Exiting...")
        exit()
        
    #import needed modules
    #import os
    import glob
    import datetime as dt
    
    #check if base name of file exists
    #logfileExists = os.path.isfile(logfile)
    
    #if logfileExists == False:
        #print a statement that file path provided is not useful then exit
        #print("No files available for import. ")
        #return None
    
    #Adding wildcard to path for glob.iglob to find all files with matching basename    
    logfile += "*"
    
    try:
        #create a list of logfiles with base name file provided
        logfiles = [log for log in glob.iglob(logfile)]
        
    except:
        print("Failed to execute finding all files with logfile basename")
        return None
        
    #begin processing files
    #print("Beginning Import")
    if len(logfiles) > 0:
        for f in logfiles: 
            try:
                objmodel_starttime = dt.datetime.now()
                result = importLogfiles(host, db, u, p, 'oms_logfiles', f, rename) 
                print(result)
                objectmodel_run_time = dt.datetime.now()
                print("    Imported in " + str(objectmodel_run_time-objmodel_starttime))
            except Exception as e:
                print("    Couldn't import " + f)
                print(e)
    else:
        print("No new logs to be inserted!")

if __name__ == "__main__":
    #
    # Update the parameters & log file path before running the utility
    #
    host = 'localhost'
    db = 'wiregrass_121' #north_ga_logs #wiregrass_2_2_0_84 #oms_inland_power
    u = 'postgres'
    p = 'usouth'
    logfile_schema = 'oms_logfiles'
    archive_schema = 'oms_archives'
    renameFile = True
    
    ### Should be no need to modify anything below this line ###
    import datetime as dt
    starttime = dt.datetime.now()
    print("Started Existing Log Backup Process: " + str(starttime))
    backup = backupOMSLogs(host, db, u, p, logfile_schema, archive_schema)
    #print(backup)
    if backup == 1:
        print("Starting Import process: " + str(dt.datetime.now()))
        
        importLogs(host, db, u, p, r"C:\map_files\Logs\ObjectModel\objectmodel.log", renameFile)
        importLogs(host, db, u, p, r"C:\map_files\Logs\OMSClient\omsclient.log", renameFile)
        importLogs(host, db, u, p, r"C:\map_files\Logs\SaveData\savedata.log", renameFile)
        
        """
        importLogs(host, db, u, p, r"C:\oms_logs\omsprod\ObjectModel\objectmodel.log", renameFile)
        importLogs(host, db, u, p, r"C:\oms_logs\omsprod\OMSClient\omsclient.log", renameFile)
        importLogs(host, db, u, p, r"C:\oms_logs\omsprod\SaveData\savedata.log", renameFile)
        """
        
        endtime = dt.datetime.now()
    else:
        if type(backup) is int:
            print("OMS Console Data Backup failed with error code: {0}".format(str(backup)))
        else:
            for err in backup:
                print(err)
        endtime = dt.datetime.now()
    
    print("Total script time: " + str(endtime-starttime))
