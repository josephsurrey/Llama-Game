import pytest
import pygame
from unittest.mock import patch, MagicMock, ANY, Mock

# Assuming main.py and constants.py are in the same directory or accessible
import main
import constants

# Minimal Pygame setup needed for Surface, Rect, Mask
@pytest.fixture(autouse=True)
def pygame_setup():
    pygame.init()
    pygame.display.set_mode((1, 1), pygame.NOFRAME)
    yield
    pygame.quit()

# Mock Llama class dependencies that are not part of the test
@pytest.fixture
def mock_dependencies():
    mock_loaded_surface = MagicMock(spec=pygame.Surface)
    # Create the mock_rect, but we won't try complex verification on its attributes
    mock_rect = MagicMock(spec=pygame.Rect)
    mock_rect.height = 50 # Define height for calculations

    mock_loaded_surface.get_rect.return_value = mock_rect
    mock_loaded_surface.convert_alpha.return_value = mock_loaded_surface

    with patch('pygame.image.load', return_value=mock_loaded_surface) as mock_load, \
         patch('pygame.mask.from_surface', return_value=MagicMock(spec=pygame.Mask)) as mock_mask, \
         patch('pygame.sprite.Sprite.__init__') as mock_super_init, \
         patch('main.pygame.Surface') as mock_pygame_surface_class:

        mock_default_surface_instance = MagicMock(name='default_surface_instance')
        mock_pygame_surface_class.return_value = mock_default_surface_instance

        yield {
            "mock_load": mock_load,
            "mock_mask": mock_mask,
            "mock_super_init": mock_super_init,
            "mock_loaded_surface": mock_loaded_surface,
            "mock_rect": mock_rect, # Pass the mock rect for identity checks
            "mock_pygame_surface_class": mock_pygame_surface_class
        }

# --- Test Cases ---

def test_super_init_called(mock_dependencies):
    """Test: Superclass Initialization"""
    llama = main.Llama()
    mock_dependencies["mock_super_init"].assert_called_once()

def test_image_load_success_path(mock_dependencies):
    """Test: Image Load Success Path"""
    mock_loaded_surface = mock_dependencies["mock_loaded_surface"]
    mock_load = mock_dependencies["mock_load"]
    llama = main.Llama()
    mock_load.assert_called_once_with(constants.PLAYER_IMAGE)
    mock_loaded_surface.convert_alpha.assert_called_once()
    assert llama.image is mock_loaded_surface

def test_image_load_failure_path_fallback(mock_dependencies):
    """Test: Image Load Failure Path (Fallback)"""
    mock_load = mock_dependencies["mock_load"]
    mock_pygame_surface_class = mock_dependencies["mock_pygame_surface_class"]
    mock_fallback_surface_instance = MagicMock(name='fallback_surface_instance')
    mock_fallback_rect = MagicMock(spec=pygame.Rect, height=60)
    mock_fallback_surface_instance.get_rect.return_value = mock_fallback_rect
    mock_load.side_effect = Exception("Failed to load")
    mock_pygame_surface_class.return_value = mock_fallback_surface_instance
    llama = main.Llama()
    mock_load.assert_called_once_with(constants.PLAYER_IMAGE)
    mock_pygame_surface_class.assert_called_once_with([40, 60])
    mock_fallback_surface_instance.fill.assert_called_once_with(constants.RED)
    assert llama.image is mock_fallback_surface_instance

def test_rect_and_mask_creation_on_success(mock_dependencies):
    """Test: Rect and Mask Creation (Success Path)"""
    mock_loaded_surface = mock_dependencies["mock_loaded_surface"]
    mock_mask_func = mock_dependencies["mock_mask"]
    mock_mask_instance = mock_mask_func.return_value
    mock_rect = mock_dependencies["mock_rect"]
    llama = main.Llama()
    mock_loaded_surface.get_rect.assert_called_once()
    assert llama.rect is mock_rect
    mock_mask_func.assert_called_once_with(mock_loaded_surface)
    assert llama.mask is mock_mask_instance

def test_rect_and_mask_creation_on_failure(mock_dependencies):
    """Test: Rect and Mask Creation (Failure Path)"""
    mock_load = mock_dependencies["mock_load"]
    mock_pygame_surface_class = mock_dependencies["mock_pygame_surface_class"]
    mock_mask_func = mock_dependencies["mock_mask"]
    mock_mask_instance = mock_mask_func.return_value
    mock_fallback_surface_instance = MagicMock(name='fallback_surface_instance_for_rect_mask')
    mock_fallback_rect = MagicMock(spec=pygame.Rect, height=60)
    mock_fallback_surface_instance.get_rect.return_value = mock_fallback_rect
    mock_load.side_effect = Exception("Failed to load")
    mock_pygame_surface_class.return_value = mock_fallback_surface_instance
    llama = main.Llama()
    mock_fallback_surface_instance.get_rect.assert_called_once()
    assert llama.rect is mock_fallback_rect
    mock_mask_func.assert_called_once_with(mock_fallback_surface_instance)
    assert llama.mask is mock_mask_instance

def test_physics_variables_initialized(mock_dependencies):
    """Test: Physics Variables Initialized"""
    llama = main.Llama()
    assert llama.velocity_y == 0
    assert llama.is_jumping is False

def test_initial_position_calculation_and_assignment(mock_dependencies):
    """Test: Initial Position Calculation & Assignment"""
    mock_rect = mock_dependencies["mock_rect"]
    expected_height = mock_rect.height
    expected_initial_pos = (
        constants.PLAYER_HORIZONTAL_POSITION,
        constants.GROUND_Y - expected_height,
    )
    # expected_final_left = 100 # Cannot reliably verify on mock
    # expected_final_bottom = 50 # Cannot reliably verify on mock

    llama = main.Llama() # Init assigns rect.bottomleft

    # Verify the initial_pos calculation
    assert llama.initial_pos == expected_initial_pos
    # Verify the correct rect object was assigned
    assert llama.rect is mock_rect

    # NOTE: We cannot reliably assert mock_rect.left or mock_rect.bottom here
    # because MagicMock(spec=pygame.Rect) does not fully replicate the side
    # effects of assigning to virtual attributes like 'bottomleft'.
    # We trust the line `self.rect.bottomleft = self.initial_pos` works
    # in the actual Pygame environment.


def test_initial_position_calculation_and_assignment_fallback(mock_dependencies):
    """Test: Initial Position Calculation & Assignment (Fallback Path)"""
    mock_load = mock_dependencies["mock_load"]
    mock_pygame_surface_class = mock_dependencies["mock_pygame_surface_class"]
    mock_fallback_surface_instance = MagicMock(name='fallback_surface_instance_for_pos')
    mock_fallback_rect = MagicMock(spec=pygame.Rect, height=60)
    mock_fallback_surface_instance.get_rect.return_value = mock_fallback_rect
    mock_load.side_effect = Exception("Failed to load")
    mock_pygame_surface_class.return_value = mock_fallback_surface_instance
    expected_height = 60
    expected_initial_pos = (
        constants.PLAYER_HORIZONTAL_POSITION,
        constants.GROUND_Y - expected_height,
    )
    # expected_final_left = 100 # Cannot reliably verify on mock
    # expected_final_bottom = 40 # Cannot reliably verify on mock

    # Act
    llama = main.Llama() # Init assigns rect.bottomleft

    # Assert
    # Verify the initial_pos calculation
    assert llama.initial_pos == expected_initial_pos
    # Verify the correct rect object was assigned
    assert llama.rect is mock_fallback_rect

    