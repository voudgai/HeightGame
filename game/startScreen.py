import pygame

from game.buttons import Button
from game.intro import IntroVideo
from game.settings import start_screen_background_image, start_button_image, FPS


class StartScreen:
    def __init__(self, game_window):
        self.game_window = game_window
        self.display_board = game_window.display
        self.background_image = start_screen_background_image
        self.startButton = Button(self.game_window.winWidth // 2 - start_button_image.get_width() // 2, self.game_window.winHeight - 80, start_button_image)
        self.intro = IntroVideo(self.game_window.winWidth, self.game_window.winHeight, self.game_window)



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
                self.game_window.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if event.button == 1 and self.startButton.pressed(mouse_x, mouse_y):
                    self.startPressed = True