import numpy as np


class Mesh:
    def __init__(self, pixels, nw, center):
        self.nw = nw
        self.center = center

        self.pixels = pixels

        self.matrix = np.zeros(pixels.shape[0:2])
        self._fill_matrix()

    def _fill_matrix(self):
        for x in range(self.matrix.shape[0]):
            for y in range(self.matrix.shape[1]):
                red, green, blue = self.pixels[y, x]

                self.matrix[y, x] = (red * 256 + green + blue / 256) - 32768

    def get_heights(self):
        return self.matrix

    def get_pixel_coord(self, utm_pos):
        delta_x = (self.center[0] - self.nw[0]) / (self.matrix.shape[0] / 2)
        delta_y = (self.nw[1] - self.center[1]) / (self.matrix.shape[1] / 2)

        return (utm_pos[0] - self.nw[0]) // delta_x, \
               (self.nw[1] - utm_pos[1]) // delta_y
