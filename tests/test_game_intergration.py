# test_game_integration.py
import sys
import pytest
import pygame
from unittest.mock import patch, MagicMock, call, ANY

# Ensure constants are loaded relatively if tests are run from a specific directory
try:
    import constants
    from main import Game, Llama, Obstacle, Scoreboard
except ImportError:
    # If running tests from a different structure, adjust path
    # This might be needed depending on your test execution context
    # import os
    # sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    import constants
    from main import Game, Llama, Obstacle, Scoreboard


# --- Pygame Mocking Setup ---

# Mock fundamental pygame modules/functions needed before Game init
@pytest.fixture(autouse=True)
def mock_pygame_essentials():
    """Automatically mock essential pygame functions for all tests."""
    # Import the real Group class *before* patching it
    RealGroup = pygame.sprite.Group

    with patch('pygame.init', return_value=None) as mock_init, \
         patch('pygame.mixer.init', return_value=None) as mock_mixer_init, \
         patch('pygame.font.init', return_value=None) as mock_font_init, \
         patch('pygame.display.set_mode', return_value=MagicMock()) as mock_set_mode, \
         patch('pygame.display.set_caption', return_value=None) as mock_set_caption, \
         patch('pygame.time.Clock', return_value=MagicMock()) as mock_clock, \
         patch('pygame.time.get_ticks', return_value=0) as mock_get_ticks, \
         patch('pygame.time.set_timer') as mock_set_timer, \
         patch('pygame.image.load') as mock_image_load, \
         patch('pygame.font.SysFont') as mock_sysfont, \
         patch('pygame.event.get', return_value=[]) as mock_event_get, \
         patch('pygame.quit', return_value=None) as mock_pygame_quit, \
         patch('sys.exit', side_effect=SystemExit("Simulated sys.exit")) as mock_sys_exit, \
         patch('pygame.sprite.spritecollide', return_value=[]) as mock_spritecollide, \
         patch('pygame.sprite.Group') as mock_group, \
         patch('pygame.draw.rect') as mock_draw_rect, \
         patch('pygame.display.flip') as mock_display_flip, \
         patch('pygame.transform.scale') as mock_transform_scale: # ***** ADDED MOCK HERE *****

        # Configure image loading mock
        mock_surface = MagicMock(spec=pygame.Surface)
        mock_surface.get_rect.return_value = MagicMock(spec=pygame.Rect, width=50, height=50, bottom=constants.GROUND_Y)
        mock_surface.convert_alpha.return_value = mock_surface # convert_alpha returns the same mock
        mock_surface.get_width.return_value = 100 # Example width for ground scaling
        mock_surface.get_height.return_value = 100 # Example height for ground scaling
        mock_image_load.return_value = mock_surface

        # ***** CONFIGURE MOCK FOR TRANSFORM.SCALE *****
        # Let transform.scale return a mock surface (can be the same one or a different configured one)
        mock_transform_scale.return_value = mock_surface

        # Configure font mock
        mock_font = MagicMock(spec=pygame.font.Font)
        mock_font.render.return_value = MagicMock(spec=pygame.Surface, get_rect=MagicMock(return_value=MagicMock(spec=pygame.Rect)))
        mock_sysfont.return_value = mock_font

        # Configure sprite group mock
        mock_group_instance = MagicMock()
        _mock_sprites_list = []
        mock_group_instance.add = MagicMock(side_effect=lambda sprite: _mock_sprites_list.append(sprite))
        mock_group_instance.empty = MagicMock(side_effect=lambda: _mock_sprites_list.clear())
        mock_group_instance.update = MagicMock()
        mock_group_instance.draw = MagicMock()
        mock_group_instance.sprites = MagicMock(side_effect=lambda: list(_mock_sprites_list))
        mock_group_instance.__len__ = MagicMock(side_effect=lambda: len(_mock_sprites_list))
        mock_group.side_effect = lambda *args: mock_group_instance


        yield {
            "init": mock_init, "mixer_init": mock_mixer_init, "font_init": mock_font_init,
            "set_mode": mock_set_mode, "set_caption": mock_set_caption, "clock": mock_clock,
            "get_ticks": mock_get_ticks, "set_timer": mock_set_timer, "image_load": mock_image_load,
            "sysfont": mock_sysfont, "event_get": mock_event_get, "pygame_quit": mock_pygame_quit,
            "sys_exit": mock_sys_exit, "spritecollide": mock_spritecollide, "group": mock_group,
            "draw_rect": mock_draw_rect, "display_flip": mock_display_flip,
            "mock_surface": mock_surface, "mock_font": mock_font, "mock_group_instance": mock_group_instance,
            "transform_scale": mock_transform_scale # ***** ADDED TO YIELD *****
        }


# --- Mock Game Components ---
# (No changes needed in mock_game_components fixture)
@pytest.fixture
def mock_game_components():
    """Mocks Llama, Obstacle, and Scoreboard classes."""
    with patch('main.Llama', autospec=True) as MockLlama, \
         patch('main.Obstacle', autospec=True) as MockObstacle, \
         patch('main.Scoreboard', autospec=True) as MockScoreboard:

        # Configure mock instances that will be created by Game.__init__
        mock_llama_instance = MockLlama.return_value
        mock_llama_instance.rect = MagicMock(spec=pygame.Rect, width=40, height=60)
        mock_llama_instance.initial_pos = (constants.PLAYER_HORIZONTAL_POSITION, constants.GROUND_Y - 60)
        mock_llama_instance.reset = MagicMock()
        mock_llama_instance.update = MagicMock()
        mock_llama_instance.jump = MagicMock()
        mock_llama_instance.mask = MagicMock() # Needed for spritecollide

        mock_scoreboard_instance = MockScoreboard.return_value
        mock_scoreboard_instance.score = 0
        mock_scoreboard_instance.update = MagicMock()
        mock_scoreboard_instance.draw = MagicMock()
        mock_scoreboard_instance.reset = MagicMock()


        # Make MockObstacle return a mock obstacle instance when called
        mock_obstacle_instance = MagicMock(spec=Obstacle) # Spec with the real class is fine here
        mock_obstacle_instance.rect = MagicMock(spec=pygame.Rect)
        mock_obstacle_instance.mask = MagicMock() # Needed for spritecollide
        mock_obstacle_instance.update = MagicMock()
        mock_obstacle_instance.kill = MagicMock()
        MockObstacle.return_value = mock_obstacle_instance

        yield {
            "Llama": MockLlama, "Obstacle": MockObstacle, "Scoreboard": MockScoreboard,
            "llama_instance": mock_llama_instance,
            "scoreboard_instance": mock_scoreboard_instance,
            "obstacle_instance": mock_obstacle_instance
        }


# --- Test Class ---

class TestGameIntegration:

    def test_game_initialization(self, mock_pygame_essentials, mock_game_components):
        """Test Case: Game Initialization"""
        game = Game() # This triggers __init__

        # --- Assertions ---
        # (Previous assertions for init, mixer, font, display, clock, state...)
        mock_pygame_essentials["init"].assert_called_once()
        mock_pygame_essentials["mixer_init"].assert_called_once()
        mock_pygame_essentials["font_init"].assert_called_once()
        mock_pygame_essentials["set_mode"].assert_called_once_with((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
        mock_pygame_essentials["set_caption"].assert_called_once_with(constants.WINDOW_TITLE)
        mock_pygame_essentials["clock"].assert_called_once()
        assert game.running is True
        assert game.game_over is False
        assert game.screen is mock_pygame_essentials["set_mode"].return_value
        assert game.clock is mock_pygame_essentials["clock"].return_value
        assert game.start_time == 0

        # Component instantiation
        mock_game_components["Llama"].assert_called_once()
        mock_game_components["Scoreboard"].assert_called_once()
        assert game.llama is mock_game_components["llama_instance"]
        assert game.scoreboard is mock_game_components["scoreboard_instance"]
        mock_game_components["llama_instance"].reset.assert_called_once()

        # Sprite groups
        assert mock_pygame_essentials["group"].call_count == 2
        mock_pygame_essentials["mock_group_instance"].add.assert_called_once_with(mock_game_components["llama_instance"])
        assert game.all_sprites is mock_pygame_essentials["mock_group_instance"]
        assert game.obstacles is mock_pygame_essentials["mock_group_instance"]

        # Image loading and scaling
        mock_pygame_essentials["image_load"].assert_any_call(constants.GROUND_IMAGE)
        # Check that transform.scale was called (arguments depend on image mock size)
        expected_target_height = constants.WINDOW_HEIGHT
        expected_target_width = int(float(100) / float(100) * expected_target_height) # Based on mock W/H
        mock_pygame_essentials["transform_scale"].assert_called_once_with(
            mock_pygame_essentials["mock_surface"], # The result of convert_alpha
            (expected_target_width, expected_target_height)
        )
        # Check the result of scale was assigned
        assert game.scaled_ground_image is mock_pygame_essentials["mock_surface"] # Since scale mock returns it

        # Timer setup
        mock_pygame_essentials["set_timer"].assert_called_once_with(
            constants.OBSTACLE_SPAWN_EVENT, constants.OBSTACLE_CREATION_INTERVAL
        )

        # Font setup
        mock_pygame_essentials["sysfont"].assert_any_call(None, 36)
        assert game.score_font is mock_pygame_essentials["mock_font"]


    # --- Other Test Methods (no changes needed below this line) ---

    def test_basic_gameplay_tick_no_collision(self, mock_pygame_essentials, mock_game_components):
        """Test Case: Basic Gameplay Loop (Tick)"""
        game = Game()
        game.game_over = False # Ensure playing state
        mock_pygame_essentials["get_ticks"].return_value = 1000 # Simulate time passing

        game._update()

        # Check updates are called
        mock_pygame_essentials["mock_group_instance"].update.assert_called_once() # all_sprites.update()
        mock_game_components["scoreboard_instance"].update.assert_called_once_with(1000, game.start_time)

        # Check collision check is performed
        mock_pygame_essentials["spritecollide"].assert_called_once_with(
            game.llama, game.obstacles, False, pygame.sprite.collide_mask
        )
        assert game.game_over is False # No collision simulated


    def test_player_jump_event(self, mock_pygame_essentials, mock_game_components):
        """Test Case: Player Jump Event"""
        game = Game()
        game.game_over = False
        jump_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
        mock_pygame_essentials["event_get"].return_value = [jump_event]

        game._handle_events()

        mock_game_components["llama_instance"].jump.assert_called_once()
        assert game.running is True # Game shouldn't stop


    def test_obstacle_spawn_event(self, mock_pygame_essentials, mock_game_components):
        """Test Case: Obstacle Spawn Event"""
        game = Game()
        game.game_over = False
        spawn_event = pygame.event.Event(constants.OBSTACLE_SPAWN_EVENT)
        mock_pygame_essentials["event_get"].return_value = [spawn_event]

        # Get the mock group instance used by the game
        mock_group = game.all_sprites # or game.obstacles, they point to the same mock

        game._handle_events() # This calls _spawn_obstacle which adds to groups

        # Check Obstacle was created
        mock_game_components["Obstacle"].assert_called_once_with(constants.OBSTACLE_INITIAL_SPEED)
        new_obstacle = mock_game_components["Obstacle"].return_value

        # Check add was called with the new obstacle instance on the mock group
        # It should be called twice because _spawn_obstacle adds to both all_sprites and obstacles
        mock_group.add.assert_has_calls([
            call(new_obstacle), # Added to all_sprites
            call(new_obstacle)  # Added to obstacles
        ])


    def test_collision_detection_game_over(self, mock_pygame_essentials, mock_game_components):
        """Test Case: Collision Detection"""
        game = Game()
        game.game_over = False
        # Simulate an obstacle exists (it needs to be "in" the obstacles group for collide)
        mock_obstacle = mock_game_components["obstacle_instance"]
        game.obstacles.add(mock_obstacle) # Add to the mock group instance

        # Configure spritecollide to return the obstacle
        mock_pygame_essentials["spritecollide"].return_value = [mock_obstacle]

        # Need to call _update which calls _check_collisions internally
        game._update()

        assert game.game_over is True
        # Check timer was stopped
        # It might have been called multiple times (init, reset), check the *last* call
        mock_pygame_essentials["set_timer"].assert_called_with(constants.OBSTACLE_SPAWN_EVENT, 0)


    def test_restart_event(self, mock_pygame_essentials, mock_game_components):
        """Test Case: Restart Event"""
        game = Game()
        game.game_over = True # Set game over state
        game.scoreboard.score = 100 # Give some score

        # Get the mock group instance
        mock_group = game.all_sprites

        # Manually add a mock obstacle to check clearing
        mock_obstacle = mock_game_components["obstacle_instance"]
        game.obstacles.add(mock_obstacle)
        game.all_sprites.add(mock_obstacle) # Adds to the same list in our mock setup

        restart_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r)
        mock_pygame_essentials["event_get"].return_value = [restart_event]
        mock_pygame_essentials["get_ticks"].return_value = 5000 # Simulate time for new start_time

        # ***** ADD THIS LINE: Reset mock history before the action *****
        mock_game_components["llama_instance"].reset.reset_mock()
        mock_game_components["scoreboard_instance"].reset.reset_mock() # Also reset scoreboard mock if needed

        game._handle_events() # This should trigger _reset_game via the event

        # Check state reset
        assert game.game_over is False
        assert game.start_time == 5000

        # Check components reset (Now assert_called_once should pass)
        mock_game_components["scoreboard_instance"].reset.assert_called_once()
        mock_game_components["llama_instance"].reset.assert_called_once() # Will check only calls after reset_mock()

        # Check groups cleared and llama re-added
        # empty() should have been called twice (once for obstacles, once for all_sprites)
        assert mock_group.empty.call_count == 2
        # Check llama was added back to all_sprites after empty
        mock_group.add.assert_called_with(game.llama)
        # Check the internal list of the mock group now only contains the llama
        # NOTE: Depending on exact mock implementation, add might be called multiple times
        # Let's refine this check slightly: ensure llama is the *last* thing added after empty
        assert mock_group.add.call_args_list[-1] == call(game.llama)
        assert mock_group.sprites() == [game.llama]


        # Check timer restarted
        # Allow for previous calls (init, stop on collision potentially)
        mock_pygame_essentials["set_timer"].assert_called_with(
            constants.OBSTACLE_SPAWN_EVENT, constants.OBSTACLE_CREATION_INTERVAL
        )
        assert game.running is True


    def test_quit_event_game_over(self, mock_pygame_essentials, mock_game_components):
        """Test Case: Quit Event (Game Over)"""
        game = Game()
        game.game_over = True
        quit_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_q)
        mock_pygame_essentials["event_get"].return_value = [quit_event]

        game._handle_events()

        assert game.running is False


    def test_quit_event_window_close(self, mock_pygame_essentials, mock_game_components):
        """Test Case: Quit Event (Window Close)"""
        game = Game()
        quit_event = pygame.event.Event(pygame.QUIT)
        mock_pygame_essentials["event_get"].return_value = [quit_event]

        game._handle_events()

        assert game.running is False


    def test_drawing_cycle_playing(self, mock_pygame_essentials, mock_game_components):
        """Test Case: Drawing Cycle (Playing)"""
        game = Game()
        game.game_over = False
        game.scaled_ground_image = mock_pygame_essentials["mock_surface"] # Ensure ground image exists

        # Get mock screen and mock group
        mock_screen = game.screen
        mock_group = game.all_sprites

        game._draw()

        mock_screen.fill.assert_called_once_with(constants.WHITE)
        # Check ground blit (might be multiple calls if wider than screen)
        mock_screen.blit.assert_any_call(game.scaled_ground_image, (0, 0))
        mock_group.draw.assert_called_once_with(mock_screen) # all_sprites.draw
        mock_game_components["scoreboard_instance"].draw.assert_called_once_with(mock_screen)
        mock_pygame_essentials["display_flip"].assert_called_once()


    def test_drawing_cycle_game_over(self, mock_pygame_essentials, mock_game_components):
        """Test Case: Drawing Cycle (Game Over)"""
        game = Game()
        game.game_over = True
        game.scaled_ground_image = mock_pygame_essentials["mock_surface"]
        game.scoreboard.score = 123 # Example score

        # Get mock screen and mock group
        mock_screen = game.screen
        mock_group = game.all_sprites

        # Mock the specific fonts used in game over (assign the generic mock font)
        game.game_over_font = mock_pygame_essentials["mock_font"]
        game.instruction_font = mock_pygame_essentials["mock_font"]

        game._draw()

        mock_screen.fill.assert_called_once_with(constants.WHITE)
        # Ground, sprites, score drawn as usual
        mock_screen.blit.assert_any_call(game.scaled_ground_image, (0, 0))
        mock_group.draw.assert_called_once_with(mock_screen)
        mock_game_components["scoreboard_instance"].draw.assert_called_once_with(mock_screen)

        # Check Game Over specific text rendering and blitting
        render_calls = mock_pygame_essentials["mock_font"].render.call_args_list
        blit_calls = mock_screen.blit.call_args_list

        # Check if "GAME OVER" text was rendered
        assert any(
            call("GAME OVER", True, constants.BLACK) == r_call for r_call in render_calls
        ), "GAME OVER text not rendered"
        # Check if Final Score text was rendered
        assert any(
            call(f"Final Score: {game.scoreboard.score}", True, constants.BLACK) == r_call for r_call in render_calls
        ), "Final Score text not rendered"
         # Check if instructions text was rendered
        assert any(
            call("Press 'R' to Restart or 'Q' to Quit", True, constants.BLACK) == r_call for r_call in render_calls
        ), "Instructions text not rendered"

        # Check blit was called multiple times (ground + sprites.draw + scoreboard.draw + 3 text lines)
        # Note: Ground blit might happen multiple times depending on width, so check >= 6
        assert len(blit_calls) >= 6, f"Expected at least 6 blit calls, got {len(blit_calls)}"

        mock_pygame_essentials["display_flip"].assert_called_once()


    def test_run_loop_terminates_on_running_false(self, mock_pygame_essentials, mock_game_components):
        """Test simulation of the run loop exiting"""
        game = Game()

        # Simulate loop running once then stopping because _handle_events sets running=False
        mock_pygame_essentials["event_get"].return_value = [pygame.event.Event(pygame.QUIT)]
        game.running = True # Start running

        # Store original methods
        original_handle_events = game._handle_events
        original_update = game._update
        original_draw = game._draw

        # Use side effect to ensure state change happens and track calls
        call_tracker = {'handle': 0, 'update': 0, 'draw': 0, 'tick': 0}

        def handle_events_side_effect():
            call_tracker['handle'] += 1
            original_handle_events() # Call real logic which processes QUIT

        def update_side_effect():
             call_tracker['update'] += 1
             original_update()

        def draw_side_effect():
             call_tracker['draw'] += 1
             original_draw()

        def tick_side_effect(*args):
            call_tracker['tick'] +=1
            # Prevent infinite loop if running doesn't get set to False somehow
            if call_tracker['tick'] > 5:
                game.running = False


        with patch.object(game, '_handle_events', side_effect=handle_events_side_effect), \
             patch.object(game, '_update', side_effect=update_side_effect), \
             patch.object(game, '_draw', side_effect=draw_side_effect), \
             patch.object(game.clock, 'tick_busy_loop', side_effect=tick_side_effect) as mock_tick:

            with pytest.raises(SystemExit, match="Simulated sys.exit"): # Expect sys.exit
                game.run()

            # Assertions after loop exit
            assert call_tracker['handle'] >= 1 # Should be called at least once
            assert call_tracker['update'] >= 1 # Should be called while running=True
            assert call_tracker['draw'] >= 1   # Should be called while running=True
            mock_tick.assert_called_with(constants.FPS)

        # Check cleanup calls happen *after* loop
        mock_pygame_essentials["pygame_quit"].assert_called_once()
        mock_pygame_essentials["sys_exit"].assert_called_once()