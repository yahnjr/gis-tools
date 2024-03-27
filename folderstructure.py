import arcpy

def list_features(gdb_path):
    arcpy.env.workspace = gdb_path
    feat_list = arcpy.ListFeatureClasses()
    for feat in feat_list:
        print(feat)
    # files_list = arcpy.ListFiles()
    # if gdb_path[-3:] != "gdb":
    #     for file in files_list:
    #         print(file)
        
list_features(r"J:\Planning\GIS\Washington\Wahkiakum County")