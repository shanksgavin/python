'''
Title: Enable/Disable Audit Trigger Functions on Public Schema
Created: April 9, 2013
Modified: April 9, 2013

@author: williamg

@version: 0.1
'''

def updateTriggers(host=None, db=None, u=None, p=None, schema=None, action=None):
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
            
if __name__ == "__main__":
    host = 'localhost'
    db = 'inland_20140204'
    user = 'postgres'
    pw = 'usouth'
    schema = 'public'
    action = 'DISABLE' #ENABLE
    
    updateTriggers(host, db, user, pw, schema, action)
    print("Script Completed.")