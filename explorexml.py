import xml.etree.ElementTree as ET

from inspect import getmembers, isclass, isfunction

def xml_explore(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    print(root.tag)

    for child in root:
        print("--" + child.tag)
        if len(child) > 0:
            for child1 in child:
                print("----" + child1.tag)
                if len(child1) > 0:
                    for child2 in child1:
                        print("------" + child2.tag)
                        if len(child2) > 0:
                            for child3 in child2:
                                print("--------" + child3.tag)

xml_explore(file-path-here)

import xml.etree.ElementTree as ET

def attribute_explore(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    print(root[3][0][0])

attribute_explore(file-path-here)