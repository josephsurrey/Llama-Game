import pytest
import json
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path
import pygame # Import pygame
from pygame.sprite import Sprite # Import Sprite

# Assuming main.py contains the Game class and Llama/Obstacle/Scoreboard stubs
# Assuming constants.py exists in the same directory or python path
from main import Game
import constants # Ensure constants are imported if needed by __init__

# Minimal stubs for classes instantiated by Game.__init__
# FIX: Inherit from pygame.sprite.Sprite
class MockLlama(Sprite):
    def __init__(self):
        super().__init__() # Initialize the parent Sprite class
        # Add dummy rect/image if any methods in Game rely on them during init
        self.rect = pygame.Rect(0, 0, 10, 10)
        self.image = pygame.Surface((10, 10))

    def reset(self): pass
    def jump(self): pass
    def update(self): pass
    # Sprite group requires add_internal/remove_internal, inheriting Sprite handles this

# FIX: Inherit from pygame.sprite.Sprite
class MockObstacle(Sprite):
    def __init__(self, speed):
        super().__init__() # Initialize the parent Sprite class
        # Add dummy rect/image
        self.rect = pygame.Rect(0, 0, 10, 10)
        self.image = pygame.Surface((10, 10))
        self.speed = speed

    def update(self): pass

class MockScoreboard:
    def __init__(self):
        self.score = 0
    def reset(self): self.score = 0
    def update(self, *args): pass
    def draw(self, screen): pass

@pytest.fixture
def game_instance(mocker):
    """Fixture to create a Game instance with mocked dependencies."""
    # Mock pygame initialization and modules that Game.__init__ uses
    mocker.patch('pygame.init')
    mocker.patch('pygame.mixer.init')
    mocker.patch('pygame.font.init')
    mocker.patch('pygame.display.set_mode')
    mocker.patch('pygame.display.set_caption')
    mocker.patch('pygame.time.Clock', return_value=MagicMock()) # Mock Clock object creation
    mocker.patch('pygame.time.get_ticks', return_value=1000) # Mock time func
    mocker.patch('pygame.time.set_timer')

    # Mock image loading - ensure convert returns a mock surface with get_height
    mock_surface = MagicMock(spec=pygame.Surface)
    mock_surface.get_height.return_value = 10 # Example height if needed by init logic
    mocker.patch('pygame.image.load', return_value=MagicMock(convert=lambda: mock_surface))

    mocker.patch('pygame.font.SysFont', return_value=MagicMock()) # Mock font creation

    # Mock classes instantiated by Game - Now using corrected Mock classes
    # We patch 'main.Llama' etc. so that when Game() is called, it uses our Mocks
    # that inherit from Sprite correctly.
    mocker.patch('main.Llama', new=MockLlama)
    mocker.patch('main.Scoreboard', new=MockScoreboard)
    mocker.patch('main.Obstacle', new=MockObstacle)

    # Mock file operations used by _load_high_scores called in __init__
    # Prevent actual file access during setup
    # Mock Path methods directly
    mock_path_instance = MagicMock(spec=Path)
    mock_path_instance.is_file.return_value = False # Simulate file not existing on load
    mocker.patch('main.Path', return_value=mock_path_instance) # Ensure Path() returns our mock
    mocker.patch("builtins.open", mock_open()) # Mock open for loading

    # Create the game instance
    game = Game()
    # Set a known high score file name for tests
    game.high_score_file = "test_high_scores.json"
    return game

# --- Test Cases remain the same ---

# Test Case 1: Save Valid List
def test_save_high_scores_valid_list(game_instance, mocker):
    """Verify saving a valid list of high scores."""
    game_instance.high_scores = [{"name": "Player1", "score": 100}, {"name": "Player2", "score": 50}]
    expected_json = json.dumps(game_instance.high_scores, indent=4)

    # Mock Path and open specifically for the _save_high_scores method
    # Use a NEW mock for Path within the test scope if needed, or rely on fixture's patch
    mock_save_path = MagicMock(spec=Path)
    path_patch = mocker.patch('main.Path', return_value=mock_save_path) # Re-patch for save call

    mock_file = mock_open()
    open_patch = mocker.patch("builtins.open", mock_file) # Re-patch open for save call

    mock_json_dump = mocker.patch("json.dump")

    game_instance._save_high_scores()

    # Verify Path was called with the correct file name for saving
    path_patch.assert_called_once_with(game_instance.high_score_file)
    # Verify open was called correctly for saving
    open_patch.assert_called_once_with(mock_save_path, 'w')
    # Verify json.dump was called with the correct data and file handle
    mock_json_dump.assert_called_once_with(
        game_instance.high_scores,
        mock_file(), # Get the file handle mock_open provides
        indent=4
    )

# Test Case 2: Save Empty List
def test_save_high_scores_empty_list(game_instance, mocker):
    """Verify saving an empty list of high scores."""
    game_instance.high_scores = []
    expected_json = json.dumps([], indent=4)

    mock_save_path = MagicMock(spec=Path)
    path_patch = mocker.patch('main.Path', return_value=mock_save_path)

    mock_file = mock_open()
    open_patch = mocker.patch("builtins.open", mock_file)

    mock_json_dump = mocker.patch("json.dump")

    game_instance._save_high_scores()

    path_patch.assert_called_once_with(game_instance.high_score_file)
    open_patch.assert_called_once_with(mock_save_path, 'w')
    mock_json_dump.assert_called_once_with(
        [],
        mock_file(),
        indent=4
    )

# Test Case 3: Invalid Data in List (json.dump TypeError)
def test_save_high_scores_invalid_data(game_instance, mocker, capsys):
    """Verify handling of non-JSON serializable data."""
    # Example of non-serializable data (a class instance)
    game_instance.high_scores = [{"name": "Player1", "score": 100}, object()]

    mock_save_path = MagicMock(spec=Path)
    path_patch = mocker.patch('main.Path', return_value=mock_save_path)

    mock_file = mock_open()
    open_patch = mocker.patch("builtins.open", mock_file)

    # Make json.dump raise TypeError when called
    mock_json_dump = mocker.patch("json.dump", side_effect=TypeError("Object is not JSON serializable"))

    game_instance._save_high_scores()

    path_patch.assert_called_once_with(game_instance.high_score_file)
    open_patch.assert_called_once_with(mock_save_path, 'w')
    # Check that json.dump was called
    mock_json_dump.assert_called_once()
    # Check that the error message was printed (caught by generic Exception)
    captured = capsys.readouterr()
    assert "An unexpected error occurred saving high scores" in captured.out
    assert "Object is not JSON serializable" in captured.out

# Test Case 4: File Write IO Error
def test_save_high_scores_io_error(game_instance, mocker, capsys):
    """Verify handling of IOError during file writing."""
    game_instance.high_scores = [{"name": "Player1", "score": 100}]

    mock_save_path = MagicMock(spec=Path)
    path_patch = mocker.patch('main.Path', return_value=mock_save_path)

    # Make open raise IOError
    open_patch = mocker.patch("builtins.open", side_effect=IOError("Permission denied"))

    mock_json_dump = mocker.patch("json.dump") # Mock dump to ensure it's NOT called

    game_instance._save_high_scores()

    path_patch.assert_called_once_with(game_instance.high_score_file)
    # Check that open was attempted
    open_patch.assert_called_once_with(mock_save_path, 'w')
    # Check that json.dump was NOT called because open failed
    mock_json_dump.assert_not_called()
    # Check that the specific IOError message was printed
    captured = capsys.readouterr()
    assert f"Error writing high scores to '{game_instance.high_score_file}'" in captured.out
    assert "Permission denied" in captured.out