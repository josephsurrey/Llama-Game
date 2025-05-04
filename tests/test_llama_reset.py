# test_llama_reset.py

import pygame
import pytest

# Assuming constants.py and main.py (with Llama class) are in the same directory
# or accessible via Python path
import constants
from main import Llama

# --- Fixtures ---

@pytest.fixture(scope="module", autouse=True)
def pygame_init():
    """Initialize pygame for all tests in this module."""
    pygame.init()
    # Create a dummy display required by some pygame functions
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()

@pytest.fixture
def llama_instance():
    """Provides a fresh Llama instance for each test."""
    # Rely on Llama's __init__ fallback for image if needed
    llama = Llama()
    # Explicitly check image height from fallback for calculations
    assert llama.rect.height == 60 # Assuming fallback is used
    return llama

# --- Test Cases ---

def test_reset_after_jump(llama_instance):
    """
    Test resetting the Llama after it has jumped (in the air, moving up).
    Verifies position, velocity, and jumping state are reset.
    Corresponds to: Reset After Jump
    """
    # Simulate a jump state
    llama_instance.is_jumping = True
    llama_instance.velocity_y = -10  # Moving upwards
    initial_actual_pos = llama_instance.rect.bottomleft
    llama_instance.rect.y -= 50 # Move it up significantly

    assert llama_instance.rect.bottomleft != initial_actual_pos
    assert llama_instance.velocity_y == -10
    assert llama_instance.is_jumping is True

    # --- Act ---
    llama_instance.reset()

    # --- Assert ---
    # Calculate the expected initial position based on how reset() calculates it
    expected_initial_pos_tuple = (
        constants.PLAYER_HORIZONTAL_POSITION, # 100
        constants.GROUND_Y - llama_instance.rect.height, # 100 - 60 = 40 (This is TOP-LEFT Y)
    )
    # reset() sets bottomleft, so calculate the expected bottomleft
    expected_bottomleft = (
        constants.PLAYER_HORIZONTAL_POSITION, # 100
        constants.GROUND_Y                  # 100
    )

    assert llama_instance.rect.bottomleft == expected_bottomleft
    assert llama_instance.velocity_y == 0
    assert llama_instance.is_jumping is False

def test_reset_while_moving(llama_instance):
    """
    Test resetting the Llama while it is moving (e.g., falling mid-air).
    Verifies position, velocity, and jumping state are reset.
    Corresponds to: Reset While Moving
    """
    # Simulate a mid-air falling state (not necessarily triggered by jump)
    llama_instance.is_jumping = False # Could be True or False, test False
    llama_instance.velocity_y = 5 # Moving downwards
    initial_actual_pos = llama_instance.rect.bottomleft
    llama_instance.rect.y -= 30 # Move it up a bit from initial (0,0) top-left

    assert llama_instance.rect.bottomleft != initial_actual_pos
    assert llama_instance.velocity_y == 5
    assert llama_instance.is_jumping is False

    # --- Act ---
    llama_instance.reset()

    # --- Assert ---
    # Calculate the expected bottomleft position after reset
    expected_bottomleft = (
        constants.PLAYER_HORIZONTAL_POSITION, # 100
        constants.GROUND_Y                  # 100
    )
    assert llama_instance.rect.bottomleft == expected_bottomleft
    assert llama_instance.velocity_y == 0
    assert llama_instance.is_jumping is False

def test_reset_from_ground(llama_instance):
    """
    Test resetting the Llama when it is already on the ground (or technically,
    at its initial position as set by __init__).
    Verifies position, velocity, and jumping state are correctly SET by reset().
    Corresponds to: Reset From Ground
    """
    # Llama starts at ACTUAL position after __init__ because __init__ doesn't set it
    initial_actual_bottomleft = llama_instance.rect.bottomleft
    initial_velocity_after_init = llama_instance.velocity_y
    initial_jumping_state_after_init = llama_instance.is_jumping

    # Ensure initial state is as ACTUALLY created by __init__
    # Fallback surface is 40x60, rect starts at (0,0) top-left
    assert initial_actual_bottomleft == (0, 60) # Actual bottom-left coord
    assert initial_velocity_after_init == 0
    assert initial_jumping_state_after_init is False

    # --- Act ---
    llama_instance.reset() # This should now SET the correct position

    # --- Assert ---
    # Calculate the expected bottomleft position after reset
    expected_bottomleft = (
        constants.PLAYER_HORIZONTAL_POSITION, # 100
        constants.GROUND_Y                  # 100
    )
    # Check final state matches expected reset state
    assert llama_instance.rect.bottomleft == expected_bottomleft
    assert llama_instance.velocity_y == 0
    assert llama_instance.is_jumping is False

    # Explicitly check that the bottom is now at GROUND_Y
    assert llama_instance.rect.bottom == constants.GROUND_Y