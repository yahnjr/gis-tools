import arcpy
from arcpy.sa import *
import os

arcpy.env.overwriteOutput = True
arcpy.env.workspace = r"Make special workspace with inputs"
cad_output = r"output folder"
exportma = "no"
exportcad = "yes"
extent = "FILL-YOUR-EXTENT-HERE (Extract from ArcGIS Pro Python Command)"

workspace = arcpy.env.workspace

# If you want to make a script
# arcpy.env.workspace = arcpy.GetParameterAsText(0)
# output_path = arcpy.GetParameterAsText(1)
# processma = arcpy.GetParameterAsText(2)


# Process into polygon layers from continuous raster layer
def hecrasProcess(raster_name, remap):
    raster = arcpy.Raster(raster_name)

    out_reclass = raster_name + "_reclass"
    with arcpy.EnvManager(extent=extent):
        arcpy.ddd.Reclassify(
            in_raster=raster,
            reclass_field="VALUE",
            remap=remap,
            out_raster=out_reclass,
            missing_values="DATA",
        )

    print(f"{out_reclass} reclassified")
    arcpy.AddMessage(f"{out_reclass} reclassified")

    out_polygon = raster_name + "_polygons"
    arcpy.conversion.RasterToPolygon(
        in_raster=out_reclass,
        out_polygon_features=out_polygon,
        simplify="NO_SIMPLIFY",
        raster_field="Value",
        create_multipart_features="MULTIPLE_OUTER_PART",
        max_vertices_per_feature=None,
    )

    print(f"converted to polygon file {out_polygon}")
    arcpy.AddMessage(f"converted to polygon file {out_polygon}")

    arcpy.conversion.AddCADFields(
        input_table=out_polygon,
        Entities="ADD_ENTITY_PROPERTIES",
        LayerProps="NO_LAYER_PROPERTIES",
        TextProps="NO_TEXT_PROPERTIES",
        DocProps="NO_DOCUMENT_PROPERTIES",
        XDataProps="NO_XDATA_PROPERTIES",
    )

    arcpy.management.CalculateField(
        in_table=out_polygon,
        field="Layer",
        field_type="TEXT",
        expression="!GRIDCODE! / 10",
    )

    print("added real value field")
    arcpy.AddMessage("added real value field")


raster_list = arcpy.ListRasters()
print(raster_list)


def processList(workspace, raster_list):
    for raster in raster_list:
        first_letter = raster[0].lower()
        # Standardized tables- s for scour, d for depth, and v for velocity
        if first_letter == "s" or first_letter == "d":
            remap = "0 0.5 5;0.5 1.0 10;1.0 1.5 15;1.5 2.0 20;2.0 5.0 50;5.0 10000 60"
        elif first_letter == "v":
            remap = "0 1.0 10;1.0 2.0 20;2.0 3.0 30;3.0 4.0 40;4.0 5.0 50;5.0 1000 60"
        else:
            remap = "0 50 50;50 100 100;100 150 150;150 200 200;200 500 500;500 10 600"
        hecrasProcess(raster, remap)

    print("all rasters processed")
    arcpy.AddMessage("all rasters processed")


processList(workspace, raster_list)


if exportcad == "yes":

    for feature in feature_list:
        feature_short = "_".join(feature.split("_")[:-1])
        print(feature_short)
        output_path = os.path.join(cad_output, f"{feature_short}.dwg")

        first_letter = feature[0].lower()
        if first_letter == "s":
            seedFile = r"J:\\Engineering\\GIS\\seedfiles\\ScourSeed.dwg"
        elif first_letter == "v":
            seedFile = r"J:\\Engineering\\GIS\\seedfiles\\VelocitySeed.dwg"
        elif first_letter == "d":
            seedFile = r"J:\\Engineering\\GIS\\seedfiles\\DepthSeed.dwg"
        else:
            seedFile = None
        arcpy.conversion.ExportCAD(
            in_features=feature,
            Output_Type="DWG_R2018",
            Output_File=output_path,
            Ignore_FileNames="Ignore_Filenames_in_Tables",
            Append_To_Existing="Overwrite_Existing_Files",
            Seed_File=seedFile,
        )
        print(f"{feature} processed")
    print(f"exported all features to {cad_output}")
    arcpy.AddMessage(f"exported all features to {cad_output}")
else:
    print(f"finished processing")
    arcpy.AddMessage(f"finished processing")


# Extract a layer for each bin of data and make into separate shapefile
def explode_shp(feature, workspace):
    arcpy.env.workspace = workspace
    folder_path = os.path.dirname(arcpy.env.workspace)
    split_gdb = os.path.join(folder_path + "polygons_split.gdb")
    arcpy.CreateFileGDB_management(folder_path, "polygons_split.gdb")
    with arcpy.da.SearchCursor(feature, ["OID@", "Real_val"]) as cursor:
        for row in cursor:
            # Create a query for the current feature
            where_clause = f"OBJECTID = {row[0]}"

            row_clean = str(row[1]).replace(".", "_")
            print(row_clean)

            # Set the output name based on the unique field
            output_name = f"{feature}_{row_clean}"

            output_gdb = os.path.join(split_gdb, output_name)

            # Select and export the feature
            arcpy.Select_analysis(feature, output_gdb, where_clause)

            print(f"extracted {output_name} from {feature}")
    arcpy.Delete_management(feature)
    print(f"deleted {feature}")


# Run the process together
def hecrasShp(workspace):
    arcpy.env.workspace = workspace
    raster_list = arcpy.ListRasters()
    print(raster_list)
    for raster in raster_list:
        first_letter = raster[0].lower()
        # Standardized tables- s for scour, d for depth, and v for velocity
        if first_letter == "s" or first_letter == "d":
            remap = "0 0.5 5;0.5 1.0 10;1.0 1.5 15;1.5 2.0 20;2.0 5.0 50;5.0 10000 60"
        elif first_letter == "v":
            remap = "0 1.0 10;1.0 2.0 20;2.0 3.0 30;3.0 4.0 40;4.0 5.0 50;5.0 1.0 60"
        else:
            remap = "0 50 50;50 100 100;100 150 150;150 200 200;200 500 500;500 10 600"
        hecrasProcess(raster, remap)

    print("all rasters processed")
    arcpy.AddMessage("all rasters processed")

    feature_list = arcpy.ListFeatureClasses()
    # for feature in feature_list:
    #     explode_shp(feature, workspace)
    print("Extracted all features")
    arcpy.AddMessage("Extracted all features")


feature_list = arcpy.ListFeatureClasses()

# Optional step for exporting
if exportma == "yes":
    for feature in feature_list:
        arcpy.conversion.FeatureClassToShapefile(
            Input_Features=feature, Output_Folder=output_path
        )
        print(feature)
    print(f"exported all features to {output_path}")
    arcpy.AddMessage(f"exported all features to {output_path}")
else:
    print(f"finished processing")
    arcpy.AddMessage(f"finished processing")
