import pytest
import pygame
from unittest.mock import MagicMock, patch, call

# Assuming main.py contains the Game, Llama, Scoreboard classes
# and constants.py is in the same directory or accessible path.
pygame.init() # Initialize pygame here or ensure it's done globally for tests

from main import Game, Llama, Scoreboard
import constants

# Define dummy event types if not already defined in constants
if not hasattr(constants, 'OBSTACLE_SPAWN_EVENT'):
    constants.OBSTACLE_SPAWN_EVENT = pygame.USEREVENT + 1


# --- Fixtures ---

@pytest.fixture(autouse=True)
def mock_pygame_core_functions():
    """Automatically mock core pygame functions NOT involved in event creation."""
    # Keep pygame.init() active from above
    with patch('pygame.mixer.init'), \
         patch('pygame.font.init'), \
         patch('pygame.display.set_mode'), \
         patch('pygame.display.set_caption'), \
         patch('pygame.time.Clock'), \
         patch('pygame.time.get_ticks', return_value=0), \
         patch('pygame.image.load'), \
         patch('pygame.time.set_timer'), \
         patch('pygame.quit'), \
         patch('sys.exit'):
        yield # Allows the test to run with these mocks active


@pytest.fixture
def game_instance():
    """Provides a Game instance with mocked dependencies."""
    # Mock classes used by Game.__init__
    with patch('main.Llama', autospec=True) as MockLlama, \
         patch('main.Scoreboard', autospec=True) as MockScoreboard:

        # Mock methods called during Game.__init__
        with patch.object(Game, '_load_high_scores') as mock_load_scores:
            game = Game()
            # Assign mocks back if needed for assertion later
            game.llama = MockLlama.return_value
            game.scoreboard = MockScoreboard.return_value
            game.scoreboard.score = 100 # Example score for testing saves
            game._load_high_scores = mock_load_scores # Make mock accessible

            # Mock methods called by _handle_events
            game._spawn_obstacle = MagicMock(name='_spawn_obstacle')
            game._reset_game = MagicMock(name='_reset_game')
            game._add_high_score = MagicMock(name='_add_high_score')

            # Reset initial states for clarity in tests if needed
            game.running = True
            game.game_over = False
            game.entering_name = False
            game.displaying_scores = False
            game.score_eligible_for_save = False
            game.player_name = ""
            return game

# --- Helper Function ---
def create_event(event_type, key=None, unicode_char=None):
    """Helper function to create Pygame event objects."""
    attrs = {}
    if key is not None:
        attrs['key'] = key

    # Ensure 'unicode' attribute exists for KEYDOWN events, defaulting to ''
    # if not explicitly provided, as the game code accesses it directly.
    # This mimics Pygame's behavior for non-character keys like Shift.
    if event_type == pygame.KEYDOWN:
        if unicode_char is not None:
            attrs['unicode'] = unicode_char
        elif 'unicode' not in attrs: # Only add default if not explicitly given
             attrs['unicode'] = ''
    elif unicode_char is not None:
         # Allow setting unicode for non-KEYDOWN if explicitly passed (less common)
         attrs['unicode'] = unicode_char

    # Create event using type and keyword arguments from the dict
    return pygame.event.Event(event_type, **attrs)


# --- Test Cases ---

# General Events
def test_handle_events_quit(game_instance):
    event = create_event(pygame.QUIT)
    with patch('pygame.event.get', return_value=[event]):
        game_instance._handle_events()
    assert not game_instance.running

# Gameplay State Events
def test_handle_events_jump_space_playing(game_instance):
    game_instance.game_over = False
    event = create_event(pygame.KEYDOWN, key=pygame.K_SPACE)
    with patch('pygame.event.get', return_value=[event]):
        game_instance._handle_events()
    game_instance.llama.jump.assert_called_once()

def test_handle_events_jump_up_playing(game_instance):
    game_instance.game_over = False
    event = create_event(pygame.KEYDOWN, key=pygame.K_UP)
    with patch('pygame.event.get', return_value=[event]):
        game_instance._handle_events()
    game_instance.llama.jump.assert_called_once()

def test_handle_events_jump_game_over(game_instance):
    game_instance.game_over = True
    event_space = create_event(pygame.KEYDOWN, key=pygame.K_SPACE)
    event_up = create_event(pygame.KEYDOWN, key=pygame.K_UP)
    with patch('pygame.event.get', return_value=[event_space, event_up]):
        game_instance._handle_events()
    game_instance.llama.jump.assert_not_called()

def test_handle_events_obstacle_spawn_playing(game_instance):
    game_instance.game_over = False
    event = create_event(constants.OBSTACLE_SPAWN_EVENT)
    with patch('pygame.event.get', return_value=[event]):
        game_instance._handle_events()
    game_instance._spawn_obstacle.assert_called_once()

def test_handle_events_obstacle_spawn_game_over(game_instance):
    game_instance.game_over = True
    event = create_event(constants.OBSTACLE_SPAWN_EVENT)
    with patch('pygame.event.get', return_value=[event]):
        game_instance._handle_events()
    game_instance._spawn_obstacle.assert_not_called()

def test_handle_events_unexpected_key_playing(game_instance):
    game_instance.game_over = False
    event = create_event(pygame.KEYDOWN, key=pygame.K_a, unicode_char='a') # Provide unicode for this case
    with patch('pygame.event.get', return_value=[event]):
        game_instance._handle_events()
    game_instance.llama.jump.assert_not_called()
    game_instance._spawn_obstacle.assert_not_called() # Ensure no other actions

# Game Over State Events
def test_handle_events_restart_game_over(game_instance):
    game_instance.game_over = True
    event = create_event(pygame.KEYDOWN, key=pygame.K_r)
    with patch('pygame.event.get', return_value=[event]):
        game_instance._handle_events()
    game_instance._reset_game.assert_called_once()

def test_handle_events_restart_playing(game_instance):
    game_instance.game_over = False
    event = create_event(pygame.KEYDOWN, key=pygame.K_r)
    with patch('pygame.event.get', return_value=[event]):
        game_instance._handle_events()
    game_instance._reset_game.assert_not_called()

def test_handle_events_quit_key_game_over(game_instance):
    game_instance.game_over = True
    event = create_event(pygame.KEYDOWN, key=pygame.K_q)
    with patch('pygame.event.get', return_value=[event]):
        game_instance._handle_events()
    assert not game_instance.running

def test_handle_events_quit_key_playing(game_instance):
    game_instance.game_over = False
    event = create_event(pygame.KEYDOWN, key=pygame.K_q)
    with patch('pygame.event.get', return_value=[event]):
        game_instance._handle_events()
    assert game_instance.running # Should still be running

def test_handle_events_save_confirm_eligible(game_instance):
    game_instance.game_over = True
    game_instance.score_eligible_for_save = True
    game_instance.player_name = "should be cleared"
    event = create_event(pygame.KEYDOWN, key=pygame.K_y)
    with patch('pygame.event.get', return_value=[event]):
        game_instance._handle_events()
    assert game_instance.entering_name
    assert game_instance.player_name == "" # Check name is reset

def test_handle_events_save_decline_eligible(game_instance):
    game_instance.game_over = True
    game_instance.score_eligible_for_save = True
    event = create_event(pygame.KEYDOWN, key=pygame.K_n)
    with patch('pygame.event.get', return_value=[event]):
        game_instance._handle_events()
    assert not game_instance.entering_name
    assert not game_instance.score_eligible_for_save

def test_handle_events_save_keys_not_eligible(game_instance):
    game_instance.game_over = True
    game_instance.score_eligible_for_save = False
    event_y = create_event(pygame.KEYDOWN, key=pygame.K_y)
    event_n = create_event(pygame.KEYDOWN, key=pygame.K_n)
    with patch('pygame.event.get', return_value=[event_y, event_n]):
        game_instance._handle_events()
    assert not game_instance.entering_name
    assert not game_instance.score_eligible_for_save # Should remain False

def test_handle_events_unexpected_key_game_over(game_instance):
    game_instance.game_over = True
    game_instance.score_eligible_for_save = False # Test standard game over
    event = create_event(pygame.KEYDOWN, key=pygame.K_p)
    with patch('pygame.event.get', return_value=[event]):
        game_instance._handle_events()
    assert game_instance.running # No state changes expected
    assert not game_instance.entering_name
    game_instance._reset_game.assert_not_called()

# Entering Name State Events
def test_handle_events_enter_name_alphanumeric(game_instance):
    game_instance.entering_name = True
    game_instance.player_name = "ABC"
    # Pass unicode explicitly for text input events
    event = create_event(pygame.KEYDOWN, key=pygame.K_d, unicode_char='d')
    with patch('pygame.event.get', return_value=[event]):
        game_instance._handle_events()
    assert game_instance.player_name == "ABCd"

def test_handle_events_enter_name_space(game_instance):
    game_instance.entering_name = True
    game_instance.player_name = "A B"
    event = create_event(pygame.KEYDOWN, key=pygame.K_SPACE, unicode_char=' ')
    with patch('pygame.event.get', return_value=[event]):
        game_instance._handle_events()
    assert game_instance.player_name == "A B "

def test_handle_events_enter_name_length_limit(game_instance):
    game_instance.entering_name = True
    game_instance.player_name = "123456" # Already at limit
    event = create_event(pygame.KEYDOWN, key=pygame.K_a, unicode_char='a')
    with patch('pygame.event.get', return_value=[event]):
        game_instance._handle_events()
    assert game_instance.player_name == "123456" # Name should not change

def test_handle_events_enter_name_backspace(game_instance):
    game_instance.entering_name = True
    game_instance.player_name = "Test"
    # Backspace needs key and will get unicode='' from helper
    event = create_event(pygame.KEYDOWN, key=pygame.K_BACKSPACE)
    with patch('pygame.event.get', return_value=[event]):
        game_instance._handle_events()
    assert game_instance.player_name == "Tes"

def test_handle_events_enter_name_submit_valid(game_instance):
    game_instance.entering_name = True
    game_instance.player_name = "Player1"
    game_instance.scoreboard.score = 150 # Set a score to save
    event = create_event(pygame.KEYDOWN, key=pygame.K_RETURN)
    with patch('pygame.event.get', return_value=[event]):
        game_instance._handle_events()
    game_instance._add_high_score.assert_called_once_with("Player1", 150)
    assert not game_instance.entering_name
    assert not game_instance.score_eligible_for_save

def test_handle_events_enter_name_submit_empty(game_instance):
    game_instance.entering_name = True
    game_instance.player_name = "" # Empty name
    game_instance.scoreboard.score = 150
    event = create_event(pygame.KEYDOWN, key=pygame.K_RETURN)
    with patch('pygame.event.get', return_value=[event]):
        game_instance._handle_events()
    game_instance._add_high_score.assert_not_called() # Should not be called
    assert not game_instance.entering_name
    assert not game_instance.score_eligible_for_save

def test_handle_events_enter_name_unexpected_key(game_instance):
    game_instance.entering_name = True
    game_instance.player_name = "Joe"
    # Event for a non-input key (like shift). Will get unicode='' from helper.
    event = create_event(pygame.KEYDOWN, key=pygame.K_LSHIFT)
    with patch('pygame.event.get', return_value=[event]):
        game_instance._handle_events()
    # Check unicode is '', isalnum is False, not in [' '] is True -> condition fails
    assert game_instance.player_name == "Joe" # Name shouldn't change

# Displaying Scores State Events
def test_handle_events_display_scores_escape(game_instance):
    game_instance.displaying_scores = True
    event = create_event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
    with patch('pygame.event.get', return_value=[event]):
        game_instance._handle_events()
    assert not game_instance.displaying_scores

def test_handle_events_display_scores_unexpected_key(game_instance):
    game_instance.displaying_scores = True
    event = create_event(pygame.KEYDOWN, key=pygame.K_a) # Gets unicode=''
    with patch('pygame.event.get', return_value=[event]):
        game_instance._handle_events()
    assert game_instance.displaying_scores # Should remain true

# Multiple Events
def test_handle_events_multiple_events_playing(game_instance):
    game_instance.game_over = False
    event_spawn = create_event(constants.OBSTACLE_SPAWN_EVENT)
    event_jump = create_event(pygame.KEYDOWN, key=pygame.K_SPACE)
    with patch('pygame.event.get', return_value=[event_spawn, event_jump]):
        game_instance._handle_events()
    game_instance._spawn_obstacle.assert_called_once()
    game_instance.llama.jump.assert_called_once()

# Teardown pygame after tests run
def teardown_module(module):
    pygame.quit()