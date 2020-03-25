from dotenv import load_dotenv
import os

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
print(ROOT_PATH + '/.env')
load_dotenv(ROOT_PATH+'/.env')

from make_daily_2002_tract_geojson import assign_counts 
from translate_to_2010_tracts import translate_counts_to_2010

import requests 
import pandas as pd 
import geopandas as gp 
import numpy as np
from pathlib import Path
from urllib.request import urlretrieve
import subprocess


KEY = os.getenv('APIKEY')
print("KEY ",KEY)

def fetch_daily_counts(variables,state):
    stateNo = f"0{state}" if state < 10 else  f"{state}"
    url = 'https://api.census.gov/data/2020/dec/responserate?get={cvars}&for=tract:*&in=state:{state}&in=county:*&key={key}'.format(cvars=','.join(variables + ['GEO_ID','RESP_DATE']), state=stateNo, key=KEY)
    try:
        response_rate = requests.get(url).json()
        headers = response_rate[0]
        data = pd.DataFrame(response_rate[1:], columns= headers)
        data = data.astype(dtype=dict(zip(variables, [np.float64]*len(variables))))
        return data
    except: 
        raise Exception('Failed to download')

def combine_all_states(directory,outfile):
    all_data = pd.DataFrame()
    for f in directory.glob('*.csv'):
        all_data= all_data.append(pd.read_csv(f))
    all_data.to_csv(outfile,index=False)

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
    outdir = Path(ROOT_PATH + '/../data/')
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

    print("Grabbing todays data")

    for state in range(1,57):
        try:
            data = fetch_daily_counts(variables,state)
            res_date = data.RESP_DATE.unique()[0]
            outdir = (rawdir / res_date)
            outdir.mkdir(exist_ok = True)

            print("Saving todays data")
            data.to_csv( outdir /  f"{state}.csv",index=False)
        except:
            print('Issue with state ', state)

    print("Combining with previous days data")
    combine_all_states(outdir, rawdir / f"{res_date}.csv")


    print("Grabbing all states data")
    (outdir / 'all_states').mkdir(exist_ok=True)
    urlretrieve('https://www2.census.gov/programs-surveys/decennial/2020/data/2020map/2020/decennialrr2020.csv',  outdir / f'all_states/{res_date}.csv')


    print('Updating geojson with counts')
    assign_counts()

    print('Translating counts to 2010')
    translate_counts_to_2010()


    print("Updating the git repo")
    update_git(res_date)


