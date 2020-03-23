import geopandas as gp 

tracts = gp.read_file('../data/geo/tract_bas20_sr_detailed.shp').to_crs({'init':'epsg:4326'})

for state,group in tracts.groupby("STATE"): 
    group.to_file(f"../data/geo/2020_tracts/{state}.geojson", driver='GeoJSON') 
    

