# coding:utf-8
'''
Created on February 28, 2014
Updated on February 28, 2014
@author: williamg

'''

def getOMSFeatures(src, dst, symlinks=False, ignore=None):
    import shutil, os
    
    try:
        if os.path.isdir(dst):
            try:
                shutil.rmtree(dst, True)
                #shutil.copytree(src, dst, symlinks, ignore)
            except:
                print("Failed to delete existing OMS Features GDB")
                return -2
        shutil.copytree(src, dst, symlinks, ignore)
        return 0
    except OSError as e:
        print(e)
        return -1
    

if __name__ == '__main__':
    try:
        result = getOMSFeatures(r"\\orion\Common\GISServerSetupDVD\OMS\Master_OMS_Features.gdb", r"C:\map_files\OMS_Features.gdb", False, None)
        print("Updated OMS Features.gdb; Result Code: {0}".format(str(result)))
    except:
        print("Updated OMS Features.gdb Failed")
    
    print("Script Completed.")
        