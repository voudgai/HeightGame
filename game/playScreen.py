import random

import pygame.mixer

from game.characterSprite import CharacterSprite
from game.randomIslandGenerator import RandomIslandGenerator
from game.settings import *
from game.sprites.archipelago import Archipelago
from game.sprites.drawings import Drawing
from game.user import User


class PlayScreen:
    def __init__(self, game_window):
        self.game_window = game_window # whole window on which game is being played
        self.display_board = game_window.display # display to draw on, part of the window
        self.background = Drawing(0,0,play_screen_background_image) # drawing of background image
        self.running = True
        self.buttons = [] #TODO assign each button a position # list of buttons
        self.levels = [LevelSelector()] #level 0 is level selector, others are normal levels
        self.levelSelected = 0 # 0 is for SELECTOR LEVEL, levels can be only 1 to N, N > 0
        self.numOfLevels = NUM_OF_LEVELS # + 1 for level chooser
        self.populateLevels()
        self.levelSelected = self.levels[0]
        self.levelsInstrumentals = levels_instrumentals
        self.currentSound = None
        self.user = User()
        self.font = pygame.font.Font('../assets/Minecraft.ttf', 14)
        self.pressEnterToSubmit_text = self.font.render('PRESS ENTER TO SUBMIT', True,DARKGREY, LIGHTGREY)

        self.mainCharacter = CharacterSprite(80,80)

    def populateLevels(self):
        mapFromNordeus = True
        for i in range(0, self.numOfLevels):
            self.levels.append(Level(mapFromNordeus, i + 1, level_icons_coordinates[i][0], level_icons_coordinates[i][1]))
            #mapFromNordeus = not mapFromNordeus


    def start(self):
        self.updateSound()
        while self.running:
            self.game_window.clock.tick(FPS)
            self.events()
            self.draw()
            pygame.display.flip()
        pygame.quit()

    def updateSound(self):
        if self.currentSound is not None: self.currentSound.stop()
        if self.levelSelected == self.levels[0]: # this means we are on selector level
            self.currentSound = self.levelsInstrumentals[0]
        else:
            self.currentSound = self.levelsInstrumentals[random.randint(1,NUM_OF_INSTRUMENTALS - 1)]
        self.currentSound.play(1000000)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.game_window.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handleClick(pygame.mouse.get_pos(), event.button)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if self.levelSelected != self.levels[0]:
                        self.handleSubmission()
                    else:
                        self.handleClick(self.mainCharacter.getCoordinates(), 1)


    def updateMainCharacter(self):
        dx, dy = 0, 0
        keys = pygame.key.get_pressed()
        movX, movY = self.mainCharacter.movX, self.mainCharacter.movY
        if keys[pygame.K_LEFT]:
            dx -= movX
        if keys[pygame.K_RIGHT]:
            dx += movX
        if keys[pygame.K_UP]:
            dy -= movY
        if keys[pygame.K_DOWN]:
            dy += movY
        self.mainCharacter.move(dx, dy , self.display_board)


    def handleSubmission(self):
        print("Enter pressed")
        if not self.levelSelected.checkSolution():
            self.user.looseHeart()
            if self.user.getNumOfHearts() <= 0:
                self.running = False  # TODO
        else:
            self.levelSelected.setFinishedTo(True)
            self.levelSelected.resetLevel()
            self.changeLevel(0)


    def handleClick(self, mouseCoord, mouseButton):
        mouse_x, mouse_y = mouseCoord
        lvlXLeft, lvlXRight = MAP_OFFSET_X, LEVEL_WIDTH + MAP_OFFSET_X
        lvlYUp, lvlYDown = MAP_OFFSET_Y, LEVEL_HEIGHT + MAP_OFFSET_Y
        if self.levelSelected != self.levels[0] and lvlXLeft <= mouse_x < lvlXRight and lvlYUp <= mouse_y < lvlYDown:
            self.levelSelected.handleClick(mouse_x, mouse_y, mouseButton)
            return
        print("UGRADI OBRADU KLIKA ZA PLAYSCREEN") # here we can potentially check for every button is it clicked
        if self.levelSelected == self.levels[0]:
            for i in range(1, self.numOfLevels + 1):
                if self.levels[i].checkActivation(mouse_x, mouse_y):
                    self.levelSelected.resetLevel()
                    self.changeLevel(i)
                    break
        else: # we pressed return to map
            if self.levels[0].checkActivation(mouse_x, mouse_y):
                self.levelSelected.resetLevel()
                self.changeLevel(0)


    def draw(self):
        self.background.draw(self.display_board)
        if self.levelSelected != self.levels[0]:
            self.levelSelected.drawLevel(self.display_board.subsurface([MAP_OFFSET_X, MAP_OFFSET_Y, MAP_OFFSET_X + LEVEL_WIDTH, MAP_OFFSET_Y + LEVEL_HEIGHT]))
            self.levels[0].drawIcon(self.display_board)
            self.display_board.blit(self.pressEnterToSubmit_text, (WINDOW_WIDTH // 2 - self.pressEnterToSubmit_text.get_width() // 2, WINDOW_HEIGHT - MAP_OFFSET_Y // 2 - 25))
        else:
            for i in range(1,self.numOfLevels + 1):
                self.levels[i].drawIcon(self.display_board)
        self.user.draw(self.display_board)
        self.updateMainCharacter()


    def changeLevel(self, levelId):
        if not 0 <= levelId < len(self.levels): return False
        if self.levelSelected == self.levels[levelId]: return True
        self.levelSelected = self.levels[levelId]
        self.updateSound()
        return True








class Level:
    def __init__(self, mapFromNordeus, levelId, levelIdX, levelIdY): #
        self.finishedLevelIcon = Drawing(levelIdX, levelIdY, finished_level_icon_image)
        self.levelIcon = Drawing(levelIdX, levelIdY, level_icon_images[levelId])
        self.levelIconX = levelIdX # idX of icon for this levels number
        self.levelIconY = levelIdY # idY of icon for this levels number
        self.levelOver = False
        self.elevationLegendDrawing = Drawing(LEVEL_WIDTH + 10, LEVEL_HEIGHT // 2 - elevation_legend_image.get_height() // 2, elevation_legend_image)

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
        if self.levelOver:
            self.finishedLevelIcon.draw(display_board)
        else: self.levelIcon.draw(display_board)

    def drawLevel(self, display_board):
        self.archipelago.draw(display_board)
        self.elevationLegendDrawing.draw(display_board)

    def handleClick(self, mouse_x, mouse_y, mouseButton):
        mouse_x -= MAP_OFFSET_X
        mouse_y -= MAP_OFFSET_Y
        mouse_x //= TILESIZE
        mouse_y //= TILESIZE

        if mouseButton == 1: # left button click
            self.archipelago.selectIslandAt(mouse_x, mouse_y)
        else: # right button click
            self.archipelago.selectIslandAt(mouse_x, mouse_y)

    def checkSolution(self):
        if self.archipelago.isHighestSelected():
            self.levelOver = True
            return True
        return False


    def resetLevel(self):
        self.archipelago.resetArchipelago()

    def setFinishedTo(self, finished):
        self.levelOver = finished
        if finished: self.resetLevel()





class LevelSelector:
    def __init__(self):
        self.mapIcon = Drawing(WINDOW_WIDTH - BACK_TO_MAP_X_OFFS, WINDOW_HEIGHT - BACK_TO_MAP_Y_OFFS, level_icon_images[0])

    def drawIcon(self, display_board):
        self.mapIcon.draw(display_board)

    def checkActivation(self, mouse_x, mouse_y):
        xLeft, xRight = (WINDOW_WIDTH - BACK_TO_MAP_X_OFFS), (WINDOW_WIDTH - BACK_TO_MAP_X_OFFS + self.mapIcon.image.get_width())
        yUp, yDown = (WINDOW_HEIGHT - BACK_TO_MAP_Y_OFFS), (WINDOW_HEIGHT - BACK_TO_MAP_Y_OFFS + self.mapIcon.image.get_height())
        if xLeft <= mouse_x <= xRight and yUp <= mouse_y <= yDown:
            return True
        return False

    def resetLevel(self):
        pass

    def handleClick(self, mouse_x, mouse_y, mouseButton):
        print("You clicked on LevelSelector...")
        pass