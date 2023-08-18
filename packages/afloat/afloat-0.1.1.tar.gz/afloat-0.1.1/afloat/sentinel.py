import fiona
import geopandas as gpd

fiona.drvsupport.supported_drivers['kml'] = 'rw' # enable KML support which is disabled by default
fiona.drvsupport.supported_drivers['KML'] = 'rw' # enable KML support which is disabled by default

# with open(kml_file) as f:

#      doc = kmlparser.parse(f)
    
def get_kml_chunk_bounds(kml_file, chunks):
    """
    Slow function to read that big old KML file on the sentinel site and strip out boundaries. 

    KML file is in afloat-extras\data\sentinel\spatial_chunk_kml or can be found on their website. 

    Locations of interest:
        UWA 2023 SWOT moorings:
            - Middle of 51LVE
            - Western edge of 51LWE
        Scott reef:
            - 51LUE
        Broome:
            - T51KVA

    """
    print('Reading KML file.')
    my_map = gpd.read_file(kml_file, driver='KML')
    my_map
    print('....done.')

    my_latbounds = {}
    my_lonbounds = {}
    
    chunk_col = my_map.Name.values
    
    for chunk in chunks:
        ci = chunk_col == chunk
        my_chunk = my_map[ci]

        my_gemometry = my_chunk['geometry'].values[0]
        type(my_gemometry)
        dir(my_gemometry)
        my_bounds = my_gemometry.bounds
        print(my_bounds)

        my_lonbounds[chunk] = [my_bounds[0], my_bounds[2], my_bounds[2], my_bounds[0], my_bounds[0]]
        my_latbounds[chunk] = [my_bounds[1], my_bounds[1], my_bounds[3], my_bounds[3], my_bounds[1]]

    return my_lonbounds, my_latbounds