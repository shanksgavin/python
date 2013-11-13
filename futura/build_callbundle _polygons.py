import arcpy
import psycopg2
import psycopg2.extras
import datetime

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

def build_polygons(f=None):
    if f is None:
        return "No Filename Supplied"
    else:
        #import os
        fo = open(f, "r")
        #fw = open(f + ".sql", "w+")
        #last_values = {}
        fc = "C:\\map_files\\OMS_Features.gdb\\callbundle_multipoint"
        try:
            if arcpy.Exists(fc):
                arcpy.Delete_management(fc)
                print("Callbundle_multipoint deleted")
            arcpy.CreateFeatureclass_management("C:\\map_files\\OMS_Features.gdb", "callbundle_multipoint", "MULTIPOINT")
            print("Callbundle_multipoint created")
            arcpy.AddField_management(fc, "audit_id", "LONG")
            print("Audit_ID field added")
        except:
            print("failed to prep feature class")
            exit()
        
        for line in fo:
            if len(line.strip()) == 0 or line == '\n':
                pass
            else:
                try:
                    point = arcpy.Point()
                    array = arcpy.Array()
                    data = line.split('|', 1)
                    id = data[0]
                    poly_pts = data[1].strip('\n').replace('(','').replace(')','').split(',')
                    print(poly_pts)
                    if len(poly_pts) > 1:
                        # Do more stuff here with the data points to create a polygon
                        cnt = 0
                        for pt in poly_pts:
                            if (cnt % 2) == 0:
                                point.X = pt
                            else:
                                point.Y = pt
                                array.add(point)
                            cnt += 1
#                             box += 1
#                             if (box % 8) == 0:
#                                 array.add(arcpy.Point(poly_pts[0],poly_pts[1]))
#                                 pg = arcpy.Polygon(array)
                        
                        multipoint = arcpy.Multipoint(array)
                        #print("Multi-points have been created")
                        with arcpy.da.InsertCursor(fc, ["SHAPE@", "audit_id"]) as cursor:
                            cursor.insertRow([multipoint, id])
                        #print("Multi-points inserted into feature class")
                    else:
                        print("need 1 or more points to create a multi-point")
                        exit()
                except:
                    print("something failed")
        fo.close()
        return "completed file " + f

if __name__ == "__main__":
    print(build_polygons("C:\\map_files\\callbundle_polygons.csv"))