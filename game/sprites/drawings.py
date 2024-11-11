from ..settings import *
from abc import ABC, abstractmethod

class Drawing:
    def __init__(self, x, y, image, radius = 5):
        self.x = x
        self.y = y
        self.R = radius
        self.image = image

    def draw(self, board_surface):
        board_surface.blit(self.image, (self.x, self.y))

    def overlaps(self, otherDrawing):
        # return self.image.get_rect().colliderect(otherDrawing.image.get_rect())
        dx = abs(self.x - otherDrawing.x)
        dy = abs(self.y - otherDrawing.y)
        return bool(pow(pow(dx, 2) + pow(dy, 2), 1/2) < min(self.R, otherDrawing.R))


class BlackCellBorder(Drawing):
    SIDE_UP = 1 # 0001
    SIDE_DOWN = 2 # 0010
    SIDE_LEFT = 4 # 0100
    SIDE_RIGHT = 8 # 1000

    def __init__(self, x, y, SIDE):
        #side should be example: side = SIDE_UP | SIDE_LEFT
        if not 0 <= SIDE <= 15:
            print("SIDE must be between 0 and 15, example: SIDE = SIDE_UP | SIDE_RIGHT, if you want red line which goes down and right")
            pass
        Drawing.__init__(self, x, y, black_lines_images[SIDE], 0)


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
        Drawing.__init__(self, x, y, red_lines_images[SIDE], 0)

class Ship(Drawing):
    def __init__(self, x, y):
        Drawing.__init__(self, x * TILESIZE, y * TILESIZE, ship_images[random.randint(0,5)], SHIP_HEIGHT * 1.5 // 1)

class Boat(Drawing):
    def __init__(self, x, y):
        Drawing.__init__(self, x * TILESIZE, y * TILESIZE, boat_image, BOAT_HEIGHT * 1.5 // 1)
class Flag(Drawing):
    def __init__(self, x, y):
        Drawing.__init__(self, x * TILESIZE, y * TILESIZE, flag_image, TILESIZE)

class Tree(Drawing):
    def __init__(self, x, y):
        Drawing.__init__(self, x * TILESIZE, y * TILESIZE, tree_image, TILESIZE)

class Palm(Drawing):
    def __init__(self, x, y):
        Drawing.__init__(self, x * TILESIZE, y * TILESIZE, palm_image, TILESIZE)


class Terrain(Drawing):
    def __init__(self, x, y, height):
        x, y = x * TILESIZE, y * TILESIZE
        self.height = height
        self.image = height_levels_images[getHeightLevel(self.height)]
        Drawing.__init__(self, x, y, self.image, TILESIZE)

    def __repr__(self):
        return self.height
