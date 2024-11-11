from game.randomIslandGenerator import RandomIslandGenerator
from game.settings import *
from game.sprites.archipelago import Archipelago
from game.sprites.drawings import Drawing


class PlayScreen:
    def __init__(self, game_window):
        self.game_window = game_window # whole window on which game is being played
        self.display_board = game_window.display # display to draw on, part of the window
        self.background = Drawing(0,0,play_screen_background_image) # drawing of background image
        self.running = True
        self.buttons = [] #TODO assign each button a position # list of buttons
        self.levels = [LevelSelector()] #TODO add levels and assign each level an id, level 0 is level selector # list of levels
        self.levelSelected = 0 # 0 is for SELECTOR LEVEL, levels can be only 1 to N, N > 0
        self.numOfLevels = NUM_OF_LEVELS + 1 # + 1 for level chooser
        self.populateLevels()
        self.levelSelected = self.levels[0]

    def populateLevels(self):
        mapFromNordeus = True
        for i in range(self.numOfLevels):
            self.levels.append(Level(mapFromNordeus, i, i*25, i*25))
            mapFromNordeus = not mapFromNordeus

        print("PROMENI POCETNI SELEKTOVANI LEVEL")


    def start(self):
        while self.running:
            self.game_window.clock.tick(FPS)
            self.events()
            self.draw()
            pygame.display.flip()
        pygame.quit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.handleClick(mouse_x, mouse_y, event.button)

    def handleClick(self, mouse_x, mouse_y, mouseButton):
        if MAP_OFFSET_X <= mouse_x < LEVEL_WIDTH + MAP_OFFSET_X and MAP_OFFSET_Y <= mouse_y < LEVEL_HEIGHT + MAP_OFFSET_Y:
            self.levelSelected.handleClick(mouse_x, mouse_y, mouseButton)
            return
        print("UGRADI OBRADU KLIKA ZA PLAYSCREEN")
        # for button in self.buttons:
        #     if mouseButton == 1 and button.pressed(mouse_x, mouse_y):   #TODO
        #         self.startPressed = True
        if self.levelSelected == self.levels[0]:
            for i in range(1, self.numOfLevels + 1):
                if self.levels[i].checkActivation(mouse_x, mouse_y):
                    self.levelSelected = self.levels[i]
                    break


    def draw(self):
        self.background.draw(self.display_board)
        if self.levelSelected != self.levels[0]:
            self.levelSelected.getDrawing().draw(self.display_board.subsurface([MAP_OFFSET_X, MAP_OFFSET_Y, MAP_OFFSET_X + LEVEL_WIDTH, MAP_OFFSET_Y + LEVEL_HEIGHT]))
        else:
            for i in range(1,self.numOfLevels + 1):
                self.levels[i].drawIcon(self.display_board)


    def changeLevel(self, level):
            if not 0 <= level < len(self.levels): return False
            level.selected = self.levels[level]
            return True

class Level:
    def __init__(self, mapFromNordeus, levelId, levelIdX, levelIdY): #
        self.levelIcon = Drawing(levelIdX, levelIdY, level_icon_images[levelId])
        self.levelIconX = levelIdX # idX of icon for this levels number
        self.levelIconY = levelIdY # idY of icon for this levels number

        if mapFromNordeus: heightLevelString = requests.get(GET_REQ_LINK).text
        else: heightLevelString = RandomIslandGenerator.generate_distinct_islands_map(30, 1000, 10)
        self.archipelago = Archipelago(heightLevelString)

    def checkActivation(self, mouse_x, mouse_y):
        xLeft, xRight = (self.levelIconX), (self.levelIconX + self.levelIcon.image.get_width())
        yUp, yDown = (self.levelIconY), (self.levelIconY + self.levelIcon.image.get_height())
        if xLeft <= mouse_x <= xRight and yUp <= mouse_y <= yDown:
            return True
        return False

    def drawIcon(self,display_board):
        self.levelIcon.draw(display_board)

    def getDrawing(self):
        return self.archipelago

    def handleClick(self, mouse_x, mouse_y, mouseButton):
        mouse_x -= MAP_OFFSET_X
        mouse_y -= MAP_OFFSET_Y
        mouse_x //= TILESIZE
        mouse_y //= TILESIZE

        if mouseButton == 1: # left button click
            self.archipelago.selectIslandAt(mouse_x, mouse_y)
        else: # right button click
            self.archipelago.selectIslandAt(mouse_x, mouse_y)



class LevelSelector:
    def __init__(self):
        pass

    def handleClick(self, mouse_x, mouse_y, mouseButton):
        print("You clicked on LevelSelector...")
        pass