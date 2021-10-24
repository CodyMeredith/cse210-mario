import os
from pathlib import Path

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Mario"

# Constants used to scale our sprites from their original size
TILE_SIZE = 48 # Must be multiple of 16
CHARACTER_SCALING = TILE_SIZE / 16
TILE_SCALING = TILE_SIZE / 16
COIN_SCALING = TILE_SIZE / 16
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING
PLAYER_START_X = TILE_SIZE * 6.5
PLAYER_START_Y = TILE_SIZE * 5 + CHARACTER_SCALING

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = TILE_SIZE / 8
ENEMY_MOVEMENT_SPEED = TILE_SIZE/ 24
GRAVITY = 1
PLAYER_JUMP_SPEED = 20
RIGHT_FACING = 0
LEFT_FACING = 1

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 150
RIGHT_VIEWPORT_MARGIN = 150
BOTTOM_VIEWPORT_MARGIN = 100
TOP_VIEWPORT_MARGIN = 100

#Path
SPRITE_DIR = Path(__file__).parent.parent / "sprites"
SOUND_DIR = Path(__file__).parent.parent / "sounds"
MAP_DIR = Path(__file__).parent.parent / "maps"

# Layer Names from our TileMap
LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_COINS = "Coins"
LAYER_NAME_BACKGROUND = "Scenery"
LAYER_NAME_ENEMIES = "Enemies"
LAYER_NAME_PLAYER = "Player"
LAYER_NAME_OBJECTS = "Objects"