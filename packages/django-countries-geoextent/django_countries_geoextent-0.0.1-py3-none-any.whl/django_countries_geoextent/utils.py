import json

import geopandas as gpd

"""
Function for generating a json file will all GADM 4.1 countries, with their geographic extents

To regenerate, a json file must be created that contains the latest data. Here's
how to do that:

1. Visit https://gadm.org/download_world.html
2. Download the GADM data for the entire world as a geopackage. Choose the option to download as separate layers. 
3. Once the geopackage has been downloaded, you can use this function
4. The geopackage_path parameter is the absolute path to where you saved the GADM data. The out_file argument is 
the absolute path to where the country json data will be saved
"""


def read_gadm_countries(geopackage_path, out_file):
    gdf = gpd.read_file(geopackage_path, layer="ADM_0")

    countries = {}

    for index, row in gdf.iterrows():
        countries[row["GID_0"]] = {
            "name": row["COUNTRY"],
            "bbox": row["geometry"].bounds
        }

    with open(out_file, "w") as outfile:
        json.dump(countries, outfile)
