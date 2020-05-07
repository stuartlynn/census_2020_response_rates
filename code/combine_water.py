import geopandas as gp
import pandas as pd 
from pathlib import Path
from zipfile import ZipFile
import matplotlib.pyplot as plt 

water_path = Path('../data/geo/water')

for area in water_path.glob('*.zip'):
    with ZipFile(area) as z:
        z.extractall(water_path)

all_water = pd.DataFrame()
for area in water_path.glob("*.shp"):
    data=  gp.read_file(area).to_crs({'init':'EPSG:4326'})
    print(data.crs)
    all_water = all_water.append(data)
all_water = gp.GeoDataFrame(all_water)
all_water.to_file(water_path / "NYC_Water.geojson", driver='GeoJSON')
all_water.plot()
plt.savefig(water_path / "NYC_Water.png")