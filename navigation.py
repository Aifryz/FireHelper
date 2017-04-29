import math
import numpy as np


class Pathfinder:
    def __init__(self, weights):
        self.weights = weights


def heights_to_weights(matrix):
    """Returns the differences of heights (that is - the gradient)."""
    return np.gradient(matrix)


def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom

    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(
        math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)

    return xtile, ytile


def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom

    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)

    return lat_deg, lon_deg
