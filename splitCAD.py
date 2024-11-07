import arcpy
import os

workspace = arcpy.GetParameterAsText(0)
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True
input_cad = arcpy.GetParameterAsText(1)


# create normalized name convention for later loop function, no spaces or dashes
cad_split = input_cad.split("\\")
cad_name = cad_split[-1].split(".")[0]
cad_nospace = cad_name.replace(" ", "")
cad_nodash = cad_nospace.replace("-", "_")
cad_gdb = "a" + cad_nodash + "_CADGDB"
cad_fc = cad_nodash + "_CAD_fc"

arcpy.conversion.CADToGeodatabase(input_cad, workspace, cad_gdb, 1000)

# Create list of feature classes inside CAD for loop
CAD_classes = arcpy.ListFeatureClasses(
    feature_dataset=cad_gdb
)  # output: ['Annotation', 'Point', 'Polyline', 'Polygon', 'TextPoint']

for CAD in CAD_classes:
    CAD_class = cad_nodash + "_" + CAD
    arcpy.management.CreateFeatureDataset(workspace, CAD_class)
    print(CAD + " feature set created")

CAD_desc = arcpy.Describe(os.path.join(workspace, cad_gdb, CAD_classes[1]))
CAD_sr = CAD_desc.spatialReference
# spatial_ref = arcpy.SpatialReference()

print(f"Spatial reference acquired: {CAD_sr}")

for CAD in CAD_classes:
    # Get a list of unique values in the "Layer" field
    unique_types = set(row[0] for row in arcpy.da.SearchCursor(CAD, "Layer"))

    # Create a new layer for each unique layer/type
    for types in unique_types:
        query_expression = f"Layer = '{types}'"

        # Create a new layer with the selected features
        output_layer = f"{types}_{CAD}"
        arcpy.MakeFeatureLayer_management(CAD, output_layer, query_expression)
        output_path = workspace + "\\" + cad_nodash + "_" + CAD
        final_out = arcpy.FeatureClassToGeodatabase_conversion(
            output_layer, output_path
        )
        arcpy.management.DefineProjection(final_out, CAD_sr)

    print(f"{CAD} layers created successfully!")

print(f"{cad_nodash} file processed successfully.")
