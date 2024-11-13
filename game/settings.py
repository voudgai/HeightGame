#COLOURS (R, G, B)
import random
import pygame
import requests
import sys
import os

import pygame
from pyvidplayer2 import VideoPlayer, Video
main_character_spawn_X = 160
main_character_spawn_Y = 205
main_character_runningR_path = "../assets/warriors_pack/Warrior_1/Run.png"
main_character_runningL_path = "../assets/warriors_pack/Warrior_1/RunLeft.png"
main_character_standing_path = "../assets/warriors_pack/Warrior_1/Idle.png"

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
TILESIZE = 20
ROWS = 30
COLS = 30
FPS = 60

LEVEL_WIDTH = COLS * TILESIZE
LEVEL_HEIGHT = TILESIZE * ROWS
WINDOW_WIDTH = LEVEL_WIDTH + 140
WINDOW_HEIGHT = LEVEL_HEIGHT + 140

MAP_OFFSET_X = (WINDOW_WIDTH - LEVEL_WIDTH) // 2
MAP_OFFSET_Y = (WINDOW_HEIGHT - LEVEL_HEIGHT) // 2

TITLE = "John without Teeth and His Gold"

HEIGHT_LEVELS_NUM = 15
elevation_legend_image = pygame.transform.scale(pygame.image.load(os.path.join("../assets", "elevation_legend.png")),(20, 300))
height_levels = [0]
for i in range(HEIGHT_LEVELS_NUM - 1): height_levels.append( i * 75 )
height_levels.append(1000)

def getHeightLevel(height):
    if height == 0: return 0
    if height < 975: return (height + 74) // 75
    else: return HEIGHT_LEVELS_NUM -1

height_levels_images = []
for i in range(0 , HEIGHT_LEVELS_NUM):
    height_levels_images.append(pygame.transform.scale(pygame.image.load(os.path.join("../assets", f"height{height_levels[i]}_2.png")), (TILESIZE, TILESIZE)))

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

NUM_OF_LEVELS = 5
# this num is without selector level, with him its +1
# selector levels image is level_icon_images[0]
BACK_TO_MAP_X_OFFS = WINDOW_WIDTH - MAP_OFFSET_X # for level selector shortcut
BACK_TO_MAP_Y_OFFS = 55 # for level selector shortcut

playBackground_zoom_ratio_X = WINDOW_WIDTH / 550
playBackground_zoom_ratio_Y = WINDOW_HEIGHT / 550
level_icons_coordinates = [( playBackground_zoom_ratio_X * 200, playBackground_zoom_ratio_Y * 130),
                           ( playBackground_zoom_ratio_X * 160, playBackground_zoom_ratio_Y * 190),
                           ( playBackground_zoom_ratio_X * 250, playBackground_zoom_ratio_Y * 270),
                           ( playBackground_zoom_ratio_X * 340, playBackground_zoom_ratio_Y * 330),
                           ( playBackground_zoom_ratio_X * 190, playBackground_zoom_ratio_Y * 400)]
level_icon_images = [
    pygame.transform.scale(pygame.image.load(os.path.join("../assets", "level_icon_selector.png")), (150, 50)),
    pygame.transform.scale(pygame.image.load(os.path.join("../assets", "level_icon_1.png")), (75, 75)),
    pygame.transform.scale(pygame.image.load(os.path.join("../assets", "level_icon_2.png")), (75, 75)),
    pygame.transform.scale(pygame.image.load(os.path.join("../assets", "level_icon_3.png")), (75, 75)),
    pygame.transform.scale(pygame.image.load(os.path.join("../assets", "level_icon_4.png")), (75, 75)),
    pygame.transform.scale(pygame.image.load(os.path.join("../assets", "level_icon_random.png")), (75, 75))]

finished_level_icon_image = pygame.transform.scale(pygame.image.load(os.path.join("../assets", "level_icon_finished.png")), (75,75))

NUM_OF_INSTRUMENTALS = 3
levels_instrumentals = [pygame.mixer.Sound("../assets/Drunken Sailor Instrumental.mp3"),pygame.mixer.Sound("../assets/level_music_1.mp3"),pygame.mixer.Sound("../assets/level_music_2.mp3")]

NUM_OF_HEARTS = 3
HEARTS_PLACEHOLDER_X_OFFS = MAP_OFFSET_X + 150
HEARTS_PLACEHOLDER_Y_OFFS = BACK_TO_MAP_Y_OFFS

heart_placeholder_image0 = pygame.transform.scale(pygame.image.load(os.path.join("../assets", "heart_placeholder0.png")),(150,50))
heart_placeholder_image1 = pygame.transform.scale(pygame.image.load(os.path.join("../assets", "heart_placeholder1.png")),(150,50))
heart_placeholder_image2 = pygame.transform.scale(pygame.image.load(os.path.join("../assets", "heart_placeholder2.png")),(150,50))
heart_placeholder_image3 = pygame.transform.scale(pygame.image.load(os.path.join("../assets", "heart_placeholder3.png")),(150,50))

loose_heart_video = Video("../assets/heart_lost_animation.mp4")
chest_found_video = Video("../assets/chest_found_video.mp4")

SCORE_PLACEHOLDER_X_OFFS = MAP_OFFSET_X
SCORE_PLACEHOLDER_Y_OFFS = 50


end_screen_instrumental = pygame.mixer.Sound("../assets/ending_scene_music.mp3")
end_screen_background = pygame.transform.scale(pygame.image.load(os.path.join("../assets", "dark_end_pirate_map_3.jpg")), (WINDOW_WIDTH, WINDOW_WIDTH))
restart_button_image = pygame.transform.scale(pygame.image.load(os.path.join("../assets", "reset_button.png")), (225,75))
play_button_image = pygame.transform.scale(pygame.image.load(os.path.join("../assets", "play_button.png")), (225,75))
quit_button_image = pygame.transform.scale(pygame.image.load(os.path.join("../assets", "quit_button.png")), (225,75))