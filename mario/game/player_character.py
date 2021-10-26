from game import constants
from game.character import Character

class PlayerCharacter(Character):
    """Player Sprite
    
    Stereotype:
        Informaiton Holder

    Attributes:
        TODO
    """

    def __init__(self):
        """
        Set up the parent class

        Args:
            self(PlayerCharacter): an instance of PlayerCharacter
        """
        # Set up parent class
        self.mario_state = "mario_small"
        self.mario_lives = 0
        super().__init__(self.mario_state)

        # Track our state
        self.jumping = False
        self.invulnerable = False
        self.invulnerable_timer = 5

    def update_animation(self, delta_time: float = 1 / 60):
        """
        PlayerCharacter animation updates

        Args:
            self(PlayerCharacter): an instance of PlayerCharacter
            delta_time:
        """
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

        # Remove invulnerability
        if self.invulnerable == True:
            self.invulnerable_timer -= .1
            if self.invulnerable_timer < 0:
                self.invulnerable = False
            
    def death_animation(self):
        """
        Animation when PlayerCharacter dies

        Args:
            self(PlayerCharacter): an instance of PlayerCharacter
        """
        self.texture = self.fall_texture_pair[self.facing_direction]
    
    def grow_mario(self):
        """
        Animation on power up

        Args:
            self(PlayerCharacter): an instance of PlayerCharacter
        """
        self.mario_state = "mario_big"
        self.mario_lives = 1
        self.load_character_textures(self.mario_state)

    def shrink_mario(self):
        """
        Animation for shrinking down to normal size

        Args:
            self(PlayerCharacter): an instance of PlayerCharacter
        """
        self.mario_state = "mario_small"
        self.mario_lives = 0
        self.load_character_textures(self.mario_state)

    def get_mario_lives(self):
        """
        Retrieving the number of lives for PlayerCharacter

        Args:
            self(PlayerCharacter): an instance of PlayerCharacter
        """
        return self.mario_lives