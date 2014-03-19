'''
Title: Set all active OMS calls to closed
Created: March 17, 2014
Modified: March 17, 2014

@author: williamg

@version: 0.1
'''

#import sys

def createResetOMS(host=None, db=None, schema=None, u=None, p=None):
    """
    Create a pgSQL Function to set all active calls in OMS to closed
    """
    errors = tuple()
    if host is None:
        errors += ("host not supplied",)
    if db is None:
        errors += ("database not supplied",)
    if schema is None:
        errors += ("schema not supplied",)
    if u is None:
        errors += ("username not supplied",)
    if p is None:
        errors += ("password not supplied",)
        
    #test if any errors exist. if any exit function and return errors
    if len(errors) > 0:
        return errors
    else:
        #import required postgresql modules
        try:
            import psycopg2 as psy
        except:
            errors += ("Failed to import python-postgresql drivers.",)
            return errors
        #import datetime module
        try:
            import datetime as dt
        except:
            errors += ("Failed to import datetime module.",)
            return errors
        #build connection string & make connection cursor to db
        try:
            conn_string = "host='" + host + "' dbname='" + db + "' user='" + u + "' password='" + p + "'"
            conn = psy.connect(conn_string)
            cursor = conn.cursor()
            curtime = dt.datetime.now()
            errors += (curtime,)
            
        except:
            errors += ("Failed to create connection to database.",)
            return errors
        #build sql statement to create function
        sql = """        CREATE OR REPLACE FUNCTION resetOMSforTesting() RETURNS void AS
        $$
        BEGIN
            UPDATE calls
            SET deleted = True
            WHERE callstatus = 'ACTIVE';
            
            UPDATE calls
            SET callstatus = 'CLOSED'
            WHERE callstatus = 'ACTIVE';
        END;
        $$
        LANGUAGE 'plpgsql';
        """
        #execute sql to build function
        try:
            cursor.execute(sql)
            del cursor
        except:
            errors += ("Failed to create resetOMSforTesting().",)
            return errors
    #End script successfully
    errors += ("Script Completed without Error.",)
    return errors

if __name__ == '__main__':
    #Set Variables
    host = 'localhost'
    db = 'coweta-fayette' #north_ga_logs #wiregrass_2_2_0_84 #oms_inland_power
    schema = 'public'
    u = 'postgres'
    p = 'usouth'
    logfile_schema = 'oms_logfiles'
    archive_schema = 'oms_archives'
    
    #Run Function
    result = createResetOMS(host, db, schema, u, p)
    for msg in result:
        print(msg)