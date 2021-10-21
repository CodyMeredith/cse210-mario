import arcade
from game import constants
from scenes.pauseview import PauseView
from scenes.loss import LossView
from scenes.win import WinView

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
        self.gui_camera = None
        self.tile_map = None

        self.score = 0
        self.end_of_map = 0

        self.collect_coint_sound = arcade.load_sound(constants.SOUND_DIR / "collect_coin.wav")
        self.jump_sound = arcade.load_sound(constants.SOUND_DIR / "jump_small.wav")
        self.gameover_sound = arcade.load_sound(constants.SOUND_DIR / "gameover.wav")
    
    def setup(self):
        # Set up the Cameras
        self.camera = arcade.Camera(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        self.gui_camera = arcade.Camera(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        
        # Import the tiled map
        map_name = constants.MAP_DIR / "level_1.json"
        layer_options = {
            constants.LAYER_NAME_PLATFORMS: {
                "use_spatial_hash": True,
            },
            constants.LAYER_NAME_COINS: {
                "use_spatial_hash": True,
            },
            constants.LAYER_NAME_DONT_TOUCH: {
                "use_spatial_hash": True,
            },
        }
        self.tile_map = arcade.load_tilemap(map_name, constants.TILE_SCALING, layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Initiate Variables
        self.score = 0

        #Mario
        player_sprite_img = constants.SPRITE_DIR / "mario_small_idle.png"
        self.player_sprite = arcade.Sprite(player_sprite_img, constants.CHARACTER_SCALING)
        self.player_sprite.left = constants.PLAYER_START_X
        self.player_sprite.top = constants.PLAYER_START_Y
        self.scene.add_sprite("Player", self.player_sprite)

        # Calculate right edge of map
        self.end_of_map = self.tile_map.tiled_map.map_size.width * constants.GRID_PIXEL_SIZE

        # Set map background color
        if self.tile_map.tiled_map.background_color:
            arcade.set_background_color(self.tile_map.tiled_map.background_color)

        # Set up Physics Engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.scene.get_sprite_list("Platforms"), constants.GRAVITY)

    def on_show(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.csscolor.SKY_BLUE)

    def on_draw(self):
        """Render the screen."""
        arcade.start_render()
        self.camera.use()
        self.scene.draw(pixelated = True)

        self.gui_camera.use()
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10, constants.SCREEN_HEIGHT - constants.TILE_SIZE / 2, arcade.csscolor.WHITE, 18)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = constants.PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
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

        # Check to see if player collided with any coins, remove them from the game, and play a sound
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene.get_sprite_list("Coins"))

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coint_sound)
            self.score += 1

        # Check if player fell off the map
        if self.player_sprite.top < - 100:
            # self.player_sprite.left = constants.PLAYER_START_X
            # self.player_sprite.top = constants.PLAYER_START_Y
            arcade.play_sound(self.gameover_sound)
            loss = LossView(self)
            self.window.show_view(loss)


        # Center the camera on the player
        self.ceneter_camera_to_player()