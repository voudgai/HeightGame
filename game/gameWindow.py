import sys

from game.playScreen import PlayScreen
from game.randomIslandGenerator import RandomIslandGenerator
from game.sprites.archipelago import *

from game.startScreen import StartScreen


class Game:
    def __init__(self):
        pygame.init()  # Initialize pygame
        self.rows = ROWS
        self.cols = COLS
        self.winWidth = WINDOW_WIDTH
        self.winHeight = WINDOW_HEIGHT
        self.running = True

        self.display = pygame.display.set_mode((self.winWidth, self.winHeight))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.startScreen = StartScreen(self)
        self.playScreen = PlayScreen(self)


    def new(self):
        pass


    def run(self):
        if self.running: self.startScreen.start()
        if self.running: self.playScreen.start()
        pygame.quit()


    def update(self):
        pass


    def draw(self):
        pass


def main():
    game = Game()

    game.new()
    game.run()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()