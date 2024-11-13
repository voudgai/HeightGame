import pygame

from game.buttons import Button
from game.videosAndAnimations import IntroVideo
from game.settings import start_screen_background_image, start_button_image, FPS, play_button_image


class StartScreen:
    def __init__(self, game_window):
        self.game_window = game_window
        self.display_board = game_window.display
        self.background_image = start_screen_background_image
        self.startButton = Button(self.game_window.winWidth // 2 - play_button_image.get_width() // 2, self.game_window.winHeight - 80, play_button_image)
        self.intro = IntroVideo(self.game_window.winWidth, self.game_window.winHeight, self.game_window)
        self.startPressed = False



    def start(self):
        self.startPressed = False
        while not self.startPressed and self.game_window.running:
            self.game_window.clock.tick(FPS)
            self.display_board.blit(self.background_image,(0,0))
            self.startButton.draw(self.game_window.display)
            self.events()
            pygame.display.flip()
        self.display_board.blit(self.background_image, (0, 0))
        pygame.display.flip()
        self.intro.start()


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.terminateGame()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.checkSkipButton(event)

    def terminateGame(self):
        self.game_window.terminateGame() # terminates whole game

    def terminateStartScreen(self):
        self.startPressed = True # so the while loop will end

    def checkSkipButton(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.button == 1 and self.startButton.pressed(mouse_x, mouse_y):
            self.terminateStartScreen()