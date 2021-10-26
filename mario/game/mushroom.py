import arcade
from game import constants

class Mushroom(arcade.Sprite):
    def __init__(self):
        super().__init__(constants.SPRITE_DIR / "mushroom.png", constants.CHARACTER_SCALING)