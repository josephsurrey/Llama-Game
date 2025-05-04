import pytest
from unittest.mock import MagicMock, patch
import sys

# Assume constants.py is in the same directory or accessible path
import constants

# --- Mocking Setup ---
# Create mocks for pygame elements BEFORE importing main
mock_font_surface = MagicMock()
mock_font_surface.get_rect.return_value = MagicMock(topleft=(0, 0)) # Mock rect object

mock_font = MagicMock()
mock_font.render.return_value = mock_font_surface

# Mock the font module and its functions
mock_pygame_font = MagicMock()
mock_pygame_font.SysFont.return_value = mock_font
mock_pygame_font.init = MagicMock() # Mock init() to prevent error
mock_pygame_font.Font = MagicMock(return_value=mock_font) # Mock Font class as well

# Prepare all necessary pygame mocks
pygame_modules = {
    "pygame": MagicMock(),
    "pygame.font": mock_pygame_font, # Use our detailed font mock
    "pygame.sprite": MagicMock(),
    "pygame.Surface": MagicMock(),
    "pygame.Rect": MagicMock(),
    "pygame.image": MagicMock(),
    "pygame.mask": MagicMock(),
    "pygame.mixer": MagicMock(),
    "pygame.time": MagicMock(),
    "pygame.display": MagicMock(),
    "pygame.event": MagicMock(), # Added event mock just in case
}

# Ensure base pygame.init is also mocked if needed by other parts
pygame_modules["pygame"].init = MagicMock()
# Crucially, link the mocked font module back to the main pygame mock
pygame_modules["pygame"].font = mock_pygame_font


# Use patch.dict to inject mocks into sys.modules BEFORE main is imported
# This ensures that when 'main' imports pygame, it gets our mocks
with patch.dict(sys.modules, pygame_modules):
    from main import Scoreboard
# --- End Mocking Setup ---


@pytest.fixture
def scoreboard():
    """Fixture to create a Scoreboard instance for testing."""
    # Reset mocks for each test to ensure isolation, especially render/get_rect
    mock_font.render.reset_mock()
    mock_font_surface.get_rect.reset_mock()
    mock_pygame_font.SysFont.reset_mock() # Reset SysFont call count if needed

    # Instantiate Scoreboard - pygame.font.init should be mocked now
    # and SysFont will return our mock_font
    board = Scoreboard(x=5, y=15, font_size=30, color=constants.GREEN)

    # Verify SysFont was called during init
    mock_pygame_font.SysFont.assert_called_once_with(None, 30)

    # Check initial render during __init__ occurred
    # (Note: The original code renders once in __init__)
    mock_font.render.assert_called_once_with("Score: 0", True, constants.GREEN)
    mock_font_surface.get_rect.assert_called_once_with(topleft=(5, 15))

    # *** Reset mocks *after* init to specifically track calls made by update ***
    mock_font.render.reset_mock()
    mock_font_surface.get_rect.reset_mock()

    assert board.score == 0 # Verify initial state after __init__
    assert board.x == 5
    assert board.y == 15
    assert board.color == constants.GREEN
    return board

# --- Test Functions (Remain the same as previous version) ---

def test_no_score_change_less_than_10ms(scoreboard):
    """Test score doesn't change and render isn't called if time < 10ms."""
    start_time = 1000
    current_time = 1009 # 9ms elapsed

    scoreboard.update(current_time, start_time)

    assert scoreboard.score == 0
    mock_font.render.assert_not_called() # Render was called in init, but not here

def test_score_increase_at_10ms(scoreboard):
    """Test score increases by 1 and render is called at exactly 10ms."""
    start_time = 1000
    current_time = 1010 # 10ms elapsed

    scoreboard.update(current_time, start_time)

    assert scoreboard.score == 1
    mock_font.render.assert_called_once_with("Score: 1", True, constants.GREEN)
    assert scoreboard.image == mock_font_surface # Check image assignment
    mock_font_surface.get_rect.assert_called_once_with(topleft=(scoreboard.x, scoreboard.y))
    assert scoreboard.rect is not None # Check rect assignment


def test_score_increase_greater_than_10ms(scoreboard):
    """Test score increases and render is called if time >= 10ms."""
    start_time = 1000
    current_time = 1015 # 15ms elapsed

    scoreboard.update(current_time, start_time)

    assert scoreboard.score == 1 # 15 // 10 = 1
    mock_font.render.assert_called_once_with("Score: 1", True, constants.GREEN)
    assert scoreboard.image == mock_font_surface
    mock_font_surface.get_rect.assert_called_once_with(topleft=(scoreboard.x, scoreboard.y))
    assert scoreboard.rect is not None

def test_multiple_interval_update(scoreboard):
    """Test score reflects multiple 10ms intervals passed."""
    start_time = 5000
    current_time = 5055 # 55ms elapsed

    scoreboard.update(current_time, start_time)

    assert scoreboard.score == 5 # 55 // 10 = 5
    mock_font.render.assert_called_once_with("Score: 5", True, constants.GREEN)
    mock_font_surface.get_rect.assert_called_once_with(topleft=(scoreboard.x, scoreboard.y))


def test_no_render_if_score_unchanged(scoreboard):
    """Test render is not called again if the score doesn't change on update."""
    start_time = 10000
    current_time_1 = 10055 # 55ms -> score 5
    current_time_2 = 10059 # 59ms -> score 5

    # First update triggers render
    scoreboard.update(current_time_1, start_time)
    assert scoreboard.score == 5
    mock_font.render.assert_called_once_with("Score: 5", True, constants.GREEN)
    mock_font_surface.get_rect.assert_called_once_with(topleft=(scoreboard.x, scoreboard.y))


    # Reset mocks for the second call check
    mock_font.render.reset_mock()
    mock_font_surface.get_rect.reset_mock()


    # Second update should not trigger render
    scoreboard.update(current_time_2, start_time)
    assert scoreboard.score == 5
    mock_font.render.assert_not_called()
    mock_font_surface.get_rect.assert_not_called()


def test_large_time_values(scoreboard):
    """Test score calculation with large time values."""
    start_time = 1000000
    current_time = 1000000 + 1234567 # 1,234,567ms elapsed

    scoreboard.update(current_time, start_time)

    expected_score = 123456 # 1234567 // 10
    assert scoreboard.score == expected_score
    mock_font.render.assert_called_once_with(f"Score: {expected_score}", True, constants.GREEN)
    mock_font_surface.get_rect.assert_called_once_with(topleft=(scoreboard.x, scoreboard.y))

def test_time_reset_conceptual(scoreboard):
    """Test score calculation uses the latest start_time provided."""
    start_time_1 = 1000
    current_time_1 = 1055 # 55ms -> score 5

    scoreboard.update(current_time_1, start_time_1)
    assert scoreboard.score == 5
    mock_font.render.assert_called_once_with("Score: 5", True, constants.GREEN)
    mock_font_surface.get_rect.assert_called_once_with(topleft=(scoreboard.x, scoreboard.y))

    # Reset mocks for the second call check
    mock_font.render.reset_mock()
    mock_font_surface.get_rect.reset_mock()


    # Simulate game reset - new start time
    start_time_2 = 2000
    current_time_2 = 2033 # 33ms elapsed since NEW start time -> score 3

    scoreboard.update(current_time_2, start_time_2)
    assert scoreboard.score == 3 # Calculation based on 2033 - 2000
    mock_font.render.assert_called_once_with("Score: 3", True, constants.GREEN)
    mock_font_surface.get_rect.assert_called_once_with(topleft=(scoreboard.x, scoreboard.y))


def test_negative_time_difference(scoreboard):
    """Test behavior when current_time < start_time."""
    start_time = 100
    current_time = 50 # -50ms difference

    scoreboard.update(current_time, start_time)

    # Floor division: -50 // 10 = -5
    assert scoreboard.score == -5
    mock_font.render.assert_called_once_with("Score: -5", True, constants.GREEN)
    mock_font_surface.get_rect.assert_called_once_with(topleft=(scoreboard.x, scoreboard.y))


def test_render_arguments_and_rect_update(scoreboard):
    """Verify arguments passed to render and that rect is updated."""
    start_time = 0
    current_time = 10 # 10ms elapsed -> score 1

    # Set up a distinct mock rect to be returned by get_rect *specifically for this test*
    # This allows us to check if scoreboard.rect is assigned this specific object
    mock_new_rect = MagicMock(topleft=(1, 1))
    mock_font_surface.get_rect.return_value = mock_new_rect # Configure the mock surface

    scoreboard.update(current_time, start_time)

    assert scoreboard.score == 1
    # Check render call
    mock_font.render.assert_called_once_with("Score: 1", True, constants.GREEN)
    # Check get_rect call on the surface returned by render
    mock_font_surface.get_rect.assert_called_once_with(topleft=(scoreboard.x, scoreboard.y))
    # Check that the scoreboard's rect was updated *to the specific mock rect*
    assert scoreboard.rect == mock_new_rect