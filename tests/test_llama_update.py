# test_llama_update.py
import pytest
from unittest.mock import patch, MagicMock
import pygame  # Keep this import for pygame.Rect

# Import the module under test
import main

# Mock pygame globally for all tests in this module
@pytest.fixture(autouse=True)
def mock_pygame(mocker):
    """Automatically mocks pygame components needed for Llama."""
    # Mock the 'pygame' module accessed by 'main'
    mocker.patch('main.pygame', MagicMock())
    # Mock the base Sprite class initialization if needed
    mocker.patch('main.pygame.sprite.Sprite', MagicMock())

    # --- Mock Surface and Rect ---
    # 1. Create a mock Surface
    mock_surface = MagicMock(spec=pygame.Surface)

    # 2. Create a REAL Rect instance to be returned by get_rect
    #    Initialize with dummy values; llama_instance fixture will position it.
    real_rect = pygame.Rect(0, 0, 40, 60) # width=40, height=60
    mock_surface.get_rect.return_value = real_rect

    # 3. Mock convert_alpha to return the same mock surface
    mock_surface.convert_alpha.return_value = mock_surface

    # Patch the specific functions within the mocked main.pygame
    mocker.patch('main.pygame.image.load', return_value=mock_surface)
    mocker.patch('main.pygame.mask.from_surface', return_value=MagicMock())
    # Patch Surface creation for the fallback case in Llama.__init__
    mocker.patch('main.pygame.Surface', return_value=mock_surface)

# Mock constants necessary for Llama.update and __init__ positioning
@pytest.fixture
def mock_constants(mocker):
    """Provides mocked constants for the tests."""
    mocker.patch('main.constants.PLAYER_HORIZONTAL_POSITION', 100)
    mocker.patch('main.constants.GROUND_Y', 300) # Example ground Y
    mocker.patch('main.constants.GRAVITY', 2)    # Mock GRAVITY to non-zero
    mocker.patch('main.constants.PLAYER_IMAGE', "dummy_path.png")
    mocker.patch('main.constants.RED', (255, 0, 0))

# Fixture for the Llama instance
@pytest.fixture
def llama_instance(mock_constants): # mock_pygame runs automatically
    """Provides a Llama instance initialized with a real Rect."""
    llama = main.Llama() # __init__ gets the real_rect via mocked get_rect

    # --- Refinement: Ensure rect positioning uses the REAL rect ---
    # llama.rect is now the real_rect object created in mock_pygame
    assert isinstance(llama.rect, pygame.Rect) # Verify it's a real Rect

    # Recalculate initial_pos based *exactly* on mocked values and REAL rect height
    llama.initial_pos = (
        main.constants.PLAYER_HORIZONTAL_POSITION,
        main.constants.GROUND_Y - llama.rect.height # Use the real rect's height
    )
    # Set the position of the REAL rect
    llama.rect.bottomleft = llama.initial_pos

    # Reset physics variables
    llama.velocity_y = 0
    llama.is_jumping = False

    # print(f"Initial llama rect in fixture: {llama.rect}") # Debug print
    return llama

# --- Test Cases ---

# Test Case: Apply Gravity (velocity_y is 0)
def test_update_apply_gravity_from_stationary(llama_instance):
    initial_y = llama_instance.rect.y
    initial_velocity_y = llama_instance.velocity_y # Should be 0
    assert isinstance(initial_y, int) # Verify attribute is int

    llama_instance.update()

    # Velocity should increase by GRAVITY
    assert llama_instance.velocity_y == initial_velocity_y + main.constants.GRAVITY
    # Y position should change based on the *new* velocity (integer part)
    assert llama_instance.rect.y == initial_y + int(llama_instance.velocity_y)
    assert isinstance(llama_instance.rect.y, int) # Verify still int
    # is_jumping state should not change here
    assert not llama_instance.is_jumping

# Test Case: Apply Gravity (velocity_y is positive, falling)
def test_update_apply_gravity_while_falling(llama_instance):
    llama_instance.velocity_y = 5 # Already falling
    initial_y = llama_instance.rect.y
    initial_velocity_y = llama_instance.velocity_y
    assert isinstance(initial_y, int)

    llama_instance.update()

    # Velocity should increase by GRAVITY
    assert llama_instance.velocity_y == initial_velocity_y + main.constants.GRAVITY
    # Y position should change based on the *new* velocity (integer part)
    assert llama_instance.rect.y == initial_y + int(llama_instance.velocity_y)
    assert isinstance(llama_instance.rect.y, int)
    # is_jumping state should not change here
    assert not llama_instance.is_jumping

# Test Case: Apply Gravity (Moving Up, velocity_y is negative)
def test_update_apply_gravity_while_moving_up(llama_instance):
    llama_instance.velocity_y = -10 # Moving up
    llama_instance.is_jumping = True # Typically true when moving up
    initial_y = llama_instance.rect.y
    initial_velocity_y = llama_instance.velocity_y
    assert isinstance(initial_y, int)

    llama_instance.update()

    # Velocity should increase by GRAVITY (become less negative)
    assert llama_instance.velocity_y == initial_velocity_y + main.constants.GRAVITY
    # Y position should change based on the *new* velocity (integer part)
    assert llama_instance.rect.y == initial_y + int(llama_instance.velocity_y)
    assert isinstance(llama_instance.rect.y, int)
    # is_jumping state should remain True
    assert llama_instance.is_jumping

# Test Case: Ground Collision Check (On Ground)
def test_update_ground_collision_on_ground(llama_instance):
    # Place llama exactly on the ground
    llama_instance.rect.bottom = main.constants.GROUND_Y
    llama_instance.velocity_y = 0
    llama_instance.is_jumping = False
    initial_y = llama_instance.rect.y # Y position before update
    assert isinstance(llama_instance.rect.bottom, int)
    assert isinstance(initial_y, int)

    # print(f"Before update (on ground): {llama_instance.rect}, vy={llama_instance.velocity_y}")
    llama_instance.update()
    # print(f"After update (on ground): {llama_instance.rect}, vy={llama_instance.velocity_y}")


    # Gravity (2) applied (vy=2), y increases by 2
    # Collision check snaps bottom to GROUND_Y, sets vy=0, is_jumping=False
    assert llama_instance.velocity_y == 0, "Velocity should be 0 after ground collision"
    # Position snapped back to ground
    assert llama_instance.rect.bottom == main.constants.GROUND_Y, "Bottom should be exactly ground Y"
    # Check Y position corresponds to bottom - height
    assert llama_instance.rect.y == main.constants.GROUND_Y - llama_instance.rect.height, "Y position incorrect after snap"
    assert isinstance(llama_instance.rect.y, int)
    # Should confirm not jumping
    assert not llama_instance.is_jumping, "is_jumping should be False after ground collision"

# Test Case: Ground Collision Check (Slightly Below Ground)
def test_update_ground_collision_below_ground(llama_instance):
    # Place llama slightly below the ground
    llama_instance.rect.bottom = main.constants.GROUND_Y + 5
    llama_instance.velocity_y = 10 # Example positive velocity
    llama_instance.is_jumping = False
    assert isinstance(llama_instance.rect.bottom, int)

    # print(f"Before update (below ground): {llama_instance.rect}, vy={llama_instance.velocity_y}")
    llama_instance.update()
    # print(f"After update (below ground): {llama_instance.rect}, vy={llama_instance.velocity_y}")


    # Gravity (2) applied (vy=12), y increases by 12
    # Collision check snaps bottom to GROUND_Y, sets vy=0, is_jumping=False
    assert llama_instance.velocity_y == 0, "Velocity should be 0 after ground collision"
    # Position snapped back to ground
    assert llama_instance.rect.bottom == main.constants.GROUND_Y, "Bottom should be exactly ground Y"
    # Check Y position corresponds to bottom - height
    assert llama_instance.rect.y == main.constants.GROUND_Y - llama_instance.rect.height, "Y position incorrect after snap"
    assert isinstance(llama_instance.rect.y, int)
    # Should confirm not jumping
    assert not llama_instance.is_jumping, "is_jumping should be False after ground collision"

# Test Case: No Ground Collision (Mid-Air)
def test_update_no_ground_collision_mid_air(llama_instance):
    # Place llama above the ground
    llama_instance.rect.bottom = main.constants.GROUND_Y - 50
    llama_instance.velocity_y = -5 # Moving upwards initially
    llama_instance.is_jumping = True
    initial_y = llama_instance.rect.y
    initial_velocity_y = llama_instance.velocity_y
    assert isinstance(initial_y, int)
    assert isinstance(llama_instance.rect.bottom, int)

    # print(f"Before update (mid-air): {llama_instance.rect}, vy={llama_instance.velocity_y}")
    llama_instance.update()
    # print(f"After update (mid-air): {llama_instance.rect}, vy={llama_instance.velocity_y}")


    # Velocity should just update due to gravity
    assert llama_instance.velocity_y == initial_velocity_y + main.constants.GRAVITY
    # Y position should change based on the *new* velocity
    assert llama_instance.rect.y == initial_y + int(llama_instance.velocity_y)
    assert isinstance(llama_instance.rect.y, int)
    # Should still be considered jumping
    assert llama_instance.is_jumping
    # Ensure it didn't snap to ground
    assert llama_instance.rect.bottom < main.constants.GROUND_Y