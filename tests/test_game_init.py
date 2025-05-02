# test_game_init.py
import pytest
from unittest.mock import patch, MagicMock, call
import pygame # Import the real pygame to access its exception type if needed

# Import the class to be tested
from main import Game, Llama, Scoreboard

# Import constants used directly in __init__
import constants


# Use a fixture to automatically patch pygame and component classes for all tests
@pytest.fixture(autouse=True)
def mock_pygame_and_components(mocker):
    """Mocks pygame modules and custom classes used within Game.__init__."""
    # ****** CHANGE HERE: Remove autospec=True for pygame ******
    # This prevents the issue where the mocked pygame.error class
    # doesn't inherit from BaseException.
    mock_pygame = mocker.patch('main.pygame')
    # Keep autospec for custom classes if desired
    mock_llama = mocker.patch('main.Llama', autospec=True)
    mock_scoreboard = mocker.patch('main.Scoreboard', autospec=True)

    # Configure return values for mocks that are assigned or used
    # We need to manually add attributes that were previously handled by autospec
    mock_pygame.display = MagicMock()
    mock_pygame.mixer = MagicMock()
    mock_pygame.font = MagicMock()
    mock_pygame.time = MagicMock()
    mock_pygame.sprite = MagicMock()
    mock_pygame.image = MagicMock()
    mock_pygame.error = pygame.error # Explicitly use the real pygame.error

    mock_pygame.display.set_mode.return_value = MagicMock(spec=pygame.Surface)
    mock_pygame.time.Clock = MagicMock() # Mock the class itself
    mock_pygame.time.get_ticks.return_value = 12345 # Example start time
    mock_pygame.sprite.Group = MagicMock() # Mock the Group class

    # Mock image loading and conversion
    mock_surface = MagicMock(spec=pygame.Surface)
    mock_converted_surface = MagicMock(spec=pygame.Surface)
    mock_surface.convert.return_value = mock_converted_surface
    mock_pygame.image.load.return_value = mock_surface

    # Mock font creation
    mock_font = MagicMock(spec=pygame.font.Font)
    mock_pygame.font.SysFont.return_value = mock_font

    # Mock Llama and Scoreboard instances
    mock_llama_instance = MagicMock(spec=Llama)
    mock_llama.return_value = mock_llama_instance
    mock_scoreboard_instance = MagicMock(spec=Scoreboard)
    mock_scoreboard.return_value = mock_scoreboard_instance

    # Mock internal method call (_load_high_scores)
    # Need to patch it on the Game class itself before instantiation
    mocker.patch.object(Game, '_load_high_scores', return_value=None) # Mock the instance method

    # Return mocks if needed by specific tests (though often accessed via patch object)
    return {
        "pygame": mock_pygame,
        "Llama": mock_llama,
        "Scoreboard": mock_scoreboard,
        "llama_instance": mock_llama_instance,
        "scoreboard_instance": mock_scoreboard_instance,
        "mock_surface": mock_surface,
        "mock_converted_surface": mock_converted_surface,
        "mock_font": mock_font
    }


# --- Test Cases ---
# (The rest of your test functions remain the same)

def test_init_pygame_modules(mock_pygame_and_components):
    """Test Case: Standard Initialization (Pygame Modules)"""
    mock_pygame = mock_pygame_and_components["pygame"]
    game = Game()
    mock_pygame.init.assert_called_once()
    mock_pygame.mixer.init.assert_called_once()
    mock_pygame.font.init.assert_called_once()

def test_init_screen_and_caption(mock_pygame_and_components):
    """Test Case: Standard Initialization (Screen & Caption)"""
    mock_pygame = mock_pygame_and_components["pygame"]
    game = Game()
    mock_pygame.display.set_mode.assert_called_once_with(
        (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)
    )
    mock_pygame.display.set_caption.assert_called_once_with(
        constants.WINDOW_TITLE
    )
    assert game.screen == mock_pygame.display.set_mode.return_value

def test_init_clock_and_start_time(mock_pygame_and_components):
    """Test Case: Standard Initialization (Clock & Start Time)"""
    mock_pygame = mock_pygame_and_components["pygame"]
    game = Game()
    assert game.clock == mock_pygame.time.Clock # Check it's assigned the class
    mock_pygame.time.get_ticks.assert_called_once()
    assert game.start_time == 12345 # Matches the mock return value

def test_init_attribute_values(mock_pygame_and_components):
    """Test Case: Attribute Value Checks (Flags, Name)"""
    game = Game()
    assert game.running is True
    assert game.game_over is False
    assert game.entering_name is False
    assert game.displaying_scores is False
    assert game.score_eligible_for_save is False
    assert game.player_name == ""

def test_init_component_instantiation(mock_pygame_and_components):
    """Test Case: Component Instantiation (Llama, Scoreboard)"""
    mock_Llama = mock_pygame_and_components["Llama"]
    mock_Scoreboard = mock_pygame_and_components["Scoreboard"]
    mock_llama_instance = mock_pygame_and_components["llama_instance"]
    mock_scoreboard_instance = mock_pygame_and_components["scoreboard_instance"]

    game = Game()

    mock_Llama.assert_called_once_with()
    mock_Scoreboard.assert_called_once_with()
    assert game.llama == mock_llama_instance
    assert game.scoreboard == mock_scoreboard_instance

def test_init_sprite_group_setup(mock_pygame_and_components):
    """Test Case: Sprite Group Setup"""
    mock_pygame = mock_pygame_and_components["pygame"]
    mock_llama_instance = mock_pygame_and_components["llama_instance"]

    # Isolate the Group mock calls for this test
    mock_all_sprites_group = MagicMock(spec=pygame.sprite.Group)
    mock_obstacles_group = MagicMock(spec=pygame.sprite.Group)
    mock_pygame.sprite.Group.side_effect = [
        mock_all_sprites_group,
        mock_obstacles_group
    ]

    game = Game()

    assert mock_pygame.sprite.Group.call_count == 2
    assert game.all_sprites == mock_all_sprites_group
    assert game.obstacles == mock_obstacles_group
    mock_all_sprites_group.add.assert_called_once_with(mock_llama_instance)

def test_init_ground_image_load_success(mock_pygame_and_components):
    """Test Case: Ground Image Load Success"""
    mock_pygame = mock_pygame_and_components["pygame"]
    mock_surface = mock_pygame_and_components["mock_surface"]
    mock_converted_surface = mock_pygame_and_components["mock_converted_surface"]

    game = Game()

    mock_pygame.image.load.assert_called_once_with(constants.GROUND_IMAGE)
    mock_surface.convert.assert_called_once_with()
    assert game.ground_image == mock_converted_surface

def test_init_ground_image_load_failure_pygame_error(mock_pygame_and_components, capsys):
    """Test Case: Ground Image Load Failure (pygame.error)"""
    mock_pygame = mock_pygame_and_components["pygame"]
    # Use the *real* pygame.error for the side effect now
    mock_pygame.image.load.side_effect = pygame.error("Test pygame error")

    game = Game() # This should no longer raise TypeError

    mock_pygame.image.load.assert_called_once_with(constants.GROUND_IMAGE)
    assert game.ground_image is None
    # Optional: Check if error message was printed
    captured = capsys.readouterr()
    assert "Error loading ground image" in captured.out
    assert "Test pygame error" in captured.out

def test_init_ground_image_load_failure_file_not_found(mock_pygame_and_components, capsys):
    """Test Case: Ground Image Load Failure (FileNotFoundError)"""
    mock_pygame = mock_pygame_and_components["pygame"]
    # FileNotFoundError is a standard Python exception, less likely to have issues
    mock_pygame.image.load.side_effect = FileNotFoundError("Test file not found")

    game = Game()

    mock_pygame.image.load.assert_called_once_with(constants.GROUND_IMAGE)
    assert game.ground_image is None
    # Optional: Check if error message was printed
    captured = capsys.readouterr()
    assert "Ground image file not found" in captured.out

def test_init_obstacle_timer_set(mock_pygame_and_components):
    """Test Case: Obstacle Timer Set"""
    mock_pygame = mock_pygame_and_components["pygame"]
    game = Game()
    # Ensure OBSTACLE_SPAWN_EVENT constant is handled correctly by mock
    mock_pygame.USEREVENT = pygame.USEREVENT # Assign real value if needed
    mock_pygame.time.set_timer.assert_called_once_with(
        constants.OBSTACLE_SPAWN_EVENT, # Uses the constant
        constants.OBSTACLE_CREATION_INTERVAL
    )

# Note: Patching _load_high_scores separately is still a good idea
@patch.object(Game, '_load_high_scores')
def test_init_high_score_load_called(mock_load_high_scores, mock_pygame_and_components):
    """Test Case: High Score Load Called"""
    game = Game()
    mock_load_high_scores.assert_called_once_with()

def test_init_font_object_creation(mock_pygame_and_components):
    """Test Case: Font Object Creation"""
    mock_pygame = mock_pygame_and_components["pygame"]
    mock_font = mock_pygame_and_components["mock_font"]

    game = Game()

    expected_calls = [
        call(None, 36), # score_font
        call(None, 74), # game_over_font
        call(None, 24), # button_font
        call(None, 36)  # input_font
    ]
    mock_pygame.font.SysFont.assert_has_calls(expected_calls, any_order=False)
    assert mock_pygame.font.SysFont.call_count == 4

    assert game.score_font == mock_font
    assert game.game_over_font == mock_font
    assert game.button_font == mock_font
    assert game.input_font == mock_font