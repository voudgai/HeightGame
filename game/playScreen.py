import random

import pygame.mixer

from game.characterSprite import CharacterSprite
from game.randomIslandGenerator import RandomIslandGenerator
from game.settings import *
from game.sprites.archipelago import Archipelago
from game.sprites.drawings import Drawing
from game.user import User
from game.videosAndAnimations import FoundChestVideo


class PlayScreen:
    def __init__(self, game_window, boolViking):
        self.gameWindow = game_window # whole window on which game is being played
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
        self.mainCharacter = CharacterSprite(viking_character_spawn_X, viking_character_spawn_Y, boolViking)
        self.foundChestVideo = FoundChestVideo(LEVEL_WIDTH // 2, LEVEL_HEIGHT // 2, self.gameWindow)
        self.characterOnIsland = False # used for checking if main character is currently on any island


    def terminateGame(self):
        if self.currentSound is not None: self.currentSound.stop()
        self.gameWindow.terminateGame()

    def terminatePlayScreen(self):
        if self.currentSound is not None: self.currentSound.stop()
        self.running = False

    def activatePlayScreen(self):
        self.running = True


    def populateLevels(self):
        mapFromNordeus = True
        for i in range(0, self.numOfLevels):
            #for the last level we want it to be random, so we are sending True as i == self.numOfLevels, and each time it starts it will form other archipelago
            boolRandom = (i == self.numOfLevels - 1)
            self.levels.append(Level(mapFromNordeus, i + 1, level_icons_coordinates[i][0], level_icons_coordinates[i][1], boolRandom))
            #mapFromNordeus = not mapFromNordeus


    def start(self):
        self.activatePlayScreen()
        self.updateSound()
        while self.running:
            self.gameWindow.clock.tick(FPS)
            self.events()
            self.draw()
            pygame.display.flip()


    def updateSound(self):
        if self.currentSound is not None: self.currentSound.stop()
        if self.levelSelected == self.levels[0]: # this means we are on selector level
            self.currentSound = self.levelsInstrumentals[0]
        else:
            self.currentSound = self.levelsInstrumentals[random.randint(1,NUM_OF_INSTRUMENTALS - 1)]
        self.currentSound.play(1000000)
        self.currentSound.set_volume(0.4)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.terminateGame()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handleClick(pygame.mouse.get_pos(), event.button)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    self.handleEnter()


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
        if self.levelSelected != self.levels[0]:
            xCh, yCh = self.mainCharacter.getCoordinates()
            if self.levelSelected.handleClick(xCh, yCh, 1):
                self.characterOnIsland = True
            else:
                self.characterOnIsland = False

    def handleEnter(self):
        xCh, yCh = self.mainCharacter.getCoordinates()
        if self.levelSelected != self.levels[0]:
            # we pressed enter on level to submit or to return to map
            if self.levels[0].checkActivation(xCh, yCh):
                self.changeLevel(0)
            else:
                self.handleSubmissionByCharacter()
            return
        # we are on level selector since we would return if we were on some other level
        for i in range(1, self.numOfLevels + 1):
            # for each level, check if we clicked on its icon for activation
            if self.levels[i].checkActivation(xCh, yCh):
                self.changeLevel(i) # if we did, start that level
                break


    def handleSubmissionByCharacter(self):
        if self.characterOnIsland:
            # since this submission is by character, he is already on some island
            self.submitSelectedIsland() # so we can call this function


    def handleClick(self, mouseCoord, mouseButton):
        mouse_x, mouse_y = mouseCoord
        lvlXLeft, lvlXRight = MAP_OFFSET_X, LEVEL_WIDTH + MAP_OFFSET_X
        lvlYUp, lvlYDown = MAP_OFFSET_Y, LEVEL_HEIGHT + MAP_OFFSET_Y
        if self.levelSelected != self.levels[0]:
            # we are in some level other than selector
            if lvlXLeft <= mouse_x < lvlXRight and lvlYUp <= mouse_y < lvlYDown:
                # we clicked inside the map
                if self.levelSelected.handleClick(mouse_x, mouse_y, mouseButton):
                    # we clicked on some island and want to check if thats the solution
                    self.submitSelectedIsland()
            elif self.levels[0].checkActivation(mouse_x, mouse_y):
                # level selector icon activated - we pressed return to map
                self.changeLevel(0)
            return
        # we are on level selector since we would return from function otherwise
        for i in range(1, self.numOfLevels + 1):
            # for each level, check if we clicked on its icon for activation
            if self.levels[i].checkActivation(mouse_x, mouse_y):
                self.changeLevel(i) # if we did, start that level
                break

    def submitSelectedIsland(self):
        # returns True if submission is correct, False otherwise
        # firstly island must be selected before this function is called
        self.emergencyDrawWithFlip()  # so we can update the look of the map before submission
        if self.levelSelected.checkSolution():
            self.foundChestVideo.start()
            self.levelSelected.setFinishedTo(True) # this level is finished
            self.changeLevel(0) # return to level selector
            return True # good solution, return True
        # since we got here solution is wrong
        self.user.looseHeart(self.gameWindow) # deduct one heart
        if self.user.getNumOfHearts() <= 0:
            # number of hearts is 0 or less - end of the game
            self.terminatePlayScreen() # game over
        return False # bad solution, return False

    def draw(self):
        self.background.draw(self.display_board)
        if self.levelSelected != self.levels[0]: # we are not on selector of levels
            self.levelSelected.drawLevel(self.display_board.subsurface([MAP_OFFSET_X, MAP_OFFSET_Y, MAP_OFFSET_X + LEVEL_WIDTH, MAP_OFFSET_Y + LEVEL_HEIGHT]))
            self.levels[0].drawIcon(self.display_board) # draw back to map icon
            self.display_board.blit(self.pressEnterToSubmit_text, (WINDOW_WIDTH // 2 - self.pressEnterToSubmit_text.get_width() // 2, WINDOW_HEIGHT - MAP_OFFSET_Y // 2 - 25))
        else: # otherwise, draw every icon for every level so we can access them
            for i in range(1,self.numOfLevels + 1):
                self.levels[i].drawIcon(self.display_board)
        self.user.draw(self.display_board) # draw users health bar
        self.updateMainCharacter() # draw main character

    def emergencyDrawWithFlip(self):
        print("Emegency drawing")
        self.background.draw(self.display_board)
        if self.levelSelected != self.levels[0]: # we are not on selector of levels
            self.levelSelected.drawLevel(self.display_board.subsurface([MAP_OFFSET_X, MAP_OFFSET_Y, MAP_OFFSET_X + LEVEL_WIDTH, MAP_OFFSET_Y + LEVEL_HEIGHT]))
            self.levels[0].drawIcon(self.display_board) # draw back to map icon
            self.display_board.blit(self.pressEnterToSubmit_text, (WINDOW_WIDTH // 2 - self.pressEnterToSubmit_text.get_width() // 2, WINDOW_HEIGHT - MAP_OFFSET_Y // 2 - 25))
        else: # otherwise, draw every icon for every level so we can access them
            for i in range(1,self.numOfLevels + 1):
                self.levels[i].drawIcon(self.display_board)
        self.user.draw(self.display_board) # draw users health bar
        self.mainCharacter.move(0, 0 , self.display_board)
        pygame.display.flip()


    def changeLevel(self, levelId):
        if not 0 <= levelId < len(self.levels): return False # cannot change level to that
        if self.levelSelected == self.levels[levelId]: return True # already set to that level
        self.levelSelected.resetLevel() # reset selected island on the level
        self.levelSelected = self.levels[levelId] # change to new level
        self.updateSound() # update soundtrack
        return True # changed level








class Level:
    def __init__(self, mapFromNordeus, levelId, levelIdX, levelIdY, boolRandom): #
        self.finishedLevelIcon = Drawing(levelIdX, levelIdY, finished_level_icon_image)
        self.levelIcon = Drawing(levelIdX, levelIdY, level_icon_images[levelId])
        self.levelIconX = levelIdX # idX of icon for this levels number
        self.levelIconY = levelIdY # idY of icon for this levels number
        self.levelOver = False
        self.elevationLegendDrawing = Drawing(LEVEL_WIDTH + 10, LEVEL_HEIGHT // 2 - elevation_legend_image.get_height() // 2, elevation_legend_image)
        self.randomEveryTimeActivated = boolRandom
        self.formArchipelago(mapFromNordeus)


    def formArchipelago(self, mapFromNordeus):
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
            return self.archipelago.selectIslandAt(mouse_x, mouse_y) # return True if hit an island, else it hit the water so returns False
        else: # right button click
            return self.archipelago.selectIslandAt(mouse_x, mouse_y)

    def checkSolution(self, foundChestVideo = None): # fix this if you want to use foundChestVideo here
        if self.archipelago.isHighestSelected():
            self.levelOver = True
            # foundChestVideo.start()
            return True
        return False


    def resetLevel(self):
        self.archipelago.resetArchipelago()

        if self.randomEveryTimeActivated:
            # if this is the random level, every time player quits this level, refresh the map
            print("exited random level")
            self.formArchipelago(True)
            self.levelOver = False

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