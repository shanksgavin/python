# coding:utf-8
'''
Created on February 28, 2014
Updated on February 28, 2014
@author: williamg

'''

#Import Modules
import arcpy

def createFGDB(folder=None, name=None):
    #Set Variables
    outFolder = folder
    outName = name
    
    #Start the process
    try:
        arcpy.CreateFileGDB_management(outFolder, outName)
        return 0
    except:
        return -1
    
def copyMDBtoGDB():
    pass

if __name__ == '__main__':
    createFGDB(r'C:\map_files', r'TaylorEC.gdb')
    copyMDBtoGDB()