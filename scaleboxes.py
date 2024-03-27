import arcpy
import math

# Set the map document
aprx = arcpy.mp.ArcGISProject("CURRENT")
# Accessing the layout
layout = aprx.listLayouts(arcpy.GetParameterAsText(0))[0]  # Assuming there's only one layout named "Name"
# Accessing the map frame within the layout
map_frame = layout.listElements("MAPFRAME_ELEMENT", "Map Frame")[0]

def scale_boxes(value1, value2, value3):
      # Assuming the map frame is named "Acreage_Map_Frame"
    # Getting the current scale
    current_scale = map_frame.camera.scale
    
    #Derives size in inches from desired acres
    factor1 = math.sqrt(int(value1) * 43560) * 12
    factor2 = math.sqrt(int(value2) * 43560) * 12
    factor3 = math.sqrt(int(value3) * 43560) * 12
#     five_acre_side = 5600.285707/current_scale
#     twenty_acre_side = 12522.6195343/current_scale
#     fifty_acre_side = 17709.6/current_scale
    five_acre_side = factor1/current_scale
    twenty_acre_side = factor2/current_scale
    fifty_acre_side = factor3/current_scale

    print("The current map scale is 1 to " + str(current_scale))

    print("A "+ str(value1) + " acre square would be " + str(five_acre_side) + " inches")

    print("A "+ str(value2) + " acre square would be " + str(twenty_acre_side) + " inches")

    print("A "+ str(value3) + " acre square would be " + str(fifty_acre_side) + " inches")
    
    #Clone a graphic element rectangle twice and apply the dimensions for the size
    element = [elm for elm in layout.listElements("GRAPHIC_ELEMENT")][0]
    
    clone = element.clone()
    
    # Change the dimensions
    new_width = five_acre_side
    new_height = five_acre_side

    clone.elementWidth = new_width
    clone.elementHeight = new_height
    
    # Set new name for the clone
    clone.name = "box1"

    clone2 = clone.clone()
    
    # Change the dimensions of the clone
    width_25 = twenty_acre_side
    height_25 = twenty_acre_side

    clone2.elementWidth = width_25
    clone2.elementHeight = height_25
    
    clone3 = clone2.clone()

    # Set new name for the clone
    clone3.name = "box3"

    # Change the dimensions of the clone
    # Change the dimensions of the clone
    width_50 = fifty_acre_side
    height_50 = fifty_acre_side

    clone3.elementWidth = width_50
    clone3.elementHeight = height_50

    # Position both squares in the bottom left of the layout
    clone.elementPositionX = 0  
    clone.elementPositionY = 0
    
    clone2.elementPositionX = 0  
    clone2.elementPositionY = 0
    
    clone3.elementPositionX = 0  
    clone3.elementPositionY = 0
    
    print("Scale boxes created")
    
    #Repeat process for text labels
    
    # Specify the original text element
    text_element = [elm for elm in layout.listElements("TEXT_ELEMENT")][0]
    
    # Clone the text element
    text_clone = text_element.clone()

    # Set new name for the clone
    text_clone.name = "text2"
    text_clone.textHorizontalAlignment = "Right"
    text_clone.text = str(value2) + " Acres"

    # Position the right side of the text at the specified x-coordinate
    text_clone.elementPositionX = twenty_acre_side - text_clone.elementWidth
    
    # Clone the text element
    text_clone2 = text_clone.clone()

    # Set new name for the clone
    text_clone2.name = "text3"
    text_clone2.textHorizontalAlignment = "Right"
    text_clone2.text = str(value3) + " Acres"

    # Position the right side of the text at the specified x-coordinate
    text_clone2.elementPositionX = fifty_acre_side - text_clone2.elementWidth
    
    # Clone the text element
    text_clone3 = text_clone2.clone()

    # Set new name for the clone
    text_clone3.name = "text"
    text_clone3.textHorizontalAlignment = "Right"
    text_clone3.text = str(value1) + " Acres"

    # Position the right side of the text at the specified x-coordinate
    text_clone3.elementPositionX = five_acre_side - text_clone3.elementWidth
    
    text_clone3.elementPositionY = 0 + five_acre_side
    text_clone.elementPositionY = 0 + twenty_acre_side
    text_clone2.elementPositionY = 0 + fifty_acre_side

    print("Text labels created")

scale_boxes(arcpy.GetParameterAsText(1), arcpy.GetParameterAsText(2), arcpy.GetParameterAsText(3))