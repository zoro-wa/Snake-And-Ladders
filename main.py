import pygame
from os.path import join
import random


class Dice(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.faces = [
            pygame.image.load(
                join("Game", "dice", f"inverted-dice-{i}.png")
            ).convert_alpha()
            for i in range(1, 7)
        ]

        self.image = self.faces[0]
        self.image = pygame.transform.rotozoom(self.image, 0, 0.1)
        self.rect = self.image.get_rect(center=pos)

        # rolling_logic attributes
        self.current_value = 1
        self.is_rolling = False
        self.roll_timer = 0
        self.roll_duration = 0.5

    def start_roll(self):
        if not self.is_rolling:
            self.is_rolling = True
            self.roll_timer = 0

    def update(self, dt):
        if self.is_rolling:
            self.roll_timer += dt

            self.image = pygame.transform.rotozoom(random.choice(self.faces), 0, 0.1)

            if self.roll_timer >= self.roll_duration:
               self.is_rolling = False
               self.current_value = random.randint(1, 6)
               final_face = self.faces[self.current_value - 1]
               self.image = pygame.transform.rotozoom(final_face , 0, 0.1)
               print(f"🎲 Dice-rolled : {self.current_value}")


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(
            join("Game", "player", "player1.png")
        ).convert_alpha()
        self.image = pygame.image.load(
            join("Game", "player", "player2.png")
        ).convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.1)
        self.rect = self.image.get_rect(bottomleft=pos)


class Board(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)


pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 640, 640
display_surf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake And Ladders")
running = True
clock = pygame.time.Clock()

# Gamesetup
board_size = 100
snakes = {17: 7, 62: 19, 54: 34, 64: 60, 87: 36, 93: 73, 94: 75, 98: 79}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 94, 51: 67, 72: 91, 80: 99}

# import
bg_surf = pygame.image.load(join("Game", "bg.png")).convert_alpha()

all_sprites = pygame.sprite.Group()

player = Player((10, 630), all_sprites)
dice = Dice((320, 320), all_sprites)


while running:
    dt = clock.tick() / 1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            dice.start_roll()

    display_surf.blit(bg_surf, (0, 0))
    all_sprites.draw(display_surf)

    all_sprites.update(dt)

    pygame.display.update()

pygame.quit()
