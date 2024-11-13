import pygame
import pygamepal
import os

# initialise Pygame
pygame.init()

# setup screen
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('SpriteImage Example')
clock = pygame.time.Clock()

# load a texture
texture = pygame.transform.scale(pygame.image.load(os.path.join('runAttack.png')), (320, 80))
# double the texture size
# split texture into a 2D list of sub-textures
splitTextures = pygamepal.splitTexture(texture, (80, 80))

# an animated sprite with multiple textures
spriteImage = pygamepal.SpriteImage(splitTextures[0][0], splitTextures[0][1], splitTextures[0][2], splitTextures[0][3],
                                    offset=(30, 80))
# simple alternative for single textures:
# spriteImage1.addTextures(pygame.image.load('image1.png'), pygame.image.load('image2.png'))

# game loop
running = True
while running:

    # advance clock
    clock.tick(60)

    # respond to quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #
    # update
    #

    spriteImage.update()

    #
    # draw
    #

    # clear screen
    screen.fill('cornflowerblue')

    # draw sprites and accompanying text
    spriteImage.draw(screen, (10, 40))

    # draw to screen
    pygame.display.flip()

#  quit Pygame
pygame.quit()