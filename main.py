import pygame
from os.path import join
import random


Player_Offset = {1: (20, 10), 2: (-20, -10)}


def get_tile_position(tile_number, offset=((0, 0))):
    row = (tile_number - 1) // 10
    col = (tile_number - 1) % 10

    if row % 2 == 1:
        col = 9 - col

    tile_size = 72
    x = col * tile_size + tile_size // 2 + offset[0]
    y = 720 - (row * tile_size + tile_size // 2) + offset[1]
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
        self.rect = self.image.get_rect(center=pos)

        self.current_tile = 1
        self.offset = (0, 0)  # separate player visually

    def move(self, steps, snakes, ladders):
        next_tile = self.current_tile + steps
        if next_tile > 100:
            next_tile = 100

        # snake and ladders
        if next_tile in snakes:
            print(f"Oh no! Snake from {next_tile} → {snakes[next_tile]}")
            next_tile = snakes[next_tile]
        elif next_tile in ladders:
            print(f"Yay! Ladder from {self.current_tile} → {ladders[next_tile]}")
            next_tile = ladders[next_tile]

        self.current_tile = next_tile
        self.rect.center = get_tile_position(self.current_tile, self.offset)
        print(f"Player Moved to tile{self.current_tile}")


pygame.init()

font = pygame.font.Font(join("Game", "fonts", "Super Kindly.ttf"), 30)
status_text = "Press SPACE to rock and roll"

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
bg_surf = pygame.transform.smoothscale(bg_surf, (720, 720))

all_sprites = pygame.sprite.Group()

player1 = Player(get_tile_position(1, Player_Offset[1]), "player1.png", [all_sprites])
player2 = Player(get_tile_position(1, Player_Offset[2]), "player2.png", [all_sprites])

dice = Dice((320, 320), all_sprites)

mode = "menu_mode"
cpu_timer = 0

start_bg = pygame.image.load(join("Game", "start.png")).convert_alpha()
start_bg = pygame.transform.smoothscale(start_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))

show_start = True

menu_mode = None

title_font = pygame.font.Font(join("Game", "fonts", "Super Kindly.ttf"), 60)
button_font = pygame.font.Font(join("Game", "fonts", "Super Kindly.ttf"), 36)

# Button_Setup
pvp_rect = pygame.Rect(WINDOW_WIDTH // 2 - 150, 320, 300, 60)
cpu_rect = pygame.Rect(WINDOW_WIDTH // 2 - 150, 420, 300, 60)
quit_rect = pygame.Rect(WINDOW_WIDTH // 2 - 150, 520, 300, 60)


def draw_button(rect, text, hovered=False, color=(255, 255, 255)):
    # creating a hover effect on bordered buttons"
    bg_color = (50, 50, 50) if hovered else (30, 30, 30)
    border_color = (255, 255, 0) if hovered else (180, 180, 180)
    pygame.draw.rect(display_surf, bg_color, rect, border_radius=12)
    pygame.draw.rect(display_surf, bg_color, rect, width=3, border_radius=12)
    text_surf = button_font.render(text, True, color)
    text_rect = text_surf.get_rect(center=rect.center)
    display_surf.blit(text_surf, text_rect)


while show_start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pvp_rect.collidepoint(event.pos):
                menu_mode = "2player"
                show_start = False

            elif cpu_rect.collidepoint(event.pos):
                menu_mode = "cpu"
                show_start = False

            elif quit_rect.collidepoint(event.pos):
                pygame.quit()
                exit()


    mouse_pos = pygame.mouse.get_pos()

    display_surf.blit(start_bg, (0, 0))
    title = title_font.render(" Snake & Ladders ", True, (255, 255, 255))
    title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 180))
    display_surf.blit(title, title_rect)

    # Draw Buttons with hover effect.
    draw_button(pvp_rect, "Player vs Player", hovered=pvp_rect.collidepoint(mouse_pos))
    draw_button(cpu_rect, "Player vs Computer", hovered=cpu_rect.collidepoint(mouse_pos))
    draw_button(
        quit_rect,
        "Quit Game",
        hovered=quit_rect.collidepoint(mouse_pos),
        color=(255, 100, 100),
    )

    pygame.display.update()

current_player = 1
dice.roll_complete = False


while running:
    dt = clock.tick() / 1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if mode == "2player":
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
                and not dice.is_rolling
            ):
                dice.start_roll()

        elif mode == "cpu":
            if current_player == 1:

                if (
                    event.type == pygame.KEYDOWN
                    and event.key == pygame.K_SPACE
                    and not dice.is_rolling
                ):
                    dice.start_roll()

    if mode == "cpu" and current_player == 2:
        if not dice.is_rolling and not dice.roll_complete:
            cpu_timer += dt
            if cpu_timer > 1.0:
                dice.start_roll()
                cpu_timer = 0

    display_surf.blit(bg_surf, (0, 0))
    all_sprites.draw(display_surf)

    all_sprites.update(dt)

    if dice.roll_complete:
        status_text = f" Dice rolled: "

        if current_player == 1:
            player1.move(dice.current_value, snakes, ladders)
            current_player = 2
            status_text += " Player 2's Turn"

        else:
            player2.move(dice.current_value, snakes, ladders)
            current_player = 1
            status_text += " Player 1's Turn"

        dice.roll_complete = False

    pygame.draw.rect(display_surf, (30, 30, 30), (720, 0, 560, 720))

    # turn_text = font.render(f" Player {current_player}'s Turn", True, (255, 255, 255))
    # display_surf.blit(turn_text, (750, 100))

    dice_text = font.render(f" Dice: {dice.current_value}", True, (200, 200, 200))
    display_surf.blit(dice_text, (750, 180))

    status_display = font.render(status_text, True, (255, 255, 100))
    display_surf.blit(status_display, (750, 300))

    pygame.display.update()

pygame.quit()
