import arcpy, psycopg2, datetime
import psycopg2.extras

def getClosedCasePieChartData(startDate=None, endDate=None):
    """ Get Closed Case information to display in HighChart's Pie Chart"""
    #Set default dates with startDate 1 day before endDate = now()
    if (startDate and endDate) == None:
        defaultEndDate = datetime.datetime.now()
        endDate = defaultEndDate.strftime("%Y-%m-%d")
        defaultDaysBack = datetime.timedelta(days=1)
        defaultStartDate = defaultEndDate - defaultDaysBack
        startDate = defaultStartDate.strftime("%Y-%m-%d")
    #Set startDate if None to 1 day before endDate
    if startDate == None:
        defaultDaysBack = datetime.timedelta(days=1)
        defaultStartDate = endDate - defaultDaysBack
        startDate = defaultStartDate.strftime("%Y-%m-%d")
    #Set endDate if None to today
    if endDate == None:
        defaultEndDate = datetime.datetime.now()
        endDate = defaultEndDate.strftime("%Y-%m-%d")
    
    #Show me the dates being supplied to sql     
    #print("Start Date: {0} and End Date: {1}".format(startDate, endDate))
    
    conn_string = "host='localhost' dbname='omsprod' user='postgres' password='usouth'"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor('cursor_unique_name', cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("""Select distinct(cause) as cause, count(cause) as cause_counts 
                        from cases
                        where casestatus = 'Closed'
                        and datestrt >= '"""+startDate+"""'::date
                        and dateend <= '"""+endDate+"""'::date
                        and deleted = 'false'
                        and repowereddate != startdate
                        group by cause
                        order by cause asc""")
    
    row_count = 0
    ifNone = True
    for row in cursor:
        ifNone = False
        row_count += 1
        if row['cause'] == '':
            print("['{0}', {1}],".format('BLANK', row['cause_counts']))
        else:
            print("['{0}', {1}],".format(row['cause'], row['cause_counts']))
    if ifNone == True:
        print("No data available between "+startDate+" and "+endDate)

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
    print("Get Closed Case Causes with explicit dates")
    getClosedCasePieChartData("2011-01-01","2011-12-31")
    
    #print("Get Closed Case Causes with default dates")
    #getClosedCasePieChartData()
    
    #getCalls()
    #listWorkspaces()