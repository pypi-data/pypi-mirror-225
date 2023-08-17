import numpy as np
import re
from shapely.geometry import Point    
import requests
import xml.etree.ElementTree as ET 

def retrieve_postcode(item:str):
    """ This function retrieves the postal code of a string by searching specifc regex in line with Dutch postal codes.
        Regex source: https://forum.mendix.com/link/questions/88423
    """
    try:
        item = item.strip()
        # find position of 4 digits
        output = re.findall(r"^[1-9][0-9]{3}\s?[a-zA-Z]{2}$", item)[-1]
        output = ''.join(output.upper().split())
        return output
    except:
        return np.nan


def retrieve_housenumber(item:str):
    """ This function retrieves the housenumber of an address (string).
        It assumes that the last number in the string is housenumber.
    """
    item = str(item).replace('.0', '').replace('nan', '')

    if item in [np.nan] or item == '':
        return np.nan
    else:
        try:
            return re.findall("\d+", item)[-1]
        except:
            return np.nan


# def retrieve_alpha_suffix(item:str):
#     """ This function returns the suffix in case all characters are alphabetical.
#     """

#     if item in [np.nan]:
#         return np.nan
#     else:
#         item = ''.join(item.upper().split())


def geocode_pdok(postal_code, house_number, suffix=False):
    """ this function geocodes a given postcode and housenumber (and suffix) into a Point(lat, lon) using PDOK API """
    # https://www.pdok.nl/introductie/-/article/pdok-locatieserver-1

    # postal_code = ''.join(postal_code.split(' '))
    postal_code = postal_code.strip()
    postal_code = postal_code[:4] + ' ' + postal_code[4:]

    house_number = str(int(house_number))

    if suffix == False or suffix in [np.nan]:
        url = "https://geodata.nationaalgeoregister.nl/locatieserver/v3/free?wt=xml&rows=1&fq=type:adres&q=postcode:{}%20AND%20huis_nlt:{}".format(postal_code, house_number)        
    else:
        hn_sx = house_number + str(suffix)
        url = "https://geodata.nationaalgeoregister.nl/locatieserver/v3/free?wt=xml&rows=1&fq=type:adres&q=postcode:{}%20AND%20huis_nlt:{}".format(postal_code, hn_sx)

    response = requests.get(url)

    try:
        # Parse the XML response
        root = ET.fromstring(response.content)
        # Find the 'doc' element
        doc = root.find(".//doc")
        # Find the 'centroide_rd' element
        centroide_rd = doc.find(".//str[@name='centroide_ll']")
        # retrieve lat and lon
        lat = float(centroide_rd.text.split(' ')[1].split(')')[0])
        lon = float(centroide_rd.text.split(' ')[0].split('(')[1])
        return (Point(lat, lon))
    
    except:
        return np.nan

