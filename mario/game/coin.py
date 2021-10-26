import arcade
from game import constants

class Coin(arcade.Sprite):
    """
    Set up the coin sprite

    Stereotype:
        Information Holder

    Attributes:
        TODO    
    """
    def __init__(self):
        """
        The class constructor

        Args:
            self (Character): an instance of the Character
        """
        super().__init__()

        self.current_texture = 0
        self.scale = constants.CHARACTER_SCALING

        self.coin_sprites = []
        for i in range(1, 5):
            self.coin_sprites.append(arcade.load_texture(constants.SPRITE_DIR / f"coin{i}.png"))

        self.texture = self.coin_sprites[0]
        self.hit_box = self.texture.hit_box_points

    def update_animation(self, delta_time: float = 1 / 60):
        """
        Coin animation method

        Args:
            self (Character): an instance of the Character
            delta_time: time passed since last update        
        """
        # Coin animation
        self.current_texture += .1
        if self.current_texture > 4:
            self.current_texture = 0
        self.texture = self.coin_sprites[int(self.current_texture)]
        return