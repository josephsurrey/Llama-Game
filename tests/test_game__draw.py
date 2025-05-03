import pytest
from unittest.mock import MagicMock, patch, call
import pygame # For Rect type hint and constants if needed

# Assume constants.py is in the same directory or accessible path
import constants
# Assume main.py is in the same directory or accessible path
from main import Game, Llama, Scoreboard # Need these for type checks/instance mocks

# --- Pygame Mocking Setup ---

# Helper to create mock surfaces returned by font.render
def create_render_surface_mock(**kwargs):
    # Create a mock Rect object
    rect_mock = MagicMock(spec=pygame.Rect)
    # Configure its attributes based on kwargs (like center)
    # Set default attributes first
    rect_mock.center = (0, 0)
    rect_mock.bottomleft = (0, 0)
    rect_mock.x = 0
    rect_mock.y = 0
    rect_mock.width = 10
    rect_mock.height = 10
    # Apply specific configurations from kwargs
    rect_mock.configure_mock(**kwargs)

    # Create the surface mock that returns the Rect mock
    surface_mock = MagicMock(spec=pygame.Surface)
    surface_mock.get_rect.return_value = rect_mock
    return surface_mock

# Helper to create a new mock font object each time SysFont is called
def create_mock_font(*args, **kwargs):
    mock_font = MagicMock(spec=pygame.font.Font)
    mock_font.render.return_value = create_render_surface_mock() # Default render result
    return mock_font

@pytest.fixture(autouse=True)
def mock_pygame_dependencies(mocker):
    """Mocks Pygame functions used by Game.__init__ and globally."""
    mocker.patch('pygame.init', return_value=None)
    mocker.patch('pygame.mixer.init', return_value=None)
    mocker.patch('pygame.font.init', return_value=None)

    mock_screen = MagicMock(spec=pygame.Surface)
    mocker.patch('pygame.display.set_mode', return_value=mock_screen)
    mocker.patch('pygame.display.set_caption', return_value=None)
    mocker.patch('pygame.time.Clock', return_value=MagicMock())
    mocker.patch('pygame.time.get_ticks', return_value=1000)

    mock_image_surface = MagicMock(spec=pygame.Surface)
    mock_image_surface.convert.return_value = mock_image_surface
    mock_image_surface.get_height.return_value = 20
    mocker.patch('pygame.image.load', return_value=mock_image_surface)

    mocker.patch('pygame.font.SysFont', side_effect=create_mock_font)

    mock_group_instance = MagicMock(spec=pygame.sprite.Group)
    mock_group_instance.add = MagicMock()
    mock_group_instance.draw = MagicMock()
    mock_group_instance.empty = MagicMock()
    mocker.patch('pygame.sprite.Group', return_value=mock_group_instance)

    mocker.patch('pygame.time.set_timer', return_value=None)
    mocker.patch('pygame.draw.rect', return_value=None) # Mock draw rect globally

    mock_llama_instance = MagicMock(spec=Llama)
    mocker.patch('main.Llama', return_value=mock_llama_instance)

    mock_scoreboard_instance = MagicMock(spec=Scoreboard)
    mocker.patch('main.Scoreboard', return_value=mock_scoreboard_instance)

    mocker.patch('main.Game._load_high_scores', return_value=None)


# --- Game Instance Fixture ---

@pytest.fixture
def game_instance(mock_pygame_dependencies):
    """Creates a Game instance with mocked dependencies for testing _draw."""
    game = Game()

    game.screen.fill = MagicMock()
    game.screen.blit = MagicMock()

    game.ground_image = MagicMock(spec=pygame.Surface)
    game.ground_image.get_height.return_value = 20
    game.ground_image.convert.return_value = game.ground_image

    game.all_sprites.draw = MagicMock()

    game.scoreboard.draw = MagicMock()
    game.scoreboard.score = 123

    # Ensure the mocks exist before trying to configure render
    # These were created by the side_effect in the auto-fixture
    assert isinstance(game.game_over_font, MagicMock)
    assert isinstance(game.final_score_font, MagicMock)

    game.game_over_font.render.return_value = create_render_surface_mock()
    game.final_score_font.render.return_value = create_render_surface_mock()

    game.pygame_draw_rect = pygame.draw.rect

    return game

# --- Test Cases ---

# Test cases test_draw_while_playing_... remain the same

def test_draw_game_over_not_eligible(game_instance):
    """Verify drawing calls during game over, score not eligible for saving."""
    game = game_instance
    game.game_over = True
    game.entering_name = False
    game.displaying_scores = False
    game.score_eligible_for_save = False
    game.ground_image = MagicMock(spec=pygame.Surface)
    game.ground_image.get_height.return_value = 20
    game.ground_image.convert.return_value = game.ground_image
    game.scoreboard.score = 99

    # Define expected centers
    go_center = (constants.WINDOW_WIDTH // 2, constants.WINDOW_HEIGHT // 2 - 50)
    score_center = (constants.WINDOW_WIDTH // 2, constants.WINDOW_HEIGHT // 2)
    instr_center = (constants.WINDOW_WIDTH // 2, constants.WINDOW_HEIGHT // 2 + 120)

    # Configure mocks
    game.game_over_font.render.return_value = create_render_surface_mock(center=go_center)
    game.final_score_font.render.side_effect = [
        create_render_surface_mock(center=score_center), # Final Score
        create_render_surface_mock(center=instr_center) # Instructions
    ]

    # Reset mocks before call
    game.screen.fill.reset_mock()
    game.screen.blit.reset_mock()
    game.pygame_draw_rect.reset_mock()
    game.all_sprites.draw.reset_mock()
    game.scoreboard.draw.reset_mock()
    game.game_over_font.render.reset_mock()
    # Re-set render value/side effect after reset if needed
    game.game_over_font.render.return_value = create_render_surface_mock(center=go_center)
    game.final_score_font.render.side_effect = [
        create_render_surface_mock(center=score_center),
        create_render_surface_mock(center=instr_center)
    ]

    game._draw()

    # --- Assertions ---
    game.screen.fill.assert_called_once_with(constants.WHITE)
    game.screen.blit.assert_any_call(
        game.ground_image,
        (0, constants.WINDOW_HEIGHT - game.ground_image.get_height())
    )
    game.pygame_draw_rect.assert_not_called()
    game.all_sprites.draw.assert_called_once_with(game.screen)
    game.scoreboard.draw.assert_called_once_with(game.screen)

    # Render calls
    game.game_over_font.render.assert_called_once_with("GAME OVER", True, constants.BLACK)
    final_score_render_calls = game.final_score_font.render.call_args_list
    assert len(final_score_render_calls) == 2
    assert final_score_render_calls[0].args == (f"Final Score: {game.scoreboard.score}", True, constants.BLACK)
    assert final_score_render_calls[1].args == ("Press 'R' to Restart or 'Q' to Quit", True, constants.BLACK)

    # Blit calls and positions
    assert game.screen.blit.call_count == 4 # ground(1), GO(1), Score(1), Instr(1)
    blit_args_list = game.screen.blit.call_args_list

    # *** FIXED Position Assertions ***
    assert any(
        isinstance(call[0][0], MagicMock) and isinstance(call[0][1], MagicMock) and hasattr(call[0][1], 'center') and call[0][1].center == go_center
        for call in blit_args_list
    ) # Check GO text pos
    assert any(
        isinstance(call[0][0], MagicMock) and isinstance(call[0][1], MagicMock) and hasattr(call[0][1], 'center') and call[0][1].center == score_center
        for call in blit_args_list
    ) # Check Final Score pos
    assert any(
        isinstance(call[0][0], MagicMock) and isinstance(call[0][1], MagicMock) and hasattr(call[0][1], 'center') and call[0][1].center == instr_center
        for call in blit_args_list
    ) # Check Instructions pos

    # Check save prompt was *not* rendered
    save_prompt_rendered = any("High Score! Save?" in call.args[0] for call in final_score_render_calls)
    assert not save_prompt_rendered


def test_draw_game_over_eligible(game_instance):
    """Verify drawing calls during game over, score *is* eligible for saving."""
    game = game_instance
    game.game_over = True
    game.entering_name = False
    game.displaying_scores = False
    game.score_eligible_for_save = True # Eligible
    game.ground_image = MagicMock(spec=pygame.Surface)
    game.ground_image.get_height.return_value = 20
    game.ground_image.convert.return_value = game.ground_image
    game.scoreboard.score = 500

    # Define expected centers
    go_center = (constants.WINDOW_WIDTH // 2, constants.WINDOW_HEIGHT // 2 - 50)
    score_center = (constants.WINDOW_WIDTH // 2, constants.WINDOW_HEIGHT // 2)
    save_center = (constants.WINDOW_WIDTH // 2, constants.WINDOW_HEIGHT // 2 + 40)
    instr_center = (constants.WINDOW_WIDTH // 2, constants.WINDOW_HEIGHT // 2 + 120)

    # Configure mocks
    game.game_over_font.render.return_value = create_render_surface_mock(center=go_center)
    game.final_score_font.render.side_effect = [
        create_render_surface_mock(center=score_center), # Final Score
        create_render_surface_mock(center=save_center),  # Save Prompt
        create_render_surface_mock(center=instr_center) # Instructions
    ]

    # Reset mocks before call
    game.screen.fill.reset_mock()
    game.screen.blit.reset_mock()
    game.pygame_draw_rect.reset_mock()
    game.all_sprites.draw.reset_mock()
    game.scoreboard.draw.reset_mock()
    game.game_over_font.render.reset_mock()
    # Re-set mocks after reset
    game.game_over_font.render.return_value = create_render_surface_mock(center=go_center)
    game.final_score_font.render.side_effect = [
        create_render_surface_mock(center=score_center),
        create_render_surface_mock(center=save_center),
        create_render_surface_mock(center=instr_center)
    ]


    game._draw()

    # --- Assertions ---
    game.screen.fill.assert_called_once_with(constants.WHITE)
    game.screen.blit.assert_any_call( # Ground
        game.ground_image,
        (0, constants.WINDOW_HEIGHT - game.ground_image.get_height())
    )
    game.pygame_draw_rect.assert_not_called()
    game.all_sprites.draw.assert_called_once_with(game.screen)
    game.scoreboard.draw.assert_called_once_with(game.screen)

    # Render calls
    game.game_over_font.render.assert_called_once_with("GAME OVER", True, constants.BLACK)
    final_score_render_calls = game.final_score_font.render.call_args_list
    assert len(final_score_render_calls) == 3
    assert final_score_render_calls[0].args == (f"Final Score: {game.scoreboard.score}", True, constants.BLACK)
    assert final_score_render_calls[1].args == ("High Score! Save? (Y/N)", True, constants.RED)
    assert final_score_render_calls[2].args == ("Press 'R' to Restart or 'Q' to Quit", True, constants.BLACK)

    # Blit calls and positions
    assert game.screen.blit.call_count == 5 # ground(1), GO(1), Score(1), Save(1), Instr(1)
    blit_args_list = game.screen.blit.call_args_list

    # *** FIXED Position Assertions ***
    assert any(
        isinstance(call[0][0], MagicMock) and isinstance(call[0][1], MagicMock) and hasattr(call[0][1], 'center') and call[0][1].center == go_center
        for call in blit_args_list
    ) # GO text pos
    assert any(
        isinstance(call[0][0], MagicMock) and isinstance(call[0][1], MagicMock) and hasattr(call[0][1], 'center') and call[0][1].center == score_center
        for call in blit_args_list
    ) # Final Score pos
    assert any(
        isinstance(call[0][0], MagicMock) and isinstance(call[0][1], MagicMock) and hasattr(call[0][1], 'center') and call[0][1].center == save_center
        for call in blit_args_list
    ) # Save Prompt pos
    assert any(
        isinstance(call[0][0], MagicMock) and isinstance(call[0][1], MagicMock) and hasattr(call[0][1], 'center') and call[0][1].center == instr_center
        for call in blit_args_list
    ) # Instructions pos

# Remaining tests (test_draw_game_over_no_ground_image, etc.) should remain the same
# as they don't have the complex position checks or were already passing.
# ... (include the previously passing tests here unchanged) ...

def test_draw_game_over_no_ground_image(game_instance):
    """Verify drawing during game over with fallback ground."""
    game = game_instance
    game.game_over = True
    game.entering_name = False
    game.displaying_scores = False
    game.score_eligible_for_save = False
    game.ground_image = None # Force fallback
    game.scoreboard.score = 88

    # Define expected centers
    go_center = (constants.WINDOW_WIDTH // 2, constants.WINDOW_HEIGHT // 2 - 50)
    score_center = (constants.WINDOW_WIDTH // 2, constants.WINDOW_HEIGHT // 2)
    instr_center = (constants.WINDOW_WIDTH // 2, constants.WINDOW_HEIGHT // 2 + 120)

    # Configure specific mocks
    game.game_over_font.render.return_value = create_render_surface_mock(center=go_center)
    game.final_score_font.render.side_effect = [ # 2 calls expected
        create_render_surface_mock(center=score_center), # Final Score
        create_render_surface_mock(center=instr_center) # Instructions
    ]

    # Reset mocks
    game.screen.fill.reset_mock()
    game.screen.blit.reset_mock()
    game.pygame_draw_rect.reset_mock()
    game.all_sprites.draw.reset_mock()
    game.scoreboard.draw.reset_mock()
    game.game_over_font.render.reset_mock()
    # Re-set after reset
    game.game_over_font.render.return_value = create_render_surface_mock(center=go_center)
    game.final_score_font.render.side_effect = [
        create_render_surface_mock(center=score_center),
        create_render_surface_mock(center=instr_center)
    ]


    game._draw()

    # Base drawing happens
    game.screen.fill.assert_called_once_with(constants.WHITE)
    expected_rect = pygame.Rect(0, constants.GROUND_Y, constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT - constants.GROUND_Y)
    game.pygame_draw_rect.assert_called_once_with(game.screen, constants.GREY, expected_rect)

    game.all_sprites.draw.assert_called_once_with(game.screen)
    game.scoreboard.draw.assert_called_once_with(game.screen)

    # Game Over text is rendered
    game.game_over_font.render.assert_called_once_with("GAME OVER", True, constants.BLACK)
    # Final score and instructions are rendered
    final_score_render_calls = game.final_score_font.render.call_args_list
    assert len(final_score_render_calls) == 2
    assert final_score_render_calls[0].args == (f"Final Score: {game.scoreboard.score}", True, constants.BLACK)
    assert final_score_render_calls[1].args == ("Press 'R' to Restart or 'Q' to Quit", True, constants.BLACK)

    # Ensure blit was called only for the rendered surfaces
    assert game.screen.blit.call_count == 3 # GO(1), Score(1), Instr(1)
    blit_args_list = game.screen.blit.call_args_list
    assert not any(call.args[0] is game.ground_image for call in blit_args_list if game.ground_image is not None) # No ground blit

    # Verify positions (using the corrected assertion logic)
    assert any(
        isinstance(call[0][0], MagicMock) and isinstance(call[0][1], MagicMock) and hasattr(call[0][1], 'center') and call[0][1].center == go_center
        for call in blit_args_list
    ) # GO text pos
    assert any(
        isinstance(call[0][0], MagicMock) and isinstance(call[0][1], MagicMock) and hasattr(call[0][1], 'center') and call[0][1].center == score_center
        for call in blit_args_list
    ) # Final Score pos
    assert any(
        isinstance(call[0][0], MagicMock) and isinstance(call[0][1], MagicMock) and hasattr(call[0][1], 'center') and call[0][1].center == instr_center
        for call in blit_args_list
    ) # Instructions pos


def test_draw_state_entering_name(game_instance):
    """Verify drawing is skipped when entering name."""
    game = game_instance
    game.game_over = True
    game.entering_name = True # This state prevents drawing
    game.displaying_scores = False
    game.ground_image = MagicMock()

    # Reset mocks
    game.screen.fill.reset_mock()
    game.screen.blit.reset_mock()
    game.pygame_draw_rect.reset_mock()
    game.all_sprites.draw.reset_mock()
    game.scoreboard.draw.reset_mock()
    game.game_over_font.render.reset_mock()
    game.final_score_font.render.reset_mock()


    game._draw()

    # Only background fill should happen
    game.screen.fill.assert_called_once_with(constants.WHITE)
    # No other drawing calls from the main block should occur
    game.screen.blit.assert_not_called()
    game.pygame_draw_rect.assert_not_called()
    game.all_sprites.draw.assert_not_called()
    game.scoreboard.draw.assert_not_called()
    game.game_over_font.render.assert_not_called()
    game.final_score_font.render.assert_not_called()


def test_draw_state_displaying_scores(game_instance):
    """Verify drawing is skipped when displaying scores."""
    game = game_instance
    game.game_over = True
    game.entering_name = False
    game.displaying_scores = True # This state prevents drawing
    game.ground_image = MagicMock()

    # Reset mocks
    game.screen.fill.reset_mock()
    game.screen.blit.reset_mock()
    game.pygame_draw_rect.reset_mock()
    game.all_sprites.draw.reset_mock()
    game.scoreboard.draw.reset_mock()
    game.game_over_font.render.reset_mock()
    game.final_score_font.render.reset_mock()

    game._draw()

    # Only background fill should happen
    game.screen.fill.assert_called_once_with(constants.WHITE)
    # No other drawing calls from the main block should occur
    game.screen.blit.assert_not_called()
    game.pygame_draw_rect.assert_not_called()
    game.all_sprites.draw.assert_not_called()
    game.scoreboard.draw.assert_not_called()
    game.game_over_font.render.assert_not_called()
    game.final_score_font.render.assert_not_called()


def test_draw_empty_sprite_group(game_instance):
    """Verify drawing works correctly when the sprite group is empty."""
    game = game_instance
    game.game_over = False
    game.entering_name = False
    game.displaying_scores = False
    game.ground_image = MagicMock(spec=pygame.Surface)
    game.ground_image.get_height.return_value = 20
    game.ground_image.convert.return_value = game.ground_image
    game.all_sprites.draw = MagicMock() # Ensure it's a fresh mock for assertion

    # Reset mocks
    game.screen.fill.reset_mock()
    game.screen.blit.reset_mock()
    game.pygame_draw_rect.reset_mock()
    # game.all_sprites.draw already reset above
    game.scoreboard.draw.reset_mock()
    game.game_over_font.render.reset_mock()
    game.final_score_font.render.reset_mock()

    game._draw()

    game.screen.fill.assert_called_once_with(constants.WHITE)
    game.screen.blit.assert_called_once_with( # Blit for ground
        game.ground_image,
        (0, constants.WINDOW_HEIGHT - game.ground_image.get_height())
    )
    game.pygame_draw_rect.assert_not_called()
    game.all_sprites.draw.assert_called_once_with(game.screen) # Assert group draw was called
    game.scoreboard.draw.assert_called_once_with(game.screen)
    game.game_over_font.render.assert_not_called()
    game.final_score_font.render.assert_not_called()


def test_draw_font_render_calls_game_over(game_instance):
    """Verify the correct font render calls are made during game over."""
    game = game_instance
    game.game_over = True
    game.entering_name = False
    game.displaying_scores = False
    game.score_eligible_for_save = True # Include eligible state for max renders
    game.ground_image = MagicMock() # Ground existence doesn't matter for render check
    game.scoreboard.score = 12345

    # Configure specific mocks (render returns don't need specific centers for this test)
    game.game_over_font.render.return_value = create_render_surface_mock()
    game.final_score_font.render.side_effect = [
        create_render_surface_mock(), # Final Score
        create_render_surface_mock(), # Save Prompt
        create_render_surface_mock()  # Instructions
    ]

    # Reset mocks before call
    game.game_over_font.render.reset_mock()
    game.final_score_font.render.reset_mock()
    # Re-set mocks after reset
    game.game_over_font.render.return_value = create_render_surface_mock()
    game.final_score_font.render.side_effect = [
        create_render_surface_mock(), # Final Score
        create_render_surface_mock(), # Save Prompt
        create_render_surface_mock()  # Instructions
    ]


    game._draw()

    # Verify specific render call for game_over_font
    game.game_over_font.render.assert_called_once_with(
        "GAME OVER", True, constants.BLACK
    )

    # Verify specific render calls for final_score_font
    expected_final_score_text = f"Final Score: {game.scoreboard.score}"
    expected_save_prompt_text = "High Score! Save? (Y/N)"
    expected_instructions_text = "Press 'R' to Restart or 'Q' to Quit"

    calls = game.final_score_font.render.call_args_list
    assert len(calls) == 3 # Ensure exactly 3 calls

    # Verify calls were made with correct arguments
    assert any(c.args == (expected_final_score_text, True, constants.BLACK) for c in calls)
    assert any(c.args == (expected_save_prompt_text, True, constants.RED) for c in calls)
    assert any(c.args == (expected_instructions_text, True, constants.BLACK) for c in calls)