import geopandas as gp 
import pandas as pd 
from pathlib import Path

DATA_DIR = Path('../data/')
STATE_DATA_DIR = DATA_DIR / 'raw'
GEO_DIR = DATA_DIR / 'geo' / '2020_geometries'

def load_daily_count_data():
    all_data = pd.DataFrame()
    for f in STATE_DATA_DIR.glob('*.csv'):
        print(pd.read_csv(f))
        all_data = all_data.append(pd.read_csv(f)) 
    return all_data

def assign_counts():
    counts = load_daily_count_data()
    outdir = GEO_DIR / '2020_tracts_with_counts'
    outdir.mkdir(exist_ok=True)
    for f in  (GEO_DIR / '2020_tracts' ).glob("*.geojson"):
        print("doing file ", f)
        tracts = gp.read_file(f)
        merged = pd.merge(tracts, counts, on='GEO_ID', how='inner').sort_values(by='RESP_DATE')

        columns_to_include = ['DRRINT', 'DRRALL', 'CRRINT', 'CRRALL', 'RESP_DATE']
        merged_by_day = pd.DataFrame()
        for column in columns_to_include:
            merged_by_day[column] = merged.groupby('GEO_ID')[column].apply(list)

        result = gp.GeoDataFrame(pd.merge(tracts, merged_by_day.reset_index(), on='GEO_ID'))
        with open(outdir /  f.name, 'w') as f:
            f.write(result.to_json())
        

if __name__ == '__main__':
    result = assign_counts()
