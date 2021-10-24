from game import constants
from game.character import Character

class PlayerCharacter(Character):
    """Player Sprite"""

    def __init__(self):
        # Set up parent class
        super().__init__("mario_small")

        # Track our state
        self.jumping = False

    def update_animation(self, delta_time: float = 1 / 60):
        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == constants.RIGHT_FACING:
            self.character_face_direction = constants.LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == constants.LEFT_FACING:
            self.character_face_direction = constants.RIGHT_FACING

        # Jumping animation
        if self.change_y > 0 or self.change_y < 0:
            self.texture = self.jump_texture_pair[self.character_face_direction]
            return

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        self.current_texture += 0.2
        if self.current_texture > 3:
            self.current_texture = 0
        self.texture = self.walk_textures[int(self.current_texture)][self.character_face_direction]

    def death_animation(self):
        self.texture = self.fall_texture_pair[self.facing_direction]