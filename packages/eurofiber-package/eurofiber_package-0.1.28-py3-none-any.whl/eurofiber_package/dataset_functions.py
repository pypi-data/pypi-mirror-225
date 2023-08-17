import pandas as pd
import numpy as np
import os
import geopandas as gpd
from glob import glob

def load_most_recent_dnb():
    """ This function retrieves the most recent dnb data according to a specific folder structure.
    """
    user_name = os.getcwd().split('\\')[2]
    dnb_folder = [(item, int(''.join(item.split('\\')[-2].split()))) for item in glob(r"C:\Users\{}\Eurofiber Nederland BV\Project GLOBE - General\02 Data Lake\01 Companies\Smart Profile/*/".format(user_name), recursive=True)]
    dnb_folder.sort(key=lambda x:x[1], reverse=True)
    dnb = pd.read_csv(dnb_folder[0][0] + 'EurofibreData_NL.csv', low_memory=False)
    return dnb  


def load_ibis(specific_year=False):
    """ this function retrieves the most recent ibis file from the specific folder, unless a specifc year is provided in string format """

    user_name = os.getcwd().split('\\')[2]
    if specific_year == False:
        folder = [(item, int(item.split('_')[-1].split('.')[0])) for item in glob(r"C:\Users\{}\Eurofiber Nederland BV\My Folder - General\database\ibis/*".format(user_name))]
        folder.sort(key=lambda x:x[1], reverse=True)     

        ibis = gpd.read_file(folder[0][0])
        ibis = ibis[~ibis['geometry'].isna()]
        ibis['geometry'] = ibis['geometry'].to_crs(epsg=4326)       
        return ibis   
    else:
        try:
            ibis = gpd.read_file(r"C:\Users\{}\Eurofiber Nederland BV\My Folder - General\database\ibis/IBIS_NL_{}.zip".format(user_name, specific_year))
            ibis = ibis[~ibis['geometry'].isna()]
            ibis['geometry'] = ibis['geometry'].to_crs(epsg=4326)      
            return ibis        
        except:
            return np.nan     


def load_pc6(specific_year=False):
    """ this function retrieves the most recent pc6 file from the specific folder, unless a specifc year is provided in string format """

    user_name = os.getcwd().split('\\')[2]
    if specific_year == False:
        folder = [(item, int(item.split('-')[-1].split('.')[0])) for item in glob(r"C:\Users\{}\Eurofiber Nederland BV\My Folder - General\database\postcode\pc6/*".format(user_name))]
        folder.sort(key=lambda x:x[1], reverse=True)     

        pc_6 = gpd.read_file(folder[0][0])
        pc_6 = pc_6.dropna(subset='geometry') 
        pc_6 = pc_6.to_crs({'init': 'epsg:4326'})   
        return pc_6   
    else:
        try:
            pc_6 = gpd.read_file(r"C:\Users\{}\Eurofiber Nederland BV\My Folder - General\database\postcode\pc6/CBS-PC6-{}.zip".format(user_name, specific_year))
            pc_6 = pc_6.dropna(subset='geometry') 
            pc_6 = pc_6.to_crs({'init': 'epsg:4326'})     
            return pc_6        
        except:
            return np.nan     


def load_pc4(specific_year=False):
    """ this function retrieves the most recent pc4 file from the specific folder, unless a specifc year is provided in string format """

    user_name = os.getcwd().split('\\')[2]
    if specific_year == False:
        folder = [(item, int(item.split('-')[-1].split('.')[0])) for item in glob(r"C:\Users\{}\Eurofiber Nederland BV\My Folder - General\database\postcode\pc4/*".format(user_name))]
        folder.sort(key=lambda x:x[1], reverse=True)     

        pc_4 = gpd.read_file(folder[0][0])
        pc_4 = pc_4.dropna(subset='geometry') 
        pc_4 = pc_4.to_crs({'init': 'epsg:4326'})   
        return pc_4   
    else:
        try:
            pc_4 = gpd.read_file(r"C:\Users\{}\Eurofiber Nederland BV\My Folder - General\database\postcode\pc4/CBS-PC4-{}.zip".format(user_name, specific_year))
            pc_4 = pc_4.dropna(subset='geometry') 
            pc_4 = pc_4.to_crs({'init': 'epsg:4326'})     
            return pc_4        
        except:
            return np.nan      