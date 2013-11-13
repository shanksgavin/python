import arcpy

lyrFile = arcpy.mapping.Layer("F:\\ksu\\anth4100\\Styles\\Witness Trees 20130326.lyr")
for lyr in arcpy.mapping.ListLayers(lyrFile):
    print("Layer Name:" + lyr.name)
    print("Sym Type: " + lyr.symbologyType)
    if lyr.symbologyType == "UNIQUE_VALUES":
#         print("Class Descriptions: ")
#         for clsDesc in lyr.symbology.classDescriptions:
#             print("    " + clsDesc)
        print("Class Labels: ")
        #classLabels = []
        for clsLbl in set(lyr.symbology.classLabels):
            print(clsLbl)
            #classLabels.append(clsLbl)
        
#         print("Class Values: ")
#         for clsVal in lyr.symbology.classValues:
#             print("    " + clsVal)
#         print("Value Field: " + lyr.symbology.valueField)