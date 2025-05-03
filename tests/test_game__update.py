import pytest
from unittest.mock import Mock, patch
import pygame  # Import pygame to access its constants/types if needed indirectly

# Assuming main.py contains the Game class and constants.py is accessible
from main import Game

# Mock necessary Pygame modules ONLY if they are directly used in __init__
# or are difficult to manage otherwise. We generally avoid mocking constants.
# In this case, we need to mock pygame functions called during __init__ and update.
@pytest.fixture(autouse=True)
def mock_pygame():
    """Automatically mock Pygame modules for all tests."""
    with patch('main.pygame', new_callable=Mock) as mock_pygame_main:
        # Mock submodules and functions called in Game.__init__
        mock_pygame_main.init = Mock()
        mock_pygame_main.mixer.init = Mock()
        mock_pygame_main.font.init = Mock()
        mock_pygame_main.display.set_mode = Mock(return_value=Mock()) # Return a mock surface
        mock_pygame_main.display.set_caption = Mock()
        mock_pygame_main.time.Clock = Mock()
        mock_pygame_main.time.get_ticks = Mock(return_value=1000) # Example start time
        mock_pygame_main.sprite.Group = Mock()
        mock_pygame_main.image.load = Mock(return_value=Mock(convert=Mock())) # Mock successful image load
        mock_pygame_main.time.set_timer = Mock()
        mock_pygame_main.font.SysFont = Mock(return_value=Mock()) # Mock font creation

        # Keep constants accessible if needed, though direct constants usage is fine
        mock_pygame_main.QUIT = pygame.QUIT
        mock_pygame_main.KEYDOWN = pygame.KEYDOWN
        # Add other constants if needed by the code under test or setup

        yield mock_pygame_main # Provide the mock for potential direct use in tests

@pytest.fixture
def game_instance(mock_pygame):
    """Provides a Game instance with mocked dependencies."""
    # Mock classes instantiated within Game
    with patch('main.Llama', new_callable=Mock) as mock_llama_cls, \
         patch('main.Scoreboard', new_callable=Mock) as mock_scoreboard_cls, \
         patch('main.Game._load_high_scores', Mock()): # Mock loading scores

        game = Game()
        # Assign mocks to instance attributes for assertion
        game.llama = mock_llama_cls.return_value
        game.scoreboard = mock_scoreboard_cls.return_value
        game.all_sprites = Mock(spec=pygame.sprite.Group) # Use spec for better mocking
        game.obstacles = Mock(spec=pygame.sprite.Group)
        game._check_collisions = Mock() # Mock the method directly
        game.start_time = 1000 # Set a specific start time for predictability
        # Ensure sprites group is added to avoid errors if accessed
        game.all_sprites.add = Mock()
        game.all_sprites.update = Mock()
        game.scoreboard.update = Mock()

        # Set default states
        game.game_over = False
        game.entering_name = False
        game.displaying_scores = False
        game.running = True # Although not directly used in _update, good practice

        return game

# --- Test Cases ---

def test_update_while_playing(game_instance, mock_pygame):
    """
    Test Case: Update While Playing
    Input / Conditions: game_over=False, entering_name=False, displaying_scores=False
    Expected Output: all_sprites.update(), scoreboard.update(), _check_collisions() called.
    """
    game_instance.game_over = False
    game_instance.entering_name = False
    game_instance.displaying_scores = False
    current_ticks = 2500
    mock_pygame.time.get_ticks.return_value = current_ticks

    game_instance._update()

    game_instance.all_sprites.update.assert_called_once()
    game_instance.scoreboard.update.assert_called_once_with(current_ticks, game_instance.start_time)
    game_instance._check_collisions.assert_called_once()

def test_update_while_game_over(game_instance):
    """
    Test Case: Update While Game Over
    Input / Conditions: game_over=True
    Expected Output: Internal update methods are *not* called.
    """
    game_instance.game_over = True
    game_instance.entering_name = False
    game_instance.displaying_scores = False

    game_instance._update()

    game_instance.all_sprites.update.assert_not_called()
    game_instance.scoreboard.update.assert_not_called()
    game_instance._check_collisions.assert_not_called()

def test_update_while_entering_name(game_instance):
    """
    Test Case: Update While Entering Name
    Input / Conditions: entering_name=True
    Expected Output: Internal update methods are *not* called.
    """
    game_instance.game_over = False
    game_instance.entering_name = True
    game_instance.displaying_scores = False

    game_instance._update()

    game_instance.all_sprites.update.assert_not_called()
    game_instance.scoreboard.update.assert_not_called()
    game_instance._check_collisions.assert_not_called()

def test_update_while_displaying_scores(game_instance):
    """
    Test Case: Update While Displaying Scores
    Input / Conditions: displaying_scores=True
    Expected Output: Internal update methods are *not* called.
    """
    game_instance.game_over = False
    game_instance.entering_name = False
    game_instance.displaying_scores = True

    game_instance._update()

    game_instance.all_sprites.update.assert_not_called()
    game_instance.scoreboard.update.assert_not_called()
    game_instance._check_collisions.assert_not_called()

def test_update_no_sprites_present(game_instance, mock_pygame):
    """
    Test Case: No Sprites Present
    Input / Conditions: all_sprites group is empty, game is playing
    Expected Output: all_sprites.update() is called, no error. Other calls proceed.
    """
    game_instance.game_over = False
    game_instance.entering_name = False
    game_instance.displaying_scores = False
    # We don't need to explicitly empty the mock group, just verify update is called
    current_ticks = 3000
    mock_pygame.time.get_ticks.return_value = current_ticks

    game_instance._update()

    # Verify update is called even if the group were conceptually empty
    game_instance.all_sprites.update.assert_called_once()
    game_instance.scoreboard.update.assert_called_once_with(current_ticks, game_instance.start_time)
    game_instance._check_collisions.assert_called_once()

def test_update_scoreboard_arguments(game_instance, mock_pygame):
    """
    Test Case: Verify scoreboard.update Arguments
    Input / Conditions: Game is playing
    Expected Output: scoreboard.update() called with correct time ticks.
    """
    game_instance.game_over = False
    game_instance.entering_name = False
    game_instance.displaying_scores = False
    expected_current_ticks = 5000
    mock_pygame.time.get_ticks.return_value = expected_current_ticks

    game_instance._update()

    game_instance.scoreboard.update.assert_called_once_with(expected_current_ticks, game_instance.start_time)
    # Also check other calls happened as expected in this state
    game_instance.all_sprites.update.assert_called_once()
    game_instance._check_collisions.assert_called_once()