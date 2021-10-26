import arcade
from game import constants

class LevelCompelteView(arcade.View):
    """
    Shown when the game is paused
    
    Stereotype:
        Information Holder

    """

    def __init__(self, game_view: arcade.View, endText) -> None:
        """
        Create the pause screen
        
        Args:
            self (LevelCompleteView): an instance of LevelCompleteView
        """
        # Initialize the parent
        super().__init__()

        # Store a reference to the underlying view
        self.game_view = game_view

        # Store a semitransparent color to use as an overlay
        self.fill_color = arcade.make_transparent_color(
            arcade.color.WHITE, transparency=150
        )

        # Store the passed in end game text
        self.end_text = endText

    def on_draw(self) -> None:
        """
        Draw the underlying screen, blurred, then the Game Over text
        
        Args:
            self (LevelCompleteView): an instance of LevelCompleteView
        """

        # Show the Level Clear text
        self.game_view.on_draw()
        arcade.draw_text(self.end_text, constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 + 50,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("ENTER TO PLAY AGAIN", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=25, anchor_x="center")
        arcade.draw_text("ESC TO EXIT", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 - 50,
                         arcade.color.BLACK, font_size=25, anchor_x="center")
        

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Resume the game when the user presses ESC again

        Arguments:
            key -- Which key was pressed
            modifiers -- What modifiers were active
        """
        if key == arcade.key.ENTER:
            self.game_view.setup()
            self.window.show_view(self.game_view)
        if key == arcade.key.ESCAPE:
            arcade.exit()