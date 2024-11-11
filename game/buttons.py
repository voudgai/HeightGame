from game.sprites.drawings import Drawing


class Button(Drawing):
    def __init__(self, x, y, image):
        Drawing.__init__(self, x, y, image)
        self.width = image.get_width()
        self.height = image.get_height()

    def pressed(self, x, y):
        if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
            return True
        return False

