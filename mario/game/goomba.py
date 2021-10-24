from game import constants
from game.character import Character

class Goomba(Character):
    """Goomba Sprite"""

    def __init__(self):
        # Set up parent class
        super().__init__("goomba")

    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.facing_direction == constants.RIGHT_FACING:
            self.facing_direction = constants.LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == constants.LEFT_FACING:
            self.facing_direction = constants.RIGHT_FACING

        # Walking animation
        if self.change_x > 0:
            self.current_texture += .05
            if self.current_texture > 2:
                self.current_texture = 0
            self.texture = self.walk_textures[int(self.current_texture)][self.facing_direction]
            return

    def death_animation(self):
        self.change_x = 0
        self.hit_box = None
        self.texture = self.fall_texture_pair[self.facing_direction]