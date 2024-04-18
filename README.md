1. Check AGOL use- Used as a script in ArcGIS Pro, can check online to see if a layer is being referenced in any web maps in case you want to delete it without breaking anything. Just need the ID from the item details page. 

2. Explore xml- Given the path to an XML file, this simple script will give you the structure of the file, with one extra "-" indicating one level deeper. It goes around 5 levels deep.

3. Folder structure- Another simple script to explore a directory and tell you all the folders and subfolders. 

4. Import xml- Allows you to turn a simple xml into panda db's and CSV files, although it will need to be tweaked based on your XML's file structure. This particular file was a LandXML TIN surface file. 

5. Add Scale boxes- Adds a 2 dimensional scale to your map layout in ArcGIS Pro. Instead of a scale bar, adds three squares of customizable size to the map and labels their size in acres. REQUIRES: At least one map frame,
   one existing text box and one existing graphical rectangle already existing on the layout. These will not be altered but will be cloned and used to create the scale. 

6. Split CAD- **intended to be used as a script for an ArcGIS toolbox** takes a CAD .dwg file and an output geodatabase directory. Will convert your CAD file into individual layers, organized into thematic categories based on their geometries. NOTE: CAD file results will maintain whatever projection you defined for them, so they should be georeferenced prior to running the tool.

7. tidycensus.R- simple R script for getting started with tidycensus. 

8. BLI_automate- **WORK IN PROGRESS** An attempt to automate a basic Buildable Lands Inventory. Currently works with a parcel file and a study area/city limits polygon file. Is not functional as a script currently. Only works in Oregon due to LiDAR data at the moment, but LiDAR could be made into a parameter in the future. 

9. PPGIS_app.html- basic app for accepting comments from the public. Just need to add in a publicly editable point file with attributes "comment" and "topic" and a polygon city limits layer if you need. Don't forget to change the center of focus and zoom level to fit your needs.

10. PPGIS_automod.py- a basic script to check your public comments layer for bad words. It will read comments and send you an alert with how many bad comments need to be reviewed (no message if it is 0) and create an Excel file with the bad comments highlighted in red. 