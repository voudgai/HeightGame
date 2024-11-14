import os

import pygame
import pygamepal

from game.settings import viking_character_runningR_path, viking_character_runningL_path, \
    viking_character_standing_path, knight_character_standing_path, knight_character_runningL_path, \
    knight_character_runningR_path


class CharacterSprite:
    pathRunningRightViking = viking_character_runningR_path
    pathRunningLeftViking = viking_character_runningL_path
    pathStandingViking = viking_character_standing_path

    pathRunningRightKnight = knight_character_runningR_path
    pathRunningLeftKnight = knight_character_runningL_path
    pathStandingKnight = knight_character_standing_path

    def __init__(self, x, y, boolViking):
        self.x, self.y = x, y
        self.movX, self.movY = 1, 1
        if boolViking: self.setUpViking()
        else: self.setUpKnight()

    def getCoordinates(self):
        return self.x, self.y

    def setUpViking(self):
        print("setting viking up")
        self.setUpRunningRight(CharacterSprite.pathRunningRightViking)
        self.setUpRunningLeft(CharacterSprite.pathRunningLeftViking)
        self.setUpStanding(CharacterSprite.pathStandingViking)

    def setUpKnight(self):
        print("setting knight up")
        self.setUpRunningRight(CharacterSprite.pathRunningRightKnight)
        self.setUpRunningLeft(CharacterSprite.pathRunningLeftKnight)
        self.setUpStanding(CharacterSprite.pathStandingKnight)

    def move(self,dx,dy,display_board):
        wDB, hDB = pygame.display.get_surface().get_size()
        if 0 <= dx + self.x < wDB - 48:
            self.x = self.x + dx
        if 48 <= dy + self.y < hDB:
            self.y = self.y + dy

        if dx > 0: # to the right
            self.spriteImageRunRight.update()
            self.spriteImageRunRight.draw(display_board, (self.x,self.y))
        elif dx == 0: # up or down
            if dy > 0: # down
                self.spriteImageRunRight.update()
                self.spriteImageRunRight.draw(display_board, (self.x, self.y))
            elif dy < 0: # up
                self.spriteImageRunLeft.update()
                self.spriteImageRunLeft.draw(display_board, (self.x, self.y))
            elif dy == 0: # standing still
                self.spriteImageStanding.update()
                self.spriteImageStanding.draw(display_board,(self.x,self.y))
        elif dx < 0: # left
            self.spriteImageRunLeft.update()
            self.spriteImageRunLeft.draw(display_board,(self.x,self.y))

    def setUpRunningRight(self, pathRunningR):
        # real dimension of png document containing frames 576 x 96
        textureRunRight = pygame.transform.scale(pygame.image.load(os.path.join(pathRunningR)), (576, 96))
        # split texture into a 2D list of sub-textures,  # splits into blocks 96x96, which is size of 1 frame with buffer between each frame
        splitTextures = pygamepal.splitTexture(textureRunRight, (96, 96))
        # we take 6 frames from first row of our 2D list(only row we have since its one row animation in png) and enter buffer size between each
        self.spriteImageRunRight = pygamepal.SpriteImage(splitTextures[0][0], splitTextures[0][1], splitTextures[0][2], splitTextures[0][3], splitTextures[0][4], splitTextures[0][5],
                                            offset=(30, 96))

    def setUpRunningLeft(self, pathRunningL):
        # real dimension of png document containing frames 576 x 96
        textureRunRight = pygame.transform.scale(pygame.image.load(os.path.join(pathRunningL)),
                                                 (576, 96))
        # split texture into a 2D list of sub-textures,  # splits into blocks 96x96, which is size of 1 frame with buffer between each frame
        splitTextures = pygamepal.splitTexture(textureRunRight, (96, 96))
        # we take 6 frames from first row of our 2D list(only row we have since its one row animation in png) and enter buffer size between each
        self.spriteImageRunLeft = pygamepal.SpriteImage(splitTextures[0][0], splitTextures[0][1], splitTextures[0][2],
                                                         splitTextures[0][3], splitTextures[0][4], splitTextures[0][5],
                                                         offset=(30, 96))

    def setUpStanding(self, pathStanding):
        # real dimension of png document containing frames 576 x 96
        textureRunRight = pygame.transform.scale(pygame.image.load(os.path.join(pathStanding)),
                                                 (576, 96))
        # split texture into a 2D list of sub-textures,  # splits into blocks 96x96, which is size of 1 frame with buffer between each frame
        splitTextures = pygamepal.splitTexture(textureRunRight, (96, 96))
        # we take 6 frames from first row of our 2D list(only row we have since its one row animation in png) and enter buffer size between each
        self.spriteImageStanding = pygamepal.SpriteImage(splitTextures[0][0], splitTextures[0][1], splitTextures[0][2],
                                                        splitTextures[0][3], splitTextures[0][4], splitTextures[0][5],
                                                        offset=(30, 96))






def test():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption('SpriteImage Example')
    clock = pygame.time.Clock()

    viking = int(input("Knight = 0, Viking = 1: "))
    if viking == 1:
        character = CharacterSprite(400, 400, True)
    else:
        character = CharacterSprite(400, 400, False)

    running = True
    while running:
        clock.tick(60)

        # respond to quit event
        dx, dy = 0, 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        movX, movY = character.movX, character.movY
        if keys[pygame.K_LEFT]:
            dx -= movX
        if keys[pygame.K_RIGHT]:
            dx += movX
        if keys[pygame.K_UP]:
            dy -= movY
        if keys[pygame.K_DOWN]:
            dy += movY

        # spriteImage.update()

        screen.fill('cornflowerblue')
        # spriteImage.draw(screen, (0, 48))
        character.move(dx, dy , screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    test()