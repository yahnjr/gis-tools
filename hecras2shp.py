import arcpy
from arcpy.sa import *
import os

arcpy.env.overwriteOutput = True


# Process into polygon layers from continuous raster layer
def hecrasProcess(raster_name, remap):
    out_mult = raster_name + "_mult"

    print(f"raster multiplication complete {out_mult}")

    raster = arcpy.Raster(raster_name)

    # Multiply due to decimal values
    Raster_Calculator = out_mult
    _Name_mult = raster * 100000
    _Name_mult.save(Raster_Calculator)

    print(f"Finished {out_mult}")

    out_reclass = raster_name + "_reclass"
    # Reclassify because no continous value polygons
    arcpy.ddd.Reclassify(
        in_raster=out_mult,
        reclass_field="VALUE",
        remap=remap,
        out_raster=out_reclass,
        missing_values="DATA",
    )

    print("f{out_raster} reclassified")

    out_polygon = raster_name + "_polygons"
    # Convert to polygons by bin and convert back to decimal
    arcpy.conversion.RasterToPolygon(
        in_raster=out_reclass,
        out_polygon_features=out_polygon,
        simplify="NO_SIMPLIFY",
        raster_field="Value",
        create_multipart_features="MULTIPLE_OUTER_PART",
        max_vertices_per_feature=None,
    )

    print(f"converted to polygon file {out_polygon}")

    arcpy.management.CalculateField(
        in_table=out_polygon,
        field="Real_val",
        field_type="DOUBLE",
        expression="!GRIDCODE! / 100000",
    )

    print("added real value field")


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
            remap = "0 50000 50000;50000 100000 100000;100000 150000 150000;150000 200000 200000;200000 500000 500000;500000 10000000 600000"
        elif first_letter == "v":
            remap = "0 100000 100000;100000 200000 200000;200000 300000 300000;300000 400000 400000;400000 500000 500000;500000 100000000 60000000"
        else:
            remap = "0 50000 50000;50000 100000 100000;100000 150000 150000;150000 200000 200000;200000 500000 500000;500000 10000000 600000"
        hecrasProcess(raster, remap)

    print("all rasters processed")

    feature_list = arcpy.ListFeatureClasses()
    for feature in feature_list:
        explode_shp(feature, workspace)
    print("Extracted all features")


hecrasShp(path\to\workspace)

arcpy.env.workspace = path\to\workspace
output_path = path\to\output

feature_list = arcpy.ListFeatureClasses()

# Optional step for exporting
for feature in feature_list:
    arcpy.conversion.FeatureClassToShapefile(
        Input_Features=feature, Output_Folder=output_path
    )
    print(feature)
print(f"exported all features to {output_path}")
