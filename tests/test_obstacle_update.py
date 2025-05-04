# test_obstacle_update.py
import pygame
import pytest
from unittest.mock import patch, MagicMock

# Assuming constants.py and main.py (with Obstacle class) are in the same directory or accessible
import constants
from main import Obstacle

# --- Fixtures ---

@pytest.fixture(scope="module", autouse=True)
def pygame_init():
    """Initialize pygame modules needed for testing."""
    pygame.init()
    yield
    pygame.quit()

@pytest.fixture
def obstacle_instance(request):
    """Creates an Obstacle instance, handling potential image load errors."""
    speed = request.param if hasattr(request, "param") else 5

    # Mock image loading to force fallback surface creation, isolating the test
    with patch('pygame.image.load', side_effect=pygame.error("Test load error")):
        with patch('pygame.mask.from_surface', return_value=MagicMock()): # Mock mask creation
            obstacle = Obstacle(speed=speed)
            # Override random initial position for predictable testing
            # Use a known rect. Fallback surface size is [25, 50]
            obstacle.rect = pygame.Rect(100, constants.GROUND_Y - 50, 25, 50)
            return obstacle

# --- Test Cases ---

@pytest.mark.parametrize("obstacle_instance", [5], indirect=True)
def test_move_left(obstacle_instance):
    """Test that the obstacle moves left by its speed amount."""
    initial_x = obstacle_instance.rect.x
    obstacle_instance.update()
    assert obstacle_instance.rect.x == initial_x - obstacle_instance.speed

@pytest.mark.parametrize("obstacle_instance", [3], indirect=True)
def test_move_left_repeatedly(obstacle_instance):
    """Test that the obstacle moves steadily left after multiple updates."""
    initial_x = obstacle_instance.rect.x
    obstacle_instance.update()
    assert obstacle_instance.rect.x == initial_x - obstacle_instance.speed
    obstacle_instance.update()
    assert obstacle_instance.rect.x == initial_x - 2 * obstacle_instance.speed

@pytest.mark.parametrize("obstacle_instance", [5], indirect=True)
def test_off_screen_check_on_screen(obstacle_instance):
    """Test that the obstacle is not killed when it's still on screen."""
    obstacle_instance.rect.right = 10 # Position it partially on screen
    test_group = pygame.sprite.Group()
    test_group.add(obstacle_instance)

    obstacle_instance.update()

    assert obstacle_instance.rect.right == 5 # Moved left
    assert obstacle_instance in test_group # Should still be in the group
    assert len(test_group) == 1

@pytest.mark.parametrize("obstacle_instance", [10], indirect=True)
def test_off_screen_check_boundary(obstacle_instance):
    """Test that the obstacle is killed exactly when its right edge goes < 0."""
    obstacle_instance.rect.right = 5 # Position it close to the edge
    test_group = pygame.sprite.Group()
    test_group.add(obstacle_instance)

    obstacle_instance.update() # rect.right becomes 5 - 10 = -5

    assert obstacle_instance.rect.right == -5 # Moved off screen
    assert obstacle_instance not in test_group # Should be removed (killed)
    assert len(test_group) == 0

# --- Corrected Test Case ---
@pytest.mark.parametrize("obstacle_instance", [0], indirect=True)
def test_zero_speed_obstacle(obstacle_instance):
    """Test that an obstacle with zero speed does not move and is not killed."""
    # Set the desired position *first*
    obstacle_instance.rect.right = 50 # Ensure it's on screen (width is 25, so x becomes 25)
    x_before_update = obstacle_instance.rect.x # Capture x *after* setting right (should be 25)

    test_group = pygame.sprite.Group()
    test_group.add(obstacle_instance)

    obstacle_instance.update() # Call update with speed 0

    # Check if position changed *during* update
    assert obstacle_instance.rect.x == x_before_update # Should still be 25
    # Check if it was killed (it shouldn't be)
    assert obstacle_instance in test_group # Should still be in the group
    assert len(test_group) == 1