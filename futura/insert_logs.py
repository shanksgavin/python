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
    
    import os, shutil
        
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
            d1 = dt.datetime.today().strftime("%Y-%m-%d")
            try:
                #create new directory based on current date 
                os.makedirs(fileinfo[0]+os.sep+d1)
            except:
                #path already exists
                pass
            #Build destination path
            destination = fileinfo[0] + os.sep + d1 + os.sep + "logged_" + curtime + "_" + fileinfo[1]
            if rename:
                #move file into a folder named based on the day of import
                shutil.move(f, destination)
                #os.rename(f, destination)
                print("    Renamed {0} to {1}".format(f, destination))
        except:
            print("    Could not rename log file: " + f)
            
        return "    Completed file " + f

def importLogs(host=None, db=None, u=None, p=None, logfile=None, logfile_schema=None, rename=True):
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
                result = importLogfiles(host, db, u, p, logfile_schema, f, rename) 
                print(result)
                objectmodel_run_time = dt.datetime.now()
                print("    Imported in " + str(objectmodel_run_time-objmodel_starttime))
            except Exception as e:
                print("    Couldn't import " + f)
                print(e)
    else:
        print("No new logs to be inserted!")

def run(d_logs):
    importLogs(d_logs['host'], d_logs['db'], d_logs['u'], d_logs['p'], d_logs['objectmodel'], d_logs['logfile_schema'], d_logs['renameFile'])
    importLogs(d_logs['host'], d_logs['db'], d_logs['u'], d_logs['p'], d_logs['omsclient'], d_logs['logfile_schema'], d_logs['renameFile'])
    importLogs(d_logs['host'], d_logs['db'], d_logs['u'], d_logs['p'], d_logs['savedata'], d_logs['logfile_schema'], d_logs['renameFile'])
    
if __name__ == "__main__":
    #
    # Update the parameters & log file path before running the utility
    #
    d_logs_local = {
        'host'      : 'localhost',
        'db'        : 'wiregrass_121',
        'u'         : 'postgres',
        'p'         : 'usouth',
        'logfile_schema': 'oms_logfiles',
        'archive_schema': 'oms_archives',
        'renameFile'    : True,
        'archive'       : True,
        'oms_log_path'  :       r'C:\map_files\Logs',
        'intg_serv_path':       r'C:\map_files\Logs',
        'webservice_path':      r'C:\map_files\Logs',
        'objectmodel'   :       r'C:\map_files\Logs\ObjectModel\objectmodel.log',
        'omsclient'     :       r'C:\map_files\Logs\OMSClient\omsclient.log',
        'savedata'      :       r'C:\map_files\Logs\SaveData\savedata.log',
        'integrationservice':   r'C:\map_files\Logs\IntegrationService\FuturaOMS_Integration_ServiceLog.txt',
        'ami'       :           r'C:\map_files\Logs\ObjectModel\objectmodel.log',
        'ami_test'  :           r'C:\map_files\Logs\ObjectModel\objectmodel.log',
        'avl'       :           r'C:\map_files\Logs\ObjectModel\objectmodel.log',
        'calltracker':          r'C:\map_files\Logs\ObjectModel\objectmodel.log',
        'crc'       :           r'C:\map_files\Logs\ObjectModel\objectmodel.log',
        'ivr'       :           r'C:\map_files\Logs\ObjectModel\objectmodel.log',
        'scada'     :           r'C:\map_files\Logs\ObjectModel\objectmodel.log',
        'upn'       :           r'C:\map_files\Logs\ObjectModel\objectmodel.log'
    }
    
    d_logs_omsprod = {
        'host': 'omsprod',
        'db': 'inland_30130926',
        'u': 'postgres',
        'p': 'usouth',
        'logfile_schema': 'oms_logfiles',
        'archive_schema': 'oms_archives',
        'renameFile': True,
        'archive': True,
        'objectmodel':          r'C:\oms_logs\omsprod\ObjectModel\objectmodel.log',
        'omsclient':            r'C:\oms_logs\omsprod\OMSClient\omsclient.log',
        'savedata':             r'C:\oms_logs\omsprod\SaveData\savedata.log',
        'integrationservice':   r'C:\map_files\Logs\IntegrationService\FuturaOMS_Integration_ServiceLog.txt',
    }
    
    """
    # assign the active path dictionary before running
    """
    d_logs = d_logs_local
    
    
    ### Should be no need to modify anything below this line ###
    import datetime as dt
    starttime = dt.datetime.now()
    
    if d_logs['archive'] == True:
        print("Started Existing Log Backup Process: " + str(starttime))
        backup = backupOMSLogs(d_logs['host'], d_logs['db'], d_logs['u'], d_logs['p'], d_logs['logfile_schema'], d_logs['archive_schema'])
        print(backup)

    if d_logs['archive'] == True and backup == 1:
        print("Starting Import process: " + str(dt.datetime.now()))
        
        run(d_logs)
        
        endtime = dt.datetime.now()
    elif d_logs['archive'] == True and backup != 1:
        if type(backup) is int:
            print("OMS Console Data Backup failed with error code: {0}".format(str(backup)))
        else:
            for err in backup:
                print(err)
        endtime = dt.datetime.now()
    elif d_logs['archive'] == False:
        print("Not Archiving OMSLOGS table prior to this Import process")
        print("Starting Import process: " + str(dt.datetime.now()))
        
        run(d_logs)
        
        endtime = dt.datetime.now()
    
    print("Total script time: " + str(endtime-starttime))
