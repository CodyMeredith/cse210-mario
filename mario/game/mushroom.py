import arcade
from game import constants

class Mushroom(arcade.Sprite):
    """
    Set up the Mushroom Sprite

    Stereotype: 
        Information Holder

    Attributes: 
        TODO
    """
    def __init__(self):
        """
        The class constructor

        Args:
            self(Mushroom): an instance of Mushroom
        """
        super().__init__(constants.SPRITE_DIR / "mushroom.png", constants.CHARACTER_SCALING)