'''
Title: Insert OMS Logs into oms_logging db
Created: May 7, 2013
Modified: July 17, 2013

@author: williamg

@version: 0.24
'''

def createLoggingSchema(db=None, schema=None):
    try:
        import psycopg2 as psy
        import datetime as dt
    except:
        print("Failed to import python-postgresql drivers.")
        exit()
        
    try:
        conn_string = "host='localhost' dbname='oms_logging' user='postgres' password='usouth'"
        conn = psy.connect(conn_string)
        cursor = conn.cursor()
        curtime = dt.datetime.now()
        print(curtime)
        
    except:
        print("Failed to create connection to database.")
        exit()

def backupOMSLogging(db='omsprod'):
    try:
        import psycopg2 as psy
        import datetime as dt
    except:
        print("Failed to import python-postgresql drivers.")
        exit()
        
    try:
        conn_string = "host='localhost' dbname='" + db + "' user='postgres' password='usouth'"
        conn = psy.connect(conn_string)
        cursor = conn.cursor()
        curtime = dt.datetime.now()
        backup_tbl = str(curtime).replace(' ','_').replace('-','').replace(':','').replace('.','')
        sqlClient = "SELECT * INTO omsclient_"+backup_tbl+" from omsclient;"
        sqlObjModel = "SELECT * INTO obj_model_"+backup_tbl+" from obj_model;"
        sqlSaveData = "SELECT * INTO save_data_"+backup_tbl+" from save_data;"
        #print(sql)
        cursor.execute(sqlClient)
        conn.commit()
        cursor.execute(sqlObjModel)
        conn.commit()
        cursor.execute(sqlSaveData)
        conn.commit()
        cursor.execute("TRUNCATE omsclient;")
        conn.commit()
        cursor.execute("TRUNCATE obj_model;")
        conn.commit()
        cursor.execute("TRUNCATE save_data;")
        conn.commit()
        return 1
    except:
        return -1
    
def readLogFile(f=None):
    try:
        import psycopg2 as psy
        import datetime as dt
    except:
        print("Failed to import python-postgresql drivers.")
        exit()
        
    if f is None:
        return "No Filename Supplied"
    else:
        conn_string = "host='localhost' dbname='oms_logging' user='postgres' password='usouth'"
        conn = psy.connect(conn_string)
        cursor = conn.cursor()
        # Open File to read
        fo = open(f, "r")
        last_values = {}
        for line in fo:
            if len(line.strip()) == 0 or line == '\n':
                pass
            else:
                try:
                    int(line[:4])
                    date_ = line[:10]
                    last_values['date_'] = date_
                    time_ = line[11:23]
                    last_values['time_'] = time_
                    category = line[26:line.find(":",26)]
                    message = line[line.find(":",26)+2:-1]
                    sqlInsert = """INSERT INTO omsclient (date_, time_, category, message, logfile) VALUES (to_date('{0}', 'YYYY-MM-DD'), to_timestamp('{1}', 'HH24:MI:SS,MS'), '{2}', {3}, {4});\n""".format(date_, time_, category, psy.extensions.QuotedString(message).getquoted(), psy.extensions.QuotedString(f).getquoted())
                    #fw.write(sqlInsert)
                    #print(sqlInsert) 
                    cursor.execute(sqlInsert)
                    cursor.execute('COMMIT;')
                    #cursor.execute("""INSERT INTO omsclient (date_, time_, time_ms, category, message) VALUES (to_date('{0}', 'YYYY-MM-DD'), to_timestamp('{1}', 'HH24:MI:SS'), {2}, '{3}', {4});\n""".format(date_, time_, time_ms, category, psycopg2.extensions.QuotedString(message).getquoted()))
                except:
                    sqlInsert = """INSERT INTO omsclient (date_, time_, category, message, logfile) VALUES (to_date('{0}', 'YYYY-MM-DD'), to_timestamp('{1}', 'HH24:MI:SS,MS'), '{2}', {3}, {4});\n""".format(last_values['date_'], last_values['time_'], 'issue', psy.extensions.QuotedString(line).getquoted(), psy.extensions.QuotedString(f).getquoted())
                    #fw.write(sqlInsert)
                    cursor.execute(sqlInsert)
                    cursor.execute('COMMIT;')
            
        fo.close()
        #fw.close()
        return "completed file " + f

def importObjectModelLogs(f=None):
    try:
        import psycopg2 as psy
        import datetime as dt
    except:
        print("Failed to import python-postgresql drivers.")
        exit()

    if f is None:
        return "No Filename Supplied"
    else:
        import re
        conn_string = "host='localhost' dbname='oms_logging' user='postgres' password='usouth'"
        conn = psy.connect(conn_string)
        cursor = conn.cursor()
        
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
                        message = line[26:]
                    else:
                        category = line[26:line.find(": ",26)]
                        message = line[line.find(": ",26):].replace('\n', '')
                    try:
                        sqlInsert = u"""INSERT INTO obj_model (date_, time_, category, message, logfile) VALUES (to_date('{0}', 'YYYY-MM-DD'), to_timestamp('{1}', 'HH24:MI:SS,MS'), '{2}', {3}, {4});\n""".format(date_, time_, category, psy.extensions.QuotedString(message.replace('\n', '')).getquoted(), psy.extensions.QuotedString(f).getquoted())
                        cursor.execute(sqlInsert)
                        cursor.execute('COMMIT;')
                        #cursor.execute("""INSERT INTO omsclient (date_, time_, time_ms, category, message) VALUES (to_date('{0}', 'YYYY-MM-DD'), to_timestamp('{1}', 'HH24:MI:SS'), {2}, '{3}', {4});\n""".format(date_, time_, time_ms, category, psycopg2.extensions.QuotedString(message).getquoted()))
                    except:
                        sqlInsert = u"""INSERT INTO obj_model (date_, time_, category, message, logfile) VALUES (to_date('{0}', 'YYYY-MM-DD'), to_timestamp('{1}', 'HH24:MI:SS,MS'), '{2}', {3}, {4});\n""".format(last_values['date_'], last_values['time_'], 'issue', psy.extensions.QuotedString(line.replace('\n', '')).getquoted(), psy.extensions.QuotedString(f).getquoted())
                        cursor.execute(sqlInsert)
                        cursor.execute('COMMIT;')
                else:
                    sqlInsert = u"""INSERT INTO obj_model (date_, time_, category, message, logfile) VALUES (to_date('{0}', 'YYYY-MM-DD'), to_timestamp('{1}', 'HH24:MI:SS,MS'), '{2}', {3}, {4});\n""".format(last_values['date_'], last_values['time_'], 'additional_lines', psy.extensions.QuotedString(line.replace('\n', '')).getquoted(), psy.extensions.QuotedString(f).getquoted())
                    cursor.execute(sqlInsert)
                    cursor.execute('COMMIT;')
            
        #@todo:  implement a way to mark the files as being imported so next process can ignore or skip them
        fo.close()
        del cursor
        return "completed file " + f

def importOMSClientLogs(f=None):
    try:
        import psycopg2 as psy
        import datetime as dt
    except:
        print("Failed to import python-postgresql drivers.")
        exit()

    if f is None:
        return "No Filename Supplied"
    else:
        import re
        conn_string = "host='localhost' dbname='oms_logging' user='postgres' password='usouth'"
        conn = psy.connect(conn_string)
        cursor = conn.cursor()
        
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
                        message = line[26:]
                    else:
                        category = line[26:line.find(": ",26)]
                        message = line[line.find(": ",26):].replace('\n', '')
                    try:
                        sqlInsert = u"""INSERT INTO omsclient (date_, time_, category, message, logfile) VALUES (to_date('{0}', 'YYYY-MM-DD'), to_timestamp('{1}', 'HH24:MI:SS,MS'), '{2}', {3}, {4});\n""".format(date_, time_, category, psy.extensions.QuotedString(message.replace('\n', '')).getquoted(), psy.extensions.QuotedString(f).getquoted())
                        cursor.execute(sqlInsert)
                        cursor.execute('COMMIT;')
                        #cursor.execute("""INSERT INTO omsclient (date_, time_, time_ms, category, message) VALUES (to_date('{0}', 'YYYY-MM-DD'), to_timestamp('{1}', 'HH24:MI:SS'), {2}, '{3}', {4});\n""".format(date_, time_, time_ms, category, psycopg2.extensions.QuotedString(message).getquoted()))
                    except:
                        sqlInsert = u"""INSERT INTO omsclient (date_, time_, category, message, logfile) VALUES (to_date('{0}', 'YYYY-MM-DD'), to_timestamp('{1}', 'HH24:MI:SS,MS'), '{2}', {3}, {4});\n""".format(last_values['date_'], last_values['time_'], 'issue', psy.extensions.QuotedString(line.replace('\n', '')).getquoted(), psy.extensions.QuotedString(f).getquoted())
                        cursor.execute(sqlInsert)
                        cursor.execute('COMMIT;')
                else:
                    sqlInsert = u"""INSERT INTO omsclient (date_, time_, category, message, logfile) VALUES (to_date('{0}', 'YYYY-MM-DD'), to_timestamp('{1}', 'HH24:MI:SS,MS'), '{2}', {3}, {4});\n""".format(last_values['date_'], last_values['time_'], 'additional_lines', psy.extensions.QuotedString(line.replace('\n', '')).getquoted(), psy.extensions.QuotedString(f).getquoted())
                    cursor.execute(sqlInsert)
                    cursor.execute('COMMIT;')
            
        fo.close()
        del cursor
        return "completed file " + f
        
def importSaveDataLogs(f=None):
    try:
        import psycopg2 as psy
        import datetime as dt
    except:
        print("Failed to import python-postgresql drivers.")
        exit()

    if f is None:
        return "No Filename Supplied"
    else:
        import re
        conn_string = "host='localhost' dbname='oms_logging' user='postgres' password='usouth'"
        conn = psy.connect(conn_string)
        cursor = conn.cursor()
        
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
                        message = line[26:]
                    else:
                        category = line[26:line.find(": ",26)]
                        message = line[line.find(": ",26):].replace('\n', '')
                    try:
                        sqlInsert = u"""INSERT INTO save_data (date_, time_, category, message, logfile) VALUES (to_date('{0}', 'YYYY-MM-DD'), to_timestamp('{1}', 'HH24:MI:SS,MS'), '{2}', {3}, {4});""".format(date_, time_, category, psy.extensions.QuotedString(message.replace('\n', '')).getquoted(), psy.extensions.QuotedString(f).getquoted())
                        cursor.execute(sqlInsert)
                        cursor.execute('COMMIT;')
                        #cursor.execute("""INSERT INTO omsclient (date_, time_, time_ms, category, message) VALUES (to_date('{0}', 'YYYY-MM-DD'), to_timestamp('{1}', 'HH24:MI:SS'), {2}, '{3}', {4});\n""".format(date_, time_, time_ms, category, psycopg2.extensions.QuotedString(message).getquoted()))
                    except:
                        #print("Error Importing near line : " + str(lineNumber) + " - " + line.replace('\n', ''))
                        sqlInsert = u"""INSERT INTO save_data (date_, time_, category, message, logfile) VALUES (to_date('{0}', 'YYYY-MM-DD'), to_timestamp('{1}', 'HH24:MI:SS,MS'), '{2}', {3}, {4});""".format(last_values['date_'], last_values['time_'], 'issue', psy.extensions.QuotedString(line.replace('\n', '')).getquoted(), psy.extensions.QuotedString(f).getquoted())
                        cursor.execute(sqlInsert)
                        cursor.execute('COMMIT;')
                else:
                    sqlInsert = u"""INSERT INTO save_data (date_, time_, category, message, logfile) VALUES (to_date('{0}', 'YYYY-MM-DD'), to_timestamp('{1}', 'HH24:MI:SS,MS'), '{2}', {3}, {4});""".format(last_values['date_'], last_values['time_'], 'additional_lines', psy.extensions.QuotedString(line.replace('\n', '')).getquoted(), psy.extensions.QuotedString(f).getquoted())
                    cursor.execute(sqlInsert)
                    cursor.execute('COMMIT;')
                    
        fo.close()
        del cursor
        return "completed file " + f

def importLogfiles(db=None, schema='oms_logfiles', f=None):
    """ 
    Parse supplied logfile (f) and insert into provided database (db)
    @var db: the database to insert the logfile contents
    @var f: the file name including the full path to the log file.
    """
    try:
        import psycopg2 as psy
        import datetime as dt
    except:
        print("Failed to import python-postgresql drivers.")
        exit()

    errors = tuple()
    if db is None:
        errors += ("database not supplied",)
    if f is None:
        errors += ("No Filename Supplied",)
    #test if any errors exist. if any exit function and return errors
    if len(errors) > 0:
        return errors
    else:
        import re
        conn_string = "host='localhost' dbname='" + db + "' user='postgres' password='usouth'"
        conn = psy.connect(conn_string)
        cursor = conn.cursor()
        
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
                        message = line[26:]
                    else:
                        category = line[26:line.find(": ",26)]
                        message = line[line.find(": ",26):].replace('\n', '')
                    try:
                        sqlInsert = u"""INSERT INTO {0}.obj_model (date_, time_, category, message, logfile) VALUES (to_date('{1}', 'YYYY-MM-DD'), to_timestamp('{2}', 'HH24:MI:SS,MS'), '{3}', {4}, {5});\n""".format(schema, date_, time_, category, psy.extensions.QuotedString(message.replace('\n', '')).getquoted(), psy.extensions.QuotedString(f).getquoted())
                        cursor.execute(sqlInsert)
                        cursor.execute('COMMIT;')
                        #cursor.execute("""INSERT INTO omsclient (date_, time_, time_ms, category, message) VALUES (to_date('{0}', 'YYYY-MM-DD'), to_timestamp('{1}', 'HH24:MI:SS'), {2}, '{3}', {4});\n""".format(date_, time_, time_ms, category, psycopg2.extensions.QuotedString(message).getquoted()))
                    except:
                        sqlInsert = u"""INSERT INTO {0}.obj_model (date_, time_, category, message, logfile) VALUES (to_date('{1}', 'YYYY-MM-DD'), to_timestamp('{2}', 'HH24:MI:SS,MS'), '{3}', {4}, {5});\n""".format(schema, last_values['date_'], last_values['time_'], 'issue', psy.extensions.QuotedString(line.replace('\n', '')).getquoted(), psy.extensions.QuotedString(f).getquoted())
                        cursor.execute(sqlInsert)
                        cursor.execute('COMMIT;')
                else:
                    sqlInsert = u"""INSERT INTO {0}.obj_model (date_, time_, category, message, logfile) VALUES (to_date('{1}', 'YYYY-MM-DD'), to_timestamp('{2}', 'HH24:MI:SS,MS'), '{3}', {4}, {5});\n""".format(schema, last_values['date_'], last_values['time_'], 'additional_lines', psy.extensions.QuotedString(line.replace('\n', '')).getquoted(), psy.extensions.QuotedString(f).getquoted())
                    cursor.execute(sqlInsert)
                    cursor.execute('COMMIT;')
            
        #@todo:  implement a way to mark the files as being imported so next process can ignore or skip them
        fo.close()
        del cursor
        return "completed file " + f

def importLogs(logfile=None):
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
        print("File provided could not be found. Exiting...")
        exit()
    
    #Adding wildcard to path for glob.iglob to find all files with matching basename    
    logfile += "*"
    
    try:
        #create a list of logfiles with base name file provided
        logfiles = [log for log in glob.iglob(logfile)]
        
    except:
        print("Failed to execute finding all files with logfile basename")
        exit()
        
    #begin processing files
    print("Beginning Import")
    for f in logfiles: 
        try:
            objmodel_starttime = dt.datetime.now()
            print(importLogfiles('omsprod', 'oms_logfiles', f))
            objectmodel_run_time = dt.datetime.now()
            print("    Imported in " + str(objectmodel_run_time-objmodel_starttime))
        except:
            print("Couldn't import " + f)

def importOMSClient():
    import glob
    import datetime as dt
    
    print("Beginning OMSClient Import")
    for f in glob.iglob("C:\\omsprint\\Logs\\OMSClient\\omsclient.log*"):
        try:
            omsclient_starttime = dt.datetime.now()
            print(importOMSClientLogs(f))
            client_run_time = dt.datetime.now()
            print("Script Completed OMSClient Import of Logs in "  + str(client_run_time-omsclient_starttime))
        except:
            print("Couldn't import " + f)

def importSaveData():
    import glob
    import datetime as dt
    
    print("Beginning Savedata Import")
    for f in glob.iglob("C:\\Program Files (x86)\\Futura Systems\\Futura OMS\\Bin\\SaveData\\Logs\\savedata.log*"):
        try:
            savedata_starttime = dt.datetime.now()
            print(importSaveDataLogs(f))
            savedata_run_time = dt.datetime.now()
            print("    Script Completed SaveData Import of Logs in " + str(savedata_run_time-savedata_starttime))
        except:
            print("Couldn't import "+ f)


if __name__ == "__main__":
    import datetime as dt
    starttime = dt.datetime.now()
    print("Started Existing Log Backup Process: " + str(starttime))
    backup = backupOMSLogging('oms_logging')
    #print(backup)
    if backup == 1:
        print("Starting Import process: " + str(dt.datetime.now()))
        importLogs("C:\\omsprint\\Logs\\ObjectModel\\objectmodel.log")
        importLogs("C:\\omsprint\\Logs\\OMSClient\\omsclient.log")
        importLogs("C:\\Program Files (x86)\\Futura Systems\\Futura OMS\\Bin\\SaveData\\Logs\\savedata.log")
        
        endtime = dt.datetime.now()
    else:
        print("OMS Console Data Backup failed!")
        endtime = dt.datetime.now()
    
    print("Total script time: " + str(endtime-starttime))
