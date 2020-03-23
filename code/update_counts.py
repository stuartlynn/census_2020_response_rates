import requests 
import pandas as pd 
import geopandas as gp 
import numpy as np
from pathlib import Path
import subprocess



def fetch_daily_counts(variables):
    url = 'https://api.census.gov/data/2020/dec/responserate?get={cvars}&for=tract:*&in=state:36&in=county:*'.format(cvars=','.join(variables + ['GEO_ID','RESP_DATE']))
    response_rate = requests.get(url).json()
    headers = response_rate[0]
    data = pd.DataFrame(response_rate[1:], columns= headers)
    data = data.astype(dtype=dict(zip(variables, [np.float64]*len(variables))))
    return data


def combine_all(directory,out_dir):
    all_data = pd.DataFrame()
    for f in directory.glob('*.csv'):
        all_data= all_data.append(pd.read_csv(f))
    all_data.to_csv(outdir / 'response_rates.csv', index=False)

def update_git(last_update):
    subprocess.run(['git','pull'])
    subprocess.run(['git','add', '../data/'])
    subprocess.run(['git','commit', '-m',f'"adding data for {last_update}"'])
    subprocess.run(['git','push'])


if __name__ == "__main__":
    outdir = Path('../data/')
    outdir.mkdir(exist_ok=True)
    rawdir = outdir / 'raw'

    variables =[
        'CAVG',
        'CINTMAX',
        'CINTMED',
        'CINTMIN',
        'CMAX',
        'CMED',
        'CMIN',
        'CRRALL',
        'CRRINT',
        'DAVG',
        'DINTAVG',
        'DINTMAX',
        'DINTMED',
        'DINTMIN',
        'DMAX',
        'DMED',
        'DMIN',
        'DRRALL',
        'DRRINT',
    ] 

    data = fetch_daily_counts(variables)
    res_date = data.RESP_DATE.unique()[0]
    data.to_csv(rawdir / f"{res_date}.csv",index=False)
    combine_all(rawdir, outdir)
    update_git(res_date)


