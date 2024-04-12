# Imports
import os
import arcpy
import arcgis

# set environments
arcpy.env.overwriteOutput = True
arcpy.env.addOutputsToMap = True
input_parcels = arcpy.GetParameterAsText(0)
study_area = arcpy.GetParameterAsText(1)
# output_path = os.path.join(*input_parcels.split("\\")[:-1])
# arcpy.env.workspace = output_path
out_gdb = os.path.dirname(input_parcels)
arcpy.env.workspace = out_gdb
# gis = GIS("home")

temp_path = r"C:\Temp"
temp_gdb = r"C:\Temp\Default.gdb"

arcpy.AddMessage("Workspace is " + out_gdb + ", " + arcpy.env.workspace)

# Prepare Parcel layer

# Select parcels by city limits
parcel_file = input_parcels.split("\\")[-1] + "_Clip"
selected_parcels = arcpy.SelectLayerByLocation_management(
    in_layer=[input_parcels],
    overlap_type="INTERSECT",
    select_features=study_area,
)

describe_area = arcpy.Describe(study_area)

Coordinate_system = describe_area.spatialReference

# export selected parcels
export_parcel = arcpy.ExportFeatures_conversion(selected_parcels, parcel_file)

arcpy.AddMessage("Clipped file created.")
print("Clipped file created.")

# Add fields to parcel file


# For inline variable substitution, parameters passed as a String are evaluated using locals(), globals() and isinstance(). To override, substitute values directly.
def AddFieldstoParcelFile(input_layer):  # Add Fields to Parcel File
    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True

    arcpy.ImportToolbox(
        r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Data Management Tools.tbx"
    )

    # Process: Add Fields (multiple) (Add Fields (multiple)) (management)
    arcpy.management.AddFields(
        in_table=parcel_file,
        field_description=[
            ["ID_3J", "LONG", "", "", "", ""],
            ["Acres_3J", "DOUBLE", "", "", "", ""],
            ["Multiple", "SHORT", "", "", "", ""],
            ["NumbLots", "SHORT", "", "", "", ""],
            ["ID2_3J", "LONG", "", "", "", ""],
            ["Acres2_3J", "DOUBLE", "", "", "", ""],
            ["Split", "SHORT", "", "144", "", ""],
            ["ID3_3J", "LONG", "", "144", "", ""],
            ["Acres3_3J", "DOUBLE", "", "", "", ""],
            ["RMVland_3J", "LONG", "", "", "", ""],
            ["RMVimpr_3J", "LONG", "", "", "", ""],
            ["Bldg_land", "DOUBLE", "", "", "", ""],
            ["Res_land", "SHORT", "", "", "", ""],
            ["Emp_land", "SHORT", "", "", "", ""],
            ["Res_vac", "SHORT", "", "", "", ""],
            ["Emp_vac", "SHORT", "", "", "", ""],
            ["Developed", "LONG", "", "", "", ""],
            ["cnstr_res", "DOUBLE", "", "", "", ""],
            ["cnstr_com", "DOUBLE", "", "", "", ""],
            ["cnstr_ind", "DOUBLE", "", "", "", ""],
            ["lsw_res", "DOUBLE", "", "", "", ""],
            ["lsw_com", "DOUBLE", "", "", "", ""],
            ["lsw_ind", "LONG", "", "", "", ""],
            ["LSW_acres", "DOUBLE", "", "", "", ""],
            ["EX_LU", "TEXT", "", "12", "", ""],
            ["LotSize", "SHORT", "", "", "", ""],
            ["Zone_3J", "TEXT", "", "144", "", ""],
            ["CompPlan_3J", "TEXT", "", "144", "", ""],
            ["PV_acres", "DOUBLE", "", "", "", ""],
            ["Cnstr_acres", "DOUBLE", "", "", "", ""],
            ["BLI_acres", "DOUBLE", "", "", "", ""],
            ["Type", "TEXT", "", "144", "", ""],
            ["Review", "TEXT", "", "1500", "", ""],
            ["DEV_TYPE", "TEXT", "", "144", "", ""],
            ["VAC_ACRE", "DOUBLE", "", "", "", ""],
            ["DEVD_ACRE", "DOUBLE", "", "", "", ""],
            ["CONSTRAINED_ACRE", "DOUBLE", "", "", "", ""],
            ["EX_POP", "DOUBLE", "", "", "", ""],
            ["EX_SC_CHLDRN", "DOUBLE", "", "", "", ""],
            ["EX_HH", "DOUBLE", "", "", "", ""],
            ["EX_HU", "DOUBLE", "", "", "", ""],
            ["EX_MF", "DOUBLE", "", "", "", ""],
            ["EX_TH", "DOUBLE", "", "", "", ""],
            ["EX_SF", "DOUBLE", "", "", "", ""],
            ["EX_SF_SM", "DOUBLE", "", "", "", ""],
            ["EX_SF_MD", "DOUBLE", "", "", "", ""],
            ["EX_SF_LRG", "DOUBLE", "", "", "", ""],
            ["EX_MH", "DOUBLE", "", "", "", ""],
            ["EX_HOTEL_RM", "DOUBLE", "", "", "", ""],
            ["EX_EMP", "DOUBLE", "", "", "", ""],
            ["EX_RET", "DOUBLE", "", "", "", ""],
            ["EX_OFF", "DOUBLE", "", "", "", ""],
            ["EX_IND", "DOUBLE", "", "", "", ""],
            ["EX_PUB", "DOUBLE", "", "", "", ""],
            ["EX_EDU", "DOUBLE", "", "", "", ""],
            ["EX_HOTEL", "DOUBLE", "", "", "", ""],
            ["EX_UTIL", "DOUBLE", "", "", "", ""],
            ["EX_PRKG", "DOUBLE", "", "", "", ""],
            ["EX_AG", "DOUBLE", "", "", "", ""],
            ["ORIG_FID", "DOUBLE", "", "", "", ""],
        ],
    )[0]

    arcpy.AddMessage("ET fields created")
    print("ET fields created")

    # Process: Calculate Field (Calculate Field) (management)
    Taxlots_select_clip_explode_2_ = arcpy.management.CalculateField(
        in_table=parcel_file, field="ID_3J", expression="!OBJECTID!"
    )[0]

    arcpy.AddMessage("ID's transferred")
    print("ID's transferred")

    # Process: Calculate Geometry Attributes (Calculate Geometry Attributes) (management)
    Taxlots_select_clip_explode_4_ = arcpy.management.CalculateGeometryAttributes(
        in_features=parcel_file,
        geometry_property=[["Acres_3J", "AREA"]],
        area_unit="ACRES_US",
        coordinate_system=Coordinate_system,
    )[0]

    arcpy.AddMessage("Acreage calculated")
    print("Acreage calculated")

    blank_string = " "
    # Process: Calculate Fields (multiple) (Calculate Fields (multiple)) (management)
    Studyareas_4_ = arcpy.management.CalculateFields(
        in_table=parcel_file,
        expression_type="PYTHON3",
        fields=[
            ["Multiple", 0, ""],
            ["NumbLots", 0, ""],
            ["Split", 0, ""],
            ["RMVland_3J", 0, ""],
            ["RMVimpr_3J", 0, ""],
            ["Bldg_land", 0, ""],
            ["Res_land", 0, ""],
            ["Emp_land", 0, ""],
            ["Res_vac", 0, ""],
            ["Emp_vac", 0, ""],
            ["Developed", 0, ""],
            ["cnstr_res", 0, ""],
            ["cnstr_com", 0, ""],
            ["cnstr_ind", 0, ""],
            ["lsw_res", 0, ""],
            ["lsw_com", 0, ""],
            ["lsw_ind", 0, ""],
            ["LSW_acres", 0, ""],
            # ["EX_LU", blank_string, ""],
            ["LotSize", 0, ""],
            # ["Zone_3J", blank_string, ""],
            # ["CompPlan_3J", blank_string, ""],
            ["PV_acres", 0, ""],
            ["Cnstr_acres", 0, ""],
            ["BLI_acres", 0, ""],
            # ["Type", blank_string, ""],
            # ["Review", blank_string, ""],
            # ["DEV_TYPE", blank_string, ""],
            ["VAC_ACRE", 0, ""],
            ["DEVD_ACRE", 0, ""],
            ["CONSTRAINED_ACRE", 0, ""],
            ["EX_POP", 0, ""],
            ["EX_SC_CHLDRN", 0, ""],
            ["EX_HH", 0, ""],
            ["EX_HU", 0, ""],
            ["EX_MF", 0, ""],
            ["EX_TH", 0, ""],
            ["EX_SF", 0, ""],
            ["EX_SF_SM", 0, ""],
            ["EX_SF_MD", 0, ""],
            ["EX_SF_LRG", 0, ""],
            ["EX_MH", 0, ""],
            ["EX_HOTEL_RM", 0, ""],
            ["EX_EMP", 0, ""],
            ["EX_RET", 0, ""],
            ["EX_OFF", 0, ""],
            ["EX_IND", 0, ""],
            ["EX_PUB", 0, ""],
            ["EX_EDU", 0, ""],
            ["EX_HOTEL", 0, ""],
            ["EX_UTIL", 0, ""],
            ["EX_PRKG", 0, ""],
            ["EX_AG", 0, ""],
            ["ORIG_FID", 0, ""],
        ],
    )[0]


AddFieldstoParcelFile(parcel_file)

arcpy.AddMessage("Envision Tomorrow fields finished.")
print("ET fields finished. ")

# Split multipart features and record split
split_parcels = parcel_file + "_split"


def split_multipart(input_layer):

    arcpy.management.MultipartToSinglepart(input_layer, split_parcels)

    arcpy.management.CalculateGeometryAttributes(
        in_features=split_parcels,
        geometry_property=[["Acres2_3J", "AREA"]],
        area_unit="ACRES_US",
        coordinate_system=Coordinate_system,
    )
    print("calculated new area")

    split_expression = "split_calc(!Acres_3J!, !Acres2_3J!)"

    codeblock = """def split_calc(field1, field2):
        if field1 == field2:
            return 0
        else:
            return 1"""

    arcpy.CalculateField_management(
        split_parcels, "Split", split_expression, "PYTHON3", codeblock
    )

    arcpy.management.CalculateField(
        in_table=split_parcels, field="ID2_3J", expression="!OBJECTID!"
    )


split_multipart(parcel_file)

print("Parcels split.")

# Create slope layer from DOGAMI data


def DOGAMISlopeclippercent(workspace, study_area):  # DOGAMI Slope clip percent
    slope_url = "https://gis.dogami.oregon.gov/arcgis/rest/services/lidar/DIGITAL_TERRAIN_SLOPE_MODEL_MOSAIC/ImageServer"

    arcpy.env.extent = study_area
    arcpy.env.overwriteOutput = True
    Coordinate_System = arcpy.SpatialReference(6557)

    p = arcpy.mp.ArcGISProject("CURRENT")
    m = p.listMaps()[1]
    m.addDataFromPath(
        "https://gis.dogami.oregon.gov/arcgis/rest/services/lidar/DIGITAL_TERRAIN_SLOPE_MODEL_MOSAIC/ImageServer"
    )

    arcpy.MakeImageServerLayer_management(slope_url, "slope_raster", parcel_file)

    slope_raster = "slope_raster"

    # To allow overwriting outputs change overwriteOutput option to True.

    # # Check out any necessary licenses.
    # arcpy.CheckOutExtension("3D")
    # arcpy.CheckOutExtension("spatial")

    if arcpy.Exists(r"C:\Temp\slope_rec"):
        arcpy.Delete_management(r"C:\Temp\slope_rec")

    # Process: Reclassify (2) (Reclassify) (sa)
    out_raster = os.path.join(temp_path, "slope_rec")
    arcpy.AddMessage("Beginning Reclassification")
    print("Beginning Reclassification")
    with arcpy.EnvManager(outputCoordinateSystem=Coordinate_System):
        reclassify_out = arcpy.ddd.Reclassify(
            in_raster=slope_raster,
            reclass_field="Value",
            remap="0 5.740000 0;5.740000 14.040000 10;14.040000 89.306504 25",
            out_raster=out_raster,
            missing_values="DATA",
        )
    arcpy.AddMessage("Converting to polygons")
    print("Converting to polygons")
    # Process: Raster to Polygon (Raster to Polygon) (conversion)
    slopes_all = os.path.join(temp_gdb, "slopes_all")
    with arcpy.EnvManager(outputMFlag="Disabled", outputZFlag="Disabled"):
        arcpy.conversion.RasterToPolygon(
            in_raster=reclassify_out,
            out_polygon_features=slopes_all,
            simplify="NO_SIMPLIFY",
            create_multipart_features="MULTIPLE_OUTER_PART",
        )
    print("extracting meaningful slopes")
    print(slopes_all)
    updated_layer, Count = arcpy.SelectLayerByAttribute_management(
        slopes_all, where_clause="gridcode = 10 Or gridcode = 25"
    )

    arcpy.CopyFeatures_management("slopes_all_Layer1", "Slopes_BLI")

    Slope_BLI = "Slopes_BLI"

    arcpy.AddField_management(
        in_table=Slope_BLI, field_name="Slopes_3J", field_type="SHORT"
    )
    arcpy.CalculateField_management(
        in_table=Slope_BLI,
        field="Slopes_3J",
        expression="!gridcode!",
        expression_type="PYTHON3",
    )


DOGAMISlopeclippercent(
    arcpy.env.workspace,
    parcel_file,
)

arcpy.AddMessage("Slope BLI polygon layer created")
print("Slope Layer created")

# Create national flood zone and floodway layer

flood_layer_url = "https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/USA_Flood_Hazard_Reduced_Set_gdb/FeatureServer/0"

# temp_path = r"C:\Temp\default.gdb"
# flood_zone = os.path.join(temp_path, "Flood_Zone")
# floodway = os.path.join(temp_path, "Floodway")


def prepare_flood(flood_layer_url):
    arcpy.env.extent = parcel_file

    arcpy.MakeFeatureLayer_management(flood_layer_url, "flood_layer")

    flood_layer_clip = os.path.join(temp_gdb, "flood_layer_clip")
    arcpy.analysis.Clip("flood_layer", parcel_file, flood_layer_clip)

    updated_layer, Count = arcpy.SelectLayerByAttribute_management(
        flood_layer_clip,
        where_clause="ZONE_SUBTY = '0.2 Percent Annual Chance Flood Hazard'",
    )

    arcpy.CopyFeatures_management("flood_layer_clip_Layer1", "Flood_Zone")
    # arcpy.ExportFeatures_conversion(updated_layer, "Flood_Zone")
    arcpy.AddField_management(
        in_table="Flood_Zone", field_name="FloodZ_3J", field_type="SHORT"
    )
    arcpy.CalculateField_management(
        in_table="Flood_Zone",
        field="FloodZ_3J",
        expression=1,
        expression_type="PYTHON3",
    )

    print("Flood_Zone created")

    updated_layer1, Count1 = arcpy.SelectLayerByAttribute_management(
        flood_layer_clip, where_clause="ZONE_SUBTY = 'Regulatory Floodway'"
    )

    arcpy.ExportFeatures_conversion(updated_layer1, "Floodway")
    arcpy.CopyFeatures_management("flood_layer_clip_Layer2", "Floodway")

    arcpy.AddField_management(
        in_table="Floodway", field_name="FloodW_3J", field_type="SHORT"
    )
    arcpy.CalculateField_management(
        in_table="Floodway", field="FloodW_3J", expression=1, expression_type="PYTHON3"
    )


prepare_flood(flood_layer_url)

print("Flood layers created")

# Create national wetlands layer

wetlands_layer_url = "https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/USA_Wetlands/FeatureServer/0"


def prepare_wetlands(wetlands_layer_url):
    arcpy.env.extent = parcel_file

    arcpy.MakeFeatureLayer_management(wetlands_layer_url, "national_wetlands")

    NWI_layer_clip = os.path.join(temp_gdb, "NWI_layer_clip")
    arcpy.analysis.Clip("national_wetlands", parcel_file, NWI_layer_clip)

    updated_layer, Count = arcpy.SelectLayerByAttribute_management(
        NWI_layer_clip, where_clause="SYSTEM = 'P'"
    )
    print("wetlands selected")

    arcpy.CopyFeatures_management("NWI_layer_clip_Layer1", "National_Wetlands")

    #     with arcpy.EnvManager(extent=parcel_file):
    #         arcpy.ExportFeatures_conversion(updated_layer, "National_Wetlands")

    #     updated_layer, Count = arcpy.SelectLayerByLocation_management(
    #         in_layer=[wetland_type],
    #         overlap_type="INTERSECT",
    #         select_features=parcel_file,)

    arcpy.AddField_management(
        in_table="National_Wetlands", field_name="Natwet_3J", field_type="SHORT"
    )
    arcpy.CalculateField_management(
        in_table="National_Wetlands",
        field="Natwet_3J",
        expression=1,
        expression_type="PYTHON3",
    )

    print("National Wetlands Layer created")


prepare_wetlands(wetlands_layer_url)


# Merge constraints into new "Constraints" layer


def Union(slope, flood, floodway, NWI):  # Union
    arcpy.analysis.Union(
        in_features=[[slope, ""], [flood, ""], [floodway, ""], [NWI, ""]],
        out_feature_class="Constraints",
    )


constraints_layer = "Constraints"

Union("Slopes_BLI", "Flood_Zone", "Floodway", "National_Wetlands")

arcpy.AddMessage("Constraints layer created")
print("Constraints layer created")


arcpy.AddField_management(
    in_table="Constraints", field_name="Constrainment_3J", field_type="FLOAT"
)

constraints_layer = "Constraints"

constrain_expression = "constrain(!Natwet_3J!, !FloodZ_3J!)"

codeblock = """def constrain(field1, field2):
    if field1 == 25 or field2 == 1:
        return 1
    else:
        return 0.5"""

arcpy.CalculateField_management(
    in_table=constraints_layer,
    field="Constrainment_3J",
    expression=constrain_expression,
    expression_type="PYTHON3",
    code_block=codeblock,
)

# Intersect constraints and parcels to determine constrained acres, dissolve and create a join table

arcpy.env.overwriteOutput = True

constrained_intersect = os.path.join(temp_gdb, "constrained_intersect")

arcpy.Intersect_analysis([split_parcels, "Constraints"], constrained_intersect)

# acre_field = split_parcels + "_Cnstr_acres"

arcpy.management.CalculateGeometryAttributes(
    in_features=constrained_intersect,
    geometry_property=[["Cnstr_acres", "AREA"]],
    area_unit="ACRES_US",
    coordinate_system=Coordinate_system,
)

arcpy.CalculateField_management(
    in_table=constrained_intersect,
    field="Cnstr_acres",
    expression="!Cnstr_acres! * !Constrainment_3J!",
    expression_type="PYTHON3",
)

print("Constrained acres calculated.")
print("Dissolving constraints...")

constrained_dissolve = os.path.join(temp_gdb, "constrained_dissolve")
# id2_field = split_parcels + "_ID2_3J"
# statistics_field = split_parcels + "_Cnstr_acres"

arcpy.management.Dissolve(
    in_features=constrained_intersect,
    out_feature_class=constrained_dissolve,
    dissolve_field="ID2_3J",
    statistics_fields="Cnstr_acres SUM",
    multi_part="MULTI_PART",
    unsplit_lines="DISSOLVE_LINES",
    concatenation_separator="",
)

print("Dissolve created, joining data...")

arcpy.management.AddSpatialJoin(
    target_features=split_parcels,
    join_features=constrained_dissolve,
    join_operation="JOIN_ONE_TO_ONE",
    join_type="KEEP_ALL",
    match_option="INTERSECT",
    search_radius=None,
    distance_field_name="",
    permanent_join="NO_PERMANENT_FIELDS",
    match_fields=None,
)

print("Calculating fields...")

arcpy.management.CalculateFields(
    split_parcels,
    "PYTHON3",
    [
        ["Cnstr_acres", "!SUM_Cnstr_acres!"],
        ["BLI_acres", "!Acres2_3J! - !Cnstr_acres!"],
        ["PV_acres", "!BLI_Acres!/!Acres2_3J!"],
    ],
)

constrain_percent = "constrain_percent(!PV_acres!, !BLI_acres!)"

codeblock = """def constrain_percent(field1, field2):
    if field1 < 0.15 or field2 < 0.001:
        return 0
    else:
        return field2"""

arcpy.CalculateField_management(
    in_table=split_parcels,
    field="BLI_acres",
    expression=constrain_percent,
    expression_type="PYTHON3",
    code_block=codeblock,
)


print("Cleaning up and removing join...")

arcpy.management.RemoveJoin(split_parcels)

print("Constraints calculated")

# arcpy.CalculateField_management(in_table=constrained_intersect, field="Cnstr_acres", expression)

# Clean up unecessary layers

walk = arcpy.da.Walk(r"C:\Temp\Default.gdb", datatype="FeatureClass")

featlist = []

for dirpath, dirnames, filenames in walk:
    for filename in filenames:
        featlist.append(os.path.join(dirpath, filename))


for feat in featlist:
    arcpy.Delete_management(feat)
    print(f"Deleted intermediate layer {feat}")
