'''
Created on Apr 11, 2013

@author: williamg
'''
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
        import arcpy, os
        from arcpy import env as env
        
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
        if self.usingDefaultWorkspace == False:
            #return "Workspace needs to be set before proceeding"
            return "NOT Using Default Workspace"
        else:
            #return self.wksp
            return "Using Default Workspace"
            

if __name__ == '__main__':
    sw = findSwitchOptions()
    #sw.setWorkspace()
    print(sw.setWorkspace("F:\\ksu\\anth4100"))
    print(sw.findPossibleSwitchingOptions())
    print("Script completed.")