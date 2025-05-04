# test_scoreboard_draw.py
import pygame
import pytest
from unittest.mock import MagicMock, patch

# Assume constants.py exists in the same directory or is accessible
import constants

# Import the class to test
from main import Scoreboard

# Mock pygame dependencies that are used in Scoreboard.__init__
@pytest.fixture(autouse=True)
def mock_pygame_font(mocker):
    """Automatically mock pygame.font.SysFont for all tests."""
    mock_font = MagicMock()
    mock_font.render.return_value = MagicMock(spec=pygame.Surface)
    mock_font.render.return_value.get_rect.return_value = MagicMock(spec=pygame.Rect, topleft=(10, 10)) # Set a default rect
    mocker.patch('pygame.font.SysFont', return_value=mock_font)
    # Mock render globally within the font mock to simplify things
    mocker.patch.object(mock_font, 'render', return_value=mock_font.render.return_value)
    yield mock_font # Provide the mock font object if needed, though SysFont itself is patched

@pytest.fixture
def scoreboard_instance():
    """Creates a default Scoreboard instance for testing."""
    # __init__ calls _render_text which uses self.font.render
    # mock_pygame_font fixture handles mocking font and render
    return Scoreboard()

# --- Test Cases ---

def test_draw_current_score(scoreboard_instance, mock_pygame_font):
    """
    Test Case: Draw Current Score
    Verification: Checks that screen.blit is called with the correct image and rect.
    """
    # Arrange
    mock_screen = MagicMock(spec=pygame.Surface)
    # Get the initial image and rect created during __init__
    expected_image = scoreboard_instance.image
    expected_rect = scoreboard_instance.rect

    # Act
    scoreboard_instance.draw(mock_screen)

    # Assert
    mock_screen.blit.assert_called_once_with(expected_image, expected_rect)
    # Also check that the initial render happened correctly
    mock_pygame_font.render.assert_called_with("Score: 0", True, constants.BLACK)


def test_draw_after_update(scoreboard_instance, mock_pygame_font):
    """
    Test Case: Draw Score After Update
    Verification: Checks that screen.blit is called with the updated image and rect after score changes.
    """
    # Arrange
    mock_screen = MagicMock(spec=pygame.Surface)

    # Simulate score update (making sure score changes)
    current_time = 1000 # ms
    start_time = 0    # ms
    expected_new_score = 100 # 1000 // 10
    expected_text = f"Score: {expected_new_score}"

    # --- Mocking render result for the UPDATE step ---
    # Create a new mock surface/rect specifically for the update render call
    updated_surface = MagicMock(spec=pygame.Surface)
    updated_rect = MagicMock(spec=pygame.Rect, topleft=(scoreboard_instance.x, scoreboard_instance.y)) # Use original coords
    updated_surface.get_rect.return_value = updated_rect
    # Make the font mock return this *new* surface on the *next* render call
    mock_pygame_font.render.return_value = updated_surface
    # --- End Mocking render result ---

    scoreboard_instance.update(current_time, start_time) # Score should become 100

    # Act
    scoreboard_instance.draw(mock_screen) # Draw after the update

    # Assert
    # Check render was called twice: once in init, once in update
    assert mock_pygame_font.render.call_count == 2
    # Check the update render call had the correct text
    mock_pygame_font.render.assert_called_with(expected_text, True, constants.BLACK)
    # Check blit was called with the *updated* image and rect from the update step
    mock_screen.blit.assert_called_once_with(updated_surface, updated_rect)
    # Verify the instance's image/rect were updated
    assert scoreboard_instance.image == updated_surface
    assert scoreboard_instance.rect == updated_rect
