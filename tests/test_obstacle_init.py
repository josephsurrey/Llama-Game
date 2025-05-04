import pytest
import pygame
from unittest.mock import patch, MagicMock, ANY
import random

# Assuming main.py and constants.py are in the same directory or accessible
# Corrected Obstacle class structure assumed for testing
from main import Obstacle
import constants

# Minimal Pygame setup fixture if needed
@pytest.fixture(scope="module", autouse=True)
def pygame_init():
    """Initialize pygame modules needed for tests."""
    pygame.init()
    yield
    pygame.quit()

# --- Test Obstacle.__init__ ---

@patch('pygame.sprite.Sprite.__init__')
@patch('pygame.image.load')
@patch('pygame.mask.from_surface')
@patch('random.randint')
def test_init_calls_super(mock_randint, mock_from_surface, mock_load, mock_sprite_init):
    """Verify __init__ calls the superclass constructor."""
    mock_surface = MagicMock(spec=pygame.Surface)
    mock_surface.convert_alpha.return_value = mock_surface
    mock_surface.get_rect.return_value = MagicMock(spec=pygame.Rect)
    mock_load.return_value = mock_surface
    mock_randint.return_value = 100

    Obstacle(speed=5)
    mock_sprite_init.assert_called_once()

@patch('pygame.sprite.Sprite.__init__')
@patch('pygame.image.load')
@patch('pygame.mask.from_surface')
@patch('random.randint')
def test_init_image_load_success(mock_randint, mock_from_surface, mock_load, mock_sprite_init):
    """Verify image loading success path."""
    mock_loaded_surface = MagicMock(spec=pygame.Surface)
    mock_converted_surface = MagicMock(spec=pygame.Surface)
    mock_loaded_surface.convert_alpha.return_value = mock_converted_surface
    mock_converted_surface.get_rect.return_value = MagicMock(spec=pygame.Rect)
    mock_load.return_value = mock_loaded_surface
    mock_randint.return_value = 100

    obstacle = Obstacle(speed=5)

    mock_load.assert_called_once_with(constants.OBSTACLE_IMAGE)
    mock_loaded_surface.convert_alpha.assert_called_once()
    assert obstacle.image == mock_converted_surface

@patch('pygame.sprite.Sprite.__init__')
@patch('pygame.image.load', side_effect=pygame.error("Test load error"))
@patch('main.pygame.Surface') # Patch where it's used if main imports pygame
@patch('pygame.mask.from_surface')
@patch('random.randint')
def test_init_image_load_failure_fallback(mock_randint, mock_from_surface, mock_surface_class, mock_load, mock_sprite_init):
    """Verify fallback mechanism on image load failure."""
    # Get the mock INSTANCE that the patched Surface CLASS will return
    mock_fallback_instance = mock_surface_class.return_value

    # Configure the mock INSTANCE *before* it's used
    # The code calls get_rect() on the result of Surface()
    mock_fallback_instance.get_rect.return_value = MagicMock(spec=pygame.Rect)

    mock_randint.return_value = 100

    # Suppress expected print message during test
    with patch('builtins.print') as mock_print:
        # Instantiating Obstacle calls the patched pygame.Surface,
        # which returns mock_fallback_instance
        obstacle = Obstacle(speed=5)

    # Assert the load was attempted
    mock_load.assert_called_once_with(constants.OBSTACLE_IMAGE)

    # Assert the Surface CLASS mock was called correctly
    mock_surface_class.assert_called_once_with([25, 50])

    # Assert methods were called on the specific INSTANCE returned
    mock_fallback_instance.fill.assert_called_once_with(constants.GREEN)

    # Assert the obstacle's image attribute IS the INSTANCE returned by the class mock
    assert obstacle.image == mock_fallback_instance

    # Assert get_rect was called on the instance (implicitly checked by obstacle.rect below)
    # mock_fallback_instance.get_rect.assert_called_once() # Optional explicit check

    # Check if error message was printed (optional, good practice)
    mock_print.assert_any_call(f"Error loading obstacle image: Test load error. Creating fallback shape.")


@patch('pygame.sprite.Sprite.__init__')
@patch('pygame.image.load')
@patch('main.pygame.mask.from_surface') # Patch where used
@patch('random.randint')
def test_init_rect_and_mask_creation(mock_randint, mock_from_surface, mock_load, mock_sprite_init):
    """Verify rect and mask creation for both success and fallback paths."""
    # --- Success Path ---
    mock_loaded_surface = MagicMock(spec=pygame.Surface)
    mock_converted_surface = MagicMock(spec=pygame.Surface)
    mock_rect_success = MagicMock(spec=pygame.Rect)
    mock_mask_success = MagicMock(spec=pygame.Mask)

    mock_loaded_surface.convert_alpha.return_value = mock_converted_surface
    mock_converted_surface.get_rect.return_value = mock_rect_success
    mock_load.return_value = mock_loaded_surface
    mock_load.side_effect = None
    mock_from_surface.return_value = mock_mask_success
    mock_randint.return_value = 100

    obstacle_success = Obstacle(speed=5)

    mock_converted_surface.get_rect.assert_called_once()
    mock_from_surface.assert_called_with(mock_converted_surface)
    assert obstacle_success.rect == mock_rect_success
    assert obstacle_success.mask == mock_mask_success

    # Reset mocks for Fallback Path
    mock_load.reset_mock()
    mock_from_surface.reset_mock()
    mock_sprite_init.reset_mock()
    mock_converted_surface.reset_mock() # Reset mocks on the temp surfaces too
    mock_loaded_surface.reset_mock()
    mock_randint.reset_mock()

    # --- Failure/Fallback Path ---
    mock_load.side_effect = pygame.error("Load failed again")
    mock_rect_fallback = MagicMock(spec=pygame.Rect)
    mock_mask_fallback = MagicMock(spec=pygame.Mask)

    # Patch pygame.Surface specifically for this block
    # And configure its return_value (the instance mock) immediately
    with patch('main.pygame.Surface') as fallback_surface_class_mock:
         # Configure the instance that WILL be returned
         fallback_instance_mock = fallback_surface_class_mock.return_value
         fallback_instance_mock.get_rect.return_value = mock_rect_fallback

         # Configure mask mock return value
         mock_from_surface.return_value = mock_mask_fallback
         mock_randint.return_value = 120

         # Suppress print
         with patch('builtins.print'):
             obstacle_fallback = Obstacle(speed=5) # Creates instance using mocked Surface

    # Assertions for the fallback path
    fallback_surface_class_mock.assert_called_once_with([25, 50]) # Class called
    fallback_instance_mock.fill.assert_called_once_with(constants.GREEN) # Fill on instance
    fallback_instance_mock.get_rect.assert_called_once() # get_rect on instance
    mock_from_surface.assert_called_with(fallback_instance_mock) # mask with instance
    assert obstacle_fallback.image == fallback_instance_mock # image is the instance
    assert obstacle_fallback.rect == mock_rect_fallback # rect is from instance.get_rect
    assert obstacle_fallback.mask == mock_mask_fallback # mask is from mask(instance)


@patch('pygame.sprite.Sprite.__init__')
@patch('pygame.image.load')
@patch('main.pygame.mask.from_surface') # Patch where used
@patch('random.randint')
def test_init_position_randomness_and_ground(mock_randint, mock_from_surface, mock_load, mock_sprite_init):
    """Verify initial position uses random X and correct ground Y."""
    mock_surface = MagicMock(spec=pygame.Surface)
    mock_rect = MagicMock(spec=pygame.Rect)
    mock_rect.bottomleft = (0, 0) # Initialize attribute for checking assignment

    mock_surface.convert_alpha.return_value = mock_surface
    mock_surface.get_rect.return_value = mock_rect
    mock_load.return_value = mock_surface
    mock_randint.return_value = 150

    obstacle = Obstacle(speed=5)

    mock_randint.assert_called_once_with(50, 200)
    expected_x = constants.WINDOW_WIDTH + 150
    expected_y = constants.GROUND_Y
    # Check the final state of the rect assigned to the instance
    assert obstacle.rect is mock_rect # Ensure the mock rect was assigned
    # Check the value that was assigned to bottomleft *on the mock_rect*
    # This assertion relies on the mock object tracking attribute assignments
    # You could also access the setter mock if needed: mock_rect.mock_calls
    assert obstacle.rect.bottomleft == (expected_x, expected_y)


@patch('pygame.sprite.Sprite.__init__')
@patch('pygame.image.load')
@patch('main.pygame.mask.from_surface') # Patch where used
@patch('random.randint')
def test_init_speed_assignment(mock_randint, mock_from_surface, mock_load, mock_sprite_init):
    """Verify the speed parameter is correctly assigned."""
    mock_surface = MagicMock(spec=pygame.Surface)
    mock_surface.convert_alpha.return_value = mock_surface
    mock_surface.get_rect.return_value = MagicMock(spec=pygame.Rect)
    mock_load.return_value = mock_surface
    mock_randint.return_value = 100

    speed_value = 10
    obstacle = Obstacle(speed=speed_value)
    assert obstacle.speed == speed_value

    speed_value_zero = 0
    obstacle_zero = Obstacle(speed=speed_value_zero)
    assert obstacle_zero.speed == speed_value_zero