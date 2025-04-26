# tests/test_constants.py

import pytest
import pygame
import sys
import os
from pathlib import Path

try:
    import constants
except ImportError:
    pytest.fail("Could not import constants.py. Check PYTHONPATH or file location.")


# --- Fixture to Initialize Pygame ---

@pytest.fixture(scope="module", autouse=True)
def pygame_init():
    """Initialize Pygame display minimally for image loading tests."""
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    try:
        pygame.display.init()
        print("Pygame display initialized for tests.")
        yield  # Let tests run
        pygame.display.quit()
        print("Pygame display quit after tests.")
    except pygame.error as e:
        pytest.skip(f"Pygame display could not be initialized, skipping image load tests: {e}")


# --- Test Basic Definitions and Types ---
# (Keep the tests for WINDOW_WIDTH, FPS, GROUND_Y, etc. as before)
def test_window_dimensions_defined():
    """Check window dimension constants exist and are positive integers."""
    assert isinstance(constants.WINDOW_WIDTH, int), "WINDOW_WIDTH should be an integer"
    assert constants.WINDOW_WIDTH > 0, "WINDOW_WIDTH should be positive"
    assert isinstance(constants.WINDOW_HEIGHT, int), "WINDOW_HEIGHT should be an integer"
    assert constants.WINDOW_HEIGHT > 0, "WINDOW_HEIGHT should be positive"


def test_fps_defined():
    """Check FPS constant exists and is a positive integer."""
    assert isinstance(constants.FPS, int), "FPS should be an integer"
    assert constants.FPS > 0, "FPS should be positive"


def test_ground_y_defined():
    """Check GROUND_Y constant exists, is an integer, and within screen height."""
    assert isinstance(constants.GROUND_Y, int), "GROUND_Y should be an integer"
    assert 0 <= constants.GROUND_Y < constants.WINDOW_HEIGHT, \
        "GROUND_Y should be within the window height"


def test_gravity_defined():
    """Check gravity constant exists and is a number."""
    assert isinstance(constants.GRAVITY, (int, float)), "GRAVITY should be a number (int or float)"


def test_jump_speed_defined():
    """Check jump speed constant exists and is a number."""
    assert isinstance(constants.JUMP_SPEED, (int, float)), "JUMP_SPEED should be a number (int or float)"


def test_player_position_defined():
    """Check player starting position constant exists and is within screen width."""
    assert isinstance(constants.PLAYER_HORIZONTAL_POSITION, int), \
        "PLAYER_HORIZONTAL_POSITION should be an integer"
    assert 0 <= constants.PLAYER_HORIZONTAL_POSITION < constants.WINDOW_WIDTH, \
        "PLAYER_HORIZONTAL_POSITION should be within the window width"


def test_obstacle_settings_defined():
    """Check obstacle constants exist and have expected types/values."""
    assert isinstance(constants.OBSTACLE_INITIAL_SPEED, (int, float)), \
        "OBSTACLE_INITIAL_SPEED should be a number (int or float)"
    assert isinstance(constants.OBSTACLE_CREATION_INTERVAL, int), \
        "OBSTACLE_CREATION_INTERVAL should be an integer"
    assert constants.OBSTACLE_CREATION_INTERVAL > 0, \
        "OBSTACLE_CREATION_INTERVAL should be positive (milliseconds)"


# --- Test Complex Types ---

# List expected color constants
EXPECTED_COLORS = [
    "WHITE", "BLACK", "GREY", "RED", "GREEN", "BLUE"
]


@pytest.mark.parametrize("color_name", EXPECTED_COLORS)
def test_color_values(color_name):
    """Check color constants are 3-element tuples of integers [0-255]."""
    assert hasattr(constants, color_name), f"Constant {color_name} is not defined"
    color_value = getattr(constants, color_name)

    assert isinstance(color_value, tuple), f"{color_name} should be a tuple"
    assert len(color_value) == 3, f"{color_name} should have 3 elements"
    for component in color_value:
        assert isinstance(component, int), f"Elements of {color_name} should be integers"
        assert 0 <= component <= 255, f"Elements of {color_name} should be between 0 and 255"


# List expected image path constants
EXPECTED_IMAGE_PATHS = [
    "PLAYER_IMAGE", "OBSTACLE_IMAGE", "GROUND_IMAGE", "GAME_ICON"
]


@pytest.mark.parametrize("path_name", EXPECTED_IMAGE_PATHS)
def test_image_paths_loadable(path_name, pygame_init):
    """Check image path constants are strings and the images can be loaded relative to project root."""
    # Verify constant exists and is a non-empty string
    assert hasattr(constants, path_name), f"Constant {path_name} is not defined"
    path_value = getattr(constants, path_name)
    assert isinstance(path_value, str), f"{path_name} should be a string"
    assert len(path_value) > 0, f"{path_name} should not be an empty string"

    try:
        # Get the path to the current test file (/path/to/Llama-Game/tests/test_constants.py)
        test_file_path = Path(__file__).resolve()
        # Get the project root directory (one level up from tests/)
        project_root = test_file_path.parent.parent
        # Construct the absolute path to the image file
        absolute_image_path = project_root / path_value

        # Attempt to load the image using the calculated absolute path
        # Convert Path object to string for pygame.image.load
        img = pygame.image.load(str(absolute_image_path))
        assert img is not None  # Check if loading returned a valid Surface object

    except FileNotFoundError:
        # The absolute path wasn't found
        pytest.fail(f"Image file not found for {path_name}. Calculated absolute path: '{absolute_image_path}'")
    except pygame.error as e:
        # Catch Pygame-specific errors (e.g., unsupported format, file corruption)
        pytest.fail(f"Pygame error loading image specified by {path_name} ('{absolute_image_path}'): {e}")


# --- Test Overall Accessibility ---

def test_constants_importable():
    """Check the constants module was successfully imported."""
    assert constants is not None
