import arcade
from game import constants
from scenes.gameplay import GameplayView
from scenes.how_to_play import HowToPlayView

        
class StartView(arcade.View):
    """ Class that manages the 'menu' view. """
    

    def on_show(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.SKY_BLUE)
        # Find the title image in the images folder
        title_image_path = cse210-mario/mario/sprites/image_1.png"

        # Load our title image
        self.title_image = arcade.load_texture(title_image_path)

        # Are we showing the instructions?
        self.show_instructions = False

    def on_update(self, delta_time: float) -> None:
        """Manages the timer to toggle the instructions

        Arguments:
            delta_time -- time passed since last update
        """
        # Toggle whether to show the instructions
        self.show_instructions = not self.show_instructions

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
        if self.show_instructions:
            arcade.draw_text(
                "Enter to Start | I for Instructions",
                start_x=300,
                start_y=200,
                color=arcade.color.BLACK,
                font_size=40,
            )

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
            instructions_view = HowToPlayView()
            self.window.show_view(instructions_view)
