from arcgis.gis import GIS
import pandas as pd

# Log in to portal; 'home' uses the credentials used to login within Pro
gis = GIS('home')

# Set up input parameters to use in the GUI
find_id = arcpy.GetParameterAsText(0)
search_type = arcpy.GetParameterAsText(1)

find_url = gis.content.get(find_id).url

if search_type == 'Web Map':
    arcpy.AddMessage("Searching for Web Maps. This could take a few minutes...")
    # Pull list of all web maps in portal
    webmaps = gis.content.search('', item_type='Web Map', max_items=-1)

    # Return subset of map IDs which contain the service URL we're looking for
    matches = [m.id for m in webmaps if str(m.get_data()).find(find_url) > -1]

    # Create empty list to populate with results
    map_list = []

    # Check each web map for matches
    for w in webmaps:

        try:
            # Get the JSON as a string
            wdata2 = str(w.get_data())

            criteria = [
                wdata2.find(find_url) > -1,  # Check if URL is directly referenced
                any([wdata2.find(i) > -1 for i in matches])  # Check if any matching maps are in app
            ]

            # If layer is referenced directly or indirectly, append map to list
            if any(criteria):
                map_list.append(w)

        # Some apps don't have data, so we'll just skip them if they throw a TypeError
        except:
            continue

    output = pd.DataFrame([{'title': m.title, 'id': m.id, 'type': m.type} for m in map_list])
    arcpy.AddMessage(f"OUTPUT TABLE: \n \n {output}")

if search_type == 'Web Application':
    arcpy.AddMessage("Searching for Web Applications. This could take a few minutes...")
    # Pull list of all web apps in portal
    webapps = gis.content.search('', item_type='Application', max_items=-1)

    # Create empty list to populate with results
    app_list = []

    # Return subset of map IDs which contain the service URL we're looking for
    matches = [a.id for a in webapps if str(a.get_data()).find(find_url) > -1]

    # Check each web app for matches
    for w in webapps:

        try:
            # Get the JSON as a string
            wdata = str(w.get_data())

            criteria = [
                wdata.find(find_url) > -1, # Check if URL is directly referenced
                any([wdata.find(i) > -1 for i in matches]) # Check if any matching maps are in app
            ]

            # If layer is referenced directly or indirectly, append app to list
            if any(criteria):
                app_list.append(w)

        # Some apps don't have data, so we'll just skip them if they throw a TypeError
        except:
            continue

    output = pd.DataFrame([{'title':a.title, 'id':a.id, 'type':a.type} for a in app_list])
    arcpy.AddMessage(f"OUTPUT TABLE:  \n \n {output}")