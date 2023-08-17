import pandas as pd
import numpy as np

def convert_to_cocon_template(dataset, streetname, housenumber, suffix, postcode, town):
    output = dataset.copy()
    output['Naam'] = output[postcode].fillna('').astype(str) + ' ' + output[housenumber].fillna('').astype(str) + ' ' + output[suffix].fillna('').astype(str)     
    output['Naam'] = output['Naam'].apply(lambda x: x.replace(' ', '').replace('nan', '').replace('.0', ''))
    output['Huisnummer'] = output[housenumber].fillna('').astype(str) + ' ' + output[suffix].fillna('').astype(str)     
    output['Huisnummer'] = output['Huisnummer'].apply(lambda x: x.replace(' ', '').replace('nan', '').replace('.0', ''))
    output['Postcode'] = output[postcode].apply(lambda x: ''.join(x.split(' ')) if x not in [np.nan] else np.nan)

    output = output.rename(columns={streetname:'Straat', town:'Plaats'})
    output = output[['Naam', 'Straat', 'Huisnummer', 'Postcode', 'Plaats']]
    output = output.drop_duplicates(subset='Naam')

    return output