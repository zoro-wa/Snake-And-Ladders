import pygame
from os.path import join

pygame.init()

WINDOW_WIDTH,WINDOW_HEIGHT = 640, 640
display_surf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption ('Snake And Ladders')
running = True
clock = pygame.time.Clock()


#import
bg_surf = pygame.image.load(join('Game', 'bg.png')).convert_alpha()
#bg_surf = pygame.transform.scale(bg_surf,(WINDOW_WIDTH, WINDOW_HEIGHT))

while running:
    dt = clock.tick() / 1000
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    display_surf.blit(bg_surf,(0,0))
    pygame.display.update()

pygame.quit()