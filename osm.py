from router.route import Router
from router.loadOsm import LoadOsm
import overpass


def find_path(slat, slon, elat, elon):
    """Returns lat lon path from s to e """
    data = LoadOsm("foot")
    node1 = data.findNode(slat, slon)
    node2 = data.findNode(elat, elon)
    router = Router(data)
    result, route = router.doRoute(node1, node2)
    retlist = []
    if result == 'success':
        # list the lat/long
        for i in route:
            node = data.rnodes[i]
            retlist.append((node[0], node[1]))
    return retlist


def _calc_bb(points):
    minlat = points[0][0]
    maxlat = points[0][0]
    minlon = points[0][1]
    maxlon = points[0][1]
    for pt in points:
        lat = pt[0]
        lon = pt[1]
        if lat < minlat:
            minlat = lat
        if lat > maxlat:
            maxlat = lat

        if lon < minlon:
            minlon = lon
        if lon > maxlon:
            maxlon = lon
    return (minlat, maxlat, minlon, maxlon)


def get_building_outlines(slat, slon, elat, elon):
    """Finds building outlines in 'rectangle' constructed with given bounding box
       Returns array of tuples of 4 coords (minlat,maxlat,minlon,maxlon)
       Each of those tuples represent building"""

    minlat = str(min(slat, elat))
    maxlat = str(max(slat, elat))
    minlon = str(min(slon, elon))
    maxlon = str(max(slon, elon))
    req = "way[building~'.'](" + minlat + "," + minlon + \
        "," + maxlat + "," + maxlon + roads = osm.get_roads(slat, slong, elat, elong) ");"
    api = overpass.API()
    response = api.Get(req)
    retlist = []
    for feat in response['features']:
        points = feat['geometry']['coordinates']
        retlist.append(_calc_bb(points))
    return retlist


def get_roads(slat, slon, elat, elon):
    minlat = str(min(slat, elat))
    maxlat = str(max(slat, elat))
    minlon = str(min(slon, elon))
    maxlon = str(max(slon, elon))
    req = "way[highway~'.'](" + minlat + "," + minlon + \
        "," + maxlat + "," + maxlon + ");"
    # pre sort
    roads = []
    api = overpass.API()
    response = api.Get(req)
    for feat in response['features']:
        road = {}
        if feat['geometry']['type'] != 'LineString':
            pass
        else:
            road['points'] = feat['geometry']['coordinates']
        roads.append(road)
    return roads
