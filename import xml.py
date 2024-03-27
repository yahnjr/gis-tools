import xml.etree.ElementTree as ET
import pprint
import pandas

def parse_surface_xml_to_dict(xml_file, output_dic, num):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for child in root[3][0][1][num]:
        text_obj = str(child.text)
        split_coord = text_obj.split(" ")
        output_dic["ID"].append(child.attrib["id"])
        output_dic["x-coord"].append(split_coord[0])
        output_dic["y-coord"].append(split_coord[1])
        output_dic["z-coord"].append(split_coord[2])

points_dic = {"ID": [], "x-coord": [], "y-coord": [], "z-coord": []}

parse_surface_xml_to_dict(r"J:\Engineering\GIS\Coordination\2024-02-07 Revit and CAD Files\XML Files\Existing Surface.xml", points_dic, 0)

def parse_surface_xml_to_dict_face(xml_file, output_dic, num):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for child in root[3][0][1][num]:
        text_obj1 = str(child.text)
        text_obj2 = str(child.attrib["n"])
        split_coord = text_obj1.split(" ")
        split_n = text_obj2.split(" ")
        # output_dic["ID"].append(child.attrib["i"])
        output_dic["n1"].append(split_n[0])
        output_dic["n2"].append(split_n[1])
        output_dic["n3"].append(split_n[2])
        output_dic["vertex 1"].append(split_coord[0])
        output_dic["vertex 2"].append(split_coord[1])
        output_dic["vertex 3"].append(split_coord[2])

faces_dic = {"ID": [], "n1": [], "n2": [], "n3": [], "vertex 1": [], "vertex 2": [], "vertex 3": []}

parse_surface_xml_to_dict_face(r"J:\Engineering\GIS\Coordination\2024-02-07 Revit and CAD Files\XML Files\Existing Surface.xml", faces_dic, 1)

points_df = pandas.DataFrame(points_dic)
faces_df = pandas.DataFrame(faces_dic)

print(len(faces_df))

print(points_df)
print(faces_df)

pprint.pprint(points_dic)
pprint.pprint(faces_dic)

def save_dfs_to_disk(points_df, faces_df, path):
    points_df.to_csv(f"{path}\\points_data.csv", index=False)
    faces_df.to_csv(f"{path}\\faces_data.csv", index=False)

save_dfs_to_disk(points_df, faces_df, r"J:\Engineering\GIS\Coordination\2024-02-07 Revit and CAD Files\XML Files")