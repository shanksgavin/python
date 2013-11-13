import arcpy, psycopg2
import psycopg2.extras

def getCalls():
    conn_string = "host='localhost' dbname='omsprod' user='postgres' password='usouth'"
    #print("Connecting to database\n ->%s" % (conn_string))
    
    conn = psycopg2.connect(conn_string)
    
    cursor = conn.cursor('cursor_unique_name', cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM calls where deleted = 'f' and callstatus = 'ACTIVE' LIMIT 1000")
    #cursor.execute("SELECT * FROM calls where deleted = 'f' and record_id = 111622103")
    
    row_count = 0
    for row in cursor:
        row_count += 1
        print("Record_ID: {0:<15}".format(row['record_id']))
        print("  Customer:  {0:30}  Account: {1}".format(row['customer'], row['account']))
        print("  Street:    {0:<50}".format(row['street']))
        print("  Street2:   {0:<50}".format(row['servadr2']))
        print("  Street3:   {0:<50}".format(row['servadr3']))
        print("  Phone:     {0:<30}  Phone Change: {1:>15}".format(row['phone'], row['phonechange']))
        print("  ticketnum: {0:30}  takenby: '{1}'".format(row['ticketnum'], row['takenby']))
    
def listWorkspaces():
    wksp = "C:\\map_files"
    arcpy.env.workspace = wksp
    
    wkspList = arcpy.ListWorkspaces('*', 'FileGDB')
    for ws in wkspList:
        print(ws)

if __name__ == "__main__":
    getCalls()
    #listWorkspaces()