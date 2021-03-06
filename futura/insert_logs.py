'''
Title: Insert OMS Logs into oms_logging db
Created: May 7, 2013
Modified: May 15, 2013

@author: williamg

@todo: Validate time_ for each line being formatted into SQL; see notes in code
@todo: Add check for file locks in case Integration Service is running during log import
@todo: General Cleanup
@todo: Review entire process for conciseness and bugs
@todo: Make process object oriented 
'''

import sys

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
            import datetime as dt
        except:
            print("Failed to import datetime module.")
            sys.exit()
            
        try:
            conn_string = "host='{0}' dbanme='{1}' user='{2}' password='{3}'".format(d_logs['host'],d_logs['db'],d_logs['u'],d_logs['p'])
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
        try:
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
                        
                        # Need to validate time before moving forward
                        # The logging Config file can display time incorrectly as text
                        # e.g. HH:mm:ss.SSS -> 14:25:36.SSS
                        # Format should be ss.fff in web.config
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
                            sqlInsert = u"""INSERT INTO {0}.omslogs (date_, time_, category, message, logfile) VALUES (to_date('{1}', 'YYYY-MM-DD'), to_timestamp('{2}', 'HH24:MI:SS,MS'), '{3}', {4}, {5});\n""".format(schema, date_, time_, category, psy.extensions.QuotedString(message.replace('\n', '').strip()).getquoted(), psy.extensions.QuotedString(f).getquoted())
                            cursor.execute(sqlInsert)
                            #conn.commit()
                            #cursor.execute("""INSERT INTO omsclient (date_, time_, time_ms, category, message) VALUES (to_date('{0}', 'YYYY-MM-DD'), to_timestamp('{1}', 'HH24:MI:SS'), {2}, '{3}', {4});\n""".format(date_, time_, time_ms, category, psycopg2.extensions.QuotedString(message).getquoted()))
                        except:
                            sqlInsert = u"""INSERT INTO {0}.omslogs (date_, time_, category, message, logfile) VALUES (to_date('{1}', 'YYYY-MM-DD'), to_timestamp('{2}', 'HH24:MI:SS,MS'), '{3}', {4}, {5});\n""".format(schema, last_values['date_'], last_values['time_'], 'insert_issue', psy.extensions.QuotedString(line.replace('\n', '').strip()).getquoted(), psy.extensions.QuotedString(f).getquoted())
                            cursor.execute(sqlInsert)
                            #conn.commit()
                    else:
                        sqlInsert = u"""INSERT INTO {0}.omslogs (date_, time_, category, message, logfile) VALUES (to_date('{1}', 'YYYY-MM-DD'), to_timestamp('{2}', 'HH24:MI:SS,MS'), '{3}', {4}, {5});\n""".format(schema, last_values['date_'], last_values['time_'], 'additional_lines', psy.extensions.QuotedString(line.replace('\n', '').strip()).getquoted(), psy.extensions.QuotedString(f).getquoted())
                        cursor.execute(sqlInsert)
                        #conn.commit()
                if lineNumber % 5000 == 0:
                    conn.commit()
                    #print(str(lineNumber) + " successfully committed")
                
            fo.close()
            del cursor
            
            # Log File Management (Move & Rename)
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
            except Exception as e:
                print("    Could not rename log file: " + f)
                print(e)
                
            return "    Completed file " + f
        
        except Exception as e:
            return e, lineNumber

def importLogs(host=None, db=None, u=None, p=None, logfile=None, logfile_schema=None, rename=True):
    if logfile is None:
        print("No file was provided. Exiting...")
        exit()
        
    #import needed modules
    import glob
    import datetime as dt
    
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
                print("    Couldn't import {0} at line {1} with error {2}".format(f, result[1], result[0]))
                print(e)
    else:
        print("No new logs to be inserted! ({0})".format(logfile))

def run(d_logs):
    """
    loop over available log paths
    See dictionaries below
    """
    for log in d_logs['oms_log_path']:
        importLogs(d_logs['host'], d_logs['db'], d_logs['u'], d_logs['p'], d_logs['oms_log_path'][log], d_logs['logfile_schema'], d_logs['renameFile'])
    
if __name__ == "__main__":
    #
    # Update the parameters & log file path before running the utility
    #
    d_logs_local = {
        'host'          : 'localhost',
        'db'            : 'wiregrass_121',
        'u'             : 'postgres',
        'p'             : 'usouth',
        'logfile_schema': 'oms_logfiles',
        'archive_schema': 'oms_archives',
        'renameFile'    : True,
        'archive'       : False,
        'oms_log_path'  : {'objectmodel': r'C:\map_files\Logs\ObjectModel\objectmodel.log',
                           'omsclient': r'C:\map_files\Logs\OMSClient\omsclient.log',
                           'savedata': r'C:\map_files\Logs\SaveData\savedata.log',
                           'integrationservice': r'C:\map_files\Logs\IntegrationService\FuturaOMS_IntegrationServiceLog.txt',
                           'integrationservicecontrol': r'C:\map_files\Logs\IntegrationService\FuturaOMS_Integration_Service_Control_LOG.txt',
                           'ami': r'C:\map_files\Logs\AMI\OMS_AMI_WebserviceLog.txt',
                           'ami_test': r'C:\map_files\Logs\AMI\AMI_OMS_TEST_WebService_Log.txt',
                           'avl': r'C:\map_files\Logs\AVL\FuturaOMS_AVL.txt',
                           'crc': r'C:\map_files\Logs\CRC\FuturaOMS_CRC.txt',
                           'ivr': r'C:\map_files\Logs\IVR\OMS_IVR_Webservice.txt',
                           'ivrcallback': r'C:\map_files\Logs\IVR\IVR_OMS_Callback_Webservice.txt',
                           'scada': r'C:\map_files\Logs\SCADA\OMS_SCADA_WebserviceLog.txt',
                           'upn': r'C:\map_files\Logs\UPN\FuturaOMS_UPN.txt'}
                    }
    
    d_logs_omsprod = {
        'host'          : 'omsprod',
        'db'            : 'inland_20130926',
        'u'             : 'postgres',
        'p'             : 'usouth',
        'logfile_schema': 'oms_logfiles',
        'archive_schema': 'oms_archives',
        'renameFile'    : True,
        'archive'       : True,
        'oms_log_path'  : {
                         'objectmodel': r'C:\oms_logs\omsprod\ObjectModel\objectmodel.log',
                         'omsclient': r'C:\oms_logs\omsprod\OMSClient\omsclient.log',
                         'savedata': r'C:\oms_logs\omsprod\SaveData\savedata.log',
                         'integrationservice': r'C:\oms_logs\omsprod\IntegrationService\FuturaOMS_IntegrationServiceLog',
                         'integrationservicecontrol': r'C:\oms_logs\omsprod\IntegrationService\FuturaOMS_Integration_Service_Control_LOG.txt',
                         'ivrcallback':r'C:\oms_logs\omsprod\IVR\OMS_IVR_Callback_Webservice.txt',
                         'ivr':r'C:\oms_logs\omsprod\IVR\OMS_IVR_Webservice.txt',
                         'upn': r'C:\oms_logs\omsprod\UPN\FuturaOMS_UPN.txt'
                        }
                    }
    
    d_logs_central_ec = {
        'host'           : 'localhost',
        'db'            : 'central_ec',
        'u'             : 'postgres',
        'p'             : 'usouth',
        'logfile_schema': 'oms_logfiles',
        'archive_schema': 'oms_archives',
        'renameFile'    : True,
        'archive'       : False,
        'oms_log_path'  : {'crc': r'C:\oms_logs\CentralEC_OR\CRC Logs 5-1-5-2014\FuturaOMS_CRC.txt'},
        'oms_log_path_default'  : {'objectmodel': r'C:\map_files\Logs\ObjectModel\objectmodel.log',
                           'omsclient': r'C:\map_files\Logs\OMSClient\omsclient.log',
                           'savedata': r'C:\map_files\Logs\SaveData\savedata.log',
                           'integrationservice': r'C:\map_files\Logs\IntegrationService\FuturaOMS_IntegrationServiceLog.txt',
                           'integrationservicecontrol': r'C:\map_files\Logs\IntegrationService\FuturaOMS_Integration_Service_Control_LOG.txt',
                           'ami': r'C:\map_files\Logs\AMI\OMS_AMI_WebserviceLog.txt',
                           'ami_test': r'C:\map_files\Logs\AMI\AMI_OMS_TEST_WebService_Log.txt',
                           'avl': r'C:\map_files\Logs\AVL\FuturaOMS_AVL.txt',
                           'crc': r'C:\map_files\Logs\CRC\FuturaOMS_CRC.txt',
                           'ivr': r'C:\map_files\Logs\IVR\OMS_IVR_Webservice.txt',
                           'ivrcallback': r'C:\map_files\Logs\IVR\IVR_OMS_Callback_Webservice.txt',
                           'scada': r'C:\map_files\Logs\SCADA\OMS_SCADA_WebserviceLog.txt',
                           'upn': r'C:\map_files\Logs\UPN\FuturaOMS_UPN.txt'}
                    }
    
    d_logs_homer = {
        'host'          : 'localhost',
        'db'            : 'oms_homer',
        'u'             : 'postgres',
        'p'             : 'usouth',
        'logfile_schema': 'oms_logfiles',
        'archive_schema': 'oms_archives',
        'renameFile'    : True,
        'archive'       : False,
        'oms_log_path'  : {'objectmodel': r'C:\oms_logs\homer\ObjectModel\objectmodel.log',
                           'omsclient': r'C:\oms_logs\homer\OMSClient\omsclient.log',
                           'savedata': r'C:\oms_logs\homer\SaveData\savedata.log',
                           'integrationservice': r'C:\oms_logs\homer\IntegrationService\FuturaOMS_IntegrationServiceLog',
                           'integrationservice2': r'C:\oms_logs\homer\IntegrationService\FuturaOMS_IntegratoinServiceLog',
                           'integrationservicecontrol': r'C:\oms_logs\homer\IntegrationService\FuturaOMS_Integration_Service_Control_LOG.txt',
                           'integrationserviceIVRSocket': r'C:\oms_logs\homer\IntegrationService\OMS_IVR_SocketLog',
                           'ami': r'C:\oms_logs\homer\AMI\OMS_AMI_WebserviceLog.txt',
                           'ivr': r'C:\oms_logs\homer\IVR\OMS_IVR_Webservice.txt',
                           'upn': r'C:\oms_logs\homer\UPN\FuturaOMS_UPN.txt'}
                    }
    
    """
    # assign the active path dictionary before running
    """
    d_logs = d_logs_homer
    
    
    ### Should be no need to modify anything below this line ###
    import datetime as dt
    starttime = dt.datetime.now()
    
    if d_logs['archive'] == True:
        print("Started Existing Log Backup Process: " + str(starttime))
        backup = backupOMSLogs(d_logs['host'], d_logs['db'], d_logs['u'], d_logs['p'], d_logs['logfile_schema'], d_logs['archive_schema'])
        #print(backup)
    else:
        backup = 1

    if d_logs['archive'] and backup == 1:
        print("Starting Import process: " + str(dt.datetime.now()))
        
        run(d_logs)
        
        endtime = dt.datetime.now()
    elif d_logs['archive'] and backup != 1:
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
