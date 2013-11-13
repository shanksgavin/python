import psycopg2
import psycopg2.extras
import datetime

def createLoggingSchema():
    try:
        import psycopg2
        import psycopg2.extras
        import datetime
    except:
        print("Failed to import python-postgresql drivers.")
        exit()
        
    try:
        conn_string = "host='localhost' dbname='oms_logging' user='postgres' password='usouth'"
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        curtime = datetime.datetime.now()
        
    except:
        print("Failed to create connection to database.")
        exit()

def backupOMSLogging():
    try:
        conn_string = "host='localhost' dbname='oms_logging' user='postgres' password='usouth'"
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        curtime = datetime.datetime.now()
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
    if f is None:
        return "No Filename Supplied"
    else:
        conn_string = "host='localhost' dbname='oms_logging' user='postgres' password='usouth'"
        #print("Connecting to database\n ->%s" % (conn_string))
        
        conn = psycopg2.connect(conn_string)
        
        cursor = conn.cursor()
        
        #import os
        fo = open(f, "r")
        #fw = open(f + ".sql", "w+")
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
                    sqlInsert = """INSERT INTO omsclient (date_, time_, category, message, logfile) VALUES (to_date('{0}', 'YYYY-MM-DD'), to_timestamp('{1}', 'HH24:MI:SS,MS'), '{2}', {3}, {4});\n""".format(date_, time_, category, psycopg2.extensions.QuotedString(message).getquoted(), psycopg2.extensions.QuotedString(f).getquoted())
                    #fw.write(sqlInsert)
                    #print(sqlInsert) 
                    cursor.execute(sqlInsert)
                    cursor.execute('COMMIT;')
                    #cursor.execute("""INSERT INTO omsclient (date_, time_, time_ms, category, message) VALUES (to_date('{0}', 'YYYY-MM-DD'), to_timestamp('{1}', 'HH24:MI:SS'), {2}, '{3}', {4});\n""".format(date_, time_, time_ms, category, psycopg2.extensions.QuotedString(message).getquoted()))
                except:
                    sqlInsert = """INSERT INTO omsclient (date_, time_, category, message, logfile) VALUES (to_date('{0}', 'YYYY-MM-DD'), to_timestamp('{1}', 'HH24:MI:SS,MS'), '{2}', {3}, {4});\n""".format(last_values['date_'], last_values['time_'], 'issue', psycopg2.extensions.QuotedString(line).getquoted(), psycopg2.extensions.QuotedString(f).getquoted())
                    #fw.write(sqlInsert)
                    cursor.execute(sqlInsert)
                    cursor.execute('COMMIT;')
            
        fo.close()
        #fw.close()
        return "completed file " + f

def importObjectModelLogs(f=None):
    if f is None:
        return "No Filename Supplied"
    else:
        conn_string = "host='localhost' dbname='oms_logging' user='postgres' password='usouth'"
        #print("Connecting to database\n ->%s" % (conn_string))
        
        conn = psycopg2.connect(conn_string)
        
        cursor = conn.cursor()
        
        #import os
        fo = open(f, "r")
        #fw = open(f + ".sql", "w+")
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
                    message = line[line.find(":",26)+2:-1].replace('\n', '')
                    sqlInsert = u"""INSERT INTO obj_model (date_, time_, category, message, logfile) VALUES (to_date('{0}', 'YYYY-MM-DD'), to_timestamp('{1}', 'HH24:MI:SS,MS'), '{2}', {3}, {4});\n""".format(date_, time_, category, psycopg2.extensions.QuotedString(message).getquoted(), psycopg2.extensions.QuotedString(f).getquoted())
                    #fw.write(sqlInsert)
                    #print(sqlInsert) 
                    cursor.execute(sqlInsert)
                    cursor.execute('COMMIT;')
                    #cursor.execute("""INSERT INTO omsclient (date_, time_, time_ms, category, message) VALUES (to_date('{0}', 'YYYY-MM-DD'), to_timestamp('{1}', 'HH24:MI:SS'), {2}, '{3}', {4});\n""".format(date_, time_, time_ms, category, psycopg2.extensions.QuotedString(message).getquoted()))
                except:
                    sqlInsert = u"""INSERT INTO obj_model (date_, time_, category, message, logfile) VALUES (to_date('{0}', 'YYYY-MM-DD'), to_timestamp('{1}', 'HH24:MI:SS,MS'), '{2}', {3}, {4});\n""".format(last_values['date_'], last_values['time_'], 'issue', psycopg2.extensions.QuotedString(line).getquoted(), psycopg2.extensions.QuotedString(f).getquoted())
                    #fw.write(sqlInsert)
                    cursor.execute(sqlInsert)
                    cursor.execute('COMMIT;')
            
        fo.close()
        #fw.close()
        return "completed file " + f

def importOMSClientLogs(f=None):
    if f is None:
        return "No Filename Supplied"
    else:
        conn_string = "host='localhost' dbname='oms_logging' user='postgres' password='usouth'"
        #print("Connecting to database\n ->%s" % (conn_string))
        
        conn = psycopg2.connect(conn_string)
        
        cursor = conn.cursor()
        
        #import os
        fo = open(f, "r")
        #fw = open(f + ".sql", "w+")
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
                    message = line[line.find(":",26)+2:-1].replace('\n', '')
                    sqlInsert = u"""INSERT INTO omsclient (date_, time_, category, message, logfile) VALUES (to_date('{0}', 'YYYY-MM-DD'), to_timestamp('{1}', 'HH24:MI:SS,MS'), '{2}', {3}, {4});\n""".format(date_, time_, category, psycopg2.extensions.QuotedString(message).getquoted(), psycopg2.extensions.QuotedString(f).getquoted())
                    #fw.write(sqlInsert)
                    #print(sqlInsert) 
                    cursor.execute(sqlInsert)
                    cursor.execute('COMMIT;')
                    #cursor.execute("""INSERT INTO omsclient (date_, time_, time_ms, category, message) VALUES (to_date('{0}', 'YYYY-MM-DD'), to_timestamp('{1}', 'HH24:MI:SS'), {2}, '{3}', {4});\n""".format(date_, time_, time_ms, category, psycopg2.extensions.QuotedString(message).getquoted()))
                except:
                    sqlInsert = u"""INSERT INTO omsclient (date_, time_, category, message, logfile) VALUES (to_date('{0}', 'YYYY-MM-DD'), to_timestamp('{1}', 'HH24:MI:SS,MS'), '{2}', {3}, {4});\n""".format(last_values['date_'], last_values['time_'], 'issue', psycopg2.extensions.QuotedString(line).getquoted(), psycopg2.extensions.QuotedString(f).getquoted())
                    #fw.write(sqlInsert)
                    cursor.execute(sqlInsert)
                    cursor.execute('COMMIT;')
            
        fo.close()
        del cursor
        #fw.close()
        return "completed file " + f
        
def importSaveDataLogs(f=None):
    if f is None:
        return "No Filename Supplied"
    else:
        conn_string = "host='localhost' dbname='oms_logging' user='postgres' password='usouth'"
        #print("Connecting to database\n ->%s" % (conn_string))
        
        conn = psycopg2.connect(conn_string)
        
        cursor = conn.cursor()
        
        #import os
        fo = open(f, "r")
        #fw = open(f + ".sql", "w+")
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
                    message = line[line.find(":",26)+2:-1].replace('\n', '')
                    sqlInsert = u"""INSERT INTO save_data (date_, time_, category, message, logfile) VALUES (to_date('{0}', 'YYYY-MM-DD'), to_timestamp('{1}', 'HH24:MI:SS,MS'), '{2}', {3}, {4});\n""".format(date_, time_, category, psycopg2.extensions.QuotedString(message).getquoted(), psycopg2.extensions.QuotedString(f).getquoted())
                    #fw.write(sqlInsert)
                    #print(sqlInsert) 
                    cursor.execute(sqlInsert)
                    cursor.execute('COMMIT;')
                    #cursor.execute("""INSERT INTO omsclient (date_, time_, time_ms, category, message) VALUES (to_date('{0}', 'YYYY-MM-DD'), to_timestamp('{1}', 'HH24:MI:SS'), {2}, '{3}', {4});\n""".format(date_, time_, time_ms, category, psycopg2.extensions.QuotedString(message).getquoted()))
                except:
                    sqlInsert = u"""INSERT INTO save_data (date_, time_, category, message, logfile) VALUES (to_date('{0}', 'YYYY-MM-DD'), to_timestamp('{1}', 'HH24:MI:SS,MS'), '{2}', {3}, {4});\n""".format(last_values['date_'], last_values['time_'], 'issue', psycopg2.extensions.QuotedString(line).getquoted(), psycopg2.extensions.QuotedString(f).getquoted())
                    #fw.write(sqlInsert)
                    cursor.execute(sqlInsert)
                    cursor.execute('COMMIT;')
            
        fo.close()
        #fw.close()
        return "completed file " + f


def importObjectModel():
    import glob
    import datetime as dt
    objmodel_starttime = dt.datetime.now()
    try:
        for f in glob.iglob("C:\\omsprint\\Logs\\ObjectModel\\objectmodel.log*"):
            print(importObjectModelLogs(f))
        objectmodel_run_time = dt.datetime.now()
        print("Script Completed ObjectModel Import of Logs in " + str(objectmodel_run_time-objmodel_starttime))
    except:
        print("Couldn't import " + f)

def importOMSClient(p=''):
    if p == '':
        return "No Path Was provided. Nothing to Import. Exiting Process..."
    else:
        import glob
        import datetime as dt
        omsclient_starttime = dt.datetime.now()
        print("OMSClient Import Process Started: " + str(omsclient_starttime))
        try:
            for f in glob.iglob(p + "\\omsclient.log*"):
                print(importOMSClientLogs(f))
            client_run_time = dt.datetime.now()
            print("OMSClient Import Process Completed: "  + str(omsclient_starttime))
            print("    Total Process Time: " + str(client_run_time-omsclient_starttime))
        except:
            print("Couldn't import " + f)

def importSaveData(p=''):
    if p == '':
        return "No Path Was provided. Nothing to Import. Exiting Process..."
    else:
        import glob
        import datetime as dt
        savedata_starttime = dt.datetime.now()
        print("SaveData Import Process Started: " + str(savedata_starttime))
        try:
            for f in glob.iglob(p + "\\savedata.log*"):
                print(importSaveDataLogs(f))
            savedata_run_time = dt.datetime.now()
            print("SaveData Import Process Completed: " + str(savedata_run_time))
            print("    Total Process Time: " + str(savedata_run_time-savedata_starttime))
        except:
            print("Couldn't import "+ f)


if __name__ == "__main__":
    import datetime as dt
    import arcpy
    starttime = dt.datetime.now()
    
    # Get Path Locations for Log files
    objmodelPATH = arcpy.GetParameterAsText(0)
    omsclientPATH = arcpy.GetParameterAsText(1)
    savedataPATH = arcpy.GetParameterAsText(2)
     
    print("Started Existing Log Backup Process: " + str(starttime))
    backup = backupOMSLogging()
    #print(backup)
    if backup == 1:
        print("Starting Import process: " + str(dt.datetime.now()))
        importObjectModel()
        importOMSClient()
        importSaveData()
        
        endtime = dt.datetime.now()
    else:
        print("OMS Console Data Backup failed!")
        endtime = dt.datetime.now()
    
    print("Total script time: " + str(endtime-starttime))
