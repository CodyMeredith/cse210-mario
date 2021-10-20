import os

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Mario"

# Constants used to scale our sprites from their original size
TILE_SIZE = 48 # Must be multiple of 16
CHARACTER_SCALING = TILE_SIZE / 16
TILE_SCALING = TILE_SIZE / 16
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = TILE_SIZE / 8
GRAVITY = 1
PLAYER_JUMP_SPEED = 25

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 150
RIGHT_VIEWPORT_MARGIN = 150
BOTTOM_VIEWPORT_MARGIN = 100
TOP_VIEWPORT_MARGIN = 100

#Path
PATH = os.path.dirname(os.path.abspath(__file__))