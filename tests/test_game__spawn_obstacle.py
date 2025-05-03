# test_game_spawn_obstacle.py

import pytest
import pygame
from unittest.mock import MagicMock, patch

# Assuming main.py contains the Game, Llama, Obstacle, Scoreboard classes
# Assuming constants.py exists in the same directory or is accessible
# Note: Adjust the import path if your structure is different
try:
    from main import Game, Llama, Obstacle, Scoreboard
    import constants
except ModuleNotFoundError:
    pytest.skip("Required 'main.py' or 'constants.py' not found, skipping tests", allow_module_level=True)


# --- Test Fixture ---

@pytest.fixture
def game_instance(mocker):
    """Provides a minimally initialized Game instance with mocked dependencies."""
    # Mock Pygame initialization and resource loading/handling needed by Game.__init__
    mocker.patch('pygame.init')
    mocker.patch('pygame.mixer.init')
    mocker.patch('pygame.font.init')
    mocker.patch('pygame.display.set_mode', return_value=MagicMock())
    mocker.patch('pygame.display.set_caption')
    mocker.patch('pygame.time.Clock', return_value=MagicMock()) # Changed from class to instance
    mocker.patch('pygame.time.get_ticks', return_value=0)
    # Mock image loading to prevent file errors and return a mock surface
    mock_surface = MagicMock(spec=pygame.Surface)
    mock_surface.convert.return_value = mock_surface # Mock the convert() call
    mocker.patch('pygame.image.load', return_value=mock_surface)
    mocker.patch('pygame.time.set_timer')
    mocker.patch('pygame.font.SysFont', return_value=MagicMock())

    # Mock internal methods called by __init__ that are not under test
    mocker.patch.object(Game, '_load_high_scores')

    # Mock classes instantiated in __init__ to isolate Game class logic
    # We patch them within the 'main' namespace where Game looks for them
    mock_llama_instance = MagicMock(spec=Llama)
    mocker.patch('main.Llama', return_value=mock_llama_instance)

    mock_scoreboard_instance = MagicMock(spec=Scoreboard)
    mocker.patch('main.Scoreboard', return_value=mock_scoreboard_instance)

    # Mock the Obstacle class itself for the spawn test
    # We want to verify its instantiation and capture the instance
    mock_obstacle_class = mocker.patch('main.Obstacle', autospec=True)

    # Create the game instance - this will execute Game.__init__ with mocks
    game = Game()

    # --- Important: Reset sprite groups AFTER Game.__init__ ---
    # Game.__init__ adds the (mocked) Llama to all_sprites.
    # For the _spawn_obstacle test, we want to start with known empty groups
    # to cleanly check for the *addition* of the new obstacle.
    game.all_sprites = pygame.sprite.Group()
    game.obstacles = pygame.sprite.Group()

    # Store the mock Obstacle class and a configured return instance for easy access
    game.MockObstacleClass = mock_obstacle_class
    game.mock_obstacle_instance = MagicMock(spec=Obstacle)
    game.MockObstacleClass.return_value = game.mock_obstacle_instance

    return game

# --- Test Function ---

def test_spawn_obstacle_standard_spawn(game_instance):
    """
    Test Case ID: Standard Spawn (from documentation)
    Verification Focus: Checks if a new Obstacle is created with the correct
                        initial speed and added to the appropriate sprite groups.
    Expected Output:
        - Obstacle class is instantiated once with constants.OBSTACLE_INITIAL_SPEED.
        - The created obstacle instance is added to game_instance.all_sprites.
        - The created obstacle instance is added to game_instance.obstacles.
    """
    # Arrange
    initial_all_sprites_count = len(game_instance.all_sprites)
    initial_obstacles_count = len(game_instance.obstacles)

    # Act
    game_instance._spawn_obstacle()

    # Assert
    # 1. Verify Obstacle class was called correctly
    game_instance.MockObstacleClass.assert_called_once_with(constants.OBSTACLE_INITIAL_SPEED)

    # 2. Verify the instance returned by the mock class was added to the groups
    created_obstacle = game_instance.mock_obstacle_instance # Get the instance we configured
    assert created_obstacle in game_instance.all_sprites, "Obstacle not found in all_sprites group"
    assert created_obstacle in game_instance.obstacles, "Obstacle not found in obstacles group"

    # 3. Verify the group sizes increased by exactly one
    assert len(game_instance.all_sprites) == initial_all_sprites_count + 1, "all_sprites group size did not increase by 1"
    assert len(game_instance.obstacles) == initial_obstacles_count + 1, "obstacles group size did not increase by 1"