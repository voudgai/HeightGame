from ..settings import *
from abc import ABC, abstractmethod

class Drawing:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def draw(self, board_surface):
        board_surface.blit(self.image, (self.x, self.y))

class ColouredCellBorder(Drawing, ABC):
    def __init__(self, x, y, image):
        pass

class RedCellBorder(Drawing):
    SIDE_UP = 1 # 0001
    SIDE_DOWN = 2 # 0010
    SIDE_LEFT = 4 # 0100
    SIDE_RIGHT = 8 # 1000

    def __init__(self, x, y, SIDE):
        #side should be example: side = SIDE_UP | SIDE_LEFT
        if not 0 <= SIDE <= 15:
            print("SIDE must be between 0 and 15, example: SIDE = SIDE_UP | SIDE_RIGHT, if you want red line which goes down and right")
            pass
        Drawing.__init__(self, x, y, red_lines_images[SIDE])

class Ship(Drawing):
    def __init__(self, x, y):
        Drawing.__init__(self, x * TILESIZE, y * TILESIZE, ship_image)

class Boat(Drawing):
    def __init__(self, x, y):
        Drawing.__init__(self, x * TILESIZE, y * TILESIZE, boat_image)
class Flag(Drawing):
    def __init__(self, x, y):
        Drawing.__init__(self, x * TILESIZE, y * TILESIZE, flag_image)

class Tree(Drawing):
    def __init__(self, x, y):
        Drawing.__init__(self, x * TILESIZE, y * TILESIZE, tree_image)

class Palm(Drawing):
    def __init__(self, x, y):
        Drawing.__init__(self, x * TILESIZE, y * TILESIZE, palm_image)


class Terrain(Drawing):
    def __init__(self, x, y, height):
        x, y = x * TILESIZE, y * TILESIZE
        self.height = height
        self.image = height_levels_images[getHeightLevel(self.height)]
        Drawing.__init__(self, x, y, self.image)

    def __repr__(self):
        return self.height
