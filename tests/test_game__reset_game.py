import pytest
import pygame
from unittest.mock import MagicMock, patch, call

# Assuming main.py contains the Game class and constants.py is accessible
# Make sure Llama class is imported if used in spec
from main import Game, Llama, Scoreboard # Added Llama and Scoreboard here
import constants

# Mock Pygame modules and constants before Game class instantiation
@pytest.fixture(scope="module", autouse=True)
def mock_pygame_init():
    """Auto-mock pygame's init functions and time functions used in init."""
    with patch('pygame.init'), \
         patch('pygame.mixer.init'), \
         patch('pygame.font.init'), \
         patch('pygame.display.set_mode'), \
         patch('pygame.display.set_caption'), \
         patch('pygame.time.Clock') as mock_clock, \
         patch('pygame.image.load') as mock_load, \
         patch('pygame.font.SysFont') as mock_sysfont, \
         patch('pygame.time.get_ticks') as mock_get_ticks, \
         patch('pygame.time.set_timer') as mock_set_timer:

        # Mock image loading to return a mock surface
        mock_surface = MagicMock(spec=pygame.Surface)
        mock_surface.convert.return_value = mock_surface
        mock_surface.get_height.return_value = 50 # Example height
        mock_load.return_value = mock_surface

        # Mock font creation
        mock_font = MagicMock(spec=pygame.font.Font)
        mock_sysfont.return_value = mock_font

        # Mock clock
        mock_clock_instance = mock_clock.return_value
        mock_clock_instance.tick_busy_loop = MagicMock()

        # Mock time functions return values
        mock_get_ticks.return_value = 0 # Start ticks at 0

        yield # Allow tests to run with these mocks

@pytest.fixture
def game_instance(monkeypatch):
    """Provides a Game instance with mocked dependencies."""
    # --- Create specific mock instances ---
    # Use the actual Llama class from main as the spec
    mock_llama_instance = MagicMock(spec=Llama)
    # Use the actual Scoreboard class for spec (important if reset is called)
    mock_scoreboard_instance = MagicMock(spec=Scoreboard)
    mock_all_sprites_group = MagicMock(spec=pygame.sprite.Group)
    mock_obstacles_group = MagicMock(spec=pygame.sprite.Group)

    # --- Mock the classes/constructors ---
    # Make Llama() return our specific mock instance
    monkeypatch.setattr("main.Llama", MagicMock(return_value=mock_llama_instance))
    # Make Scoreboard() return our specific mock instance
    monkeypatch.setattr("main.Scoreboard", MagicMock(return_value=mock_scoreboard_instance))
    # Make Obstacle() return a generic mock
    monkeypatch.setattr("main.Obstacle", MagicMock(spec=pygame.sprite.Sprite))
    # Prevent file access attempts in __init__
    monkeypatch.setattr("main.Game._load_high_scores", MagicMock())

    # --- Mock pygame.sprite.Group constructor using an iterator ---
    group_mocks_iter = iter([mock_all_sprites_group, mock_obstacles_group])
    def group_side_effect(*args, **kwargs):
        return next(group_mocks_iter)

    with patch('pygame.sprite.Group', side_effect=group_side_effect) as mock_group_constructor:
        # --- Instantiate the Game class ---
        game = Game()

    # --- Verify Initialization Steps ---
    assert mock_group_constructor.call_count == 2
    mock_all_sprites_group.add.assert_called_once_with(mock_llama_instance)

    # --- Reset mocks AFTER verification for clean test state ---
    # Now that spec is correct, reset_mock() is safe
    mock_llama_instance.reset_mock()
    mock_scoreboard_instance.reset_mock()
    mock_all_sprites_group.reset_mock()
    mock_obstacles_group.reset_mock()

    # --- Set game state for reset tests ---
    game.game_over = True
    game.entering_name = True
    game.displaying_scores = True
    game.score_eligible_for_save = True
    game.player_name = "Test"
    game.start_time_ticks = 9999

    # --- Assign the correct mocks back to the instance attributes ---
    game.llama = mock_llama_instance
    game.scoreboard = mock_scoreboard_instance
    game.all_sprites = mock_all_sprites_group
    game.obstacles = mock_obstacles_group

    return game


# --- Test Cases ---
# (No changes needed in the test cases themselves)

def test_reset_game_standard_state_reset(game_instance):
    """Verify standard state variable resets."""
    initial_ticks = 50000
    with patch('pygame.time.get_ticks', return_value=initial_ticks), \
         patch('pygame.time.set_timer'): # Mock timer call within reset
        game_instance._reset_game()

    assert not game_instance.game_over
    assert not game_instance.entering_name
    assert not game_instance.displaying_scores
    assert not game_instance.score_eligible_for_save
    assert game_instance.player_name == ""
    assert game_instance.start_time_ticks == initial_ticks

def test_reset_game_component_resets(game_instance):
    """Verify calls to reset methods of components."""
    with patch('pygame.time.get_ticks', return_value=1000), \
         patch('pygame.time.set_timer'):
        game_instance._reset_game()

    # Now that spec includes 'reset', these calls should pass
    game_instance.scoreboard.reset.assert_called_once()
    game_instance.llama.reset.assert_called_once()

def test_reset_game_obstacle_group_reset(game_instance):
    """Verify the obstacles sprite group is emptied."""
    mock_obstacle = MagicMock(spec=pygame.sprite.Sprite)
    game_instance.obstacles.sprites.return_value = [mock_obstacle]

    with patch('pygame.time.get_ticks', return_value=1000), \
         patch('pygame.time.set_timer'):
        game_instance._reset_game()

    game_instance.obstacles.empty.assert_called_once()

def test_reset_game_all_sprites_group_reset(game_instance):
    """Verify the all_sprites group is emptied and llama re-added."""
    mock_obstacle = MagicMock(spec=pygame.sprite.Sprite)
    game_instance.all_sprites.sprites.return_value = [game_instance.llama, mock_obstacle]

    with patch('pygame.time.get_ticks', return_value=1000), \
         patch('pygame.time.set_timer'):
        game_instance._reset_game()

    expected_calls = [
        call.empty(),
        call.add(game_instance.llama) # Adds the mock llama instance
    ]
    game_instance.all_sprites.assert_has_calls(expected_calls)
    assert game_instance.all_sprites.add.call_count == 1


def test_reset_game_obstacle_timer_restart(game_instance):
    """Verify the obstacle spawn timer is restarted."""
    with patch('pygame.time.get_ticks', return_value=1000), \
         patch('pygame.time.set_timer') as mock_set_timer_reset: # Capture mock in test
        game_instance._reset_game()

    mock_set_timer_reset.assert_called_with(
        constants.OBSTACLE_SPAWN_EVENT,
        constants.OBSTACLE_CREATION_INTERVAL
    )
    stop_call = call(constants.OBSTACLE_SPAWN_EVENT, 0)
    assert stop_call not in mock_set_timer_reset.call_args_list


def test_reset_game_while_playing(game_instance):
    """Test calling reset when game is not over."""
    game_instance.game_over = False
    game_instance.entering_name = False
    game_instance.displaying_scores = False
    game_instance.score_eligible_for_save = False
    game_instance.player_name = "Still Playing"
    initial_ticks = 60000

    with patch('pygame.time.get_ticks', return_value=initial_ticks) as mock_ticks_reset, \
         patch('pygame.time.set_timer') as mock_timer_reset:
        # Execute without try-except first to ensure no unexpected exceptions
        game_instance._reset_game()

        # Verify state reset happened correctly
        assert not game_instance.game_over
        assert not game_instance.entering_name
        assert not game_instance.displaying_scores
        assert not game_instance.score_eligible_for_save
        assert game_instance.player_name == ""
        assert game_instance.start_time_ticks == initial_ticks
        game_instance.scoreboard.reset.assert_called_once()
        game_instance.llama.reset.assert_called_once()
        game_instance.obstacles.empty.assert_called_once()
        game_instance.all_sprites.empty.assert_called_once()
        game_instance.all_sprites.add.assert_called_once_with(game_instance.llama)
        mock_timer_reset.assert_called_with(
            constants.OBSTACLE_SPAWN_EVENT,
            constants.OBSTACLE_CREATION_INTERVAL
        )

def test_reset_game_with_empty_obstacles(game_instance):
    """Test resetting when the obstacles group is already empty."""
    game_instance.obstacles.sprites.return_value = []
    game_instance.obstacles.empty.reset_mock()

    with patch('pygame.time.get_ticks', return_value=1000), \
         patch('pygame.time.set_timer'):
        # Execute without try-except first
        game_instance._reset_game()

        game_instance.obstacles.empty.assert_called_once()
        game_instance.llama.reset.assert_called_once()
        assert not game_instance.game_over