
import pytest
import pygame
from project import get_tile_position, Player, manage_winner_actions, snakes, ladders

snakes = {17: 7, 62: 19, 54: 34, 64: 60, 87: 36, 93: 73, 94: 75, 98: 79}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 94, 51: 67, 72: 91, 80: 99}

@pytest.fixture(scope="module")
def setup_pygame():
    pygame.init()
    yield
    pygame.quit()

@pytest.fixture
def player(setup_pygame):
    group = pygame.sprite.Group()
    return Player(get_tile_position(1), 'player1.png', group)

def test_get_tile_position():
    assert get_tile_position(1) == (36, 684)
    assert get_tile_position(11) == (684, 612)
    assert get_tile_position(2) == (108, 684)
    assert get_tile_position(15) == (396, 612)

def test_basic_move(player):
    player.current_tile = 1
    player.move(4, snakes, ladders)
    assert player.current_tile == 5 # The player moves 4 steps from tile 1.

def test_ladder_up(player):
    player.current_tile = 4
    player.move(0, snakes, ladders)
    assert player.current_tile == 14 # The player jumps from tile 4 to 14.

def test_snake_down(player):
    player.current_tile = 54
    player.move(0, snakes, ladders)
    assert player.current_tile == 34 # The player slides down from tile 54 to  34.

def test_after_100(player):
    player.current_tile = 95
    player.move(6, snakes, ladders)
    assert player.current_tile == 100 # The player stops at 100 and doesn't go beyond or falls back.

def test_correct_position(player):
    player.current_tile = 15
    player.move(0, snakes, ladders)
    expected_pos = get_tile_position(15, player.offset)
    assert player.rect.center == expected_pos #Tile position must match player_rect center

def test_manage_winner_actions_play_again():
    action = manage_winner_actions("play_again")
    assert action == "play_again"

def test_manage_winner_action_menu():
    action = manage_winner_actions("menu")
    assert action == "menu"

def test_manage_winner_actions_invalid():
    action = manage_winner_actions("invalid")
    assert action is None
