import pytest
from unittest.mock import patch, MagicMock
import pygame

# Assuming constants.py and main.py (with Scoreboard class) are accessible
import constants
# Make sure the path to main is correct if it's not in the same directory
# e.g., from ..src import main if tests are in a separate folder
from main import Scoreboard

# Minimal Pygame setup needed for font initialization if not mocking everything
# We use autouse=True to ensure it runs before tests in this module
# scope="module" means it runs once per module
@pytest.fixture(scope="module", autouse=True)
def pygame_setup():
    """Initializes Pygame modules needed for the tests."""
    pygame.init()
    pygame.font.init()  # Explicitly needed for SysFont
    yield
    pygame.font.quit()
    pygame.quit()

# Fixture to create a reusable mock font object
@pytest.fixture
def mock_font():
    """Provides a MagicMock simulating a pygame.font.Font object."""
    # spec=pygame.font.Font helps mock behave more like the real object
    font = MagicMock(spec=pygame.font.Font)
    # If _render_text were implemented and used font methods, mock them here:
    # e.g., font.render = MagicMock(return_value=MagicMock(spec=pygame.Surface))
    # e.g., font.size = MagicMock(return_value=(10, 10))
    return font

# Test Suite for Scoreboard.__init__
class TestScoreboardInit:

    # Patch pygame.font.SysFont where it's used (in the 'main' module)
    # Patch Scoreboard._render_text to check its call without executing its (empty) body
    @patch('main.pygame.font.SysFont')
    @patch.object(Scoreboard, '_render_text')
    def test_initialization_defaults(self, mock_render_text, mock_sysfont, mock_font):
        """
        Tests Scoreboard initialization with default arguments.
        Verifies attributes, font creation call, and _render_text call.
        """
        # Set the return value for the mocked SysFont
        mock_sysfont.return_value = mock_font

        # Instantiate the class
        scoreboard = Scoreboard()

        # --- Assertions ---
        # Check basic attributes are set to defaults
        assert scoreboard.x == 10, "Default x position should be 10"
        assert scoreboard.y == 10, "Default y position should be 10"
        assert scoreboard.color == constants.BLACK, "Default color should be BLACK"
        assert scoreboard.score == 0, "Initial score should be 0"

        # Check font initialization call and assignment
        mock_sysfont.assert_called_once_with(None, 36) # Default font size is 36
        assert scoreboard.font is mock_font, "Font attribute should hold the mock font object"

        # Check _render_text was called
        mock_render_text.assert_called_once_with()

    @patch('main.pygame.font.SysFont')
    @patch.object(Scoreboard, '_render_text')
    def test_initialization_custom_args(self, mock_render_text, mock_sysfont, mock_font):
        """
        Tests Scoreboard initialization with custom arguments.
        Verifies attributes, font creation call, and _render_text call.
        """
        # Define custom arguments
        custom_x = 50
        custom_y = 60
        custom_font_size = 48
        custom_color = constants.RED # Use a constant for clarity

        # Configure mock and instantiate
        mock_sysfont.return_value = mock_font
        scoreboard = Scoreboard(
            x=custom_x,
            y=custom_y,
            font_size=custom_font_size,
            color=custom_color
        )

        # --- Assertions ---
        # Check attributes are set to custom values
        assert scoreboard.x == custom_x, f"Custom x position should be {custom_x}"
        assert scoreboard.y == custom_y, f"Custom y position should be {custom_y}"
        assert scoreboard.color == custom_color, f"Custom color should be {custom_color}"
        assert scoreboard.score == 0, "Initial score should still be 0"

        # Check font initialization with custom size
        mock_sysfont.assert_called_once_with(None, custom_font_size)
        assert scoreboard.font is mock_font, "Font attribute should hold the mock font object"

        # Check _render_text was called
        mock_render_text.assert_called_once_with()

    @patch('main.pygame.font.SysFont')
    @patch.object(Scoreboard, '_render_text') # Still need to patch _render_text
    def test_font_object_creation(self, mock_render_text, mock_sysfont, mock_font):
        """
        Verifies pygame.font.SysFont is called correctly (using defaults)
        and the result is stored in self.font.
        """
        mock_sysfont.return_value = mock_font
        scoreboard = Scoreboard() # Use defaults for this specific check

        # Verify the call to SysFont
        mock_sysfont.assert_called_once_with(None, 36) # Default font size

        # Verify the font attribute holds the mocked object
        assert scoreboard.font is mock_font, "self.font should contain the object returned by SysFont"

    @patch('main.pygame.font.SysFont') # Still need to patch SysFont
    @patch.object(Scoreboard, '_render_text')
    def test_render_text_call_verification(self, mock_render_text, mock_sysfont, mock_font):
        """
        Verifies specifically that the _render_text method is called
        exactly once during initialization.
        """
        # Need to provide a return value for SysFont even if not the focus
        mock_sysfont.return_value = mock_font

        # Instantiate the class
        scoreboard = Scoreboard()

        # Verify _render_text was called exactly once
        mock_render_text.assert_called_once_with()
        assert mock_render_text.call_count == 1, "_render_text should be called exactly once"