import os

import pygame
import pygamepal

from game.settings import main_character_runningR_path, main_character_runningL_path, main_character_standing_path


class CharacterSprite:
    pathRunningRight = main_character_runningR_path
    pathRunningLeft = main_character_runningL_path
    pathStanding = main_character_standing_path
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.movX, self.movY = 1, 1
        self.setUpRunningRight()
        self.setUpRunningLeft()
        self.setUpStanding()

    def getCoordinates(self):
        return self.x, self.y


    def setUpRunningRight(self):
        # real dimension of png document containing frames 576 x 96
        textureRunRight = pygame.transform.scale(pygame.image.load(os.path.join(CharacterSprite.pathRunningRight)), (576, 96))
        # split texture into a 2D list of sub-textures,  # splits into blocks 96x96, which is size of 1 frame with buffer between each frame
        splitTextures = pygamepal.splitTexture(textureRunRight, (96, 96))
        # we take 6 frames from first row of our 2D list(only row we have since its one row animation in png) and enter buffer size between each
        self.spriteImageRunRight = pygamepal.SpriteImage(splitTextures[0][0], splitTextures[0][1], splitTextures[0][2], splitTextures[0][3], splitTextures[0][4], splitTextures[0][5],
                                            offset=(30, 96))

    def setUpRunningLeft(self):
        # real dimension of png document containing frames 576 x 96
        textureRunRight = pygame.transform.scale(pygame.image.load(os.path.join(CharacterSprite.pathRunningLeft)),
                                                 (576, 96))
        # split texture into a 2D list of sub-textures,  # splits into blocks 96x96, which is size of 1 frame with buffer between each frame
        splitTextures = pygamepal.splitTexture(textureRunRight, (96, 96))
        # we take 6 frames from first row of our 2D list(only row we have since its one row animation in png) and enter buffer size between each
        self.spriteImageRunLeft = pygamepal.SpriteImage(splitTextures[0][0], splitTextures[0][1], splitTextures[0][2],
                                                         splitTextures[0][3], splitTextures[0][4], splitTextures[0][5],
                                                         offset=(30, 96))

    def setUpStanding(self):
        # real dimension of png document containing frames 576 x 96
        textureRunRight = pygame.transform.scale(pygame.image.load(os.path.join(CharacterSprite.pathStanding)),
                                                 (576, 96))
        # split texture into a 2D list of sub-textures,  # splits into blocks 96x96, which is size of 1 frame with buffer between each frame
        splitTextures = pygamepal.splitTexture(textureRunRight, (96, 96))
        # we take 6 frames from first row of our 2D list(only row we have since its one row animation in png) and enter buffer size between each
        self.spriteImageStanding = pygamepal.SpriteImage(splitTextures[0][0], splitTextures[0][1], splitTextures[0][2],
                                                        splitTextures[0][3], splitTextures[0][4], splitTextures[0][5],
                                                        offset=(30, 96))
    def move(self,dx,dy,display_board):
        wDB, hDB = pygame.display.get_surface().get_size()
        if 0 <= dx + self.x < wDB - 48:
            self.x = self.x + dx
        if 48 <= dy + self.y < hDB:
            self.y = self.y + dy
        if dx > 0 or (dx == 0 and dy != 0):
            self.spriteImageRunRight.update()
            self.spriteImageRunRight.draw(display_board, (self.x,self.y))
        elif dx < 0:
            self.spriteImageRunLeft.update()
            self.spriteImageRunLeft.draw(display_board,(self.x,self.y))
        elif dy == 0:
            self.spriteImageStanding.update()
            self.spriteImageStanding.draw(display_board,(self.x,self.y))



# # load a texture
# texture = pygame.transform.scale(pygame.image.load(os.path.join('./sprites/spriteSheetTesting2/runAttack.png')), (384, 96))
#
# # split texture into a 2D list of sub-textures
# splitTextures = pygamepal.splitTexture(texture, (96, 96))
#
# spriteImage = pygamepal.SpriteImage(splitTextures[0][0], splitTextures[0][1], splitTextures[0][2], splitTextures[0][3],
#                                     offset=(30, 96))
# # simple alternative for single textures:
# # spriteImage1.addTextures(pygame.image.load('image1.png'), pygame.image.load('image2.png'))
def test():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption('SpriteImage Example')
    clock = pygame.time.Clock()

    character = CharacterSprite(400, 400)

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