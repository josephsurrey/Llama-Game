# Relevant Implications
### Functionality
Functionality involves ensuring that the outcome functions as intended. For this project, this means creating a playable Llama game which is easily playable with no bugs. This means that the program cannot crash on edge cases, must be able to handle all possible events, etc.

Functionality is important because user experience is the most important factor in a developed outcome, and if the outcome does not have basic functionality, users will become frustrated. Additionally, the program will have no real use, as it is not able to function for its intended task.

### Useability
Useability involves making it easy for the user to use the program without requiring help or assistance from others. For this project, this means making it simple to play, with intuitive controls and instructions that explain how the game works. This means everything must be designed so someone who has never touched a computer before would be able to play the game with as little of a learning curve as possible.

Useability is important because it is another key factor in the user experience. Users must feel like they understand the game, otherwise they will get frustrated and stop playing. This will result in the program not being used.

### Aesthetics
Aesthetics involves making the game appealing to look at. For this project, this involves using images for various parts of the game, such as the background, obstacles, and character.

Aesthetics is important because users appreciate it when games have appealing graphics, and it makes the game look much more professional and developed.

### Social
Social implications involve how the outcome affects users, and the wider community as a whole. Games which can be addictive need to have safeguards in place to stop users from spending too much time on the game. Another example is gambling games, which need safeguards to restrict how much the users can lose.

Social implications are important because games can have unintended negative consequences on their users.

Fortunately, the program which I will be creating is a very simple game, which means that additional safeguards will probably not need to be implemented to stop misuse of the game.

# GUI Design
## Wireframes
### Regular Gameplay
![[gameplay_wireframe.png]]
### Game over (not high score)
![[gameover_standard_wireframe.png]]
### Game over (high score)
![[gameover_eligible_wireframe.png]]
### Enter name (high score)
![[entername_wireframe.png]]
### High scores
![[highscores_wireframe.png]]

# Program Structure
### Game Class
*   Setup Game (`__init__`)
*   Run Game Loop (`run`)
*   Handle Events (`_handle_events`)
*   Update Game State (`_update`)
*   Draw Frame (`_draw`)
*   Spawn Obstacle (`_spawn_obstacle`)
*   Check Collisions (`_check_collisions`)
*   Reset Game (`_reset_game`)
*   Load High Scores (`_load_high_scores`)
*   Save High Scores (`_save_high_scores`)
*   Check Score Eligibility (`_check_score_eligible`)
*   Add High Score (`_add_high_score`)
*   Draw High Scores Screen (`_draw_high_scores_screen`)

### Llama Class
*   Setup Player (`__init__`)
*   Update Player State (`update`)
*   Perform Jump (`jump`)
*   Reset Player (`reset`)

### Obstacle Class
*   Setup Obstacle (`__init__`)
*   Update Obstacle State (`update`)
### Scoreboard Class
*   Setup Scoreboard (`__init__`)
*   Update Score (`update`)
*   Draw Score (`draw`)
*   Reset Score (`reset`)

# Project Decomposition
![[constants.py - Llama Game Decomposition]]
![[Game Class - Llama Game Decomposition]]
![[Llama Class - Llama Game Decomposition]]
![[Obstacle Class - Llama Game Decomposition]]
![[Scoreboard Class - Llama Game Decomposition]]

# Project Development
## constants.py
#### Component Planning
![[constants.py - Llama Game Decomposition#Define Constants]]
#### Change List

| Date  | Change                                                                                        |
| ----- | --------------------------------------------------------------------------------------------- |
| 28/04 | Added constant for the window title/caption <br>`WINDOW_TITLE = "Llama Game - Joseph Surrey"` |
| 1/05  | Moved obstacle creation signal from `Game.__init__` to `constants.py`                         |

#### Test Plan: constants.py


#### Test Results
##### Test 01 - 26/04
![[Test Results - constants.py - test_01.html]]
The program passed 14/18 tests successfully. The program failed 4/18 tests. The 4 tests that were failed were the image loading tests. The issue causing the failure was the image path in `constants.py`. 
```
# Image file locations  
PLAYER_IMAGE = "/images/Llama.png"  
OBSTACLE_IMAGE = "/images/cactus.png"  
GROUND_IMAGE = "/images/ground.png"  
GAME_ICON = "/images/llama_icon.png"
```
The file locations linked to `/images`, which is an absolute path, looking for the image in the root directory of the hard drive. The image path should actually be
```
# Image file locations  
PLAYER_IMAGE = "images/Llama.png"  
OBSTACLE_IMAGE = "images/cactus.png"  
GROUND_IMAGE = "images/ground.png"  
GAME_ICON = "images/llama_icon.png"
```
This ensures that the program looks for the files in the `images` folder in the current working directory.
##### Test 02 - 26/04
![[Test Results - constants.py - test_02.html]]
The program passed 18/18 tests successfully after making the changes from [[#Test 01]].
## [[Game Class - Llama Game Decomposition]]

### Setup Game (`__init__`)
#### Component Planning
![[Game Class - Llama Game Decomposition#Setup Game (`__init__`)]]
#### Change List

| Date  | Change                                                                                        |
| ----- | --------------------------------------------------------------------------------------------- |
| 1/05  | Moved obstacle creation signal from `Game.__init__` to `constants.py`                         |

#### Test Plan

| Test Case                                     | Verification Focus                             | Expected Output                                                                                                                                                                         | Test Type        |
| :-------------------------------------------- | :--------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------- |
| Standard Initialization (Pygame Modules)      | `Game()` called                                | `pygame.init()`, `pygame.mixer.init()`, `pygame.font.init()` are called exactly once.                                                                                                   | Mock Check       |
| Standard Initialization (Screen & Caption)    | `Game()` called                                | `pygame.display.set_mode` called with `(WINDOW_WIDTH, WINDOW_HEIGHT)`. `pygame.display.set_caption` called with `WINDOW_TITLE`. `self.screen` is assigned the result of `set_mode`.     | Mock Check       |
| Standard Initialization (Clock & Start Time)  | `Game()` called                                | `self.clock` is assigned `pygame.time.Clock`. `self.start_time` is assigned the result of `pygame.time.get_ticks()`.                                                                    | Attribute Check  |
| Attribute Value Checks (Flags, Name)          | `Game()` called                                | `self.running` is True, `self.game_over` is False, `self.entering_name` is False, `self.displaying_scores` is False, `self.score_eligible_for_save` is False, `self.player_name` is "". | Attribute Check  |
| Component Instantiation (Llama, Scoreboard)   | `Game()` called                                | `Llama` class is instantiated. `Scoreboard` class is instantiated. `self.llama` and `self.scoreboard` hold the respective instances.                                                    | Mock Check/Attr  |
| Sprite Group Setup                            | `Game()` called                                | `self.all_sprites` and `self.obstacles` are instances of `pygame.sprite.Group`. Mock `Llama` instance is added to `self.all_sprites`.                                                   | Type/State Check |
| Ground Image Load Success                     | `pygame.image.load` succeeds                   | `pygame.image.load` called with `constants.GROUND_IMAGE`. `convert()` is called on the result. `self.ground_image` holds the result of `convert()`.                                     | Mock/Attr Check  |
| Ground Image Load Failure (pygame.error)      | `pygame.image.load` raises `pygame.error`      | Exception is caught, `self.ground_image` is set to `None`.                                                                                                                              | Error Handling   |
| Ground Image Load Failure (FileNotFoundError) | `pygame.image.load` raises `FileNotFoundError` | Exception is caught, `self.ground_image` is set to `None`.                                                                                                                              | Error Handling   |
| Obstacle Timer Set                            | `Game()` called                                | `pygame.time.set_timer` called once with `constants.OBSTACLE_SPAWN_EVENT` and `constants.OBSTACLE_CREATION_INTERVAL`.                                                                   | Mock Check       |
| High Score Load Called                        | `Game()` called                                | Instance's `_load_high_scores()` method is called exactly once.                                                                                                                         | Mock Check       |
| Font Object Creation                          | `Game()` called                                | `pygame.font.SysFont` is called for each font (`score_font`, `game_over_font`, `button_font`, `input_font`) with `(None, expected_size)`. Corresponding attributes are set.             | Mock Check       |

#### Test Results
##### Test 01
![[Test Results - game_init - test_01.html]]
Passed 12/12 tests
### Run Game Loop (`run`)
#### Component Planning
![[Game Class - Llama Game Decomposition#Run Game Loop (`run`)]]
#### Test Plan

| Test Case                    | Input / Conditions                                                 | Expected Output                                                                                                                                         | Test Type  |
| :--------------------------- | :----------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------ | :--------- |
| Normal Loop Execution & Exit | `self.running` starts True, then becomes False in `_handle_events` | `_handle_events`, `_update`, `_draw`, `clock.tick_busy_loop` called at least once. Loop terminates. `pygame.quit()` and `sys.exit()` called after loop. | Mock Check |
| Clean Exit Sequence          | Loop terminates (e.g., `self.running` becomes False)               | `pygame.quit()` and `sys.exit()` are called *after* the loop finishes.                                                                                  | Mock Check |
| Clock Ticking Verified       | Loop runs for at least one iteration                               | `game.clock.tick_busy_loop` is called with `constants.FPS`.                                                                                             | Mock Check |
| Exception within Loop        | `_update` (or another sub-method) raises Exception                 | Loop terminates abruptly. `pygame.quit()` and `sys.exit()` are *not* called by the `run` method itself.                                                 | Error Case |
#### Test Results
##### Test 01
![[Test Results - game_run - test_01.html]]
Passed 4/4 tests
### Handle Events (`_handle_events`)
#### Component Planning
![[Game Class - Llama Game Decomposition#Handle Events (`_handle_events`)]]
#### Test Plan
| Test Case                                   | Input / Conditions                                                | Expected Output                                                                                                   | Test Type        |
| :------------------------------------------ | :---------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------- | :--------------- |
| Quit Event (Window Close)                   | User clicks window 'X' button                                     | `pygame.QUIT` event detected, `self.running` set to False.                                                        | Expected         |
| Jump Key Press (Playing - Space)            | SPACE pressed while `game_over` is False                          | `llama.jump()` method is called.                                                                                  | Expected         |
| Jump Key Press (Playing - Up)               | UP pressed while `game_over` is False                             | `llama.jump()` method is called.                                                                                  | Expected         |
| Jump Key Press (Game Over)                  | SPACE or UP pressed while `game_over` is True                     | No action (jump not called).                                                                                      | Expected         |
| Restart Key Press (Game Over)               | 'R' pressed while `game_over` is True                             | `_reset_game()` method is called.                                                                                 | Expected         |
| Restart Key Press (Playing)                 | 'R' pressed while `game_over` is False                            | No action.                                                                                                        | Expected         |
| Quit Key Press (Game Over)                  | 'Q' pressed while `game_over` is True                             | `self.running` set to False.                                                                                      | Expected         |
| Quit Key Press (Playing)                    | 'Q' pressed while `game_over` is False                            | No action.                                                                                                        | Expected         |
| Obstacle Spawn Event (Playing)              | `pygame.USEREVENT + 1` occurs while `game_over` is False          | `_spawn_obstacle()` method is called.                                                                             | Expected         |
| Obstacle Spawn Event (Game Over)            | `pygame.USEREVENT + 1` occurs while `game_over` is True           | No action (`_spawn_obstacle` not called).                                                                         | Expected         |
| Save Score Confirm (Y - Eligible)           | 'Y' pressed while `game_over` is True & score is eligible         | Game state changes to `entering_name`, `player_name` reset to "".                                                 | Expected         |
| Save Score Decline (N - Eligible)           | 'N' pressed while `game_over` is True & score is eligible         | `score_eligible_for_save` set to False.                                                                           | Expected         |
| Save Score Keys (Not Eligible)              | 'Y' or 'N' pressed while `game_over` is True & score not eligible | No state change (`entering_name` remains False, `score_eligible_for_save` remains False).                         | Expected         |
| Enter Name Keys (Alphanumeric)              | Alphanumeric keys pressed while `entering_name`                   | Characters appended to `self.player_name`.                                                                        | Expected         |
| Enter Name Keys (Space)                     | Space key pressed while `entering_name`                           | Space appended to `self.player_name`.                                                                             | Expected         |
| Enter Name - Length Limit                   | Key pressed when `len(self.player_name)` is 6                     | Character not appended to `self.player_name`.                                                                     | Boundary         |
| Backspace Key (Entering Name State)         | BACKSPACE pressed while `entering_name`                           | Last character removed from `self.player_name`.                                                                   | Expected         |
| Enter Key (Entering Name State - Valid)     | ENTER pressed while `entering_name` with non-empty `player_name`  | `_add_high_score()` called with name/score, `entering_name` set to False, `score_eligible_for_save` set to False. | Expected         |
| Enter Key (Entering Name State - Empty)     | ENTER pressed while `entering_name` with empty `player_name`      | `_add_high_score()` not called, `entering_name` set to False, `score_eligible_for_save` set to False.             | Boundary         |
| Escape Key (Showing Scores State)           | ESC pressed while `displaying_scores`                             | `displaying_scores` set to False.                                                                                 | Expected         |
| Unexpected Key Press (Playing)              | Any key other than SPACE/UP pressed while playing                 | No action.                                                                                                        | Unexpected Input |
| Unexpected Key Press (Game Over - Standard) | Any key other than R, Q, Y, N pressed while game over             | No action.                                                                                                        | Unexpected Input |
| Unexpected Key Press (Entering Name)        | Any key other than alphanum, space, backspace, enter pressed      | No action / character not added.                                                                                  | Unexpected Input |
| Unexpected Key Press (Showing Scores)       | Any key other than ESC pressed while showing scores               | No action.                                                                                                        | Unexpected Input |
| Multiple Events Per ![[Test Results - game__handle_events - test_01.html]]Frame                   | e.g., Key press and Obstacle Spawn event in same frame            | Both events processed correctly in sequence within the loop iteration.                                            | Edge Case        |
#### Test Results
![[Test Results - game__handle_events - test_01.html]]
Passed 25/25 tests
### Update Game State (`_update`)
#### Component Planning
![[Game Class - Llama Game Decomposition#Update Game State (`_update`)]]
#### Test Plan
| Test Case                            | Input / Conditions                                              | Expected Output                                                                                                  | Test Type       |
| :----------------------------------- | :-------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------- | :-------------- |
| Update While Playing                 | `game_over`, `entering_name`, `displaying_scores` are all False | `all_sprites.update()`, `scoreboard.update()`, `_check_collisions()` are called.                                 | Mock Check      |
| Update While Game Over               | `game_over` is True                                             | `all_sprites.update()`, `scoreboard.update()`, `_check_collisions()` are *not* called.                           | Mock Check      |
| Update While Entering Name           | `entering_name` is True                                         | `all_sprites.update()`, `scoreboard.update()`, `_check_collisions()` are *not* called.                           | Mock Check      |
| Update While Displaying Scores       | `displaying_scores` is True                                     | `all_sprites.update()`, `scoreboard.update()`, `_check_collisions()` are *not* called.                           | Mock Check      |
| No Sprites Present                   | `all_sprites` group is empty, game is playing                   | `all_sprites.update()` is called without error. `scoreboard.update()` and `_check_collisions()` are also called. | Edge/Mock Check |
| Verify `scoreboard.update` Arguments | `game_over`, `entering_name`, `displaying_scores` are all False | `scoreboard.update()` called with `pygame.time.get_ticks()` result and `game.start_time`.                        | Mock Check      |
#### Test Results
##### Test 01
![[Test Results - game__update - test_01.html]]
Passed 6/6
### Draw Frame (`_draw`)
#### Component Planning
![[Game Class - Llama Game Decomposition#Draw Frame (`_draw`)]]
#### Test Plan
| Test Case                         | Input / Conditions                                                         | Expected Output / Checks                                                                                                                                                     | Test Type        |
| :-------------------------------- | :------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------- |
| Draw While Playing (Ground Image) | `game_over`, `entering_name`, `displaying_scores` all False. `ground_image` exists. | `screen.fill`, `screen.blit` (ground), `all_sprites.draw`, `scoreboard.draw` called. `font.render` for Game Over text *not* called.                                         | Expected         |
| Draw While Playing (No Ground Image) | `game_over`, `entering_name`, `displaying_scores` all False. `ground_image` is None. | `screen.fill`, `pygame.draw.rect` (fallback ground), `all_sprites.draw`, `scoreboard.draw` called. `font.render` for Game Over text *not* called.                        | Edge/Error       |
| Draw Game Over (Not Eligible)     | `game_over` True, `entering_name` False, `displaying_scores` False, `score_eligible_for_save` False. `ground_image` exists. | `screen.fill`, `screen.blit` (ground), `all_sprites.draw`, `scoreboard.draw` called. Game Over, Final Score, Instructions text rendered and blitted. "Save Score?" prompt *not* rendered. | Expected         |
| Draw Game Over (Eligible)         | `game_over` True, `entering_name` False, `displaying_scores` False, `score_eligible_for_save` True. `ground_image` exists. | `screen.fill`, `screen.blit` (ground), `all_sprites.draw`, `scoreboard.draw` called. Game Over, Final Score, "Save Score? (Y/N)", Instructions text rendered and blitted.            | Expected         |
| Draw Game Over (No Ground Image)  | `game_over` True, `entering_name` False, `displaying_scores` False, `score_eligible_for_save` False. `ground_image` is None. | `screen.fill`, `pygame.draw.rect` (fallback ground), `all_sprites.draw`, `scoreboard.draw` called. Game Over, Final Score, Instructions text rendered and blitted.                    | Edge/Error       |
| State: Entering Name              | `entering_name` True. Others False.                                        | `screen.fill` called. Gameplay/Game Over drawing block skipped (`screen.blit` for ground, `all_sprites.draw`, `scoreboard.draw`, `font.render` for Game Over not called).       | State Check
#### Test Results
##### Test 01
![[Test Results - game__draw - test_01.html]]
Passed 9/9 tests
### Spawn Obstacle (`_spawn_obstacle`)
#### Component Planning
![[Game Class - Llama Game Decomposition#Spawn Obstacle (`_spawn_obstacle`)]]
#### Test Plan
### Spawn Obstacle (`_spawn_obstacle`)
#### Component Planning
![[Game Class - Llama Game Decomposition#Spawn Obstacle (`_spawn_obstacle`)]]
#### Test Plan
| Test Case                        | Input / Conditions               | Expected Output                                                                                    | Test Type  |
| :------------------------------- | :------------------------------- | :------------------------------------------------------------------------------------------------- | :--------- |
| Standard Spawn                   | Called from event handler        | New `Obstacle` instance created. Instance added to `self.all_sprites` and `self.obstacles` groups. | Expected   |
#### Test Results
![[Test Results - game__spawn_obstacle.html]]
Passed 1/1 tests

### Check Collisions (`_check_collisions`)
#### Component Planning
![[Game Class - Llama Game Decomposition#Check Collisions (`_check_collisions`)]]
#### Test Plan

| Test Case                             | Input / Conditions                                                                    | Expected Output / Checks                                                                                                                                                                                           | Test Type      |
| :------------------------------------ | :------------------------------------------------------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------- |
| No Collision                          | `pygame.sprite.spritecollide` returns empty list.                                     | `game_over` remains `False`. `_check_score_eligible` is *not* called. `pygame.time.set_timer` is *not* called with `(OBSTACLE_SPAWN_EVENT, 0)`.                                                                    | Expected       |
| Collision Occurs (Score Eligible)     | `spritecollide` returns non-empty list. Mock `_check_score_eligible` returns `True`.  | `game_over` becomes `True`. `_check_score_eligible` is called once. `score_eligible_for_save` becomes `True`. `pygame.time.set_timer` is called once with `(OBSTACLE_SPAWN_EVENT, 0)`.                             | Expected/Mock  |
| Collision Occurs (Score Not Eligible) | `spritecollide` returns non-empty list. Mock `_check_score_eligible` returns `False`. | `game_over` becomes `True`. `_check_score_eligible` is called once. `score_eligible_for_save` becomes `False`. `pygame.time.set_timer` is called once with `(OBSTACLE_SPAWN_EVENT, 0)`.                            | Expected/Mock  |
| No Obstacles Present                  | `self.obstacles` group is empty.                                                      | `pygame.sprite.spritecollide` returns empty list. `game_over` remains `False`. `_check_score_eligible` is *not* called. `pygame.time.set_timer` is *not* called with `(OBSTACLE_SPAWN_EVENT, 0)`. No error occurs. | Edge Case/Mock |
#### Test Results
##### Test 01
![[Test Results - game__check_collisions - test_01.html]]
Passed 4/4 tests

### Reset Game (`_reset_game`)
#### Component Planning
![[Game Class - Llama Game Decomposition#Reset Game (`_reset_game`)]]
#### Test Plan
| Test Case                  | Input / Conditions                                | Expected Output / Checks                                                                                                                                                                                                        | Test Type            |
| :------------------------- | :------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------- |
| Standard Reset             | Called, e.g., from Game Over state                | `game_over`, `entering_name`, `displaying_scores`, `score_eligible_for_save` are False. `start_time_ticks` is updated (mock `pygame.time.get_ticks`). `scoreboard.reset()` called. `llama.reset()` called. `player_name` is "". | State/Mock Check     |
| Obstacle Group Reset       | `obstacles` group has sprites before call         | `obstacles.empty()` is called. The `obstacles` group is empty after the call.                                                                                                                                                   | State/Mock Check     |
| All Sprites Group Reset    | `all_sprites` has llama and obstacles before call | `all_sprites.empty()` is called. `all_sprites.add(llama)` is called. After reset, `all_sprites` group contains *only* the `llama` instance.                                                                                     | State/Mock Check     |
| Obstacle Timer Restart     | Called                                            | `pygame.time.set_timer` is called once with `constants.OBSTACLE_SPAWN_EVENT` and `constants.OBSTACLE_CREATION_INTERVAL`.                                                                                                        | Mock Check           |
| Call Reset While Playing   | Called when `game_over` is False                  | Method executes without crashing. All state variables (`game_over`, `entering_name`, etc.) are reset as per "Standard Reset".                                                                                                   | Robustness/State     |
| Reset with Empty Obstacles | `obstacles` group is already empty before call    | `obstacles.empty()` is called without error. Group remains empty. Other reset actions occur normally.                                                                                                                           | Edge Case/Mock Check |
#### Test Results
##### Test 01
![[Test Results - game__reset_game - test_01.html]]
Passed 7/7 tests

### Load High Scores (`_load_high_scores`)
#### Component Planning
![[Game Class - Llama Game Decomposition#Load High Scores (`_load_high_scores`)]]
#### Test Plan
| Test Case                      | Input / Conditions                                                              | Expected Output / Checks                                                                                                               | Test Type      |
| :----------------------------- | :------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------- | :------------- |
| File Exists, Valid JSON List   | `high_scores.json` contains `[{"name":"A","score":10}]`                         | Returns the list `[{'name':'A', 'score':10}]`.                                                                                         | Expected       |
| File Exists, Correct Sorting   | `high_scores.json` contains `[{"name":"B","score":5}, {"name":"A","score":10}]` | Returns the sorted list `[{'name':'A', 'score':10}, {'name':'B', 'score':5}]`.                                                         | Expected       |
| File Exists, Missing Keys      | `high_scores.json` contains `[{"name":"A"}, {"name":"B", "score":10}]`          | Returns sorted list `[{'name':'B', 'score':10}, {'name':'A', 'score':0}]` (uses default 0 for missing score). No error.                | Expected       |
| File Exists, Truncation        | `high_scores.json` contains 12 valid score entries                              | Returns only the top 10 highest score entries, correctly sorted.                                                                       | Boundary       |
| File Exists, Empty JSON List   | `high_scores.json` contains `[]`                                                | Returns `[]`.                                                                                                                          | Expected       |
| File Does Not Exist            | No `high_scores.json` file                                                      | Returns `[]`. No error. `is_file()` check prevents attempt to open.                                                                    | Edge Case      |
| Path Is Directory              | `high_scores.json` exists but is a directory                                    | Returns `[]`. No error. `is_file()` check prevents attempt to open.                                                                    | Edge Case      |
| File Exists, Invalid JSON      | `high_scores.json` contains `"abc"`                                             | `json.JSONDecodeError` caught, returns `[]`. No crash. Print message potentially called.                                               | Error Handling |
| File Exists, Content Not List  | `high_scores.json` contains `{"name":"A","score":10}` (a dictionary)            | `AttributeError` on sort caught by generic `except`. **Raises `TypeError`** when slicing the non-list `scores` variable in `return`.   | Error Handling |
| File Exists, List w/ Non-Dicts | `high_scores.json` contains `[1, 2, 3]`                                         | `AttributeError` on `item.get` caught by generic `except`. **Raises `TypeError`** when slicing the list `scores` variable in `return`. | Error Handling |
| File Exists, Permission Error  | `high_scores.json` exists, but `open()` raises `OSError`                        | `OSError` caught by generic `except Exception`. Returns `[]`. Print message potentially called.                                        | Error Handling |
#### Test Results
##### Test 01
![[Test Results - game__load_high_scores.html]]
Passed 11/11 tests

### Save High Scores (`_save_high_scores`)
#### Component Planning
![[Game Class - Llama Game Decomposition#Save High Scores (`_save_high_scores`)]]
#### Test Plan

| Test Case            | Input / Conditions                                      | Expected Output                                                                                            | Test Type      |
| :------------------- | :------------------------------------------------------ | :--------------------------------------------------------------------------------------------------------- | :------------- |
| Save Valid List      | `self.high_scores` is `[{"name":"A","score":10}]`       | `high_scores.json` created/overwritten with the correct JSON representation of the list. No errors raised. | Expected       |
| Save Empty List      | `self.high_scores` is `[]`                              | `high_scores.json` created/overwritten with `[]`. No errors raised.                                        | Expected       |
| Invalid Data in List | `self.high_scores` contains non-JSON serializable data  | `TypeError` during `json.dump`, caught, save fails gracefully. Print message potentially called. No crash. | Error Handling |
| File Write IO Error  | `open()` raises `IOError` when opening file for writing | `IOError` caught, save fails gracefully. Print message potentially called. No crash.                       | Error Handling |
#### Test Results
##### Test 01
![[Test Results - game__save_high_scores - test_01.html]]
Passed 4/4 tests
### Check Score Eligibility (`_check_score_eligible`)
#### Component Planning
![[Game Class - Llama Game Decomposition#Check Score Eligibility (`_check_score_eligible`)]]
#### Test Plan

| Test Case                           | Input / Conditions                                              | Expected Output | Test Type  |
| :---------------------------------- | :-------------------------------------------------------------- | :-------------- | :--------- |
| List < 10, Any Score                | `len(self.high_scores)` is 5, `final_score` is 1                | True            | Expected   |
| List = 10, Score > 10th             | `len` is 10, 10th score is 50, `final_score` is 51              | True            | Expected   |
| List = 10, Score = 10th             | `len` is 10, 10th score is 50, `final_score` is 50              | False           | Boundary   |
| List = 10, Score < 10th             | `len` is 10, 10th score is 50, `final_score` is 49              | False           | Expected   |
| Empty List                          | `self.high_scores` is `[]`, `final_score` is 10                 | True            | Edge Case  |
| List = 10, Last Entry Missing Score | `len` is 10, 10th entry is `{'name':'Bad'}`, `final_score` is 1 | True            | Robustness |
#### Test Results
##### Test 01
![[Test Results - game__check_score_eligibility.html]]
Passed 7/7 tests

### Add High Score (`_add_high_score`)
#### Component Planning
![[Game Class - Llama Game Decomposition#Add High Score (`_add_high_score`)]]
#### Test Plan
### Add High Score (`_add_high_score`) - Updated

| Test Case                       | Input / Conditions                                                            | Expected Output                                                                                                                                                                         | Test Type                  |
| :------------------------------ | :---------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------- |
| Add to Empty List               | `name`="A", `score`=10, `high_scores`=`[]`                                    | `self.high_scores` becomes `[{'name':'A', 'score':10}]`. `_save_high_scores()` called.                                                                                                  | Expected                   |
| Add to Short List               | `name`="B", `score`=5, `high_scores`=`[{'name':'A', 'score':10}]`             | `self.high_scores` becomes `[{'name':'A', 'score':10}, {'name':'B', 'score':5}]` (sorted). `_save_high_scores()` called.                                                                | Expected                   |
| Add Higher Score                | `name`="C", `score`=15, `high_scores`=`[{'name':'A', 'score':10}]`            | `self.high_scores` becomes `[{'name':'C', 'score':15}, {'name':'A', 'score':10}]` (sorted). `_save_high_scores()` called.                                                               | Expected                   |
| Add to Full List (Beats 10th)   | `name`="New", `score`=55, `high_scores` has 10 items, 10th score is 50        | New score added, list sorted, list truncated back to 10 items (lowest score dropped). `_save_high_scores()` called.                                                                     | Expected                   |
| Add to Full List (Not Top 10)   | `name`="Low", `score`=45, `high_scores` has 10 items, 10th score is 50        | (Defensive) Score added, list sorted, original 10th score dropped, list truncated to 10. `_save_high_scores()` called.                                                                  | Defensive Test             |
| Add Duplicate Score             | `name`="D", `score`=10, `high_scores`=`[{'name':'A', 'score':10}]`            | New score added, list sorted (order of duplicates may vary based on sort stability), list length increases. `_save_high_scores()` called.                                               | Edge Case                  |
| Add with Name Stripping         | `name`=" E ", `score`=20, `high_scores`=`[]`                                  | `self.high_scores` becomes `[{'name':'E', 'score':20}]`. `_save_high_scores()` called.                                                                                                  | **Added**                  |
| Add Making List Size Exactly 10 | `name`="Tenth", `score`=5, `high_scores` has 9 items (highest 100, lowest 10) | New score added as 10th item, list sorted, list length becomes 10. `_save_high_scores()` called.                                                                                        | **Added Boundary**         |
| Add Non-Numeric Score           | `name`="F", `score`="abc", `high_scores`=`[]`                                 | Score added `{'name':'F', 'score':'abc'}`, list sorted (likely placing 'abc' based on type comparison rules, potentially at the end if compared with ints). `_save_high_scores` called. | **Added Robustness**       |
| Verify `_save_high_scores` Call | Any valid addition scenario                                                   | Mocked `_save_high_scores` method is called exactly once.                                                                                                                               | **Added Mock**             |
| Invalid Name Input (None)       | `name`=None, `score`=10                                                       | `AttributeError` occurs on `name.strip()`. Exception should be caught if robustness desired, otherwise test expects failure. (Current code will raise AttributeError).                  | Error Handling             |
| Add Non-Numeric Score           | `name`="F", `score`="abc", `high_scores`=`[{'name':'Num', 'score':50}]`       | `TypeError` raised during sort due to comparison between `int` and `str`. `_save_high_scores` not called.                                                                               | **Updated Error Handling** |
#### Test Results
##### Test 01
![[Test Results - game__add_high_score.html]]
Passed 10/10 tests
### Draw High Scores Screen (`_draw_high_scores_screen`)
#### Component Planning
![[Game Class - Llama Game Decomposition#Draw High Scores Screen (`_draw_high_scores_screen`)]]
#### Test Plan

| Test Case                | Input / Conditions                                                                      | Expected Output / Checks                                                                                                                                                                                                             | Test Type         |
| :----------------------- | :-------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------- |
| Draw Empty List          | `self.high_scores` is `[]`                                                              | `screen.fill` called with `constants.GREY`. Title "High Scores" rendered & blitted (correct font, color, position). "No high scores yet!" rendered & blitted (correct font, color, position). Return instruction rendered & blitted. | Edge Case         |
| Draw Partial List (<10)  | `self.high_scores` has 3 entries                                                        | `screen.fill` called with `constants.GREY`. Title rendered & blitted. 3 score entries rendered & blitted (correct rank, name, score format, font, color, positions). Return instruction rendered & blitted.                          | Expected          |
| Draw Full List (10)      | `self.high_scores` has 10 entries                                                       | `screen.fill` called with `constants.GREY`. Title rendered & blitted. 10 score entries rendered & blitted (correct rank, name, score format, font, color, positions). Return instruction rendered & blitted.                         | Expected          |
| Draw Long Names/Scores   | Entries have very long names or large scores                                            | `font.render` called with the full long name/score strings. Blitting occurs at calculated positions (visual overflow not checked). Other elements (fill, title, return) drawn correctly.                                             | Boundary          |
| Test Malformed Entry     | `self.high_scores` contains `[{"name": "A", "score": 10}, {"score": 5}, {"name": "C"}]` | `screen.fill`, Title, Return instruction drawn correctly. Entries rendered as "1. A - 10", "2. N/A - 5", "3. C - 0" using `.get()` defaults (correct font, color, positions).                                                        | Robustness/Error  |
| Verify Element Positions | Any list state (e.g., partial list)                                                     | Title, score entries, empty message (if applicable), and return instruction are blitted at positions calculated using `center=(constants.WINDOW_WIDTH // 2, Y)` where Y depends on the element and loop index.                       | Layout Check      |
| Verify Font/Color Usage  | Any list state (e.g., partial list)                                                     | Title uses `highscore_title_font`. Entries use `highscore_entry_font`. Empty message uses `instruction_font`. Return instruction uses `button_font`. All text rendered with `constants.BLACK`.                                       | Style/State Check |
#### Test Results
##### Test 01
![[Test Results - game__draw_high_scores_screen - test_01.html]]
Passed 6/6 tests

## [[Llama Class - Llama Game Decomposition]]

### Setup Player (`__init__`)
#### Component Planning
![[Llama Class - Llama Game Decomposition#Setup Player (`__init__`)]]
#### Test Plan
| Test Case                                    | Input / Conditions                 | Expected Output                                                                                                                | Test Type |
| :------------------------------------------- | :--------------------------------- | :----------------------------------------------------------------------------------------------------------------------------- | :-------- |
| Standard Initialization (Shape)              | `Llama()` called                     | `self.image` is a Surface, `self.rect` exists, `self.mask` exists, `rect.bottomleft` matches initial pos, `velocity_y` is 0. | Expected  |
| Initial Position Correct                     | `Llama()` called                     | `self.rect.bottomleft` tuple equals `(LLAMA_START_X, GROUND_HEIGHT - LLAMA_HEIGHT)`.                                            | Expected  |
| Physics Variables Initialized                | `Llama()` called                     | `self.velocity_y` is 0, `self.is_jumping` is False.                                                                          | Expected  |
| Mask Creation                                | `Llama()` called                     | `self.mask` is a valid `pygame.Mask` object derived from `self.image`.                                                         | Expected  |
#### Test Results

### Update Player State (`update`)
#### Component Planning
![[Llama Class - Llama Game Decomposition#Update Player State (`update`)]]
#### Test Plan
| Test Case                          | Input / Conditions                                | Expected Output                                                                                                                         | Test Type |
| :--------------------------------- | :------------------------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------- | :-------- |
| Apply Gravity                      | Called while `velocity_y` is 0 or positive        | `self.velocity_y` increases by `GRAVITY`. `self.rect.y` increases.                                                                      | Expected  |
| Apply Gravity (Moving Up)          | Called while `velocity_y` is negative             | `self.velocity_y` increases (becomes less negative). `self.rect.y` changes according to `velocity_y`.                                   | Expected  |
| Ground Collision Check (On Ground) | `self.rect.bottom` is exactly `GROUND_HEIGHT`     | `self.rect.bottom` remains `GROUND_HEIGHT`, `self.velocity_y` becomes 0, `self.is_jumping` becomes False.                               | Boundary  |
| Ground Collision Check (Below)     | `self.rect.bottom` > `GROUND_HEIGHT` (e.g., +1px) | `self.rect.bottom` corrected to `GROUND_HEIGHT`, `self.velocity_y` becomes 0, `self.is_jumping` becomes False.                          | Boundary  |
| No Ground Collision (Mid-Air)      | `self.rect.bottom` < `GROUND_HEIGHT`              | `self.rect.bottom` changes based on `velocity_y`. `self.velocity_y` changes due to gravity. `is_jumping` remains True (if it was True). | Expected  |
#### Test Results

### Perform Jump (`jump`)
#### Component Planning
![[Llama Class - Llama Game Decomposition#Perform Jump (`jump`)]]
#### Test Plan
| Test Case          | Input / Conditions                                    | Expected Output                                                                 | Test Type  |
| :----------------- | :---------------------------------------------------- | :------------------------------------------------------------------------------ | :--------- |
| Jump From Ground   | Called while `rect.bottom == GROUND_HEIGHT`           | `self.velocity_y` becomes `-JUMP_STRENGTH`. `self.is_jumping` becomes True.     | Expected   |
| Attempt Double Jump| Called while `rect.bottom < GROUND_HEIGHT` (in air) | No change to `self.velocity_y` or `self.is_jumping`.                            | Expected   |
| Rapid Jumps        | Called multiple times quickly while on ground         | Only the first call (when on ground) triggers the jump; subsequent calls fail. | Edge Case  |
#### Test Results

### Reset Player (`reset`)
#### Component Planning
![[Llama Class - Llama Game Decomposition#Reset Player (`reset`)]]
#### Test Plan
| Test Case          | Input / Conditions                | Expected Output                                                                 | Test Type |
| :----------------- | :-------------------------------- | :------------------------------------------------------------------------------ | :-------- |
| Reset After Jump   | Called after Llama has jumped     | `rect.bottomleft` returns to `initial_pos`. `velocity_y` becomes 0. `is_jumping` becomes False. | Expected  |
| Reset While Moving | Called while Llama is mid-air   | `rect.bottomleft` returns to `initial_pos`. `velocity_y` becomes 0. `is_jumping` becomes False. | Expected  |
| Reset From Ground  | Called while Llama is on ground | `rect.bottomleft` remains at `initial_pos`. `velocity_y` remains 0. `is_jumping` remains False. | Expected  |
#### Test Results


## [[Obstacle Class - Llama Game Decomposition]]

### Setup Obstacle (`__init__`)
#### Component Planning
![[Obstacle Class - Llama Game Decomposition#Setup Obstacle (`__init__`)]]
#### Test Plan
| Test Case                      | Input / Conditions                    | Expected Output                                                                                                                 | Test Type |
| :----------------------------- | :------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------ | :-------- |
| Standard Initialization (Shape)| `Obstacle(speed)` called                | `self.image` is a Surface (size matches a type in `OBSTACLE_TYPES`), `rect` exists, `mask` exists, `speed` attribute set.         | Expected  |
| Random Type Selection          | Called multiple times                 | Different calls result in obstacles with different dimensions corresponding to `OBSTACLE_TYPES`.                                | Expected  |
| Initial Position Off-Screen    | `Obstacle(speed)` called                | `self.rect.left` is greater than or equal to `SCREEN_WIDTH`. `self.rect.bottom` is `GROUND_HEIGHT`.                            | Expected  |
| Speed Assignment               | `Obstacle(10)` called                 | `self.speed` attribute is set to 10.                                                                                            | Expected  |
#### Test Results

### Update Obstacle State (`update`)
#### Component Planning
![[Obstacle Class - Llama Game Decomposition#Update Obstacle State (`update`)]]
#### Test Plan
| Test Case                   | Input / Conditions                          | Expected Output                                                                    | Test Type |
| :-------------------------- | :------------------------------------------ | :--------------------------------------------------------------------------------- | :-------- |
| Move Left                   | Called once                                 | `self.rect.x` decreases by `self.speed`.                                           | Expected  |
| Move Left Repeatedly        | Called multiple times                       | Obstacle moves steadily left across the screen.                                    | Expected  |
| Off-Screen Check (On Screen)| `self.rect.right` >= 0                      | Obstacle remains in its sprite groups. `kill()` is not called.                     | Expected  |
| Off-Screen Check (Boundary) | `self.rect.right` becomes < 0               | `self.kill()` is called (verified by checking sprite group membership afterwards). | Boundary  |
| Zero Speed Obstacle         | `self.speed` is 0                           | `self.rect.x` does not change. Obstacle never goes off-screen left via movement. | Edge Case |
#### Test Results


## [[Scoreboard Class - Llama Game Decomposition]]

### Setup Scoreboard (`__init__`)
#### Component Planning
![[Scoreboard Class - Llama Game Decomposition#Setup Scoreboard (`__init__`)]]
#### Test Plan
| Test Case                       | Input / Conditions                                     | Expected Output                                                                                                   | Test Type      |
| :------------------------------ | :----------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------- | :------------- |
| Standard Initialization         | `Scoreboard()` called (with default or custom args)    | `self.x`, `self.y`, `self.color` stored. `self.font` is a valid Font object. `self.score` is 0. `self.image` rendered. | Expected       |
| Initial Render                  | `Scoreboard()` called                                  | `self.image` contains rendered text "Score: 0". `self.rect` is positioned at (`self.x`, `self.y`).                  | Expected       |
| Font Loading Fails (Fallback)   | Primary font unavailable                             | `self.font` uses the fallback system font. Initialization completes without error.                                 | Error Handling |
#### Test Results

### Update Score (`update`)
#### Component Planning
![[Scoreboard Class - Llama Game Decomposition#Update Score (`update`)]]
#### Test Plan
| Test Case                 | Input / Conditions                                     | Expected Output                                                                 | Test Type  |
| :------------------------ | :----------------------------------------------------- | :------------------------------------------------------------------------------ | :--------- |
| Score Increase            | `current_time` > `game_start_time` by >= 1000ms      | `self.score` increases. `_render_text` is called, `self.image` updates.         | Expected   |
| No Score Change (< 1 sec) | `current_time` - `game_start_time` < 1000ms          | `self.score` remains 0. `_render_text` not called again. `self.image` unchanged. | Expected   |
| Multiple Second Update    | `current_time` advances by several seconds           | `self.score` reflects the correct number of whole seconds passed.               | Expected   |
| Time Reset (Conceptual)   | `game_start_time` reset during play (e.g. via reset) | Score calculation reflects time since the *new* `game_start_time`.              | Dependency |
| Large Score Values        | Game runs for a very long time                       | Score calculation handles large millisecond values correctly.                   | Boundary   |
#### Test Results

### Draw Score (`draw`)
#### Component Planning
![[Scoreboard Class - Llama Game Decomposition#Draw Score (`draw`)]]
#### Test Plan
| Test Case                   | Input / Conditions                     | Expected Output                                                                   | Test Type  |
| :-------------------------- | :------------------------------------- | :-------------------------------------------------------------------------------- | :--------- |
| Draw Current Score          | Called with valid `screen` surface   | `self.image` (containing current score text) is drawn at `self.rect` position.  | Expected   |
| Called Before First Update  | Called immediately after `__init__`    | Draws the initial "Score: 0" image.                                             | Expected   |
| Invalid Screen (Conceptual) | `screen` is None or not a Surface      | `screen.blit` raises an error (should be caught by `Game._draw` if necessary).  | Error Case |
#### Test Results

### Reset Score (`reset`)
#### Component Planning
![[Scoreboard Class - Llama Game Decomposition#Reset Score (`reset`)]]
#### Test Plan
| Test Case          | Input / Conditions            | Expected Output                                                                 | Test Type |
| :----------------- | :---------------------------- | :------------------------------------------------------------------------------ | :-------- |
| Reset Score to Zero| Called after score increased  | `self.score` becomes 0. `_render_text` called. `self.image` shows "Score: 0". | Expected  |
| Reset When Already Zero | Called when `self.score` is 0 | `self.score` remains 0. `_render_text` called. `self.image` shows "Score: 0". | Expected  |
#### Test Results