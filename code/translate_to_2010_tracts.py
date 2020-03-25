import pandas as pd 
import geopandas as gp
from pathlib import Path
import os
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))


def translate_counts_to_2010():
    relationship = pd.read_csv(ROOT_PATH + '/../data/geo/rr_tract_rel.txt', dtype={'TRACTCE10':str, "TRACTCE20":str, 'COUNTYFP10':str, 'COUNTYFP20':str, 'GEOID10' :str, 'GEOID20': str}) 

    outpath = Path(ROOT_PATH + '/../data/counts_adjusted_for_2010/')
    outpath.mkdir(exist_ok=True)
    data_path = Path(ROOT_PATH+ '/../data/raw')
    for f in data_path.glob("*.csv"):
        print('translating ', f, ' to census tracts')
        rates = pd.read_csv(f)

        merged = (pd.merge(
            relationship, 
            rates.assign(
                GEO_ID_SHORT=rates.GEO_ID.str.replace('1400000US','')
            ), 
            left_on="GEOID20", 
            right_on='GEO_ID_SHORT',
            how='inner'))

        counts_for_2010 = (merged.assign(
            CRRALL = merged.CRRALL * merged.HUCURPCT_T10.div(100.0), 
            CRRINT= merged.CRRINT * merged.HUCURPCT_T10.div(100.0),
            DRRALL =  merged.DRRALL* merged.HUCURPCT_T10.div(100.0),
            DRRINT = merged.DRRINT * merged.HUCURPCT_T10.div(100.0)
           ).groupby('GEOID10')
                           .sum()[['CRRALL', 'CRRINT', 'DRRALL','DRRINT']]
           ) 
        counts_for_2010 = counts_for_2010.reset_index().rename(columns={"GEOID10":"GEOID"})
        counts_for_2010.to_csv(outpath / f.name,index=False)

if __name__ == '__main__':
    translate_counts_to_2010()
