import pygame
from os.path import join
import random


Player_Offset = {1: (20, 10), 2: (-20, -10)}


def get_tile_position(tile_number, offset=((0, 0))):
    row = (tile_number - 1) // 10
    col = (tile_number - 1) % 10

    if row % 2 == 1:
        col = 9 - col

    tile_size = 64
    x = col * tile_size + tile_size // 2 + offset[0]
    y = 640 - (row * tile_size + tile_size // 2) + offset[1]
    return (x, y)


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

        self.roll_complete = False

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
                self.image = pygame.transform.rotozoom(final_face, 0, 0.1)
                print(f"🎲 Dice-rolled : {self.current_value}")
        
                self.roll_complete = True

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, image, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join("Game", "player", image)).convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.1)
        self.rect = self.image.get_rect(bottomleft=pos)

        self.current_tile = 1
        self.offset = (0, 0)  # separate player visually

    def move(self, steps, snakes, ladders):
        next_tile = self.current_tile + steps
        if next_tile > 100:
            next_tile = 100

        # snake and ladders
        if next_tile in snakes:
            print(f"🐍 Oh no! Snake from {next_tile} → {snakes[next_tile]}")
            next_tile = snakes[next_tile]
        elif next_tile in ladders:
            print(f"🪜 Yay! Ladder from {self.current_tile} → {ladders[next_tile]}")
            next_tile = ladders[next_tile]

        self.current_tile = next_tile
        self.rect.center = get_tile_position(self.current_tile, self.offset)
        print(f"Player Moved to tile{self.current_tile}")


pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
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

player1 = Player((20, 630), "player1.png", [all_sprites])
player2 = Player((10, 630), "player2.png", [all_sprites])

dice = Dice((320, 320), all_sprites)

current_player = 1
dice.roll_complete = False

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

    if dice.roll_complete:
        if current_player == 1:
            player1.move(dice.current_value, snakes, ladders)
            current_player = 2

        else:
            player2.move(dice.current_value, snakes, ladders)
            current_player = 1

        dice.roll_complete = False

    pygame.display.update()

pygame.quit()
