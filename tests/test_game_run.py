import pytest
import pygame
import sys
from unittest.mock import MagicMock, patch, call

# Assuming constants.py and main.py are in the same directory or accessible
import constants
from main import Game, Llama, Scoreboard # Import necessary classes

# Mock Pygame modules and functions called during Game.__init__ and run
@pytest.fixture(autouse=True)
def mock_pygame(mocker):
    """Automatically mocks pygame modules/functions for all tests."""
    mocker.patch('pygame.init', return_value=None)
    mocker.patch('pygame.mixer.init', return_value=None)
    mocker.patch('pygame.font.init', return_value=None)
    mocker.patch('pygame.display.set_mode', return_value=MagicMock()) # Return a mock surface
    mocker.patch('pygame.display.set_caption', return_value=None)
    mocker.patch('pygame.time.Clock', return_value=MagicMock(tick_busy_loop=MagicMock())) # Mock Clock instance and its method
    mocker.patch('pygame.time.get_ticks', return_value=0) # Start time at 0
    mocker.patch('pygame.image.load', return_value=MagicMock(convert=MagicMock())) # Mock image loading and convert
    mocker.patch('pygame.time.set_timer', return_value=None)
    mocker.patch('pygame.font.SysFont', return_value=MagicMock()) # Mock font creation
    mocker.patch('pygame.sprite.Group', return_value=MagicMock()) # Mock sprite groups if needed for __init__
    mocker.patch('pygame.quit', return_value=None)
    mocker.patch('sys.exit', return_value=None) # Prevent tests from exiting
    # Mock classes instantiated in Game.__init__
    mocker.patch('main.Llama', return_value=MagicMock(spec=Llama))
    mocker.patch('main.Scoreboard', return_value=MagicMock(spec=Scoreboard))

@pytest.fixture
def game_instance(mocker):
    """Provides a Game instance with mocked internal methods for run()."""
    # Patch internal methods that would be complex to run directly
    # We only want to test the flow of the 'run' method itself
    mocker.patch.object(Game, '_load_high_scores') # Prevent file IO in init
    game = Game()
    # Mock methods called within the run loop
    game._handle_events = MagicMock()
    game._update = MagicMock()
    game._draw = MagicMock()
    # Ensure clock is the MagicMock created by mock_pygame fixture
    game.clock = pygame.time.Clock()
    return game

# --- Test Cases based on Updated Plan ---

def test_run_normal_loop_execution_and_exit(game_instance, mock_pygame, mocker):
    """
    Tests that the loop runs, calls internal methods, ticks clock,
    and exits cleanly when self.running becomes False.
    """
    # Configure _handle_events to stop the loop after the first call
    def stop_loop_side_effect():
        game_instance.running = False
    game_instance._handle_events.side_effect = stop_loop_side_effect

    game_instance.run()

    # Assert methods inside the loop were called
    game_instance._handle_events.assert_called_once()
    game_instance._update.assert_called_once()
    game_instance._draw.assert_called_once()
    game_instance.clock.tick_busy_loop.assert_called_once_with(constants.FPS)

    # Assert cleanup methods were called after the loop
    pygame.quit.assert_called_once()
    sys.exit.assert_called_once()


def test_run_clean_exit_sequence(game_instance, mock_pygame, mocker):
    """Tests that pygame.quit() and sys.exit() are called after the loop."""
    # Let the loop run once and terminate
    def stop_loop_side_effect():
        game_instance.running = False
    game_instance._handle_events.side_effect = stop_loop_side_effect

    game_instance.run()

    # Assert cleanup happens after the loop
    pygame.quit.assert_called_once()
    sys.exit.assert_called_once()

def test_run_clock_ticking_verified(game_instance, mock_pygame):
    """Tests that the clock's tick_busy_loop method is called correctly."""
    # Let the loop run once and terminate
    def stop_loop_side_effect():
        game_instance.running = False
    game_instance._handle_events.side_effect = stop_loop_side_effect

    game_instance.run()

    game_instance.clock.tick_busy_loop.assert_called_once_with(constants.FPS)

def test_run_exception_within_loop(game_instance, mock_pygame, mocker):
    """
    Tests that if an internal method raises an exception, the loop terminates
    and the standard exit sequence (pygame.quit, sys.exit) is NOT called.
    """
    test_exception = ValueError("Something went wrong in _update")
    game_instance._update.side_effect = test_exception

    # Expect the exception to propagate out of run()
    with pytest.raises(ValueError, match="Something went wrong in _update"):
        game_instance.run()

    # Assert methods inside the loop up to the exception were called
    game_instance._handle_events.assert_called_once()
    game_instance._update.assert_called_once() # Called, but raised exception
    game_instance._draw.assert_not_called() # Should not be called after exception in _update
    game_instance.clock.tick_busy_loop.assert_not_called() # Should not be called

    # CRITICAL: Assert cleanup methods were NOT called because the exception broke the flow
    pygame.quit.assert_not_called()
    sys.exit.assert_not_called()