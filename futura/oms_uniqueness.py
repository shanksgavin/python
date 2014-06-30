'''
Title: Search through OMS tables & fields reporting on DISTINCT values with counts
Created: June 26, 2014
Modified: June 26, 2014

@author: williamg

'''

import sys
import datetime as dt
# Try to import python postgres module
# Exit on fail
try:
    import psycopg2 as psy
except:
    print("Failed to import python-postgresql drivers.")
    sys.exit()


class checkUniqueness():
    def __init__(self, host='localhost', db='coweta-fayette', u='postgres', p='usouth'):
        # Constants
        self.schema = ''
        self.resultSchema = ''
        self.resultTableName = ''
        self.startTime = dt.datetime.now()
        self.reservedWords = ['A','ABORT','ABS','ABSENT','ABSOLUTE','ACCESS','ACCORDING','ACTION','ADA','ADD','ADMIN','AFTER','AGGREGATE','ALIAS','ALL',
                         'ALLOCATE','ALSO','ALTER','ALWAYS','ANALYSE','ANALYZE','AND','ANY','ARE','ARRAY','ARRAY_AGG','AS','ASC','ASENSITIVE','ASSERTION',
                         'ASSIGNMENT','ASYMMETRIC','AT','ATOMIC','ATTRIBUTE','ATTRIBUTES','AUTHORIZATION','AVG','BACKWARD','BASE64','BEFORE','BEGIN',
                         'BERNOULLI','BETWEEN','BIGINT','BINARY','BIT','BITVAR','BIT_LENGTH','BLOB','BOM','BOOLEAN','BOTH','BREADTH','BY','C','CACHE',
                         'CALL','CALLED','CARDINALITY','CASCADE','CASCADED','CASE','CAST','CATALOG','CATALOG_NAME','CEIL','CEILING','CHAIN','CHAR',
                         'CHARACTER','CHARACTERISTICS','CHARACTERS','CHARACTER_LENGTH','CHARACTER_SET_CATALOG','CHARACTER_SET_NAME','CHARACTER_SET_SCHEMA',
                         'CHAR_LENGTH','CHECK','CHECKED','CHECKPOINT','CLASS','CLASS_ORIGIN','CLOB','CLOSE','CLUSTER','COALESCE','COBOL','COLLATE',
                         'COLLATION','COLLATION_CATALOG','COLLATION_NAME','COLLATION_SCHEMA','COLLECT','COLUMN','COLUMNS','COLUMN_NAME','COMMAND_FUNCTION',
                         'COMMAND_FUNCTION_CODE','COMMENT','COMMIT','COMMITTED','COMPLETION','CONCURRENTLY','CONDITION','CONDITION_NUMBER','CONFIGURATION',
                         'CONNECT','CONNECTION','CONNECTION_NAME','CONSTRAINT','CONSTRAINTS','CONSTRAINT_CATALOG','CONSTRAINT_NAME','CONSTRAINT_SCHEMA',
                         'CONSTRUCTOR','CONTAINS','CONTENT','CONTINUE','CONVERSION','CONVERT','COPY','CORR','CORRESPONDING','COST','COUNT','COVAR_POP','COVAR_SAMP',
                         'CREATE','CREATEDB','CREATEROLE','CREATEUSER','CROSS','CSV','CUBE','CUME_DIST','CURRENT','CURRENT_CATALOG','CURRENT_DATE','CURRENT_DEFAULT_TRANSFORM_GROUP',
                         'CURRENT_PATH','CURRENT_ROLE','CURRENT_SCHEMA','CURRENT_TIME','CURRENT_TIMESTAMP','CURRENT_TRANSFORM_GROUP_FOR_TYPE','CURRENT_USER',
                         'CURSOR','CURSOR_NAME','CYCLE','DATA','DATABASE','DATE','DATETIME_INTERVAL_CODE','DATETIME_INTERVAL_PRECISION','DAY','DEALLOCATE',
                         'DEC','DECIMAL','DECLARE','DEFAULT','DEFAULTS','DEFERRABLE','DEFERRED','DEFINED','DEFINER','DEGREE','DELETE','DELIMITER','DELIMITERS',
                         'DENSE_RANK','DEPTH','DEREF','DERIVED','DESC','DESCRIBE','DESCRIPTOR','DESTROY','DESTRUCTOR','DETERMINISTIC','DIAGNOSTICS','DICTIONARY',
                         'DISABLE','DISCARD','DISCONNECT','DISPATCH','DISTINCT','DO','DOCUMENT','DOMAIN','DOUBLE','DROP','DYNAMIC','DYNAMIC_FUNCTION','DYNAMIC_FUNCTION_CODE',
                         'EACH','ELEMENT','ELSE','EMPTY','ENABLE','ENCODING','ENCRYPTED','END','END-EXEC','ENUM','EQUALS','ESCAPE','EVERY','EXCEPT',
                         'EXCEPTION','EXCLUDE','EXCLUDING','EXCLUSIVE','EXEC','EXECUTE','EXISTING','EXISTS','EXP','EXPLAIN','EXTERNAL','EXTRACT','FALSE',
                         'FAMILY','FETCH','FILTER','FINAL','FIRST','FIRST_VALUE','FLAG','FLOAT','FLOOR','FOLLOWING','FOR','FORCE','FOREIGN','FORTRAN','FORWARD','FOUND',
                         'FREE','FREEZE','FROM','FULL','FUNCTION','FUSION','G','GENERAL','GENERATED','GET','GLOBAL','GO','GOTO','GRANT','GRANTED','GREATEST',
                         'GROUP','GROUPING','HANDLER','HAVING','HEADER','HEX','HIERARCHY','HOLD','HOST','HOUR','ID','IDENTITY','IF','IGNORE','ILIKE','IMMEDIATE',
                         'IMMUTABLE','IMPLEMENTATION','IMPLICIT','IN','INCLUDING','INCREMENT','INDENT','INDEX','INDEXES','INDICATOR','INFIX','INHERIT',
                         'INHERITS','INITIALIZE','INITIALLY','INNER','INOUT','INPUT','INSENSITIVE','INSERT','INSTANCE','INSTANTIABLE','INSTEAD','INT',
                         'INTEGER','INTERSECT','INTERSECTION','INTERVAL','INTO','INVOKER','IS','ISNULL','ISOLATION','ITERATE','JOIN','K','KEY','KEY_MEMBER','KEY_TYPE',
                         'LAG','LANCOMPILER','LANGUAGE','LARGE','LAST','LAST_VALUE','LATERAL','LC_COLLATE','LC_CTYPE','LEAD','LEADING','LEAST','LEFT',
                         'LENGTH','LESS','LEVEL','LIKE','LIKE_REGEX','LIMIT','LISTEN','LN','LOAD','LOCAL','LOCALTIME','LOCALTIMESTAMP','LOCATION','LOCATOR','LOCK',
                         'LOGIN','LOWER','M','MAP','MAPPING','MATCH','MATCHED','MAX','MAXVALUE','MAX_CARDINALITY','MEMBER','MERGE','MESSAGE_LENGTH','MESSAGE_OCTET_LENGTH',
                         'MESSAGE_TEXT','METHOD','MIN','MINUTE','MINVALUE','MOD','MODE','MODIFIES','MODIFY','MODULE','MONTH','MORE','MOVE','MULTISET','MUMPS',
                         'NAME','NAMES','NAMESPACE','NATIONAL','NATURAL','NCHAR','NCLOB','NESTING','NEW','NEXT','NFC','NFD','NFKC','NFKD','NIL','NO','NOCREATEDB',
                         'NOCREATEROLE','NOCREATEUSER','NOINHERIT','NOLOGIN','NONE','NORMALIZE','NORMALIZED','NOSUPERUSER','NOT','NOTHING','NOTIFY','NOTNULL',
                         'NOWAIT','NTH_VALUE','NTILE','NULL','NULLABLE','NULLIF','NULLS','NUMBER','NUMERIC','OBJECT','OCCURRENCES_REGEX','OCTETS','OCTET_LENGTH',
                         'OF','OFF','OFFSET','OIDS','OLD','ON','ONLY','OPEN','OPERATION','OPERATOR','OPTION','OPTIONS','OR','ORDER','ORDERING','ORDINALITY','OTHERS',
                         'OUT','OUTER','OUTPUT','OVER','OVERLAPS','OVERLAY','OVERRIDING','OWNED','OWNER','P','PAD','PARAMETER','PARAMETERS','PARAMETER_MODE','PARAMETER_NAME',
                         'PARAMETER_ORDINAL_POSITION','PARAMETER_SPECIFIC_CATALOG','PARAMETER_SPECIFIC_NAME','PARAMETER_SPECIFIC_SCHEMA','PARSER','PARTIAL','PARTITION',
                         'PASCAL','PASSING','PASSWORD','PATH','PERCENTILE_CONT','PERCENTILE_DISC','PERCENT_RANK','PLACING','PLANS','PLI','POSITION','POSITION_REGEX',
                         'POSTFIX','POWER','PRECEDING','PRECISION','PREFIX','PREORDER','PREPARE','PREPARED','PRESERVE','PRIMARY','PRIOR','PRIVILEGES','PROCEDURAL',
                         'PROCEDURE','PUBLIC','QUOTE','RANGE','RANK','READ','READS','REAL','REASSIGN','RECHECK','RECURSIVE','REF','REFERENCES','REFERENCING','REGR_AVGX',
                         'REGR_AVGY','REGR_COUNT','REGR_INTERCEPT','REGR_R2','REGR_SLOPE','REGR_SXX','REGR_SXY','REGR_SYY','REINDEX','RELATIVE','RELEASE',
                         'RENAME','REPEATABLE','REPLACE','REPLICA','RESET','RESPECT','RESTART','RESTRICT','RESULT','RETURN','RETURNED_CARDINALITY','RETURNED_LENGTH',
                         'RETURNED_OCTET_LENGTH','RETURNED_SQLSTATE','RETURNING','RETURNS','REVOKE','RIGHT','ROLE','ROLLBACK','ROLLUP','ROUTINE','ROUTINE_CATALOG','ROUTINE_NAME',
                         'ROUTINE_SCHEMA','ROW','ROWS','ROW_COUNT','ROW_NUMBER','RULE','SAVEPOINT','SCALE','SCHEMA','SCHEMA_NAME','SCOPE','SCOPE_CATALOG','SCOPE_NAME',
                         'SCOPE_SCHEMA','SCROLL','SEARCH','SECOND','SECTION','SECURITY','SELECT','SELF','SENSITIVE','SEQUENCE','SERIALIZABLE','SERVER','SERVER_NAME',
                         'SESSION','SESSION_USER','SET','SETOF','SETS','SHARE','SHOW','SIMILAR','SIMPLE','SIZE','SMALLINT','SOME','SOURCE','SPACE','SPECIFIC','SPECIFICTYPE',
                         'SPECIFIC_NAME','SQL','SQLCODE','SQLERROR','SQLEXCEPTION','SQLSTATE','SQLWARNING','SQRT','STABLE','STANDALONE','START','STATE','STATEMENT','STATIC',
                         'STATISTICS','STDDEV_POP','STDDEV_SAMP','STDIN','STDOUT','STORAGE','STRICT','STRIP','STRUCTURE','STYLE','SUBCLASS_ORIGIN','SUBLIST','SUBMULTISET','SUBSTRING',
                         'SUBSTRING_REGEX','SUM','SUPERUSER','SYMMETRIC','SYSID','SYSTEM','SYSTEM_USER','T','TABLE','TABLESAMPLE','TABLESPACE','TABLE_NAME','TEMP','TEMPLATE',
                         'TEMPORARY','TERMINATE','TEXT','THAN','THEN','TIES','TIME','TIMESTAMP','TIMEZONE_HOUR','TIMEZONE_MINUTE','TO','TOP_LEVEL_COUNT','TRAILING','TRANSACTION',
                         'TRANSACTIONS_COMMITTED','TRANSACTIONS_ROLLED_BACK','TRANSACTION_ACTIVE','TRANSFORM','TRANSFORMS','TRANSLATE','TRANSLATE_REGEX','TRANSLATION','TREAT',
                         'TRIGGER','TRIGGER_CATALOG','TRIGGER_NAME','TRIGGER_SCHEMA','TRIM','TRIM_ARRAY','TRUE','TRUNCATE','TRUSTED','TYPE','UESCAPE','UNBOUNDED','UNCOMMITTED',
                         'UNDER','UNENCRYPTED','UNION','UNIQUE','UNKNOWN','UNLISTEN','UNNAMED','UNNEST','UNTIL','UNTYPED','UPDATE','UPPER','URI','USAGE','USER','USER_DEFINED_TYPE_CATALOG',
                         'USER_DEFINED_TYPE_CODE','USER_DEFINED_TYPE_NAME','USER_DEFINED_TYPE_SCHEMA','USING','VACUUM','VALID','VALIDATOR','VALUE','VALUES','VARBINARY','VARCHAR',
                         'VARIABLE','VARIADIC','VARYING','VAR_POP','VAR_SAMP','VERBOSE','VERSION','VIEW','VOLATILE','WHEN','WHENEVER','WHERE','WHITESPACE','WIDTH_BUCKET','WINDOW',
                         'WITH','WITHIN','WITHOUT','WORK','WRAPPER','WRITE','XML','XMLAGG','XMLATTRIBUTES','XMLBINARY','XMLCAST','XMLCOMMENT','XMLCONCAT','XMLDECLARATION',
                         'XMLDOCUMENT','XMLELEMENT','XMLEXISTS','XMLFOREST','XMLITERATE','XMLNAMESPACES','XMLPARSE','XMLPI','XMLQUERY','XMLROOT','XMLSCHEMA','XMLSERIALIZE','XMLTABLE',
                         'XMLTEXT','XMLVALIDATE','YEAR','YES','ZONE']
        
        try:
            #TODO: Consider adding conn_string to object -> self.conn_string
            conn_string = "host='{0}' dbname='{1}' user='{2}' password='{3}'".format(host, db, u, p)
            self.conn = psy.connect(conn_string)
            self.cursor = self.conn.cursor()
            self.curtime = dt.datetime.now()
            
        except:
            print("Failed to create connection to database.")
            sys.exit()

    def closeConn(self):
        del self.cursor
        
    def stampIt(self):
        print(dt.datetime.now())
        
    def totalTime(self):
        print("Total Script Time: {0}".format(dt.datetime.now()-self.startTime))        
        
    def get_tables(self):
        sql = """SELECT c.relname 
        FROM pg_catalog.pg_class c 
        LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace 
        WHERE n.nspname='""" + self.schema + """' 
        AND c.relkind IN ('r','') 
        AND n.nspname NOT IN ('pg_catalog', 'pg_toast', 'information_schema') 
        ORDER BY c.relname ASC"""
        
        self.cursor.execute(sql)
        self.Tables = [tbl[0] for tbl in self.cursor]
        
        return self

        #for table in availableTables:
        #    print(table)
        #    #print(self.stampIt())
    
    def get_fields(self, table):
        sql = """        SELECT column_name
            from information_schema.columns
            where table_schema = '""" + self.schema + """'
            and table_name = '""" + table + """'
            and data_type not in ('ARRAY', 'box', 'bytea', 'path', 'point', 'polygon', 'xml')
            order by ordinal_position asc """
        #print(sql)
        self.cursor.execute(sql)
        self.Fields = [field[0] for field in self.cursor]
        
        return self.Fields

        #for table in availableTables:
        #    print(table)
        #    #print(self.stampIt())
        
    def get_unique(self, table, column_name):
        sql = """        SELECT DISTINCT("""+column_name+"""), count("""+column_name+""")
            from """+table+"""
            GROUP BY """+column_name+"""
            HAVING count("""+column_name+""") > 1
            ORDER BY count("""+column_name+""") desc"""
        #print(sql)
        self.cursor.execute(sql)
        uniqueness = [field for field in self.cursor]
        #print(uniqueness)
        if len(uniqueness) > 0:
            #print("table, column_name, data_value, data_count")
            for unq in uniqueness:
                #print("'{0}', '{1}', '{2}', '{3}'".format(table, column_name, unq[0], unq[1])) #psy.extensions.QuotedString(column_name).getquoted()
                try:
                    sql = u"INSERT INTO {0}.{1} (table_name, column_name, data_value, data_count) VALUES ('{2}', '{3}', {4}, {5})".format(self.resultSchema, self.resultTableName, table, column_name, psy.extensions.QuotedString(str(unq[0])).getquoted(), int(unq[1]))
                    self.cursor.execute(sql)
                except Exception as e:
                    print(e)
            self.conn.commit()

    def checkReservedWords(self, column_name):
        if column_name.upper() in self.reservedWords:
            new_column_name = '"' + column_name + '"'
            #print("Reserve Word Found: {0} and changed to {1}".format(column_name, new_column_name))
        else:
            new_column_name = column_name
        return new_column_name
    
    def tableExist(self):
        sql = """        SELECT table_name
            from information_schema.tables
            where table_schema = '""" + self.resultSchema + """'
            and table_name = '""" + self.resultTableName + """'"""
            
        #print(sql)
        self.cursor.execute(sql)
        tables = [table[0] for table in self.cursor]
        
        if len(tables) == 1:
            return True
        elif len(tables) == 0:
            return False
        else:
            print('ERROR: More than one table found: {0}.{1}'.format(self.resultSchema,self.resultTableName))
            sys.exit()
    
    def tableCreate(self):
        sql = """        CREATE TABLE {0}.{1} (
        table_name CHARACTER VARYING(100),
        column_name CHARACTER VARYING(100),
        data_value TEXT,
        data_count INTEGER,
        CONSTRAINT unique_data UNIQUE(table_name, column_name, data_value)
        );""".format(self.resultSchema, self.resultTableName)
            
        #print(sql)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
            sys.exit()
        return True
    
    def tableTruncate(self):
        sql = """TRUNCATE {0}.{1};""".format(self.resultSchema, self.resultTableName)
            
        #print(sql)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
            sys.exit()
        return True
    
if __name__ == '__main__':
    # Create Postgres Connection Object
    c = checkUniqueness('localhost', 'coweta-fayette', 'postgres', 'usouth')
    # Set Working Schema & Table to receive data 
    c.schema = 'public'
    c.resultSchema = 'oms_logfiles'
    c.resultTableName = 'oms_non_unique_data'
    print(c.curtime)
    # Check for table to receive data
    # Truncate if table Exists
    if c.tableExist():
        c.tableTruncate()
    else:
        c.tableCreate()
    # Get all OMS Tables in public schema
    # Includes NEW tables for exported data
    try:
        c.get_tables()
    except Exception as e:
        c.Tables = None
        print(e)
        sys.exit()
    # Test is tables returned is None
    # If True (None) then Exit 
    if c.Tables is not None:
        # Loop through each table to get the fields 
        for tbl in c.Tables:
            print('Processing {0}'.format(tbl))
            c.get_fields(tbl)
            # Run DISTINCT sql query on all data in selected column of selected table
            for fld in c.Fields:
                # Test field name as a postgres reserved word
                # If True (reserved-word) then double-quote the field before running DISTINCT query
                fld = c.checkReservedWords(fld)
                c.get_unique(tbl, fld)
    else:
        print("No Tables Found.")
    # Close postgres connection
    c.closeConn()
    c.totalTime()
    # End the Script with a notification
    print('Script Completed.')