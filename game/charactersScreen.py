from game.buttons import Button
from game.videosAndAnimations import ChooseCharacterVideo


class ChooseCharacterScreen:
    def __init__(self, game_window):
        self.game_window = game_window
        self.display_board = game_window.display
        self.chooseCharacterVideo = ChooseCharacterVideo(self.game_window.winWidth, self.game_window.winHeight, self.game_window)
        self.running = True # not used

    def start(self):
        return self.chooseCharacterVideo.start()

    def terminateGame(self):
        self.game_window.terminateGame() # terminates whole game

    def terminateStartScreen(self):
        self.running = True # so the while loop will end
