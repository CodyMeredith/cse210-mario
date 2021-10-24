import arcade
from game import constants
from scenes.gameplay import GameplayView

class StartView(arcade.View):
    """ Class that manages the 'menu' view. """
    def __init__(self) -> None:
        super().__init__()
         # Set our display timer
        self.display_timer = 0.5

        # Are we showing the instructions?
        self.show_text = False
        self.show_instructions = False

    def on_show(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.SKY_BLUE)
        # Find the title image in the images folder
        title_image_path = constants.SPRITE_DIR / "SMB_logo.png"

        # Load our title image
        self.title_image = arcade.load_texture(title_image_path)

        # Are we showing the instructions?
        self.show_instructions = False

    def on_draw(self):

        # Start the rendering loop
        arcade.start_render()

        # Draw a rectangle filled with our title image
        arcade.draw_texture_rectangle(
            center_x=constants.SCREEN_WIDTH / 2,
            center_y=constants.SCREEN_HEIGHT / 1.5,
            width=400,
            height=300,
            texture=self.title_image,
        )

        # Should we show our instructions?
        if self.show_text:
            if not self.show_instructions:
                arcade.draw_text(
                    "Enter to Start | I for Instructions",
                    start_x=300,
                    start_y=200,
                    color=arcade.color.BLACK,
                    font_size=40,
                )
            else:
                arcade.draw_text("How to Play", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2 - 125,
                    arcade.color.BLACK, font_size = 40, anchor_x = "center")
                arcade.draw_text("->Use left and right arrow keys to move", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2 - 175,
                    arcade.color.BLACK, font_size= 20, anchor_x = "center")
                arcade.draw_text("->Spacebar to jump", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2 - 225,
                    arcade.color.BLACK, font_size= 20, anchor_x = "center")
                arcade.draw_text("->Press Enter to play", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2 - 275,
                    arcade.color.BLACK, font_size= 20, anchor_x = "center")
            
    def on_update(self, delta_time: float) -> None:
        """Manages the timer to toggle the instructions

        Arguments:
            delta_time -- time passed since last update
        """
        self.display_timer -= delta_time

        # If the timer has run out, we toggle the instructions
        if self.display_timer < 0 and self.show_instructions == False:
            # Toggle whether to show the instructions
            self.show_text = not self.show_text
            # And reset the timer so the instructions flash slowly
            self.display_timer = 1.0


    def on_key_press(self, key: int, modifiers: int) -> None:
        """Resume the game when the user presses ESC again

        Arguments:
            key -- Which key was pressed
            modifiers -- What modifiers were active
        """
        
        if key == arcade.key.RETURN:
            game_view = GameplayView()
            game_view.setup()
            self.window.show_view(game_view)
        elif key == arcade.key.I:
            self.show_text = True
            self.show_instructions = True
            self.on_draw()