import pytest
from unittest.mock import MagicMock, patch

# Assume main.py is in the same directory or accessible via PYTHONPATH
# If not, adjust the import path accordingly.
try:
    from main import Game
except ModuleNotFoundError:
    # Simple fallback if main isn't directly importable
    # Requires manual adjustment if structure is complex
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from main import Game


# Create a simple mock object for the scoreboard dependency
class MockScoreboard:
    def __init__(self, score=0):
        self.score = score

@pytest.fixture
def game_instance(mocker):
    """Fixture to create a Game instance with minimal mocking."""
    # Mock pygame functions called in Game.__init__ to avoid side effects
    mocker.patch('pygame.init')
    mocker.patch('pygame.mixer.init')
    # mocker.patch('pygame.font.init') # Keep font init unmocked if needed, or mock SysFont below
    mocker.patch('pygame.display.set_mode')
    mocker.patch('pygame.display.set_caption')
    mocker.patch('pygame.time.Clock')
    mocker.patch('pygame.time.get_ticks', return_value=0)
    # Mock image loading to prevent file errors
    mock_surface = MagicMock()
    mock_surface.convert.return_value = mock_surface # Mock convert() call
    mocker.patch('pygame.image.load', return_value=mock_surface)
    mocker.patch('pygame.time.set_timer')
    # Mock internal class instantiations if they have complex dependencies
    mocker.patch('main.Llama')
    # Replace Scoreboard instantiation with our simple mock BEFORE Game() is called
    mocker.patch('main.Scoreboard', return_value=MockScoreboard(0))
    # Prevent actual file loading in __init__
    mocker.patch.object(Game, '_load_high_scores', return_value=[])
    # Mock SysFont directly to return a dummy font object
    # This prevents actual font loading errors
    mock_font = MagicMock()
    mocker.patch('pygame.font.SysFont', return_value=mock_font)

    # Instantiate the Game object - __init__ will use the mocked Scoreboard
    game = Game()

    # Ensure high_scores list is initialized for tests if needed after init
    # (though mocking _load_high_scores handles the init part)
    game.high_scores = []

    # game.scoreboard = mocker.get_original('main.Scoreboard')() # REMOVED THIS LINE

    return game

# --- Test Cases based on the Updated Plan ---

@pytest.mark.parametrize(
    "high_scores_list, current_score, expected_result",
    [
        # Test Case: List < 10, Any Score
        ([{'name': 'A', 'score': 50}, {'name': 'B', 'score': 30}], 1, True),

        # Test Case: List = 10, Score > 10th
        # Create a list where the 10th score (index 9) is 10
        ([{'name': f'P{i}', 'score': 100 - i*10} for i in range(10)], 11, True),

        # Test Case: List = 10, Score = 10th
        ([{'name': f'P{i}', 'score': 100 - i*10} for i in range(10)], 10, False),

        # Test Case: List = 10, Score < 10th
        ([{'name': f'P{i}', 'score': 100 - i*10} for i in range(10)], 9, False),

        # Test Case: Empty List
        ([], 10, True),

        # Test Case: List = 10, Last Entry Missing Score (Added Test)
        # Create a list where the 10th entry lacks 'score' key
        ([{'name': f'P{i}', 'score': 100 - i*10} for i in range(9)] + [{'name': 'BadEntry'}], 1, True),
        # Note: Checks if 1 > high_scores[-1].get('score', 0), which is 1 > 0, so True.

        # Additional check for the missing score case: score is 0, should be ineligible
        ([{'name': f'P{i}', 'score': 100 - i*10} for i in range(9)] + [{'name': 'BadEntry'}], 0, False),
         # Note: Checks if 0 > high_scores[-1].get('score', 0), which is 0 > 0, so False.

    ]
)
def test_check_score_eligible(game_instance, high_scores_list, current_score, expected_result):
    """
    Tests the _check_score_eligible method based on high_scores list state
    and the current score.
    """
    # Arrange
    # NOTE: The game instance's scoreboard is already the MockScoreboard(0)
    #       due to patching before __init__ was called.
    #       We just need to set the score on it for the specific test case.
    game_instance.scoreboard.score = current_score

    # Also set the high_scores list for the specific test case.
    # The _load_high_scores mock prevents loading, so we set it manually here.
    game_instance.high_scores = high_scores_list

    # Act
    result = game_instance._check_score_eligible()

    # Assert
    assert result == expected_result