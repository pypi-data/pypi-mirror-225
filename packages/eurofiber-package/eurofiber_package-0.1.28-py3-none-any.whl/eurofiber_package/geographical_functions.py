import numpy as np
import pandas as pd
import geopandas as gpd    
from shapely.geometry import Point    
from shapely import geometry
import requests
import xml.etree.ElementTree as ET 


def distance_to_line(lat:float, lon:float, line) -> float:
    """ This function calculates the perpendicular disance of a point to a line (KMZ file) """
    
    # calculate distance; https://stackoverflow.com/questions/69851086/calculate-distance-between-linestring-and-point-in-meters
    gdfl = gpd.GeoDataFrame(geometry=[line], crs="EPSG:4326")
    gdfp = gpd.GeoDataFrame(geometry=[Point(lon, lat)], crs="EPSG:4326")
    utm = gdfl.estimate_utm_crs()
    distance = gdfl.to_crs(utm).distance(gdfp.to_crs(utm)).iloc[0]

    return distance


def distance_to_network(lat:float, lon:float, network_kmz) -> float:
    """ This function calculates the perpendicular disance of a point to the network that is created by concatenating individual lines (KMZ file) """

    all_network = network_kmz['geometry_object'].tolist()
    multi_line = geometry.MultiLineString(all_network)

    # calculate distance; https://stackoverflow.com/questions/69851086/calculate-distance-between-linestring-and-point-in-meters
    gdfl = gpd.GeoDataFrame(geometry=[multi_line], crs="EPSG:4326")
    gdfp = gpd.GeoDataFrame(geometry=[Point(lon, lat)], crs="EPSG:4326")
    utm = gdfl.estimate_utm_crs()
    distance = gdfl.to_crs(utm).distance(gdfp.to_crs(utm)).iloc[0]

    return distance


def check_if_in_business_parc_optimized(lat:float, lon:float, province:str, ibis:gpd.GeoDataFrame, increase_search_space=False) -> object:
    """ This function checks if a certain Point(lat, lon) is in a business parc polygon taking into account the province for optimization. 
        Input is the latitude, longitude, and province of a point together with the entire ibis dataset. Output is the RIN_NUMBER in case of intersection. 
        Possibility to increase search space when province is not matching.
    """

    # as a business parc can belong to multiple provinces due to merging, this is a required step
    try:
        province = province.split(',')
        province = [item.upper().strip() for item in province]
    except:
        province = [province]

    # remove records without polygons 
    ibis = ibis.dropna(subset='geometry').reset_index(drop=True)

    # IMPORTANT: change coordinate reference sytem (https://stackoverflow.com/questions/47203938/convert-the-coordinates-of-a-shapefile-in-geopandas)
    ibis['geometry'] = ibis['geometry'].to_crs(epsg=4326)

    # clean ibis provinces
    ibis['PROV_NAMEN'] = ibis['PROV_NAMEN'].apply(lambda x: x.upper().strip() if x not in [np.nan] else np.nan)

    try:
        # make a specific subset of the ibis data based on the province    
        ibis_select = ibis[ibis['PROV_NAMEN'].isin(province)].reset_index(drop=True)
        # make a specific subset of the ibis data without the province for search space increase if required
        ibis_non_select = ibis[~(ibis['PROV_NAMEN'].isin(province))].reset_index(drop=True)
        # helper variable
        temp_val = 0

        # iterate over selected business parc and return rin number if intersect
        for index, bp in ibis_select.iterrows():
            if bp['geometry'].contains(Point(lon, lat)) == True: # contains function works only properly with (lon, lat)
                temp_val = 1
                return bp['RIN_NUMMER']

        # increase search space when no intersection on province selection
        if increase_search_space == True:
            if temp_val == 0:
                # iterate over selected business parc and return rin number if intersect
                for index, bp in ibis_non_select.iterrows():
                    if bp['geometry'].contains(Point(lon, lat)) == True: # contains function works only properly with (lon, lat)
                        return bp['RIN_NUMMER']

    except:
        # in case no province use the entire search space
        for index, bp in ibis.iterrows():
            if bp['geometry'].contains(Point(lon, lat)) == True: # contains function works only properly with (lon, lat)
                return bp['RIN_NUMMER']


def check_if_in_business_parc(lat:float, lon:float, ibis:gpd.GeoDataFrame):
    """ This function checks if a certain Point(lat, lon) is in a business parc polygon """

    # from shapely.geometry import Point 

    # remove records without polygons 
    ibis = ibis.dropna(subset='geometry').reset_index(drop=True)

    # change coordinate reference sytem (https://stackoverflow.com/questions/47203938/convert-the-coordinates-of-a-shapefile-in-geopandas)
    ibis['geometry'] = ibis['geometry'].to_crs(epsg=4326)

    # iterate over business parcs and return rin_number
    for index, bp in ibis.iterrows():
        if bp['geometry'].contains(Point(lon, lat)) == True: # contains function works only properly with (lon, lat)
            return bp['RIN_NUMMER']


def within_range(lat:float, lon:float, kmz, buffer_range:float) -> bool:
    # kmz = gpd.GeoDataFrame(kmz, crs='epsg:4326')
    kmz = kmz.to_crs('EPSG:28992') # or 3763 https://epsg.io/?q=netherlands
    kmz['geometry'] = kmz['geometry'].buffer(buffer_range)
    kmz = kmz.to_crs('EPSG:4326')

    for item in kmz['geometry']:
        if item.contains(Point(lon, lat)) == True: # contains function works only properly with (lon, lat)
            return True


def point_in_polygon(lat:float, lon:float, polygon) -> bool:
    """ This function determines whether a point falls within a specific polygon. """
    try:
        if polygon.contains(Point(lon, lat)) == True: # contains function works only properly with (lon, lat)
            return True
        else:
            return False
    except:
        return np.nan
    

def intersect_ibis_pc4(ibis, pc4):
    """ this function retrieves the intersecting pc4 for given ibis. input is an ibis dataframe and a pc4 dataframe an the output will be a list of intersecting pc4 """
    ibis_pc4 = []
    for index, row in ibis.iterrows():
        for i, r in pc4.iterrows():
            if row['geometry'].intersects(r['geometry']):
                ibis_pc4.append(r['PC4'])   
    return list(set(ibis_pc4))    


def intersect_ibis_pc6(ibis, pc6):
    """ this function retrieves the intersecting pc6 for given ibis. input is an ibis dataframe and a pc6 dataframe an the output will be a list of intersecting pc6 """    
    ibis_pc6 = []
    for index, row in ibis.iterrows():
        for i, r in pc6.iterrows():
            if row['geometry'].intersects(r['geometry']):
                ibis_pc6.append(r['PC6'])   
    return list(set(ibis_pc6))    


def intersect_ibis_pc6_optimized(ibis, pc4, pc6):
    """ this function retrieves the intersecting pc6 for given ibis in an optimized way. input is an ibis dataframe, a pc4 dataframe and a pc6 dataframe an the output will be a list of intersecting pc6 """        
    
    # first search pc4 to reduce search space
    ibis_pc4 = []
    for index, row in ibis.iterrows():
        for i, r in pc4.iterrows():
            if row['geometry'].intersects(r['geometry']):
                ibis_pc4.append(r['PC4']) 
    pc6['PC4'] = pc6['PC6'].apply(lambda x: int(str(x)[:4]))                 
    pc6_relevant = pc6[pc6['PC4'].isin(ibis_pc4)]

    # based on pc4 search pc6
    ibis_pc6 = []
    for index, row in ibis.iterrows():
        for i, r in pc6_relevant.iterrows():
            if row['geometry'].intersects(r['geometry']):
                ibis_pc6.append(r['PC6'])   
    return list(set(ibis_pc6))


def find_valid_address_pc6_dnb(pc6, dnb):
    """ this function attempts to find a valid address within a given pc6 and dnb"""

    # clean pc6
    dnb['PC6'] = dnb['Postal Code'].apply(lambda x: ''.join(str(x).split()))

    # subset
    # output = dnb[(dnb['PC6']==pc6) & (dnb['House number suffix'].isna())].sort_values('House number')
    output = dnb[(dnb['PC6']==pc6) & (dnb['House number suffix'].isna()) & ~(dnb['House number'].isna())]

    try:
        # return
        postcode = output['PC6'].iloc[0]
        housenumber = output['House number'].iloc[0]
        return (postcode, str(housenumber).replace('.0', ''))
    except:
        return (np.nan, np.nan)
    

def buffer_point(lat, lon, buffer_range):
    """ this function creates a buffer of x meters around a given point (lat, lon) with the correct CRS"""
    location = pd.DataFrame({'geometry':[Point(lat, lon)]})
    location = gpd.GeoDataFrame(location, crs='epsg:4326')
    location = location.to_crs('EPSG:28992') # or 3763 https://epsg.io/?q=netherlands
    location['geometry'] = location['geometry'].buffer(buffer_range) # NOTE buffer refers to range in meters
    location = location.to_crs('EPSG:4326')
    return location.iloc[0]['geometry']


def intersect_ibis_provinces(ibis, provinces):
    """ this function retrieves the intersecting provinces for given ibis. input is a single ibis geometry and a province dataframe an the output will be a list of intersecting provinces """
    ibis_provinces = []
    for i, r in provinces.iterrows():
        if ibis.intersects(r['geometry']):
            ibis_provinces.append(r['Provincienaam'])   
    return list(set(ibis_provinces))    
