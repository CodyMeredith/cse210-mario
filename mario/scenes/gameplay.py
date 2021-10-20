import arcade
from game import constants

class GameplayView(arcade.View):
    """
    
    Stereotype:
        

    Attributes:

    """

    def __init__(self):
        """The class constructor.
        
        Args:

        """
        super().__init__()
        self.physics_engine = None
        self.scene = None
        self.player_sprite = None
        self.camera = None
    
    def setup(self):
        self.camera = arcade.Camera(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        self.scene = arcade.Scene()

        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Floor", use_spatial_hash = True)

        player_sprite_img = "cse210-mario/mario/sprites/mario_small_idle.png"
        floor_sprite_img = "cse210-mario/mario/sprites/floor.png"
        
        #Mario
        self.player_sprite = arcade.Sprite(player_sprite_img, constants.CHARACTER_SCALING)
        self.player_sprite.left = constants.TILE_SIZE
        self.player_sprite.top = (constants.TILE_SIZE * 3) + constants.CHARACTER_SCALING
        self.scene.add_sprite("Player", self.player_sprite)

        #Floor
        for x in range(0, 1250, constants.TILE_SIZE):
            floor = arcade.Sprite(floor_sprite_img, constants.TILE_SCALING)
            floor.left = x
            floor.top = constants.TILE_SIZE
            self.scene.add_sprite("Floor", floor)

            floor = arcade.Sprite(floor_sprite_img, constants.TILE_SCALING)
            floor.left = x
            floor.top = constants.TILE_SIZE * 2
            self.scene.add_sprite("Floor", floor)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.scene.get_sprite_list("Floor"), constants.GRAVITY)

    def on_show(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.csscolor.SKY_BLUE)

    def on_draw(self):
        """Render the screen."""
        arcade.start_render()
        self.camera.use()
        self.scene.draw(pixelated = True)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = constants.PLAYER_JUMP_SPEED
        # Did the user want to pause?
        elif key == arcade.key.ESCAPE:
            # Pass the current view to preserve this view's state
            pause = PauseView(self)
            self.window.show_view(pause)
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -constants.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = constants.PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.LEFT:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def ceneter_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()
        
        self.ceneter_camera_to_player()