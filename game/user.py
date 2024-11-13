from game.settings import *
from game.sprites.drawings import Drawing


class User:
    def __init__(self):
        self.heartsPH = HeartPlaceholder(WINDOW_WIDTH - HEARTS_PLACEHOLDER_X_OFFS, WINDOW_HEIGHT - HEARTS_PLACEHOLDER_Y_OFFS )
        self.scorePH = ScorePlaceholder(0 + SCORE_PLACEHOLDER_X_OFFS, WINDOW_HEIGHT - SCORE_PLACEHOLDER_Y_OFFS, 0)

    def looseHeart(self):
        self.heartsPH.looseHeart()

    def gainHeart(self):
        self.heartsPH.gainHeart()

    def getNumOfHearts(self):
        return self.heartsPH.numOfHearts

    def incScore(self, n = 1):
        self.scorePH.incScore(n)

    def decScore(self, n = 1):
        self.scorePH.decScore(n)

    def resetScore(self):
        self.scorePH.resetScore()

    def draw(self,display_board):
        self.heartsPH.draw(display_board)
        self.scorePH.draw(display_board)

class HeartPlaceholder:
    def __init__(self,x, y):
        self.holderX = x
        self.holderY = y
        self.numOfHearts = NUM_OF_HEARTS
        self.heartPhDrawings = [Drawing(x, y ,heart_placeholder_image0), Drawing(x, y ,heart_placeholder_image1),
                              Drawing(x, y ,heart_placeholder_image2), Drawing(x, y ,heart_placeholder_image3)]

    def looseHeart(self):
        if self.numOfHearts <= 0:
            print("died before")
            return False # died
        self.numOfHearts = self.numOfHearts-1
        if self.numOfHearts <= 0:
            print("died now")
            return False # died
        return True # lived

    def gainHeart(self):
        self.numOfHearts = self.numOfHearts + 1
        return True # lived

    def draw(self, display_board):
        self.heartPhDrawings[self.numOfHearts].draw(display_board)


class ScorePlaceholder:
    def __init__(self, x, y, score):
        self.holderX = x
        self.holderY = y
        self.score = score

    def incScore(self, n = 1):
        self.score += n

    def decScore(self, n = 1):
        self.score -= n

    def resetScore(self):
        self.score = 0

    def draw(self, display_board):
        pass