import pygame
from os.path import join
import random


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('Game', 'inverted-dice-1.png')).convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.1)
        self.rect = self.image.get_rect(center = pos)


pygame.init()

WINDOW_WIDTH,WINDOW_HEIGHT = 640, 640
display_surf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption ('Snake And Ladders')
running = True
clock = pygame.time.Clock()


#import
bg_surf = pygame.image.load(join('Game', 'bg.png')).convert_alpha()
#bg_surf = pygame.transform.scale(bg_surf,(WINDOW_WIDTH, WINDOW_HEIGHT))

all_sprites = pygame.sprite.Group()


player = Player((320, 320), all_sprites)

while running:
    dt = clock.tick() / 1000
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    display_surf.blit(bg_surf,(0,0))
    all_sprites.draw(display_surf)

    pygame.display.update()

pygame.quit()