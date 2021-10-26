import arcade
from game import constants

class Character(arcade.Sprite):
    def __init__(self, character_name):
        super().__init__()

        # Default to facing right
        self.facing_direction = constants.RIGHT_FACING

        # Used for image sequences
        self.current_texture = 0
        self.scale = constants.CHARACTER_SCALING
        self.character_face_direction = constants.RIGHT_FACING

        self.load_character_textures(character_name)


    def load_texture_pair(directory, filename):
        """
        Load a texture pair, with the second being a mirror image.
        """
        return [arcade.load_texture(filename), arcade.load_texture(filename, flipped_horizontally=True)]

    def load_character_textures(self, character_name):
        self.idle_texture_pair = self.load_texture_pair(constants.SPRITE_DIR / f"{character_name}_idle.png")
        self.jump_texture_pair = self.load_texture_pair(constants.SPRITE_DIR / f"{character_name}_jump.png")
        self.fall_texture_pair = self.load_texture_pair(constants.SPRITE_DIR / f"{character_name}_fall.png")

        # Load textures for walking
        self.walk_textures = []
        self.walk_textures.append(self.load_texture_pair(constants.SPRITE_DIR / f"{character_name}_walk1.png"))
        self.walk_textures.append(self.load_texture_pair(constants.SPRITE_DIR / f"{character_name}_walk2.png"))
        self.walk_textures.append(self.load_texture_pair(constants.SPRITE_DIR / f"{character_name}_walk3.png"))

        # Set the initial texture and hit box
        self.texture = self.idle_texture_pair[0]
        self.hit_box = self.texture.hit_box_points