'''
Title: Perform an Upstream Trace on every Meterbase to its DistributionSource
Created: July 09, 2014
Modified: 

@author: williamg

'''

import sys, os
import datetime as dt
# Try to import python postgres module
# Exit on fail
try:
    import psycopg2 as psy
except:
    print("Failed to import python-postgresql drivers.")
    sys.exit()

try:
    #import arcpy.env as env
    import arcpy
    
except:
    print("Failed to import arcpy ")
    sys.exit()
    
class meterbases():
    def __init__(self, host='localhost', db='coweta-fayette', u='postgres', p='usouth', mapfiles=r'C:\map_files', gdb=None):
        # Constants
        self.mapfiles = mapfiles
        self.gdb = gdb
        self.networkDS = 'ElectricNetwork'
        self.consumer = 'Consumer'
        self.PC = 'PrimaryConductor'
        self.SC = 'SecondaryConductor'
        self.DS = 'DistributionSource'
        self.trace = {} #dictionary of line segments
        self.traceCounter = 0
        self.testMapNumber = '55124044'
        self.startTime = dt.datetime.now()

        try:
            #TODO: Consider adding conn_string to object -> self.conn_string
            conn_string = "host='{0}' dbname='{1}' user='{2}' password='{3}'".format(host, db, u, p)
            self.conn = psy.connect(conn_string)
            self.cursor = self.conn.cursor()
            self.curtime = dt.datetime.now()
            
        except:
            print("Failed to create connection to database.")
            sys.exit()
            
        try:
            arcpy.env.workspace = self.mapfiles + os.sep + self.gdb + os.sep + self.networkDS
        except:
            print("Map_Files workspace cannot be set.")
            sys.exit()
            
    def closeConn(self):
        del self.cursor
    
    def getMeterbases(self):
        meterbases = []
        fc = self.consumer
        fields = ["MapNumber"]
        
        with arcpy.da.SearchCursor(fc, fields) as cursor:
            for row in cursor:
                #print("{0}, {1}, {2}".format(row[0], row[1], row[2]))
                if row[0] is not None:
                    meterbases.append(row[0])
        return meterbases
    
    def get_SC(self, mb):
        where = '"MapNumber" = \'{0}\''.format(mb)
        try:
            arcpy.MakeFeatureLayer_management(self.consumer, "mb", where) #Create feature layer for meterbase to start off the uptrace
            arcpy.MakeFeatureLayer_management(self.SC, "sc") #Create Secondary Conductor feature layer
            #mb_selected = int(arcpy.GetCount_management("mb").getOutput(0))
            #print('Consumer Layer Created for MapNumber: {0} with {1} selected features.'.format(mb, str(mb_selected)))
        except Exception as e:
            print(e)
            sys.exit()
            
        arcpy.SelectLayerByLocation_management("sc","intersect","mb", 0, "ADD_TO_SELECTION")
        sc_selected = int(arcpy.GetCount_management("sc").getOutput(0))
        if sc_selected < 1:
            print('Meterbase {0} did not intersect with {1}'.format(mb, self.SC))
            return None
        else:
            #sc = self.mapfiles + os.sep + self.gdb + os.sep + self.networkDS + os.sep + self.SC
            fields = ["MapNumber"]
            try:
                with arcpy.da.SearchCursor("sc", fields) as cursor_sc:
                    for row_sc in cursor_sc:
                        if row_sc[0] is not None:
                            self.trace[mb] = self.trace.get(mb,{"SC":{self.traceCounter:row_sc[0]}})
                            self.traceCounter += 1
                return None
            except Exception as e:
                print(e)
                sys.exit() 
    
    def get_PC(self, mapNumber):
        print('MapNumber Provided: {0}'.format(mapNumber))
    
    def traceUP(self, mb):
        self.trace = {}
        self.traceCounter = 0
        self.get_SC(mb)
        if len(self.trace[mb]['SC']) > 1:
            print('{0} SC line(s) were found'.format(str(len(self.trace))))
            print(self.trace)
        else:
            for sc in self.trace[mb]['SC']:
                self.get_PC(self.trace[mb]['SC'][sc])
        return None
    
if __name__ == '__main__':
    mbs = meterbases('localhost', 'sequachee', 'postgres', 'usouth', r'C:\map_files', r'CWF_gis.gdb')
    mapNumbers = mbs.getMeterbases()
    if len(mapNumbers) > 0:
#        print(mbs)
        if mbs.testMapNumber in mapNumbers:
            print('Found MapNumber: {0}'.format(mbs.testMapNumber))
            mbs.traceUP(mbs.testMapNumber)
            #mbs.traceUP(mb)
            print(mbs.trace)
    mbs.closeConn()
    print('Completed.')