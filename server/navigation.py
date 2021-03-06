import math
import osm
import numpy as np
from simpleai.search import SearchProblem, astar
from bresenham import bresenham
import utm


class ShortestPathProblem(SearchProblem):
    def __init__(self, matrix, start, goal):
        self.matrix = matrix
        self.start = start
        self.goal = goal

        super(ShortestPathProblem, self).__init__(initial_state=self.start)

    def is_goal(self, state):
        return state == self.goal

    def result(self, state, action):
        return tuple(sum(x) for x in zip(state, action))

    def actions(self, state):
        actions = []

        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and y == 0:
                    continue

                if 0 > state[0] + x >= self.matrix.shape[0]:
                    continue

                if 0 > state[1] + y >= self.matrix.shape[1]:
                    continue

                actions.append((x, y))

        return actions

    def cost(self, state, action, state2):
        return self.matrix[int(state2[1]), int(state2[0])]

    def heuristic(self, state):
        x, y = state
        goal_x, goal_y = self.goal

        return math.sqrt((goal_x - x) ** 2 + (goal_y - y) ** 2)


class Pathfinder:
    def __init__(self, weights):
        self.weights = weights

    def find_path(self, start, end):
        problem = ShortestPathProblem(self.weights, start, end)
        result = astar(problem, graph_search=True)

        return result


def heights_to_weights(matrix):
    """
    Returns the differences of heights (that is - the magnitude of gradient). 
    """
    gradient = np.gradient(matrix)

    return np.sqrt(gradient[0] ** 2 + gradient[1] ** 2)


def get_fire_radius():
    """Returns the fire radius in metres"""
    return 720 / 2


def fires_to_weights(mesh, fires):
    """
    Returns the weights matrix with fire point weights increased 
    :param mesh: Input mesh
    :param fires: List of fire coordinates in UTM
    :return: New weights matrix
    """
    fire_weight = 50
    matrix = np.zeros(mesh.matrix.shape)

    for fire in fires:
        x, y = (int(x) for x in mesh.get_pixel_coord(fire))
        delta = int(mesh.metres_to_pixels(get_fire_radius() * 2))

        matrix[y - delta:y + delta, x - delta:x + delta] += fire_weight

    return matrix


def _add_segment(mesh, matrix, seg, weigh):

    points = bresenham(int(seg[0][0]), int(
        seg[0][1]), int(seg[1][0]), int(seg[1][1]))
    for pt in points:
        matrix[pt[1], pt[0]] = min(matrix[pt[1], pt[0]], weigh)


def _get_road_weigh(typ):
    weighs = {'motorway': 0,
              'trunk': -0.5,
              'primary': -1.5,
              'secondary': -2,
              'tertriary': -2,
              'unclassified': -2,
              'residential': -1,
              'service': -1,}
    return weighs.get(typ, -1)


def roads_to_weights(mesh, roads):

    matrix = np.zeros(mesh.matrix.shape)

    for road in roads:
        points = road['points']
        p0 = points[0]
        beg = mesh.get_pixel_coord(utm.from_latlon(p0[1], p0[0]))

        for i in range(1, len(points)):
            end = mesh.get_pixel_coord(
                utm.from_latlon(points[i][1], points[i][0]))
            _add_segment(mesh, matrix, (beg, end), _get_road_weigh(road['type']))
            beg = mesh.get_pixel_coord(
                utm.from_latlon(points[i][1], points[i][0]))
    mat = np.zeros(mesh.matrix.shape)
    mat.fill(4)
    weighs = np.clip(matrix, -2, 0)
    return mat + weighs


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
