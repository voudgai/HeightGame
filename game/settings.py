#COLOURS (R, G, B)
import random
import pygame
import requests
import sys
import os

import pygame
from pyvidplayer2 import VideoPlayer, Video

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
TILESIZE = 18
ROWS = 30
COLS = 30
FPS = 60

LEVEL_WIDTH = COLS * TILESIZE
LEVEL_HEIGHT = TILESIZE * ROWS
WINDOW_WIDTH = LEVEL_WIDTH + 200
WINDOW_HEIGHT = LEVEL_HEIGHT + 200

MAP_OFFSET_X = 100
MAP_OFFSET_Y = 100

TITLE = "John without Teeth and His Gold"

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

NUM_OF_BOATS = random.randint(3,5)
BOAT_HEIGHT = int(TILESIZE * 1)
BOAT_WIDTH = int(TILESIZE * 1)
boat_image = pygame.transform.scale(pygame.image.load(os.path.join("../assets", "fish-boat.png")), (BOAT_HEIGHT, BOAT_WIDTH))

NUM_OF_SHIPS = random.randint(40,50)
SHIP_WIDTH = int(TILESIZE * 2)
SHIP_HEIGHT = int(TILESIZE * 2)
ship_images = []
for i in range(1,7):
    ship_images.append(pygame.transform.scale(pygame.image.load(os.path.join("../assets", f"ship{i}.png")), (SHIP_HEIGHT, SHIP_WIDTH)))

flag_image = pygame.transform.scale(pygame.image.load(os.path.join("../assets", "flag.png")), (TILESIZE * 2, TILESIZE * 2))
tree_image = pygame.transform.scale(pygame.image.load(os.path.join("../assets", "tree.png")), (TILESIZE * 2, TILESIZE * 2))
palm_image = pygame.transform.scale(pygame.image.load(os.path.join("../assets", "palm.png")), (TILESIZE * 2, TILESIZE * 2))
cloud_image = pygame.transform.scale(pygame.image.load(os.path.join("../assets", "cloud.png")), (TILESIZE * 2, TILESIZE * 2))
plane_image = pygame.transform.scale(pygame.image.load(os.path.join("../assets", "red-plane.png")), (TILESIZE * 3, TILESIZE * 3))
empty_image = pygame.transform.scale(pygame.image.load(os.path.join("../assets", "empty.png")), (TILESIZE * 3, TILESIZE * 3))

red_lines_images = []
for i in range(16): # 1 for UP, 2 for RIGHT, 4 for LEFT, 8 for DOWN, (UP | DOWN) for combinations, 16 all in all
    red_lines_images.append(pygame.transform.scale(pygame.image.load(os.path.join("../assets", f"red_line{i}.png")),(TILESIZE, TILESIZE)))

black_lines_images = []
for i in range(16): # 1 for UP, 2 for RIGHT, 4 for LEFT, 8 for DOWN, (UP | DOWN) for combinations, 16 all in all
    black_lines_images.append(pygame.transform.scale(pygame.image.load(os.path.join("../assets", f"black_line{i}.png")),(TILESIZE, TILESIZE)))



def getHeightSignImage(height):
    print("Height sign image not implemented yet")
    return flag_image

intro_video = Video("../intro_video_and_material/Pirates_game_INTRO2.mp4")
skip_button_intro_image = pygame.transform.scale(pygame.image.load(os.path.join("../intro_video_and_material", "skip_button_intro.png")),(100,50))
start_screen_background_image = pygame.transform.scale(pygame.image.load(os.path.join("../intro_video_and_material", "welcome_picture.png")), (WINDOW_WIDTH, WINDOW_WIDTH))
start_button_image = pygame.transform.scale(pygame.image.load(os.path.join("../intro_video_and_material", "start_button_retro.png")), (150,50))
play_screen_background_image = pygame.transform.scale(pygame.image.load(os.path.join("../assets", "pirate_map_3.jpg")), (WINDOW_WIDTH,WINDOW_HEIGHT))

NUM_OF_LEVELS = 4
# this num is without selector level, with him its +1
# selector levels image is level_icon_images[0]
level_icon_images = []
level_icon_images.append(plane_image)
level_icon_images.append(tree_image)
level_icon_images.append(cloud_image)
level_icon_images.append(boat_image)
level_icon_images.append(palm_image)