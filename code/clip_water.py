import geopandas as gp

New_York_State_FIPS = 36
tracts = gpd.read_file('../data/geo/2020_tracts/{}.geojson'.format(New_York_State_FIPS))
water_areas = gpd.read_file('../data/geo/water/NYC_Water.geojson')
water_clipped = gp.overlay(tracts, water_areas, how='difference')
water_clipped.to_file('clipped_tracts.geojson')
