import arcade
import random
from game import constants
from game.player_character import PlayerCharacter
from game.goomba import Goomba
from game.coin import Coin
from game.mushroom import Mushroom
from scenes.pauseview import PauseView
from scenes.level_complete import LevelCompelteView

class GameplayView(arcade.View):
    """
    Set up the GameplayView scene

    Stereotype:
        Coordinator

    Attributes:
        TODO
    """

    def __init__(self):
        """
        The class constructor
        
        Args:
            self (GameplayView): an instance of GameplayView
        """
        super().__init__()

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.jump_needs_reset = False
        self.physics_engine = None
        self.scene = None
        self.player_sprite = None
        self.camera = None
        self.gui_camera = None
        self.tile_map = None

        self.score = 0
        self.flag_location = 0
        self.enemy_death_timer = 2
        self.defeated_enemies = []

        self.collect_coint_sound = arcade.load_sound(constants.SOUND_DIR / "collect_coin.wav")
        self.pause_sound = arcade.load_sound(constants.SOUND_DIR / "smb_pause.wav")
        self.jump_small_sound = arcade.load_sound(constants.SOUND_DIR / "jump_small.wav")
        self.jump_big_sound = arcade.load_sound(constants.SOUND_DIR / "jump_big.wav")
        self.gameover_sound = arcade.load_sound(constants.SOUND_DIR / "mario_die.wav")
        self.level_clear_sound = arcade.load_sound(constants.SOUND_DIR / "level_clear.wav")
        self.stomp_sound = arcade.load_sound(constants.SOUND_DIR / "stomp.wav")
        self.bump_sound = arcade.load_sound(constants.SOUND_DIR / "bump.wav")
        self.powerup_sound = arcade.load_sound(constants.SOUND_DIR / "powerup.wav")
        self.powerup_appears_sound = arcade.load_sound(constants.SOUND_DIR / "powerup_appears.wav")
    
    def setup(self):
        """
        Set up the cameras, import the map, initiate variables, set up Mario and enemies and physics engine

        Args:
            self (GameplayView): an instance of GameplayView
        """
        # Set up the Cameras
        self.camera = arcade.Camera(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        self.gui_camera = arcade.Camera(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        
        # Import the tiled map
        map_name = constants.MAP_DIR / "level_1.json"
        layer_options = {
            constants.LAYER_NAME_PLATFORMS: {
                "use_spatial_hash": True,
            },
            constants.LAYER_NAME_OBJECTS: {
                "use_spatial_hash": True,
            },
            constants.LAYER_NAME_COINS: {
                "use_spatial_hash": True,
            },
        }
        self.tile_map = arcade.load_tilemap(map_name, constants.TILE_SCALING, layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Initiate Variables
        self.score = 0
        self.flag_location = 198.5 * constants.TILE_SIZE

        #Mario
        self.player_sprite = PlayerCharacter()
        self.player_sprite.left = constants.PLAYER_START_X
        self.player_sprite.top = constants.PLAYER_START_Y
        self.scene.add_sprite(constants.LAYER_NAME_PLAYER, self.player_sprite)

        # -- Enemies
        enemy_coordinates = [[22, 3], [40, 3], [51, 3], [53, 3], [97,3], [99,3], [107,3], [114, 3], [116,3], [124, 3], [126,3], [128,3], [130,3], [174, 3], [176,3]]

        for i in range(0, enemy_coordinates.__len__()):
            enemy = Goomba()
            enemy.left = enemy_coordinates[i][0] * constants.TILE_SIZE
            enemy.top = enemy_coordinates[i][1] * constants.TILE_SIZE

            direction = random.randint(0, 1)
            if direction == 0:
                enemy.change_x = constants.ENEMY_MOVEMENT_SPEED
            else:
                enemy.change_x = -constants.ENEMY_MOVEMENT_SPEED

            self.scene.add_sprite(constants.LAYER_NAME_ENEMIES, enemy)

        # Set map background color
        if self.tile_map.tiled_map.background_color:
            arcade.set_background_color(self.tile_map.tiled_map.background_color)

        # Set up Physics Engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, [self.scene.get_sprite_list(constants.LAYER_NAME_PLATFORMS), self.scene.get_sprite_list(constants.LAYER_NAME_OBJECTS)], constants.GRAVITY)

    def on_show(self):
        """
        Called when switching to this view
        
        Args:
            self (GameplayView): an instance of GameplayView
        """
        arcade.set_background_color(arcade.csscolor.SKY_BLUE)

    def on_draw(self):
        """Render the screen.
        
        Args:
            self (GameplayView): an instance of GameplayView
        """
        arcade.start_render()
        self.camera.use()
        self.scene.draw(pixelated = True)

        self.gui_camera.use()
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10, constants.SCREEN_HEIGHT - constants.TILE_SIZE / 2, arcade.csscolor.WHITE, 18)

    def process_keychange(self):
        """
        Called when we change a key up/down or we move on/off a ladder.

        Args:
            self (GameplayView): an instance of GameplayView
        """
        # Process jump
        if self.up_pressed and self.physics_engine.can_jump(y_distance = 10) and not self.jump_needs_reset:
            self.player_sprite.change_y = constants.PLAYER_JUMP_SPEED
            self.jump_needs_reset = True
            if self.player_sprite.mario_lives == 0:
                arcade.play_sound(self.jump_small_sound)
            else:
                arcade.play_sound(self.jump_big_sound)

        # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = constants.PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -constants.PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed.
        
        Args:
            self (GameplayView): an instance of GameplayView
            key:
            modifiers: what modifiers were active
        """

        if key == arcade.key.SPACE:
            self.up_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        # Did the user want to pause?
        elif key == arcade.key.ESCAPE:
            arcade.play_sound(self.pause_sound)
            # Pass the current view to preserve this view's state
            pause = PauseView(self)
            self.window.show_view(pause)

        self.process_keychange()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key.
        
        Args:
            self (GameplayView): an instance of GameplayView
        """

        if key == arcade.key.SPACE:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

        self.process_keychange()

    def ceneter_camera_to_player(self):
        """
        Center the screen on the current player

        Args:
            self (GameplayView): an instance of GameplayView
        """
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        """
        Movement and game logic
        
        Args:
            self (GameplayView): an instance of GameplayView
            delta_time: time passed since last update
        """

        # Move the player with the physics engine
        self.physics_engine.update()

        # Update animations
        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False
        else:
            self.player_sprite.can_jump = True

        # Update Animations
        self.scene.update_animation(delta_time, [constants.LAYER_NAME_COINS, constants.LAYER_NAME_BACKGROUND, constants.LAYER_NAME_PLAYER, constants.LAYER_NAME_ENEMIES])

        # Update enemies
        self.scene.update([constants.LAYER_NAME_ENEMIES])

        for enemy in self.scene.get_sprite_list(constants.LAYER_NAME_ENEMIES):
            enemy_collision_list = arcade.check_for_collision_with_list(enemy, self.scene.get_sprite_list(constants.LAYER_NAME_OBJECTS))

            for collision in enemy_collision_list:
                if self.scene.get_sprite_list(constants.LAYER_NAME_OBJECTS) in collision.sprite_lists:
                    enemy.change_x = -enemy.change_x

        # Check to see if player collided with any enemies
        enemy_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene.get_sprite_list(constants.LAYER_NAME_ENEMIES))

        for enemy in enemy_hit_list:
            if self.player_sprite.bottom >= enemy.top - (constants.TILE_SIZE / 2):
                arcade.play_sound(self.stomp_sound)
                enemy.death_animation()
            elif not self.player_sprite.invulnerable:
                if self.player_sprite.get_mario_lives() > 0:
                    self.player_sprite.shrink_mario()
                    arcade.play_sound(self.bump_sound)
                    self.player_sprite.invulnerable = True
                else:
                    self.player_sprite.death_animation()
                    arcade.play_sound(self.gameover_sound)
                    loss = LevelCompelteView(self, "GAME OVER")
                    self.window.show_view(loss)

        # # Check to see if player collided with any Mystery Boxes
        for box in self.scene.get_sprite_list(constants.LAYER_NAME_MYSTERY_BOXES):
            if self.player_sprite.top == box.bottom - 3:
                if (self.player_sprite.center_x > box.center_x - (constants.TILE_SIZE / 2)) and (self.player_sprite.center_x < box.center_x + (constants.TILE_SIZE / 2)):
                    rand = random.randint(1, 10)
                    box.remove_from_sprite_lists()

                    if rand == 1:
                        arcade.play_sound(self.powerup_appears_sound)
                        mushroom = Mushroom()
                        mushroom.center_x = box.center_x
                        mushroom.center_y = box.center_y + constants.TILE_SIZE
                        self.scene.add_sprite(constants.LAYER_NAME_MUSHROOMS, mushroom)
                    else:
                        arcade.play_sound(self.collect_coint_sound)
                        coin = Coin()
                        coin.center_x = box.center_x
                        coin.center_y = box.center_y + constants.TILE_SIZE + 2
                        self.scene.add_sprite(constants.LAYER_NAME_COINS, coin)


        # Check to see if player collided with any Coins
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene.get_sprite_list(constants.LAYER_NAME_COINS))

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coint_sound)
            self.score += 1

        # Check to see if player collided with any Mushrooms
        mushroom_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene.get_sprite_list(constants.LAYER_NAME_MUSHROOMS))

        for mushroom in mushroom_hit_list:
            mushroom.remove_from_sprite_lists()
            arcade.play_sound(self.powerup_sound)
            self.player_sprite.grow_mario()

        # Check if player fell off the map
        if self.player_sprite.top < - 100:
            # self.player_sprite.left = constants.PLAYER_START_X
            # self.player_sprite.top = constants.PLAYER_START_Y
            arcade.play_sound(self.gameover_sound)
            loss = LevelCompelteView(self, "GAME OVER")
            self.window.show_view(loss)

        # Check if player reached the end of the level
        if self.player_sprite.center_x >= self.flag_location:
            arcade.play_sound(self.level_clear_sound)
            win = LevelCompelteView(self, "LEVEL CLEAR")
            self.window.show_view(win)

        # Center the camera on the player
        self.ceneter_camera_to_player()