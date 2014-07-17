'''
Title: Enable/Disable Audit Trigger Functions on Public Schema
Created: April 9, 2013
Modified: April 9, 2013

@author: williamg

@version: 0.1
'''

def triggersUpdate(host=None, db=None, u=None, p=None, schema=None, action=None):
    """ 
    Update Table Definition to Enable/Disable associated trigger function
    which inserts data changes into the audit schema
    variables:
    @var host: host machine name running the database
    @var db: database to process
    @var u: username to login
    @var p: password
    @var schema: Schema used to search for audited tables
    @var action: 'DISABLE' or 'ENABLE' to be used in the sql statement 
    """
        
    try:
        import psycopg2 as psy
        #import datetime as dt
    except:
        print("Failed to import python-postgresql drivers.")
        exit()

    errors = tuple()
    if host is None:
        errors += ("host not supplied",)
    if db is None:
        errors += ("database not supplied",)
    if u is None:
        errors += ("username not supplied",)
    if p is None:
        errors += ("password not supplied",)
    if schema is None:
        errors += ("schema not supplied",)
    if action is None:
        errors += ("action not supplied",)
    #test if any errors exist. if any exit function and return errors
    if len(errors) > 0:
        return errors
    else:
        conn_string = "host='{0}' dbname='{1}' user='{2}' password='{3}'".format(host, db, u, p)
        conn = psy.connect(conn_string)
        cursor = conn.cursor()
        
        sql_omsTables = """SELECT c.relname 
        FROM pg_catalog.pg_class c 
        LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace 
        WHERE n.nspname='""" + schema + """' 
        AND c.relkind IN ('r','') 
        AND n.nspname NOT IN ('pg_catalog', 'pg_toast', 'information_schema') 
        ORDER BY c.relname ASC"""
        
        cursor.execute(sql_omsTables)
        availableTables = [tbl[0] for tbl in cursor]
        
        counter = 0
        
        for tbl in availableTables:
            counter += 1
            try:
                cursor.execute("ALTER TABLE {0}.{1} {2} TRIGGER audit_{3}_trg".format(schema, tbl, action, tbl))
                print("{0:>3}. Trigger audit_{1}_trg: {2}".format(str(counter), tbl, action))
                conn.commit()
            except Exception as e:
                print(e)
                conn.rollback()
        
        del cursor

def triggerDelete(host=None, db=None, u=None, p=None, schema=None, trigger_list=[]):
    """ 
    Update Table Definition to Enable/Disable associated trigger function
    which inserts data changes into the audit schema
    variables:
    @var host: host machine name running the database
    @var db: database to process
    @var u: username to login
    @var p: password
    @var schema: Schema used to search for audited tables
    @var trigger_list: List of tables to delete triggers
        Note: Empty list will try to delete triggers for all available tables
    """
        
    try:
        import psycopg2 as psy
        #import datetime as dt
    except:
        print("Failed to import python-postgresql drivers.")
        exit()

    errors = tuple()
    if host is None:
        errors += ("host not supplied",)
    if db is None:
        errors += ("database not supplied",)
    if u is None:
        errors += ("username not supplied",)
    if p is None:
        errors += ("password not supplied",)
    if schema is None:
        errors += ("schema not supplied",)
    #test if any errors exist. if any exit function and return errors
    if len(errors) > 0:
        return errors
    else:
        conn_string = "host='{0}' dbname='{1}' user='{2}' password='{3}'".format(host, db, u, p)
        conn = psy.connect(conn_string)
        cursor = conn.cursor()
        
        sql_omsTables = """SELECT c.relname 
        FROM pg_catalog.pg_class c 
        LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace 
        WHERE n.nspname='""" + schema + """' 
        AND c.relkind IN ('r','') 
        AND n.nspname NOT IN ('pg_catalog', 'pg_toast', 'information_schema') 
        ORDER BY c.relname ASC"""
        
        #Get all available tables in database
        cursor.execute(sql_omsTables)
        availableTables = [tbl[0] for tbl in cursor]
        
        #determine if all tables or just a selection of table will be audited
        #TODO error trap empty string in other list positions other than index[0]
        process_tables = []
        if len(trigger_list) > 0:
            for aTbl in trigger_list:
                #print(availableTables.index(aTbl))
                if aTbl not in availableTables:
                    print('Trigger "audit_{0}_trg" does not exist in database {1}'.format(aTbl, db))
                else:
                    process_tables.append(aTbl)
        else:
            process_tables = availableTables

        counter = 0
        
        for tbl in process_tables:
            counter += 1
            try:
                cursor.execute("DROP TRIGGER IF EXISTS audit_{0}_trg ON {1}.{2}".format(tbl, schema, tbl))
                print("{0:>3}. Trigger audit_{1}_trg: DELETED".format(str(counter), tbl))
                conn.commit()
            except Exception as e:
                print(e)
                conn.rollback()
        
        del cursor
        
def functionDelete(host=None, db=None, u=None, p=None, schema=None, function_list=[]):
    """ 
    Update Table Definition to Enable/Disable associated trigger function
    which inserts data changes into the audit schema
    variables:
    @var host: host machine name running the database
    @var db: database to process
    @var u: username to login
    @var p: password
    @var schema: Schema used to search for audited tables
    @var function_list: List of tables to delete functions
        Note: Empty list will try to delete functions for all available tables
    """
        
    try:
        import psycopg2 as psy
        #import datetime as dt
    except:
        print("Failed to import python-postgresql drivers.")
        return False

    errors = tuple()
    if host is None:
        errors += ("host not supplied",)
    if db is None:
        errors += ("database not supplied",)
    if u is None:
        errors += ("username not supplied",)
    if p is None:
        errors += ("password not supplied",)
    if schema is None:
        errors += ("schema not supplied",)
    #test if any errors exist. if any exit function and return errors
    if len(errors) > 0:
        return errors
    else:
        conn_string = "host='{0}' dbname='{1}' user='{2}' password='{3}'".format(host, db, u, p)
        conn = psy.connect(conn_string)
        cursor = conn.cursor()
        
        sql_omsTables = """SELECT c.relname 
        FROM pg_catalog.pg_class c 
        LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace 
        WHERE n.nspname='""" + schema + """' 
        AND c.relkind IN ('r','') 
        AND n.nspname NOT IN ('pg_catalog', 'pg_toast', 'information_schema') 
        ORDER BY c.relname ASC"""
        
        #Get all available tables in database
        cursor.execute(sql_omsTables)
        availableTables = [tbl[0] for tbl in cursor]
        
        #determine if all tables or just a selection of table will be audited
        #TODO error trap empty string in other list positions other than index[0]
        process_tables = []
        if len(function_list) > 0:
            for aTbl in function_list:
                #print(availableTables.index(aTbl))
                if aTbl not in availableTables:
                    print('Function "audit_{0}()" does not exist in database {1}'.format(aTbl, db))
                else:
                    process_tables.append(aTbl)
        else:
            process_tables = availableTables

        counter = 0
        
        for tbl in process_tables:
            counter += 1
            try:
                cursor.execute("DROP FUNCTION IF EXISTS {0}.audit_{1}() CASCADE".format(schema, tbl))
                print("{0:>3}. Function audit_{1}(): DELETED".format(str(counter), tbl))
                
            except Exception as e:
                print(e)
                conn.rollback()
        
        conn.commit()
        del cursor
        return True

if __name__ == "__main__":
    host = 'fta_omslive'
    db = 'omslive'
    user = 'postgres'
    pw = 'gis123!@#'
    schema = 'public'
    action = 'DISABLE' #ENABLE
    
    #triggersUpdate(host, db, user, pw, schema, action)
    triggerDelete(host, db, user, pw, schema, [])
    functionDelete(host, db, user, pw, schema, [])
    print("Script Completed.")