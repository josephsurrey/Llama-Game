import pytest
import pygame
from unittest.mock import MagicMock, patch, call
import sys
from pathlib import Path # Required for mocking Path operations if needed

# Assume constants.py and main.py are in the same directory or accessible via PYTHONPATH
import constants
# Need to import the actual classes used in Game.__init__ and the tested method
from main import Game # Assuming Llama, Obstacle, Scoreboard are defined/imported in main.py


# --- Mock Classes ---
# Mock dependent classes to isolate the Game class logic
class MockLlama(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(constants.PLAYER_HORIZONTAL_POSITION, constants.GROUND_Y - 50, 30, 50) # Example dimensions

    def jump(self): pass
    def reset(self): pass
    def update(self): pass

class MockObstacle(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        # Give it a rect for collision checks if they were part of the tested method
        self.rect = pygame.Rect(constants.WINDOW_WIDTH, constants.GROUND_Y - 40, 20, 40) # Example dimensions
        self.speed = speed

    def update(self): pass

class MockScoreboard:
    def __init__(self):
        self.score = 0
        # Mock surface and rect if Scoreboard draws itself directly
        # self.image = MagicMock(spec=pygame.Surface)
        # self.rect = pygame.Rect(10, 10, 50, 20)

    def update(self, current_time_ticks, game_start_time_ticks): pass
    def draw(self, screen): pass # Mocked draw method
    def reset(self): self.score = 0


# --- Fixtures ---
@pytest.fixture(autouse=True)
def mock_pygame_init():
    """
    Auto-mocks fundamental pygame functions called during Game initialization
    and potentially by the tested method. Runs for every test.
    """
    # Using spec=pygame.Surface ensures the mock behaves like a Surface (e.g., has get_rect)
    mock_surface = MagicMock(spec=pygame.Surface)
    mock_surface.get_rect.return_value = pygame.Rect(0, 0, constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)
    mock_surface.get_height.return_value = 50 # Example height for ground image

    # Mock image loading to return a mock surface
    mock_loaded_image = MagicMock(spec=pygame.Surface)
    mock_loaded_image.convert.return_value = mock_loaded_image # Mock convert() call
    mock_loaded_image.get_height.return_value = 50 # Example height

    # --- Function to create a new mock font object on demand ---
    def create_mock_font(*args, **kwargs):
        mock_font_obj = MagicMock(spec=pygame.font.Font)
        rendered_surfaces_store = {}
        def mock_render(text, antialias, color):
            # Create unique surface per text if not seen before by *this* font instance
            if text not in rendered_surfaces_store:
                surf = MagicMock(spec=pygame.Surface)
                def mock_get_rect(**kwargs):
                    rect = pygame.Rect(0, 0, len(text) * 5 + 5, 15) # Approx size
                    if 'center' in kwargs: rect.center = kwargs['center']
                    elif 'topleft' in kwargs: rect.topleft = kwargs['topleft']
                    return rect
                surf.get_rect = MagicMock(side_effect=mock_get_rect)
                surf._rendered_text = text
                rendered_surfaces_store[text] = surf
            return rendered_surfaces_store[text]
        mock_font_obj.render = MagicMock(side_effect=mock_render)
        return mock_font_obj
    # --- End of function ---

    # Apply patches using a context manager
    with patch('pygame.init') as mock_py_init, \
         patch('pygame.mixer.init') as mock_mixer_init, \
         patch('pygame.font.init') as mock_font_init, \
         patch('pygame.display.set_mode', return_value=mock_surface) as mock_set_mode, \
         patch('pygame.display.set_caption') as mock_set_caption, \
         patch('pygame.time.Clock', return_value=MagicMock()) as mock_clock, \
         patch('pygame.time.get_ticks', return_value=0) as mock_get_ticks, \
         patch('pygame.time.set_timer') as mock_set_timer, \
         patch('pygame.image.load', return_value=mock_loaded_image) as mock_image_load, \
         patch('pygame.font.SysFont', side_effect=create_mock_font) as mock_sysfont: # Use side_effect
        # Yield control and necessary mocks to the test function.
        yield {
            "mock_py_init": mock_py_init,
            "mock_mixer_init": mock_mixer_init,
            "mock_font_init": mock_font_init,
            "mock_set_mode": mock_set_mode,
            "mock_set_caption": mock_set_caption,
            "mock_clock": mock_clock,
            "mock_get_ticks": mock_get_ticks,
            "mock_set_timer": mock_set_timer,
            "mock_image_load": mock_image_load,
            "mock_sysfont": mock_sysfont, # Provide the SysFont mock itself
            "mock_screen": mock_surface, # Provide the screen mock
            # Note: We no longer provide a single 'mock_font' as each SysFont call gets a new one
        }
    # Patches are automatically removed when the 'with' block exits.


@pytest.fixture
def game_instance(mock_pygame_init):
    """
    Provides a Game instance with mocked dependencies for testing.
    Relies on mock_pygame_init to handle basic pygame setup mocks.
    Game.__init__ will now receive distinct font mocks from the patched SysFont.
    """
    # Mock dependent classes specifically for Game's __init__
    with patch('main.Llama', MockLlama) as mock_llama_class, \
         patch('main.Obstacle', MockObstacle) as mock_obstacle_class, \
         patch('main.Scoreboard', MockScoreboard) as mock_scoreboard_class:

        # Mock file operations for high scores loading/saving
        with patch('pathlib.Path.is_file') as mock_is_file, \
             patch('builtins.open') as mock_open, \
             patch('json.load') as mock_json_load, \
             patch('json.dump') as mock_json_dump:

            # Default behavior: No high score file exists initially
            mock_is_file.return_value = False

            # Create the Game instance. __init__ will use the mocks.
            # Calls to pygame.font.SysFont inside __init__ will get unique mocks.
            game = Game()

            # Assign the mocked screen from mock_pygame_init fixture
            game.screen = mock_pygame_init["mock_screen"]

            # Make mocks accessible for assertion if needed
            game._mocks = {
                "Llama": mock_llama_class,
                "Obstacle": mock_obstacle_class,
                "Scoreboard": mock_scoreboard_class,
                "is_file": mock_is_file,
                "open": mock_open,
                "json_load": mock_json_load,
                "json_dump": mock_json_dump,
                "SysFont": mock_pygame_init["mock_sysfont"] # Access to the SysFont mock itself
            }

            yield game


# --- Helper Function ---
def find_blit_call_for_text(mock_screen_blit, text):
    """
    Searches through the calls made to the screen's blit mock
    to find the call where the surface has the specified rendered text.
    """
    if not hasattr(mock_screen_blit, 'call_args_list'): return None
    for blit_call in mock_screen_blit.call_args_list:
        args, _ = blit_call
        if not args: continue
        blit_surf = args[0]
        if hasattr(blit_surf, '_rendered_text') and blit_surf._rendered_text == text:
            return blit_call
    return None


# --- Test Cases ---

def test_draw_high_scores_empty_list(game_instance):
    """Verify drawing when the high score list is empty."""
    game_instance.high_scores = []
    mock_screen = game_instance.screen
    # Get references to the distinct font mocks assigned in __init__
    title_font = game_instance.highscore_title_font
    instruction_font = game_instance.instruction_font
    button_font = game_instance.button_font
    entry_font = game_instance.highscore_entry_font # Although not used here

    # --- Act ---
    game_instance._draw_high_scores_screen()

    # --- Assert ---
    # 1. Screen Fill
    mock_screen.fill.assert_called_once_with(constants.GREY)

    # 2. Title rendering and blitting (using title_font)
    title_font.render.assert_any_call("High Scores", True, constants.BLACK)
    title_blit_call = find_blit_call_for_text(mock_screen.blit, "High Scores")
    assert title_blit_call is not None, "Blit call for 'High Scores' not found"
    _, blit_rect = title_blit_call.args
    assert blit_rect.center == (constants.WINDOW_WIDTH // 2, 50)

    # 3. "No high scores yet!" rendering and blitting (using instruction_font)
    instruction_font.render.assert_any_call("No high scores yet!", True, constants.BLACK)
    no_scores_blit_call = find_blit_call_for_text(mock_screen.blit, "No high scores yet!")
    assert no_scores_blit_call is not None, "Blit call for 'No high scores yet!' not found"
    _, blit_rect = no_scores_blit_call.args
    assert blit_rect.center == (constants.WINDOW_WIDTH // 2, constants.WINDOW_HEIGHT // 2 - 20)

    # 4. Return instruction rendering and blitting (using button_font)
    button_font.render.assert_any_call("Press ESC or Click to Return", True, constants.BLACK)
    return_blit_call = find_blit_call_for_text(mock_screen.blit, "Press ESC or Click to Return")
    assert return_blit_call is not None, "Blit call for 'Press ESC or Click to Return' not found"
    _, blit_rect = return_blit_call.args
    assert blit_rect.center == (constants.WINDOW_WIDTH // 2, constants.WINDOW_HEIGHT - 30)

    # 5. Ensure score entry font was not used for rendering
    entry_font.render.assert_not_called()


def test_draw_high_scores_partial_list(game_instance):
    """Verify drawing with a list containing fewer than 10 scores."""
    # --- Arrange ---
    game_instance.high_scores = [
        {"name": "PlayerA", "score": 100},
        {"name": "PlayerB", "score": 50},
    ]
    start_y = 120; line_height = 35
    mock_screen = game_instance.screen
    title_font = game_instance.highscore_title_font
    entry_font = game_instance.highscore_entry_font
    button_font = game_instance.button_font
    instruction_font = game_instance.instruction_font # Not used here

    # --- Act ---
    game_instance._draw_high_scores_screen()

    # --- Assert ---
    # 1. Screen Fill
    mock_screen.fill.assert_called_once_with(constants.GREY)

    # 2. Title (rendered via title_font)
    title_font.render.assert_any_call("High Scores", True, constants.BLACK)
    assert find_blit_call_for_text(mock_screen.blit, "High Scores") is not None

    # 3. Score Entries (rendered via entry_font)
    entry_font.render.assert_any_call("1. PlayerA - 100", True, constants.BLACK)
    entry_font.render.assert_any_call("2. PlayerB - 50", True, constants.BLACK)
    assert entry_font.render.call_count == 2

    blit_call_1 = find_blit_call_for_text(mock_screen.blit, "1. PlayerA - 100")
    assert blit_call_1 is not None and blit_call_1.args[1].center == (constants.WINDOW_WIDTH // 2, start_y + 0 * line_height)
    blit_call_2 = find_blit_call_for_text(mock_screen.blit, "2. PlayerB - 50")
    assert blit_call_2 is not None and blit_call_2.args[1].center == (constants.WINDOW_WIDTH // 2, start_y + 1 * line_height)

    # 4. Return Instruction (rendered via button_font)
    button_font.render.assert_any_call("Press ESC or Click to Return", True, constants.BLACK)
    assert find_blit_call_for_text(mock_screen.blit, "Press ESC or Click to Return") is not None

    # 5. Ensure "No high scores" font was not used
    instruction_font.render.assert_not_called()
    assert find_blit_call_for_text(mock_screen.blit, "No high scores yet!") is None


def test_draw_high_scores_full_list(game_instance):
    """Verify drawing with a full list of 10 scores."""
    # --- Arrange ---
    game_instance.high_scores = [{"name": f"P{i}", "score": (10 - i) * 10} for i in range(10)]
    start_y = 120; line_height = 35
    mock_screen = game_instance.screen
    title_font = game_instance.highscore_title_font
    entry_font = game_instance.highscore_entry_font
    button_font = game_instance.button_font
    instruction_font = game_instance.instruction_font # Not used here

    # --- Act ---
    game_instance._draw_high_scores_screen()

    # --- Assert ---
    # 1. Screen Fill
    mock_screen.fill.assert_called_once_with(constants.GREY)

    # 2. Title (via title_font)
    title_font.render.assert_any_call("High Scores", True, constants.BLACK)
    assert find_blit_call_for_text(mock_screen.blit, "High Scores") is not None

    # 3. Score Entries (via entry_font)
    for i in range(10):
        entry_text = f"{i + 1}. P{i} - {(10 - i) * 10}"
        entry_font.render.assert_any_call(entry_text, True, constants.BLACK)
        blit_call = find_blit_call_for_text(mock_screen.blit, entry_text)
        assert blit_call is not None, f"Blit for entry {i+1} ('{entry_text}') not found"
        assert blit_call.args[1].center == (constants.WINDOW_WIDTH // 2, start_y + i * line_height)
    assert entry_font.render.call_count == 10

    # 4. Return Instruction (via button_font)
    button_font.render.assert_any_call("Press ESC or Click to Return", True, constants.BLACK)
    assert find_blit_call_for_text(mock_screen.blit, "Press ESC or Click to Return") is not None

    # 5. Ensure "No high scores" font was not used
    instruction_font.render.assert_not_called()
    assert find_blit_call_for_text(mock_screen.blit, "No high scores yet!") is None


def test_draw_high_scores_long_names_scores(game_instance):
    """Verify rendering with long names/scores uses the correct font attribute."""
    # --- Arrange ---
    long_name = "PlayerWithAVeryLongNameIndeed"
    large_score = 9876543210
    game_instance.high_scores = [{"name": long_name, "score": large_score}]
    mock_screen = game_instance.screen
    entry_font = game_instance.highscore_entry_font # Font under test
    entry_text = f"1. {long_name} - {large_score}"

    # --- Act ---
    game_instance._draw_high_scores_screen()

    # --- Assert ---
    # Check render was called via the entry_font attribute with the full string
    entry_font.render.assert_any_call(entry_text, True, constants.BLACK)
    assert find_blit_call_for_text(mock_screen.blit, entry_text) is not None


def test_draw_high_scores_malformed_entry(game_instance):
    """Verify drawing handles missing keys using defaults via the correct font."""
    # --- Arrange ---
    game_instance.high_scores = [
        {"name": "Good", "score": 100}, {"score": 50}, {"name": "AlsoGood"}, {}
    ]
    mock_screen = game_instance.screen
    entry_font = game_instance.highscore_entry_font # Font under test
    start_y = 120; line_height = 35

    entry_1_text = "1. Good - 100"
    entry_2_text = "2. N/A - 50"
    entry_3_text = "3. AlsoGood - 0"
    entry_4_text = "4. N/A - 0"

    # --- Act ---
    game_instance._draw_high_scores_screen()

    # --- Assert ---
    # Check rendering via entry_font and blitting for each entry
    entry_font.render.assert_any_call(entry_1_text, True, constants.BLACK)
    blit_1 = find_blit_call_for_text(mock_screen.blit, entry_1_text)
    assert blit_1 and blit_1.args[1].center == (constants.WINDOW_WIDTH // 2, start_y + 0 * line_height)

    entry_font.render.assert_any_call(entry_2_text, True, constants.BLACK)
    blit_2 = find_blit_call_for_text(mock_screen.blit, entry_2_text)
    assert blit_2 and blit_2.args[1].center == (constants.WINDOW_WIDTH // 2, start_y + 1 * line_height)

    entry_font.render.assert_any_call(entry_3_text, True, constants.BLACK)
    blit_3 = find_blit_call_for_text(mock_screen.blit, entry_3_text)
    assert blit_3 and blit_3.args[1].center == (constants.WINDOW_WIDTH // 2, start_y + 2 * line_height)

    entry_font.render.assert_any_call(entry_4_text, True, constants.BLACK)
    blit_4 = find_blit_call_for_text(mock_screen.blit, entry_4_text)
    assert blit_4 and blit_4.args[1].center == (constants.WINDOW_WIDTH // 2, start_y + 3 * line_height)

    assert entry_font.render.call_count == 4 # Ensure only entry font rendered these


def test_draw_high_scores_verify_specific_fonts_and_color_usage(game_instance):
    """
    Verify that the correct font *attributes* on the game instance are used
    for rendering different parts of the screen, all with the correct color.
    """
    # --- Arrange ---
    game_instance.high_scores = [{"name": "Test", "score": 10}] # Non-empty list
    mock_screen = game_instance.screen

    # Store references to the distinct font mock objects assigned during __init__
    title_font_mock = game_instance.highscore_title_font
    entry_font_mock = game_instance.highscore_entry_font
    button_font_mock = game_instance.button_font
    instruction_font_mock = game_instance.instruction_font

    # --- Act (Non-Empty List) ---
    game_instance._draw_high_scores_screen()

    # --- Assert (Non-Empty List) ---
    # Check render was called on the correct mock object with correct color
    title_font_mock.render.assert_any_call("High Scores", True, constants.BLACK)
    entry_font_mock.render.assert_any_call("1. Test - 10", True, constants.BLACK)
    button_font_mock.render.assert_any_call("Press ESC or Click to Return", True, constants.BLACK)
    # Ensure the instruction font mock (for empty message) was NOT called
    instruction_font_mock.render.assert_not_called() # THIS SHOULD NOW PASS

    # --- Arrange (Empty List) ---
    # Reset mocks for the second part of the test
    title_font_mock.render.reset_mock()
    entry_font_mock.render.reset_mock()
    button_font_mock.render.reset_mock()
    instruction_font_mock.render.reset_mock()
    mock_screen.reset_mock() # Reset screen calls like fill/blit

    game_instance.high_scores = [] # Empty list

    # --- Act (Empty List) ---
    game_instance._draw_high_scores_screen()

    # --- Assert (Empty List) ---
    title_font_mock.render.assert_any_call("High Scores", True, constants.BLACK)
    instruction_font_mock.render.assert_any_call("No high scores yet!", True, constants.BLACK)
    button_font_mock.render.assert_any_call("Press ESC or Click to Return", True, constants.BLACK)
    # Ensure the entry font mock was NOT called
    entry_font_mock.render.assert_not_called() # THIS SHOULD NOW PASS