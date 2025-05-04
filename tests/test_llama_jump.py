# test_llama_jump.py
import pytest
import pygame # Required for fallback surface in Llama.__init__ if image fails

# Assume constants.py and main.py are in the python path or same directory
import constants
from main import Llama

# Minimal Pygame setup needed for Llama initialization if image loading fails
pygame.init()
pygame.display.set_mode((1, 1)) # Dummy display

@pytest.fixture
def llama_instance():
    """Provides a fresh Llama instance for each test."""
    # Mock image loading to avoid file dependency and pygame errors in tests
    # If Llama.__init__ handles image loading failure gracefully (which it seems to),
    # we might not strictly need mocking, but it makes tests more robust.
    try:
        original_load = pygame.image.load
        original_from_surface = pygame.mask.from_surface

        # Mock load to return a dummy surface
        dummy_surface = pygame.Surface((40, 60))
        dummy_surface.fill(constants.RED)
        pygame.image.load = lambda path: dummy_surface

        # Mock mask creation
        dummy_mask = pygame.mask.Mask((40, 60))
        pygame.mask.from_surface = lambda surface: dummy_mask

        llama = Llama()
        # Ensure initial state is consistent if needed (though jump doesn't depend on pos)
        llama.rect.bottomleft = llama.initial_pos
        llama.velocity_y = 0
        llama.is_jumping = False
        yield llama
    finally:
        # Restore original pygame functions
        pygame.image.load = original_load
        pygame.mask.from_surface = original_from_surface
        pygame.quit() # Clean up pygame init

def test_jump_when_not_jumping(llama_instance):
    """
    Test Case: Jump When Not Jumping
    Input / Conditions: self.is_jumping is False
    Expected Output: self.velocity_y becomes constants.JUMP_SPEED, self.is_jumping becomes True.
    """
    llama = llama_instance
    initial_velocity = llama.velocity_y
    initial_jumping_state = llama.is_jumping

    # Pre-condition check (optional but good practice)
    assert not initial_jumping_state
    assert initial_velocity == 0 # Based on fixture setup

    # Action
    llama.jump()

    # Assertions
    assert llama.velocity_y == constants.JUMP_SPEED
    assert llama.is_jumping is True

def test_attempt_jump_when_already_jumping(llama_instance):
    """
    Test Case: Attempt Jump When Already Jumping
    Input / Conditions: self.is_jumping is True
    Expected Output: No change to self.velocity_y or self.is_jumping.
    """
    llama = llama_instance

    # Set initial state to already jumping
    llama.is_jumping = True
    llama.velocity_y = constants.JUMP_SPEED # Or some other non-zero value simulating jump

    initial_velocity = llama.velocity_y
    initial_jumping_state = llama.is_jumping

    # Pre-condition check
    assert initial_jumping_state is True

    # Action
    llama.jump()

    # Assertions: Check that values remain unchanged
    assert llama.velocity_y == initial_velocity
    assert llama.is_jumping is True # Should remain True

# Optional: Test with different initial velocity when not jumping
def test_jump_when_not_jumping_non_zero_initial_velocity(llama_instance):
    """
    Test Case: Jump When Not Jumping (with potentially non-zero initial velocity, though unlikely)
    Input / Conditions: self.is_jumping is False, self.velocity_y is something else (e.g., falling)
    Expected Output: self.velocity_y becomes constants.JUMP_SPEED, self.is_jumping becomes True.
    """
    llama = llama_instance
    llama.is_jumping = False
    llama.velocity_y = 5 # Simulate falling slightly

    # Pre-condition check
    assert not llama.is_jumping

    # Action
    llama.jump()

    # Assertions
    assert llama.velocity_y == constants.JUMP_SPEED
    assert llama.is_jumping is True