import pygame, random
from os.path import join

# --- Helper functions ---
Player_Offset = {1: (20, 10), 2: (-20, -10)}

def get_tile_position(tile_number, offset=(0, 0)):
    row = (tile_number - 1) // 10
    col = (tile_number - 1) % 10
    if row % 2 == 1:
        col = 9 - col
    tile_size = 72
    x = col * tile_size + tile_size // 2 + offset[0]
    y = 720 - (row * tile_size + tile_size // 2) + offset[1]
    return (x, y)

# Button draw
def draw_button(rect, text, hovered=False, color=(255,255,255)):
    bg = (50,50,50) if hovered else (30,30,30)
    border = (255,255,0) if hovered else (180,180,180)
    pygame.draw.rect(display_surf, bg, rect, border_radius=12)
    pygame.draw.rect(display_surf, border, rect, width=5, border_radius=12)
    surf = button_font.render(text, True, color)
    display_surf.blit(surf, surf.get_rect(center=rect.center))

# --- Classes ---
class Dice(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        scale = 0.156
        self.faces = [pygame.transform.rotozoom(pygame.image.load(join("Game","dice",f"inverted-dice-{i}.png")).convert_alpha(), 0, scale
        ) for i in range(1,7)]
        self.image = self.faces[0]
        self.rect = self.image.get_rect(center=pos)
        self.current_value = 1
        self.is_rolling = False
        self.roll_timer = 0
        self.roll_duration = 0.5
        self.roll_complete = False

    def start_roll(self):
        if not self.is_rolling:
            self.is_rolling = True
            self.roll_timer = 0
            dice_sound.play()

    def update(self, dt):
        if self.is_rolling:
            self.roll_timer += dt
            self.image = random.choice(self.faces)
            if self.roll_timer >= self.roll_duration:
                self.is_rolling = False
                self.current_value = random.randint(1,6)
                self.image = self.faces[self.current_value-1]
                self.roll_complete = True
                dice_sound.stop()
                print("Dice rolled:", self.current_value)

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,image_name,groups):
        super().__init__(groups)
        image = pygame.image.load(join("Game","player",image_name)).convert_alpha()
        scale_factor = 0.120
        self.image = pygame.transform.rotozoom(image, 0, scale_factor)
        self.rect = self.image.get_rect(center=pos)
        
        # differs offset offset [1] or [2]
        self.offset = Player_Offset[1 if "1" in image_name else 2]

        # Setup for movement
        self.current_tile = 1
        self.target_tile = 1
        self.move_queue = []
        self.step_timer = 0
        self.step_delay = 0.14
        self.moving = False
        self.auto_jump = None
    
    def move(self, dice_value, snakes, ladders):
        target = self.current_tile + dice_value
        if target>100: return

        self.move_queue = list(range(self.current_tile + 1, target + 1))
        self.target_tile = target
        self.moving = True
        self.step_timer = 0

        if target in snakes:
            self.auto_jump = snakes[target]
        elif target in ladders:
            self.auto_jump = ladders[target]
        else:
            self.auto_jump = None        

    def update(self, dt):
        if self.moving:
            self.step_timer += dt
            if self.step_timer >=self.step_delay:
                self.step_timer = 0
                if self.move_queue:
                    next_tile = self.move_queue.pop(0)
                    self.rect.center = get_tile_position(next_tile, self.offset)
                else:
                    self.moving = False
                    self.current_tile = self.target_tile
                    if self.auto_jump:
                       self.current_tile = self.auto_jump
                       self.rect.center = get_tile_position(self.current_tile, self.offset)
                       self.auto_jump = None 


# --- Pygame init ---
pygame.init()

# Initialize mixer
pygame.mixer.init()
# Dice Sounds
dice_sound = pygame.mixer.Sound(join('Game', 'music', 'rolling_dice.wav'))
dice_sound.set_volume(1.5)

WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720
display_surf = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Snake & Ladders")
clock = pygame.time.Clock()
font = pygame.font.Font(join("Game","fonts","Super Kindly.ttf"),30)
title_font = pygame.font.Font(join("Game","fonts","Super Kindly.ttf"),60)
button_font = pygame.font.Font(join("Game","fonts","Super Kindly.ttf"),36)

bg_surf = pygame.transform.smoothscale(pygame.image.load(join("Game","bg.png")).convert_alpha(),(720,720))
start_bg = pygame.transform.smoothscale(pygame.image.load(join("Game","start.png")).convert_alpha(),(WINDOW_WIDTH,WINDOW_HEIGHT))

# --- Game setup ---
snakes = {17:7,62:19,54:34,64:60,87:36,93:73,94:75,98:79}
ladders = {4:14,9:31,21:42,28:84,51:67,72:91,80:99}

# --- Start menu ---
pvp_rect = pygame.Rect(WINDOW_WIDTH//2-150,320,360,60)
cpu_rect = pygame.Rect(WINDOW_WIDTH//2-150,420,360,60)
quit_rect = pygame.Rect(WINDOW_WIDTH//2-80,520,200,60)

def show_start_menu():
    #start menu_bg sound
    pygame.mixer.music.load(join('Game', 'music', 'start_menu.mp3'))
    pygame.mixer.music.set_volume(1.5)
    pygame.mixer.music.play(-1)

    show=True
    mode=None
    while show:
        mouse_pos = pygame.mouse.get_pos()
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                pygame.quit();exit()
            if e.type==pygame.MOUSEBUTTONDOWN:
                if pvp_rect.collidepoint(e.pos):
                    pygame.mixer.music.stop()
                    mode="2player";show=False
                elif cpu_rect.collidepoint(e.pos):
                    pygame.mixer_music.stop()
                    mode="cpu";show=False
                elif quit_rect.collidepoint(e.pos):
                    pygame.mixer.music.stop()
                    pygame.quit();exit()
        display_surf.blit(start_bg,(0,0))
        title = title_font.render("Snake & Ladders",True,(255,255,255))
        display_surf.blit(title,title.get_rect(center=(WINDOW_WIDTH//2,180)))
        draw_button(pvp_rect,"Player vs Player",hovered=pvp_rect.collidepoint(mouse_pos))
        draw_button(cpu_rect,"Player vs Computer",hovered=cpu_rect.collidepoint(mouse_pos))
        draw_button(quit_rect,"Quit Game",hovered=quit_rect.collidepoint(mouse_pos),color=(255,100,100))
        pygame.display.update()
    return mode

# --- Player names input ---
def get_names(mode):
    name1=""
    if mode=="2player":
        name2=""
        current=1
    else:
        name2="Computer"
        current=1
    active=True
    input_font = pygame.font.Font(join("Game","fonts","Super Kindly.ttf"),36)
    prompt_font = pygame.font.Font(join("Game","fonts","Super Kindly.ttf"),36)
    while active:
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit();exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_RETURN:
                    if current==1:
                        current=2
                        if mode=="cpu": active=False
                    elif current==2: active=False
                elif e.key==pygame.K_BACKSPACE:
                    if current==1: name1=name1[:-1]
                    elif current==2: name2=name2[:-1]
                else:
                    if current==1 and len(name1)<15: name1+=e.unicode
                    elif current==2 and len(name2)<15: name2+=e.unicode
        display_surf.fill((0,0,0))
        prompt = "Enter Player 1 Name:" if current==1 else "Enter Player 2 Name:"
        display_surf.blit(prompt_font.render(prompt,True,(255,255,255)),(WINDOW_WIDTH//2-150,200))
        display_surf.blit(input_font.render(name1 if current==1 else name2,True,(255,255,0)),(WINDOW_WIDTH//2-150,300))
        pygame.display.update()
    return name1 or "Player1", name2 or "Player2"


def winner_screen(winner_name):
    "Shows the winner name with options to play again or exit"

    winner_active = True
    clock = pygame.time.Clock()

    #Fonts
    title_font = pygame.font.Font(join('Game', 'fonts', 'Magic Sound.ttf'), 60)
    button_font = pygame.font.Font(join('Game', 'fonts', 'Magic Sound.ttf'), 30)
    
    gold = (255, 215, 0)
    white = (255, 255, 255)


    play_again_rect = pygame.Rect(WINDOW_WIDTH // 2 - 150, 400, 300, 60)
    menu_rect = pygame.Rect(WINDOW_WIDTH // 2 - 150, 480, 300, 60)
    quit_rect = pygame.Rect(WINDOW_WIDTH // 2 - 150, 560, 300, 60)

    while winner_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_rect.collidepoint(event.pos):
                   return "play_again"

                elif menu_rect.collidepoint(event.pos):
                    return"menu"

                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()

        
        mouse_pos = pygame.mouse.get_pos()
        display_surf.fill((54, 15, 90)) 
        #Winner text               
        winner_text = title_font.render(f"{winner_name} is Victorious!", True, gold)
        winner_rect = winner_text.get_rect(center=(WINDOW_WIDTH // 2, 200))
        display_surf.blit(winner_text, winner_rect)
        #buttons
        draw_button(play_again_rect, "Play Again", hovered=play_again_rect.collidepoint(mouse_pos))
        draw_button(menu_rect, "Main Menu", hovered= menu_rect.collidepoint(mouse_pos))
        draw_button(quit_rect, "Quit", hovered=quit_rect.collidepoint(mouse_pos),color=(255,80, 70))

        pygame.display.update()
        clock.tick(60)

def manage_winner_actions(result):
    if result == "play_again":
        return "play_again"
    
    elif result == "menu":
        return "menu"

# --- Main Game Loop ---
def main(mode,name1,name2):

    all_sprites = pygame.sprite.Group()
    player1 = Player(get_tile_position(1,Player_Offset[1]),"player1.png",[all_sprites])
    player2 = Player(get_tile_position(1,Player_Offset[2]),"player2.png",[all_sprites])
    dice = Dice((1000, 450),all_sprites)

    running=True
    current_player=1
    cpu_timer=0
    waiting_for_roll = True
    cpu_waiting = False
    status_text="Press SPACE to roll the dice"
    
    menu_button_rect = pygame.Rect(770, 580, 200, 50)
    quit_button_rect = pygame.Rect(1000, 580, 200, 50)

    while running:
        dt = clock.tick()/1000
        mouse_pos = pygame.mouse.get_pos()

        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); exit()
            if e.type==pygame.KEYDOWN and e.key==pygame.K_SPACE:
                if not dice.is_rolling and waiting_for_roll and current_player == 1:
                    dice.start_roll()
                    waiting_for_roll = False
                elif mode == "2player" and current_player == 2:
                    dice.start_roll()
                    waiting_for_roll = False

            
            if e.type ==pygame.MOUSEBUTTONDOWN:
                if menu_button_rect.collidepoint(e.pos):
                    return "menu"
                elif quit_button_rect.collidepoint(e.pos):
                    pygame.quit()
                    exit()

        if mode=="cpu" and current_player == 2 and waiting_for_roll:
            if not player1.moving and not player2.moving and not dice.is_rolling:
                cpu_timer += dt
                if cpu_timer > 1.0:
                    dice.start_roll()
                    waiting_for_roll = False
                    cpu_timer = 0

 
        all_sprites.update(dt)

  
        # Draw all sprites before everything
        display_surf.blit(bg_surf,(0,0))
        pygame.draw.rect(display_surf,(30,30,30),(720,0,560,720))
        pygame.draw.rect(display_surf, (255,255,255), (740,40,500,640), 3)
        
        all_sprites.draw(display_surf)

        #Side Panel
        display_surf.blit(font.render(f"{name1}",True,(255,255,255)),(750,80))
        display_surf.blit(font.render(f"{name2}",True,(255,255,255)),(1050,80))
        display_surf.blit(font.render(f"Dice: {dice.current_value}",True,(200,200,200)),(750,180))
        display_surf.blit(font.render(status_text,True,(255,255,100)),(750,300))
        
        draw_button(menu_button_rect, "Main_Menu", hovered=menu_button_rect.collidepoint(mouse_pos), color=(255, 255, 0))
        draw_button(quit_button_rect, "Quit", hovered=quit_button_rect.collidepoint(mouse_pos), color=(255, 100, 100) )

        # Dice result Handling
        if dice.roll_complete:
            dice.roll_complete = False
            if current_player == 1:
                player1.move(dice.current_value,snakes,ladders)
            else:
                player2.move(dice.current_value, snakes, ladders)


        if not player1.moving and not player2.moving and not dice.is_rolling:
            if player1.current_tile == 100:
                return name1
           
            elif player2.current_tile == 100:
                return name2

            if not waiting_for_roll:
                if dice.current_value == 6:
                    waiting_for_roll = True
                    if current_player == 1:
                        status_text = f"{name1} rolled a 6!, Roll again!"
                    else:
                        status_text = f"{name2} rolled a 6!, Roll again!"
                
                else:
                    current_player = 2 if current_player == 1 else 1
                    waiting_for_roll = True
                    cpu_timer = 0
                    
                    if mode == "cpu" and current_player == 2:
                        status_text = f"{name2} (CPU) is rolling..."
                    elif current_player == 1:
                        status_text = f"{name1}, press SPACE to roll the dice"
                    else:
                        status_text = f"{name2}, press SPACE to roll the dice"

                    
        pygame.display.update()

    pygame.quit()

# --- main is called (Run) ---
if __name__=="__main__":
    while True:
        mode = show_start_menu()
        name1,name2 = get_names(mode)
        while True:

            result = main(mode, name1, name2)

            if result == "menu":
                break

            winner_name = result
            action = winner_screen(winner_name)

            if action == "menu":
                break

            elif action == "play_again":
                continue

            else:
                pygame.quit()
                exit()