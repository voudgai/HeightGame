import sys, pygame
from game.gameWindow import Game


def main():
    game = Game()
    game.new()
    game.run()
    pygame.quit()
    sys.exit()

main()