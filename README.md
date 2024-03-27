1. Check AGOL use- Used as a script in ArcGIS Pro, can check online to see if a layer is being referenced in any web maps in case you want to delete it without breaking anything. Just need the ID from the item details page. 

2. Explore xml- Given the path to an XML file, this simple script will give you the structure of the file, with one extra "-" indicating one level deeper. It goes around 5 levels deep.

4. Folder structure- Another simple script to explore a directory and tell you all the folders and subfolders. 

5. Import xml- Allows you to turn a simple xml into panda db's and CSV files, although it will need to be tweaked based on your XML's file structure. This particular file was a LandXML TIN surface file. 

6. Add Scale boxes- Adds a 2 dimensional scale to your map layout in ArcGIS Pro. Instead of a scale bar, adds three squares of customizable size to the map and labels their size in acres. REQUIRES: At least one map frame,
   one existing text box and one existing graphical rectangle already existing on the layout. These will not be altered but will be cloned and used to create the scale. 
