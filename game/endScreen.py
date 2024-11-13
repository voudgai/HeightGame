import pygame

from game.buttons import Button
from game.settings import FPS, end_screen_instrumental, restart_button_image, quit_button_image, end_screen_background
from game.sprites.drawings import Drawing


class EndScreen:
    def __init__(self, gameWin):
        self.gameWindow = gameWin
        self.running = True
        self.music = end_screen_instrumental
        self.backgroundImage = Drawing(0,0,end_screen_background)
        self.restartButton = Button(self.gameWindow.display.get_width() // 2 - restart_button_image.get_width() // 2, self.gameWindow.display.get_height() // 2 - restart_button_image.get_height() // 2 - 75, restart_button_image)
        self.quitButton = Button(self.gameWindow.display.get_width() // 2 - quit_button_image.get_width() // 2, self.gameWindow.display.get_height() // 2 - quit_button_image.get_height() // 2 + 75, quit_button_image)

    def terminateGame(self):
        self.music.stop()
        self.gameWindow.terminateGame()

    def terminateEndScreen(self):
        self.music.stop()
        self.running = False

    def activateEndScreen(self):
        self.running = True


    def start(self):
        print("Endgame reached")
        self.activateEndScreen()
        self.updateSound()
        while self.running:
            self.gameWindow.clock.tick(FPS)
            self.events()
            self.draw()
            pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.terminateGame()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handleClick(pygame.mouse.get_pos(), event.button)


    def updateSound(self):
        self.music.play(1000000000)

    def handleClick(self, coordinates, leftButtonClick):
        x, y = coordinates
        if self.restartButton.pressed(x,y):
            self.terminateEndScreen()
        if self.quitButton.pressed(x,y):
            self.terminateGame()

    def draw(self):
        self.backgroundImage.draw(self.gameWindow.display)
        self.restartButton.draw(self.gameWindow.display)
        self.quitButton.draw(self.gameWindow.display)

