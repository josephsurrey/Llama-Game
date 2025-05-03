import pytest
import pygame
from unittest.mock import patch, MagicMock, call

# Assuming constants.py and main.py are in the same directory or accessible
import constants
from main import Game, Llama, Obstacle  # Import necessary classes

# Minimal Pygame setup needed for tests to run without display errors
@pytest.fixture(scope="session", autouse=True)
def pygame_setup():
    pygame.init()
    pygame.display.set_mode((1, 1)) # Minimal display
    yield
    pygame.quit()

@pytest.fixture
def game_instance(mocker):
    """Fixture to create a Game instance with minimal mocking."""
    # Mock modules/functions called during Game.__init__
    mocker.patch('pygame.mixer.init')
    mocker.patch('pygame.font.init')
    mocker.patch('pygame.display.set_caption')
    mocker.patch('pygame.time.Clock', return_value=MagicMock())
    mocker.patch('pygame.time.get_ticks', return_value=0)
    mocker.patch('pygame.image.load', return_value=MagicMock(convert=MagicMock()))
    mocker.patch('pygame.font.SysFont', return_value=MagicMock())
    mocker.patch('main.Llama', spec=Llama) # Use spec for better mocking
    mocker.patch('main.Scoreboard', spec_set=True) # spec_set enforces attribute existence

    # Mock methods called within __init__ that might have side effects
    mocker.patch.object(Game, '_load_high_scores')
    mocker.patch('pygame.time.set_timer') # Mock set_timer globally for __init__ call

    # Create instance - __init__ will run with mocks
    game = Game()

    # Reset mocks that might have been called during init if needed for specific tests
    pygame.time.set_timer.reset_mock()
    # Ensure necessary attributes exist for the test
    game.llama = MagicMock(spec=Llama) # Mock llama instance
    game.obstacles = pygame.sprite.Group() # Real group is fine
    game.game_over = False
    game.score_eligible_for_save = False
    # Mock the method we want to check the call/return value of
    game._check_score_eligible = MagicMock()

    return game

# --- Test Cases ---

@patch('pygame.sprite.spritecollide')
@patch('pygame.time.set_timer')
def test_no_collision(mock_set_timer, mock_spritecollide, game_instance):
    """
    Test _check_collisions when no collision occurs.
    """
    # Arrange: spritecollide returns an empty list
    mock_spritecollide.return_value = []
    game_instance.game_over = False

    # Act
    game_instance._check_collisions()

    # Assert
    mock_spritecollide.assert_called_once_with(
        game_instance.llama, game_instance.obstacles, False, pygame.sprite.collide_mask
    )
    assert game_instance.game_over is False, "game_over should remain False"
    game_instance._check_score_eligible.assert_not_called()
    # Ensure set_timer wasn't called to stop the timer
    for call_args in mock_set_timer.call_args_list:
        assert call_args != call((constants.OBSTACLE_SPAWN_EVENT, 0)), \
               f"set_timer should not be called with 0, but was called with {call_args}"


@patch('pygame.sprite.spritecollide')
@patch('pygame.time.set_timer')
def test_collision_occurs_score_eligible(mock_set_timer, mock_spritecollide, game_instance):
    """
    Test _check_collisions when a collision occurs and score is eligible.
    """
    # Arrange: spritecollide returns a list with a mock obstacle
    mock_obstacle = MagicMock(spec=Obstacle)
    mock_spritecollide.return_value = [mock_obstacle]
    game_instance._check_score_eligible.return_value = True # Score is eligible
    game_instance.game_over = False

    # Act
    game_instance._check_collisions()

    # Assert
    mock_spritecollide.assert_called_once_with(
        game_instance.llama, game_instance.obstacles, False, pygame.sprite.collide_mask
    )
    assert game_instance.game_over is True, "game_over should be set to True"
    game_instance._check_score_eligible.assert_called_once()
    assert game_instance.score_eligible_for_save is True, "score_eligible_for_save should be True"
    mock_set_timer.assert_called_with(constants.OBSTACLE_SPAWN_EVENT, 0)


@patch('pygame.sprite.spritecollide')
@patch('pygame.time.set_timer')
def test_collision_occurs_score_not_eligible(mock_set_timer, mock_spritecollide, game_instance):
    """
    Test _check_collisions when a collision occurs and score is NOT eligible.
    """
    # Arrange: spritecollide returns a list with a mock obstacle
    mock_obstacle = MagicMock(spec=Obstacle)
    mock_spritecollide.return_value = [mock_obstacle]
    game_instance._check_score_eligible.return_value = False # Score is not eligible
    game_instance.game_over = False

    # Act
    game_instance._check_collisions()

    # Assert
    mock_spritecollide.assert_called_once_with(
        game_instance.llama, game_instance.obstacles, False, pygame.sprite.collide_mask
    )
    assert game_instance.game_over is True, "game_over should be set to True"
    game_instance._check_score_eligible.assert_called_once()
    assert game_instance.score_eligible_for_save is False, "score_eligible_for_save should be False"
    mock_set_timer.assert_called_with(constants.OBSTACLE_SPAWN_EVENT, 0)


@patch('pygame.sprite.spritecollide')
@patch('pygame.time.set_timer')
def test_no_obstacles_present(mock_set_timer, mock_spritecollide, game_instance):
    """
    Test _check_collisions when the obstacles group is empty.
    """
    # Arrange: Obstacles group is empty, spritecollide returns empty list
    game_instance.obstacles.empty() # Ensure the group is empty
    mock_spritecollide.return_value = []
    game_instance.game_over = False

    # Act
    game_instance._check_collisions()

    # Assert
    mock_spritecollide.assert_called_once_with(
        game_instance.llama, game_instance.obstacles, False, pygame.sprite.collide_mask
    )
    assert game_instance.game_over is False, "game_over should remain False"
    game_instance._check_score_eligible.assert_not_called()
    # Ensure set_timer wasn't called to stop the timer
    for call_args in mock_set_timer.call_args_list:
         assert call_args != call((constants.OBSTACLE_SPAWN_EVENT, 0)), \
               f"set_timer should not be called with 0, but was called with {call_args}"