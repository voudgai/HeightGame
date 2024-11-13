import pygame
import json

class SpriteSheet:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()
        self.meta_data = self.filename.replace('png','json')
        with open(self.meta_data) as file: # cand do try catch
            self.data = json.load(file)
        file.close()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface((width, height))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (x,y, width, height))
        return sprite

    def parse_sprite(self,name):
        sprite = self.data['frames'][name]['frame']
        x,y, width, height = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self.get_sprite(x, y + 50, width, height)
        return image

pygame.init()
clock = pygame.time.Clock()
DISPLAY_W , DISPLAY_H = 480, 270
canvas = pygame.Surface((DISPLAY_W, DISPLAY_H))
window = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
running = True

my_spriteSheet = SpriteSheet('ShootNoFire.png')
pirate = [my_spriteSheet.parse_sprite('pirateShooting1.png'),my_spriteSheet.parse_sprite('pirateShooting2.png'),
          my_spriteSheet.parse_sprite('pirateShooting3.png'), my_spriteSheet.parse_sprite('pirateShooting4.png'),
          my_spriteSheet.parse_sprite('pirateShooting5.png')]
index = 0
while running:
    clock.tick(8)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
               pass
    index = (index + 1) % len(pirate)
    canvas.fill((255, 255, 255))
    canvas.blit(pirate[index], (0,DISPLAY_H - 128))
    window.blit(canvas,(0,0))
    pygame.display.update()
