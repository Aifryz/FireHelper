import shapefile
import navigation
import maps
import utm

from skimage.io import imread


def get_fire_data(filename):
    return shapefile.Reader(filename)


starting_point = [51.693007, 8.752484]
ending_point = [51.701799, 8.733623]

pixels = imread('tile.png')
zoom = 12
xtile, ytile = navigation.deg2num(*[51.693007, 8.752484], zoom)

nw = utm.from_latlon(*navigation.num2deg(xtile, ytile, zoom))
center = utm.from_latlon(*navigation.num2deg(xtile+0.5, ytile+0.5, zoom))

mesh = maps.Mesh(pixels, nw, center)
weights_height = navigation.heights_to_weights(mesh.get_heights())

start_coord = mesh.get_pixel_coord(utm.from_latlon(*starting_point))
end_coord = mesh.get_pixel_coord(utm.from_latlon(*ending_point))

sf = get_fire_data('VNP14IMGTDL_NRT_Europe_24h.shp')
local_fires = set()

for fire in sf.records():
    lat, long = fire[0:2]
    utm_pos = utm.from_latlon(lat, long)

    if mesh.within_bounds(utm_pos):
        local_fires.add(utm_pos)

print(local_fires)

weights_fires = navigation.fires_to_weights(mesh, local_fires)
weights_combined = weights_height + weights_fires

path = navigation.Pathfinder(weights_combined).find_path(start_coord, end_coord)

with open('points.csv', 'w') as file:
    for _, segment in path.path():
        lat, lon = utm.to_latlon(*mesh.get_world_coords(*segment))
        file.write('{}, {}\n'.format(lat, lon))
        print('{}, {}'.format(lat, lon))
