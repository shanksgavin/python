'''
Created on Apr 11, 2013

@author: williamg
'''
import arcpy, os
from arcpy import env as env

class findSwitchOptions:
    """ Locating Possible Switching Options within Workspace"""
    def __init__(self):
        self.workspaceIsSet = False
        self.usingDefaultWorkspace = False
        self.wksp = ""
        
    def setWorkspace(self, workspace=None):
        """ Set this function to read from the active 
        Postgres db SETTINGS table to determine default
        paths and workspace """
        
        # Define workspace path
        if workspace is None:
            workspace = "C:\\map_files\\"
            self.usingDefaultWorkspace = True
        
        # Set arcpy workspace
        env.workspace = workspace
        gdbList = arcpy.ListWorkspaces('*', 'FileGDB')
        
        for gdb in gdbList:
            #print(gdb)
            if os.path.split(gdb)[1] == 'WEC_PGDB101.gdb':
                self.wksp = gdb
                env.workspace = self.wksp
                self.workspaceIsSet = True
                self.usingDefaultWorkspace = True
                break
            else:
                self.wksp = workspace
                env.workspace = workspace
                self.usingDefaultWorkspace = False
                #print("Wiregrass FileGDB was not located")
        
        return self.wksp
    
    def findPossibleSwitchingOptions(self):
        #Create a storage container for found features
        self.foundSwitches = []
        
        if self.workspaceIsSet == False:
            return (0, self.foundSwitches, "Workspace needs to be set before proceeding")
        else:
            #Define feature layer names to be used in the geoprocess
            OpenPointFC = ("ElectricNetwork\\OpenPoint", "OpenPointLyr")
            SwitchFC = ("ElectricNetwork\\Switchbank", "SwitchLyr")
            SecLineFC = ("ElectricNetwork\\SecondaryConductor", "SecondaryConductorLyr")
            PriLineFC = ("ElectricNetwork\\PrimaryConductor", "PrimaryConductorLyr")
            
            #print out the acrpy workspace to ensure it is set
            env.workspace = self.wksp
            print(env.workspace)
            
            #Create feature layer
            try:
                if arcpy.Exists(OpenPointFC[0]):
                    print("Found: " + OpenPointFC[0])
                    #arcpy.MakeFeatureLayer_management(OpenPointFC[0], OpenPointFC[1])
                    arcpy.MakeFeatureLayer_management(OpenPointFC[0], OpenPointFC[1])
                    arcpy.MakeFeatureLayer_management(SwitchFC[0], SwitchFC[1])
                    arcpy.MakeFeatureLayer_management(SecLineFC[0], SecLineFC[1])
                    arcpy.MakeFeatureLayer_management(PriLineFC[0], PriLineFC[1])
                    print("Feature layers created")
                    
                else:
                    print(OpenPointFC[0] + " was not found in " + env.workspace)
                    
            except:
                #print("Failed to create feature layers")
                return (-1, self.foundSwitches, "Failed to create feature layers")

            
            #Loop through each SwitchBank and perform a series of spatial selections
            #  to find possible switching scenarios.
            whereClause = "{0} = 0".format(arcpy.AddFieldDelimiters(SwitchFC[0], "Enabled"))
            print(whereClause)
            with arcpy.da.SearchCursor(SwitchFC[0], ("FuturaGUID", "StructureGUID", "NetworkID", "MapNumber", "PhaseCode", "Enabled", "Comments", "Type"), whereClause) as switchCursor:
                for switchesRow in switchCursor:
                    #Clear Any possible selection on Secondary Lines before spatial selection
                    #arcpy.SelectLayerByAttribute_management(SecLineFC[1], "CLEAR_SELECTION")
                    #Select layer by attribute
                    arcpy.SelectLayerByAttribute_management(SwitchFC[1], "NEW_SELECTION", "\"FuturaGUID\" = '" + switchesRow[0] + "'")
                    #Perform a spatial selection of OpenPoints within 15ft of Secondary Line
                    #arcpy.SelectLayerByLocation_management(SecLineFC[1], "INTERSECT", SwitchFC[1], "", "NEW_SELECTION")
                    #Get count of selected Secondary lines that INTERESECT the selected open point
                    numberOfSelectedSecondaryLines = 0 #int(arcpy.GetCount_management(SecLineFC[1]).getOutput(0))
                    #Perform a spatial selection of OpenPoints within 15ft of Secondary Line
                    arcpy.SelectLayerByLocation_management(PriLineFC[1], "INTERSECT", SwitchFC[1], "", "NEW_SELECTION")
                    #Get count of selected Priamry lines that INTERESECT the selected SwitchBank
                    numberOfSelectedPrimaryLines = int(arcpy.GetCount_management(PriLineFC[1]).getOutput(0))
                    #print(type(numberOfSelectedSecondaryLines))
                    totalSelectedLines = numberOfSelectedSecondaryLines + numberOfSelectedPrimaryLines
                    #Print a statement indicating Secondary lines intersected the current Open Point
                    if totalSelectedLines > 1:
                        #print("Number of Selected Secondary Lines for Open Point " + openPointsRow[4] + " is " + str(numberOfSelectedSecondaryLines))
                        with arcpy.da.SearchCursor(PriLineFC[1], ["FuturaGUID", "MapNumber", "PhaseCode", "Placement", "Enabled", "FEEDER", "VOLTAGE"]) as priLineCursor:
                            #print("OpenPoint MapNum, OpenPoint Phase: SecLine Phase")
                            for priLineRow in priLineCursor:
                                if switchesRow[4] == priLineRow[2]:
                                    #print("Switch " + str(switchesRow[3]) + " has a phase " + str(switchesRow[4]) + " and matches primary line " + str(priLineRow[1]))
                                    if switchesRow[0] not in self.foundSwitches:
                                        self.foundSwitches.append(switchesRow[0])

            
        return (1, self.foundSwitches, "findPossibleSwitchingOption completed successfully")

if __name__ == '__main__':
    sw = findSwitchOptions()
    sw.setWorkspace()
    #print(sw.setWorkspace())
    #print(sw.findPossibleSwitchingOptions())
    errCode, resultList, msg = sw.findPossibleSwitchingOptions()
    if errCode == 1:
        print(len(resultList))
        print(resultList)
    else:
        print(str(errCode), msg)
#     for x in range(arcpy.GetMessageCount()):
#         print(arcpy.GetMessage(x))
    print("Script completed.")
    