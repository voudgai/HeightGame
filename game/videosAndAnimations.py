import pygame
from pyvidplayer2.video import Video
from game.buttons import Button
from game.settings import intro_video, skip_button_intro_image, FPS, loose_heart_video, chest_found_video


class IntroVideo:
    def __init__(self, width, height, game_window):
        self.introVid = intro_video
        print("made intro video")
        self.introVid.resize((width, height))
        self.game_window = game_window
        self.introPlaying = False
        self.skip_button = Button(width // 1.5, height - 100,skip_button_intro_image)

    def start(self):
        print("play intro video")
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
                self.game_window.terminateGame()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if event.button == 1 and self.skip_button.pressed(mouse_x, mouse_y):
                    self.introPlaying = False





class LooseHeartVideo:
    def __init__(self, width, height, game_window):
        self.width, self.height = width, height
        self.looseHeartVid = loose_heart_video
        print("made heart lost video")
        self.looseHeartVid.resize((width, height))
        self.game_window = game_window
        self.videoPlaying = False

    def start(self):
        self.videoPlaying = True
        print("play heart lost video")
        while self.game_window.running and self.videoPlaying and self.looseHeartVid.active:
            self.game_window.clock.tick(FPS)
            self.looseHeartVid.draw(self.game_window.display, (self.game_window.display.get_width() // 2 - self.width // 2, self.game_window.display.get_height() // 2 - self.height // 2))
            self.events()
            pygame.display.update()
        self.looseHeartVid.restart()


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_window.terminateGame()




class FoundChestVideo:
    def __init__(self, width, height, game_window):
        self.width, self.height = width, height
        self.chestFoundVid = chest_found_video
        print("made chest found video")
        self.chestFoundVid.resize((width, height))
        self.game_window = game_window
        self.videoPlaying = False

    def start(self):
        self.videoPlaying = True
        print("play chest found video")
        while self.game_window.running and self.videoPlaying and self.chestFoundVid.active:
            self.game_window.clock.tick(FPS)
            self.chestFoundVid.draw(self.game_window.display, (self.game_window.display.get_width() // 2 - self.width // 2, self.game_window.display.get_height() // 2 - self.height // 2))
            self.events()
            pygame.display.update()
        self.chestFoundVid.restart()


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_window.terminateGame()