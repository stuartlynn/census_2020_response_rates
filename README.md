# 2020 Census Daily Self Response Rates

This repo contains the daily 2020 US census self response rate data at a census tract level. It's updated daily at around 3:30pm with new data pulled from the [census API](https://api.census.gov/data/2020/dec/responserate).

The script that does the bulk of the work is [/code/update_counts.py](update_counts.py). It performs the following steps:

- Downloads the latest data from the [census API](https://api.census.gov/data/2020/dec/responserate).
- Performs an interpolation between 2020 census tracts and 2010 census tracts.
- Adds geometry for 2020 census tracts and saves the results as GeoJSON.

The data here is primarily being collected to power the [Hester Street census map](https://nyc2020censusmap.hesterstreet.org/) but can be used by anyone who finds it useful.

### Data files 

- [/data/raw](https://github.com/stuartlynn/census_2020_response_rates/tree/master/data/raw) : Contains the raw data pulled from the API. There is a combined CSV for each day and a folder that contains a file for each state. 
- [data/counts_adjusted_for_2010](https://github.com/stuartlynn/census_2020_response_rates/tree/master/data/counts_adjusted_for_2010) Contains a csv for each day with the 2020 self response counts mapped to the 2010 census tract geometries. For more information on how this is done have a look at the [translate_to_2010_tracts.py](https://github.com/stuartlynn/census_2020_response_rates/blob/master/code/translate_to_2010_tracts.py) script.  
- [/data/geo/2020_tracts_with_counts](https://github.com/stuartlynn/census_2020_response_rates/tree/master/data/geo/2020_tracts_with_counts) Contains a GeoJSON file per state containing each tract and its most recent response rate.

### Variables 

There are 4 numbers reported by the API for the response rates 

- CRRALL : Cumulative Response Rate All - the cumulative response rate of both main forms and internet submissions.
- CRRINT : Cumulative Response Rate Internet - the cumulative response rate of internet submissions alone.
- DRRALL : Daily Response Rate All - the cumulative response rate of both main forms and internet submissions.
- DRRINT : Daily Response Rate Internet - the cumulative response rate of internet submissions alone.
