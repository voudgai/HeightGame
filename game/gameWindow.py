import sys

from game.charactersScreen import ChooseCharacterScreen
from game.endScreen import EndScreen
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

        self.chooseCharacterScreen = None
        self.startScreen = None
        self.playScreen = None
        self.endScreen = None


    def new(self):
        pass


    def run(self):
        self.startScreen = StartScreen(self)
        self.startScreen.start()
        if self.running:
            self.chooseCharacterScreen = ChooseCharacterScreen(self)
            character = self.chooseCharacterScreen.start()
            boolViking = (character == 1)
        while self.running:
            self.playScreen = PlayScreen(self, boolViking)
            self.playScreen.start()
            if self.running:
                self.endScreen = EndScreen(self)
                self.endScreen.start()
        pygame.quit()

    def terminateGame(self):
        self.running = False
        if self.chooseCharacterScreen:
            self.chooseCharacterScreen.running = False
        if self.startScreen:
            self.startScreen.running = False
        if self.playScreen:
            self.playScreen.running = False
        if self.endScreen:
            self.endScreen.running = False

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