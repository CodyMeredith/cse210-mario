import arcade
from game import constants
from scenes.gameplay import GameplayView

class HowToPlayView(arcade.View):
    def __init__(self) -> None:
        """Create the Instructions screen"""
        # Initialize the parent
        super().__init__()

        # # Store a reference to the underlying view
        # self.game_view = game_view

    """ Class to manage the how to play view """
    def on_show(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def on_draw(self):
        """ Draw the instruction screen view """
        arcade.start_render()
        arcade.draw_text("How to Play", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2,
            arcade.color.BLACK, font_size = 40, anchor_x = "center")
        arcade.draw_text("->Use left and right arrow keys to move", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2-50,
            arcade.color.BLACK, font_size= 20, anchor_x = "center")
        arcade.draw_text("->Spacebar to jump", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2-100,
            arcade.color.BLACK, font_size= 20, anchor_x = "center")
        arcade.draw_text("->Press Enter to play", constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2-150,
            arcade.color.BLACK, font_size= 20, anchor_x = "center")

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Return to the start menu when the user presses Enter
        Arguments:
            key -- Which key was pressed
            modifiers -- What modifiers were active
        """
        if key == arcade.key.RETURN:
            gameplay_view = GameplayView()
            gameplay_view.setup()
            self.window.show_view(gameplay_view)
