#COLOURS (R, G, B)
import random
import pygame
import requests
import sys
import os

GET_REQ_LINK = "https://jobfair.nordeus.com/jf24-fullstack-challenge/test"

BGCOLOUR = (0, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
DARKGREEN = (0, 200, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BGCOLOUR = DARKGREY

# game settings
TILESIZE = 16
ROWS = 30
COLS = 30
FPS = 60

WIDTH = COLS * TILESIZE
HEIGHT = TILESIZE * ROWS
WINDOW_WIDTH = WIDTH + 200
WINDOW_HEIGHT = HEIGHT + 200

MAP_OFFSET_X = 100
MAP_OFFSET_Y = 100

TITLE = "Top Hill"

HEIGHT_LEVELS_NUM = 9
height_levels = [0,50,200,300,450,650,800,950,1000]

def getHeightLevel(height):
    if height == 0:
        return 0
    if height <= 50:
        return 1
    if height <= 200:
        return 2
    if height <= 300:
        return 3
    if height <= 450:
        return 4
    if height <= 650:
        return 5
    if height <= 800:
        return 6
    if height <= 950:
        return 7
    if height <= 1000:
        return 8

    return 2
height_levels_images = []
for i in range(0 , HEIGHT_LEVELS_NUM):
    height_levels_images.append(pygame.transform.scale(pygame.image.load(os.path.join("../assets", f"height{height_levels[i]}_1.png")), (TILESIZE, TILESIZE)))

NUM_OF_BOATS = random.randint(1,5)
BOAT_HEIGHT = int(TILESIZE * 1)
BOAT_WIDTH = int(TILESIZE * 1)
boat_image = pygame.transform.scale(pygame.image.load(os.path.join("../assets", "fish-boat.png")), (BOAT_HEIGHT, BOAT_WIDTH))

NUM_OF_SHIPS = random.randint(1,9)
SHIP_WIDTH = int(TILESIZE * 2)
SHIP_HEIGHT = int(TILESIZE * 2)
ship_images = []
for i in range(1,5):
    ship_images.append(pygame.transform.scale(pygame.image.load(os.path.join("../assets", f"ship{i}.png")), (SHIP_HEIGHT, SHIP_WIDTH)))

flag_image = pygame.transform.scale(pygame.image.load(os.path.join("../assets", "flag.png")), (TILESIZE * 2, TILESIZE * 2))
tree_image = pygame.transform.scale(pygame.image.load(os.path.join("../assets", "tree.png")), (TILESIZE * 2, TILESIZE * 2))
palm_image = pygame.transform.scale(pygame.image.load(os.path.join("../assets", "palm.png")), (TILESIZE * 2, TILESIZE * 2))
cloud_image = pygame.transform.scale(pygame.image.load(os.path.join("../assets", "cloud.png")), (TILESIZE * 2, TILESIZE * 2))
plane_image = pygame.transform.scale(pygame.image.load(os.path.join("../assets", "red-plane.png")), (TILESIZE * 3, TILESIZE * 3))

red_lines_images = []
for i in range(16): # 1 for UP, 2 for RIGHT, 4 for LEFT, 8 for DOWN, (UP | DOWN) for combinations, 16 all in all
    red_lines_images.append(pygame.transform.scale(pygame.image.load(os.path.join("../assets", f"red_line{i}.png")),(TILESIZE, TILESIZE)))