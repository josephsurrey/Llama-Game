import pytest
import pygame
from unittest.mock import MagicMock, patch

# Assume constants.py exists in the same directory or is accessible
# Assume main.py with the Game class exists
from main import Game
# import constants # Keep constants import if needed, though not strictly for these tests


# Define a fixture to create a Game instance for testing
# We mock essential pygame functions to avoid actual window creation etc.
@pytest.fixture
def game_instance(mocker):
    """Fixture to create a Game instance with mocked dependencies."""
    mocker.patch('pygame.init', return_value=None)
    mocker.patch('pygame.mixer.init', return_value=None)
    mocker.patch('pygame.font.init', return_value=None)
    mocker.patch('pygame.display.set_mode', return_value=MagicMock())
    mocker.patch('pygame.display.set_caption', return_value=None)
    mocker.patch('pygame.time.Clock', return_value=MagicMock())
    # Mock image loading as it's not relevant to _add_high_score
    mocker.patch('pygame.image.load', side_effect=pygame.error("Mocked image load failure"))
    mocker.patch('pygame.time.set_timer', return_value=None)
    mocker.patch('pygame.font.SysFont', return_value=MagicMock())

    # Mock methods that interact with files or other complex state
    mocker.patch.object(Game, '_load_high_scores', return_value=[])
    mocker.patch.object(Game, '_save_high_scores', return_value=None)

    # Mock sprite classes if their specifics aren't needed for this test
    mocker.patch('main.Llama', return_value=MagicMock(spec=pygame.sprite.Sprite))
    mocker.patch('main.Scoreboard', return_value=MagicMock())
    # Don't strictly need to mock Obstacle unless its init is complex

    game = Game()
    # Ensure high_scores starts empty for predictable tests, unless overridden
    game.high_scores = []
    return game

# Test cases based on the updated plan

def test_add_high_score_empty_list(game_instance, mocker):
    """Test adding a score when the high score list is empty."""
    save_spy = mocker.spy(game_instance, '_save_high_scores')
    game_instance._add_high_score("Alice", 100)
    assert game_instance.high_scores == [{"name": "Alice", "score": 100}]
    save_spy.assert_called_once()

def test_add_high_score_short_list_sorted(game_instance, mocker):
    """Test adding a score to a short list, ensuring it's sorted."""
    save_spy = mocker.spy(game_instance, '_save_high_scores')
    game_instance.high_scores = [{"name": "Alice", "score": 100}]
    game_instance._add_high_score("Bob", 50)
    # Check if sorted descending by score
    assert game_instance.high_scores == [
        {"name": "Alice", "score": 100},
        {"name": "Bob", "score": 50},
    ]
    save_spy.assert_called_once()

def test_add_high_score_higher_score_sorted(game_instance, mocker):
    """Test adding a score higher than existing ones, ensuring sorting."""
    save_spy = mocker.spy(game_instance, '_save_high_scores')
    game_instance.high_scores = [{"name": "Bob", "score": 50}]
    game_instance._add_high_score("Charlie", 150)
    # Check if sorted descending by score
    assert game_instance.high_scores == [
        {"name": "Charlie", "score": 150},
        {"name": "Bob", "score": 50},
    ]
    save_spy.assert_called_once()

def test_add_high_score_full_list_beats_10th(game_instance, mocker):
    """Test adding a score that qualifies for a full list, replacing the lowest."""
    save_spy = mocker.spy(game_instance, '_save_high_scores')
    # Create a full list of 10 scores
    game_instance.high_scores = [
        {"name": f"P{i}", "score": 100 - i * 10} for i in range(10)
    ] # Scores: 100, 90, ..., 10
    lowest_score = game_instance.high_scores[-1]['score'] # Should be 10
    original_lowest_name = game_instance.high_scores[-1]['name'] # Should be P9

    # Add a score better than the lowest
    game_instance._add_high_score("NewBest", lowest_score + 5) # Score 15

    assert len(game_instance.high_scores) == 10
    # The new score (15) should now be the 9th item after sorting (index 8)
    # The original 9th item (P8, 20) should be the 8th (index 7)
    # The original 10th item (P9, 10) should be gone.
    # The new 10th item should be the new score (15)
    assert game_instance.high_scores[9]['score'] == lowest_score + 5
    assert game_instance.high_scores[9]['name'] == "NewBest"

    # Check that the original lowest score/name ('P9', 10) is gone
    assert not any(entry['name'] == original_lowest_name for entry in game_instance.high_scores)
    save_spy.assert_called_once()

def test_add_high_score_full_list_not_top_10(game_instance, mocker):
    """Test adding a score lower than the 10th score on a full list (defensive)."""
    save_spy = mocker.spy(game_instance, '_save_high_scores')
    # Create a full list of 10 scores
    game_instance.high_scores = [
        {"name": f"P{i}", "score": 100 - i * 10} for i in range(10)
    ] # Scores: 100, 90, ..., 10
    lowest_score = game_instance.high_scores[-1]['score'] # Should be 10
    original_10th_name = game_instance.high_scores[-1]['name'] # 'P9'

    # Add a score worse than the lowest (this scenario implies eligibility check failed/was bypassed)
    game_instance._add_high_score("TooLow", lowest_score - 5) # Score 5

    assert len(game_instance.high_scores) == 10
    # The new low score should NOT be in the list after truncation
    assert not any(entry['name'] == "TooLow" for entry in game_instance.high_scores)
    # The original 10th score should still be the 10th score
    assert game_instance.high_scores[-1]['name'] == original_10th_name
    assert game_instance.high_scores[-1]['score'] == lowest_score
    save_spy.assert_called_once() # Save is still called because add happened before truncation

def test_add_high_score_duplicate_score(game_instance, mocker):
    """Test adding a score that is identical to an existing score."""
    save_spy = mocker.spy(game_instance, '_save_high_scores')
    game_instance.high_scores = [{"name": "Alice", "score": 100}]
    game_instance._add_high_score("David", 100)

    assert len(game_instance.high_scores) == 2
    # Both entries should exist
    assert any(e['name'] == 'Alice' and e['score'] == 100 for e in game_instance.high_scores)
    assert any(e['name'] == 'David' and e['score'] == 100 for e in game_instance.high_scores)
    # The exact order depends on sort stability, but both must be present
    save_spy.assert_called_once()

def test_add_high_score_name_stripping(game_instance, mocker):
    """Test that leading/trailing whitespace is stripped from the name."""
    save_spy = mocker.spy(game_instance, '_save_high_scores')
    game_instance._add_high_score("  Eve  ", 75)
    assert game_instance.high_scores == [{"name": "Eve", "score": 75}]
    save_spy.assert_called_once()

def test_add_high_score_makes_list_exactly_10(game_instance, mocker):
    """Test adding the 10th score to a list of 9."""
    save_spy = mocker.spy(game_instance, '_save_high_scores')
    game_instance.high_scores = [
        {"name": f"P{i}", "score": 100 - i * 10} for i in range(9)
    ] # 9 scores: 100 down to 20
    game_instance._add_high_score("Tenth", 5) # Add 10th score

    assert len(game_instance.high_scores) == 10
    assert game_instance.high_scores[-1] == {"name": "Tenth", "score": 5}
    save_spy.assert_called_once()

def test_add_high_score_non_numeric_score_raises_typeerror(game_instance, mocker):
    """Test adding an entry with a non-numeric score raises TypeError during sort."""
    save_spy = mocker.spy(game_instance, '_save_high_scores')
    game_instance.high_scores = [{"name": "Num", "score": 50}]

    # Expect a TypeError because sort cannot compare int and str in Python 3
    with pytest.raises(TypeError, match="'<' not supported"):
        game_instance._add_high_score("StrScore", "abc")

    # Assert that save was not called because the sort failed
    save_spy.assert_not_called()

def test_add_high_score_invalid_name_none(game_instance, mocker):
    """Test adding a score with None as the name (should raise AttributeError)."""
    save_spy = mocker.spy(game_instance, '_save_high_scores')
    with pytest.raises(AttributeError, match="'NoneType' object has no attribute 'strip'"):
        game_instance._add_high_score(None, 100)
    save_spy.assert_not_called() # Save should not be called if strip fails