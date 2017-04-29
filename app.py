import os

import requests
import shapefile
import utm
from flask import Flask, jsonify
from skimage.io import imread

import maps
import navigation

app = Flask(__name__)
zoom = 12

api_key = os.getenv('MAPZEN_KEY')
url = 'https://tile.mapzen.com/mapzen/terrain/v1/terrarium/{}/{}/{}.png'


def get_fire_data(filename):
    return shapefile.Reader(filename)


def get_local_fires(mesh, records):
    local_fires = set()

    for fire in records:
        lat, long = fire[0:2]
        utm_pos = utm.from_latlon(lat, long)

        if mesh.within_bounds(utm_pos):
            local_fires.add(utm_pos)

    return local_fires

sf = get_fire_data('VNP14IMGTDL_NRT_Europe_24h.shp')


def download_or_cache_and_read_image(xtile, ytile, zoom):
    filename = 'cache/{}_{}_{}.png'.format(xtile, ytile, zoom)

    if not os.path.exists(filename):
        download = requests.get(
            url.format(zoom, xtile, ytile) + '?api_key=' + api_key)

        with open(filename, 'wb') as file:
            file.write(download.content)

    return imread(filename)


@app.route('/<float:slat>/<float:slong>/<float:elat>/<float:elong>')
def show_route(slat, slong, elat, elong):
    xtile, ytile = navigation.deg2num(slat, slong, zoom)

    pixels = download_or_cache_and_read_image(xtile, ytile, zoom)

    nw = utm.from_latlon(*navigation.num2deg(xtile, ytile, zoom))
    center = utm.from_latlon(*navigation.num2deg(xtile + 0.5, ytile + 0.5, zoom))

    mesh = maps.Mesh(pixels, nw, center)
    weights_height = navigation.heights_to_weights(mesh.get_heights())

    start_coord = mesh.get_pixel_coord(utm.from_latlon(slat, slong))
    end_coord = mesh.get_pixel_coord(utm.from_latlon(elat, elong))

    local_fires = get_local_fires(mesh, sf.records())

    weights_fires = navigation.fires_to_weights(mesh, local_fires)
    weights_combined = weights_height + weights_fires

    path = navigation.Pathfinder(weights_combined).find_path(start_coord,
                                                             end_coord).path()

    data = {
        'fires': [
            {
                'radius': navigation.get_fire_radius(),
                'coords': utm.to_latlon(*x)
            } for x in local_fires],
        'path': [utm.to_latlon(*mesh.get_world_coords(*segment)) for _, segment in path]
    }

    return jsonify(**data)
