class EndScreen:
    def __init__(self, gameWin):
        self.gameWindow = gameWin # set self.gameWindow.running to false if want to end the game

    def start(self):
        print("Endgame reached")

    def endGame(self):
        self.running = False
        self.gameWindow.running = False