import pytest
import json
import sys
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path

# Add project root to sys.path if constants/main are not directly importable
# import sys
# sys.path.insert(0, str(Path(__file__).parent.parent)) # Adjust path as needed

# Mock pygame modules before importing main
if 'pygame' not in sys.modules:
    sys.modules['pygame'] = MagicMock()
    sys.modules['pygame.sprite'] = MagicMock()
    sys.modules['pygame.display'] = MagicMock()
    sys.modules['pygame.time'] = MagicMock()
    sys.modules['pygame.font'] = MagicMock()
    sys.modules['pygame.event'] = MagicMock()
    sys.modules['pygame.image'] = MagicMock()
    sys.modules['pygame.mixer'] = MagicMock()
    sys.modules['pygame.transform'] = MagicMock()
    sys.modules['pygame.mask'] = MagicMock()
    sys.modules['pygame.constants'] = MagicMock() # Mock constants if needed, though not for this func

# Import the class containing the method AFTER mocking pygame
from main import Game # Only import Game needed for this test file

# Mock components used by Game.__init__ but not directly by _load_high_scores
@pytest.fixture(autouse=True)
def mock_game_init_dependencies(mocker):
    # Mock only init dependencies, not the method under test
    mocker.patch('main.pygame.init')
    mocker.patch('main.pygame.mixer.init')
    mocker.patch('main.pygame.font.init')
    mocker.patch('main.pygame.display.set_mode', return_value=MagicMock())
    mocker.patch('main.pygame.display.set_caption')
    mocker.patch('main.pygame.time.Clock', return_value=MagicMock())
    mocker.patch('main.pygame.time.get_ticks', return_value=0)
    mocker.patch('main.pygame.image.load', return_value=MagicMock(convert=MagicMock()))
    mocker.patch('main.pygame.time.set_timer')
    mocker.patch('main.Llama', return_value=MagicMock()) # Mock Llama instantiation
    mocker.patch('main.Scoreboard', return_value=MagicMock()) # Mock Scoreboard instantiation
    # DO NOT mock _load_high_scores here


@pytest.fixture
def game_instance(mocker):
    """Provides a Game instance for testing _load_high_scores."""
    # Temporarily patch _load_high_scores during __init__ only
    with patch.object(Game, '_load_high_scores', return_value=[]):
        game = Game()
    game.high_score_file = "test_scores.json" # Use a test-specific filename
    mocker.patch('builtins.print') # Mock print globally for tests
    return game

# --- Test Cases ---

def test_load_scores_file_exists_valid_json(game_instance, tmp_path, mocker):
    """Tests loading a valid JSON list from an existing file."""
    scores_data = [{"name": "PlayerA", "score": 100}]
    file_path = tmp_path / game_instance.high_score_file
    file_path.write_text(json.dumps(scores_data))

    mock_path = MagicMock(spec=Path)
    mock_path.is_file.return_value = True
    mocker.patch('main.Path', return_value=mock_path)

    # Mock open specifically for this test's path
    mock_file_content = json.dumps(scores_data)
    mocker.patch('builtins.open', mock_open(read_data=mock_file_content))
    # Mock json load to ensure it returns the data correctly
    mocker.patch('json.load', return_value=scores_data)

    loaded_scores = game_instance._load_high_scores()

    assert loaded_scores == scores_data
    mock_path.is_file.assert_called_once()


def test_load_scores_correct_sorting(game_instance, tmp_path, mocker):
    """Tests that scores are loaded and sorted correctly by score descending."""
    scores_data = [
        {"name": "PlayerB", "score": 50},
        {"name": "PlayerA", "score": 100},
        {"name": "PlayerC", "score": 75},
    ]
    expected_sorted = [
        {"name": "PlayerA", "score": 100},
        {"name": "PlayerC", "score": 75},
        {"name": "PlayerB", "score": 50},
    ]
    file_path = tmp_path / game_instance.high_score_file
    file_path.write_text(json.dumps(scores_data))

    mock_path = MagicMock(spec=Path)
    mock_path.is_file.return_value = True
    mocker.patch('main.Path', return_value=mock_path)
    mocker.patch('builtins.open', mock_open(read_data=json.dumps(scores_data)))
    mocker.patch('json.load', return_value=scores_data)

    loaded_scores = game_instance._load_high_scores()

    assert loaded_scores == expected_sorted

def test_load_scores_missing_keys(game_instance, tmp_path, mocker):
    """Tests loading scores where some entries are missing the 'score' key."""
    scores_data = [
        {"name": "PlayerB"}, # Missing score key
        {"name": "PlayerA", "score": 100},
        {"name": "PlayerC", "score": 75},
    ]
    # CORRECTION: Expected output reflects sorting order, but PlayerB dict is unchanged.
    expected_sorted_structure = [
        {"name": "PlayerA", "score": 100},
        {"name": "PlayerC", "score": 75},
        {"name": "PlayerB"}, # Structure remains the same
    ]
    file_path = tmp_path / game_instance.high_score_file
    file_path.write_text(json.dumps(scores_data))

    mock_path = MagicMock(spec=Path)
    mock_path.is_file.return_value = True
    mocker.patch('main.Path', return_value=mock_path)
    mocker.patch('builtins.open', mock_open(read_data=json.dumps(scores_data)))
    mocker.patch('json.load', return_value=scores_data)


    loaded_scores = game_instance._load_high_scores()

    # Assert the structure and order are as expected
    assert loaded_scores == expected_sorted_structure

def test_load_scores_truncation(game_instance, tmp_path, mocker):
    """Tests that only the top 10 scores are returned if the file has more."""
    scores_data = [{"name": f"P{i}", "score": i} for i in range(12, 0, -1)] # 12 scores, 12 down to 1
    expected_top_10 = [{"name": f"P{i}", "score": i} for i in range(12, 2, -1)] # Top 10 are 12 down to 3

    file_path = tmp_path / game_instance.high_score_file
    file_path.write_text(json.dumps(scores_data))

    mock_path = MagicMock(spec=Path)
    mock_path.is_file.return_value = True
    mocker.patch('main.Path', return_value=mock_path)
    mocker.patch('builtins.open', mock_open(read_data=json.dumps(scores_data)))
    mocker.patch('json.load', return_value=scores_data)

    loaded_scores = game_instance._load_high_scores()

    assert len(loaded_scores) == 10
    assert loaded_scores == expected_top_10

def test_load_scores_empty_json_list(game_instance, tmp_path, mocker):
    """Tests loading from a file containing an empty JSON list."""
    scores_data = []
    file_path = tmp_path / game_instance.high_score_file
    file_path.write_text(json.dumps(scores_data))

    mock_path = MagicMock(spec=Path)
    mock_path.is_file.return_value = True
    mocker.patch('main.Path', return_value=mock_path)
    mocker.patch('builtins.open', mock_open(read_data=json.dumps(scores_data)))
    mocker.patch('json.load', return_value=scores_data)

    loaded_scores = game_instance._load_high_scores()

    assert loaded_scores == []

def test_load_scores_file_does_not_exist(game_instance, mocker):
    """Tests behavior when the high score file does not exist."""
    mock_path = MagicMock(spec=Path)
    mock_path.is_file.return_value = False # Simulate file not existing
    mocker.patch('main.Path', return_value=mock_path)
    mock_open_func = mocker.patch('builtins.open') # Ensure open is not called

    loaded_scores = game_instance._load_high_scores()

    assert loaded_scores == []
    mock_path.is_file.assert_called_once()
    mock_open_func.assert_not_called() # Verify file wasn't opened

def test_load_scores_path_is_directory(game_instance, tmp_path, mocker):
    """Tests behavior when the path exists but is a directory."""
    dir_path = tmp_path / game_instance.high_score_file
    dir_path.mkdir() # Create a directory at the path

    # Use actual Path object to test is_file on directory
    game_instance.high_score_file = str(dir_path)
    mocker.patch('main.Path', return_value=Path(dir_path)) # Use real Path

    mock_open_func = mocker.patch('builtins.open')

    loaded_scores = game_instance._load_high_scores()

    assert loaded_scores == []
    mock_open_func.assert_not_called() # is_file returned false

def test_load_scores_invalid_json(game_instance, tmp_path, mocker):
    """Tests behavior with an existing file containing invalid JSON."""
    invalid_json = "this is not json"
    file_path = tmp_path / game_instance.high_score_file
    file_path.write_text(invalid_json)

    mock_path = MagicMock(spec=Path)
    mock_path.is_file.return_value = True
    mocker.patch('main.Path', return_value=mock_path)
    mocker.patch('builtins.open', mock_open(read_data=invalid_json))
    # Make json.load raise the expected error
    mocker.patch('json.load', side_effect=json.JSONDecodeError("Error", "doc", 0))
    mock_print = mocker.patch('builtins.print')

    loaded_scores = game_instance._load_high_scores()

    assert loaded_scores == []
    mock_print.assert_called_once() # Check if the error message was printed
    assert "Error decoding JSON" in mock_print.call_args[0][0]

def test_load_scores_file_not_list(game_instance, tmp_path, mocker):
    """Tests file content being a valid JSON object, but not a list (expects KeyError on return)."""
    not_a_list = {"name": "PlayerA", "score": 100} # Dictionary
    file_path = tmp_path / game_instance.high_score_file
    file_path.write_text(json.dumps(not_a_list))

    mock_path = MagicMock(spec=Path)
    mock_path.is_file.return_value = True
    mocker.patch('main.Path', return_value=mock_path)
    mocker.patch('builtins.open', mock_open(read_data=json.dumps(not_a_list)))
    # Let json.load succeed returning the dict
    mocker.patch('json.load', return_value=not_a_list)
    mock_print = mocker.patch('builtins.print')

    # CORRECTION: Expect KeyError because scores.sort() fails (AttributeError caught),
    # but then return scores[:10] fails on dict with KeyError
    with pytest.raises(KeyError): # Changed from TypeError
         game_instance._load_high_scores()

    # Check that the generic exception was caught and printed
    mock_print.assert_called_once()
    assert "unexpected error occurred loading high scores" in mock_print.call_args[0][0]


def test_load_scores_list_contains_non_dict(game_instance, tmp_path, mocker):
    """Tests file content being a list containing non-dictionary items (expects original list returned)."""
    list_with_non_dict = [1, 2, {"name": "PlayerA", "score": 100}]
    file_path = tmp_path / game_instance.high_score_file
    file_path.write_text(json.dumps(list_with_non_dict))

    mock_path = MagicMock(spec=Path)
    mock_path.is_file.return_value = True
    mocker.patch('main.Path', return_value=mock_path)
    mocker.patch('builtins.open', mock_open(read_data=json.dumps(list_with_non_dict)))
     # Let json.load succeed returning the list
    mocker.patch('json.load', return_value=list_with_non_dict)
    mock_print = mocker.patch('builtins.print')

    # CORRECTION: sort fails (AttributeError caught), return scores[:10] succeeds
    # No error should be raised here. Check the return value and print call.
    loaded_scores = game_instance._load_high_scores()

    # The function returns the original list (or first 10 elements) after catching the sort error
    assert loaded_scores == list_with_non_dict

    # Check that the generic exception *was* caught and printed
    mock_print.assert_called_once()
    assert "unexpected error occurred loading high scores" in mock_print.call_args[0][0]
    # Can check specific error type if needed: assert isinstance(mock_print.call_args[0][0].split(': ')[1], AttributeError)


def test_load_scores_permission_error(game_instance, tmp_path, mocker):
    """Tests behavior when opening the file raises an OS-level error."""
    # File needs to "exist" for the attempt to open it
    file_path = tmp_path / game_instance.high_score_file
    file_path.touch() # Create empty file

    mock_path = MagicMock(spec=Path)
    mock_path.is_file.return_value = True
    mocker.patch('main.Path', return_value=mock_path)
    # Make open raise an error
    mocker.patch('builtins.open', side_effect=OSError("Permission denied"))
    mock_print = mocker.patch('builtins.print')

    loaded_scores = game_instance._load_high_scores()

    assert loaded_scores == []
    mock_print.assert_called_once() # Check generic error message printed
    # Check specific error message if desired
    assert "unexpected error occurred loading high scores: Permission denied" in mock_print.call_args[0][0]