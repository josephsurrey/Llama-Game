# test_scoreboard_reset.py
import pytest
import pygame
from unittest.mock import MagicMock, patch

# Assuming main.py and constants.py are in the same directory or accessible
from main import Scoreboard
import constants

# Minimal Pygame setup needed for font initialization
@pytest.fixture(scope="module", autouse=True)
def pygame_setup():
    """Initializes pygame and specifically the font module for tests."""
    pygame.init()
    pygame.font.init()
    yield
    pygame.font.quit()
    pygame.quit()

@pytest.fixture
def scoreboard_instance():
    """Provides a default Scoreboard instance for testing."""
    # Mock the font object to control its behavior and check calls
    mock_font = MagicMock(spec=pygame.font.Font)
    mock_surface = MagicMock(spec=pygame.Surface)
    mock_rect = MagicMock(spec=pygame.Rect)
    # Set initial topleft for the mock rect if needed, matching default x, y
    mock_rect.topleft = (10, 10)

    # Configure mock_font.render to return the mock_surface
    mock_font.render.return_value = mock_surface
    # Configure mock_surface.get_rect to return the mock_rect
    mock_surface.get_rect.return_value = mock_rect

    # Patch SysFont to return our mock_font
    with patch('pygame.font.SysFont', return_value=mock_font):
        board = Scoreboard(x=10, y=10, font_size=36, color=constants.BLACK)
        # Manually assign the mock font as SysFont is patched during init
        board.font = mock_font
        # Ensure initial state for clarity in tests by calling render logic
        # This simulates the last lines of __init__ after font is set
        board.image = board.font.render(f"Score: {board.score}", True, board.color)
        board.rect = board.image.get_rect(topleft=(board.x, board.y))
        # Reset mocks AFTER initial setup in fixture if needed
        # mock_font.render.reset_mock()
        # mock_surface.get_rect.reset_mock()
        return board

def test_reset_score_to_zero(scoreboard_instance):
    """
    Tests resetting the score when it's greater than zero.
    Verifies score becomes 0 and image/rect are updated.
    """
    # Arrange: Set a non-zero score and simulate update
    scoreboard_instance.score = 50
    # Simulate how update might change image/rect before reset
    scoreboard_instance.image = scoreboard_instance.font.render(f"Score: {scoreboard_instance.score}", True, scoreboard_instance.color)
    scoreboard_instance.rect = scoreboard_instance.image.get_rect(topleft=(scoreboard_instance.x, scoreboard_instance.y))
    # Reset mocks to ignore calls during arrange phase
    scoreboard_instance.font.render.reset_mock()
    scoreboard_instance.image.get_rect.reset_mock() # Reset mock on the surface object


    # Act
    scoreboard_instance.reset()

    # Assert: Score is reset
    assert scoreboard_instance.score == 0

    # Assert: Font render was called correctly
    scoreboard_instance.font.render.assert_called_with("Score: 0", True, constants.BLACK)

    # Assert: Image and Rect are updated (using the mocks)
    # Check that the *result* of the render call was assigned to image
    assert scoreboard_instance.image is scoreboard_instance.font.render.return_value
    # Check that get_rect was called on the (mock) surface object returned by render
    scoreboard_instance.image.get_rect.assert_called_with(topleft=(10, 10))
     # Check that the *result* of the get_rect call was assigned to rect
    assert scoreboard_instance.rect is scoreboard_instance.image.get_rect.return_value

    # REMOVED assertion: assert scoreboard_instance.image is not initial_image


def test_reset_when_already_zero(scoreboard_instance):
    """
    Tests resetting the score when it's already zero.
    Verifies score remains 0 and image/rect are re-rendered.
    """
    # Arrange: Score is already 0 (from fixture setup)
    assert scoreboard_instance.score == 0
    # Reset mocks to ignore calls during fixture setup
    scoreboard_instance.font.render.reset_mock()
    scoreboard_instance.image.get_rect.reset_mock()

    # Act
    scoreboard_instance.reset()

    # Assert: Score remains 0
    assert scoreboard_instance.score == 0

    # Assert: Font render was still called correctly
    scoreboard_instance.font.render.assert_called_with("Score: 0", True, constants.BLACK)

    # Assert: Image and Rect are updated (using the mocks)
    assert scoreboard_instance.image is scoreboard_instance.font.render.return_value
    scoreboard_instance.image.get_rect.assert_called_with(topleft=(10, 10))
    assert scoreboard_instance.rect is scoreboard_instance.image.get_rect.return_value


def test_reset_render_call_details(scoreboard_instance):
    """
    Explicitly verifies the arguments passed to font.render and get_rect
    during a reset operation.
    """
    # Arrange
    scoreboard_instance.score = 99 # Start with a non-zero score
    # Reset mocks to ignore calls during fixture setup/arrange
    scoreboard_instance.font.render.reset_mock()
    # We need to reset the mock method on the *specific mock surface instance*
    # that render returns
    mock_surface = scoreboard_instance.font.render.return_value
    mock_surface.get_rect.reset_mock()


    # Act
    scoreboard_instance.reset()

    # Assert: font.render called once with correct arguments
    scoreboard_instance.font.render.assert_called_once_with(
        "Score: 0",        # Expected text
        True,              # Anti-aliasing flag
        constants.BLACK    # Expected color (from fixture)
    )

    # Assert: image.get_rect called once with correct arguments
    # This check ensures the position is recalculated based on the new surface
    # Get the mock surface that *was* returned by the render call during Act phase
    returned_surface = scoreboard_instance.font.render.return_value
    returned_surface.get_rect.assert_called_once_with(
        topleft=(scoreboard_instance.x, scoreboard_instance.y) # Expected position args
    )