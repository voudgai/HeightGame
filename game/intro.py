import pygame
from pyvidplayer2.video import Video
from game.buttons import Button
from game.settings import intro_video, skip_button_intro_image, FPS


class IntroVideo:
    def __init__(self, width, height, game_window):
        self.introVid = intro_video
        print("Success")
        self.introVid.resize((width, height))
        self.game_window = game_window
        self.introPlaying = False
        self.skip_button = Button(width // 1.5, height - 100,skip_button_intro_image)

    def start(self):
        self.introPlaying = True
        frameCnt = 0
        while self.game_window.running and self.introPlaying and self.introVid.active:
            self.game_window.clock.tick(FPS)
            self.introVid.draw(self.game_window.display, (0, 0))
            if frameCnt < 120: frameCnt = frameCnt + 1
            else: self.skip_button.draw(self.game_window.display)
            self.events()
            pygame.display.update()
        self.introVid.close()


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_window.running = False;
                self.introPlaying = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if event.button == 1 and self.skip_button.pressed(mouse_x, mouse_y):
                    self.introPlaying = False


IntroVideo(0,0,0)