import arcade
from game import constants

class PauseView(arcade.View):
    """
    Shown when the game is paused
    
    Stereotype:
        Information Holder

    Attributes:
        TODO
    """

    def __init__(self, game_view: arcade.View) -> None:
        """
        Create the pause screen
        
        Args:
            self (PauseView): an instance of PauseView
            game_view: a reference to the underlying view
        """
        # Initialize the parent
        super().__init__()

        # Store a reference to the underlying view
        self.game_view = game_view

        # Store a semitransparent color to use as an overlay
        self.fill_color = arcade.make_transparent_color(
            arcade.color.WHITE, transparency=150
        )

    def on_draw(self) -> None:
        """Draw the underlying screen, blurred, then the Paused text
        
        Args:
            self (PauseView): an instance of PauseView
            """

        # Now show the Pause text
        self.game_view.on_draw()
        arcade.draw_text("PAUSED", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 + 50,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        # Now create a filled rect that covers the current viewport
        # We get the viewport size from the game view
        arcade.draw_text("Press Esc. to return",
                         constants.SCREEN_WIDTH / 2,
                         constants.SCREEN_HEIGHT / 2,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")
        

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Resume the game when the user presses ESC again

        Arguments:
            key -- Which key was pressed
            modifiers -- What modifiers were active
        """
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)