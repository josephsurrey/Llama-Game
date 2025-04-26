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
# Project Development
## constants.py
#### Component Planning
![[constants.py - Llama Game Decomposition#Define Constants]]
# Test Plan: constants.py

| Test Case / Constant Name          | Verification Focus        | Expected Type / Value / Constraint                                                                             | Test Type     |
| :--------------------------------- | :------------------------ | :------------------------------------------------------------------------------------------------------------- | :------------ |
| `WINDOW_WIDTH` / `WINDOW_HEIGHT`   | Definition & Value        | Defined as positive integers. Plausible dimensions for a game window.                                          | Value Check   |
| `FPS`                              | Definition & Value        | Defined as a positive integer. Represents a reasonable frame rate.                                             | Value Check   |
| `GROUND_Y`                         | Definition & Value        | Defined as an integer. Value should be less than `WINDOW_HEIGHT`, representing a Y-coordinate on the screen.   | Value Check   |
| `GRAVITY`                          | Definition & Value        | Defined as a number (float or int). Represents acceleration.                                                   | Value Check   |
| `JUMP_SPEED`                       | Definition & Value        | Defined as a number (float or int). Represents initial jump velocity (likely negative for upward movement).    | Value Check   |
| `PLAYER_HORIZONTAL_POSITION`       | Definition & Value        | Defined as an integer. Represents starting X position within the window width.                                 | Value Check   |
| `OBSTACLE_INITIAL_SPEED`           | Definition & Value        | Defined as a number (float or int). Represents initial obstacle speed (likely positive for leftward movement). | Value Check   |
| `OBSTACLE_CREATION_INTERVAL`       | Definition & Value        | Defined as a positive integer. Represents milliseconds between spawns.                                         | Value Check   |
| Color Tuples (e.g., `WHITE`)       | Definition & Type & Value | Defined as 3-element tuples of integers. Each element between 0-255.                                           | Type & Value  |
| Image Paths (e.g., `PLAYER_IMAGE`) | Definition & Type & Value | Defined as strings. Represent file paths (validity depends on file system).                                    | Type & Value  |
| Constant Accessibility             | Importability             | Other modules can successfully import and use these constants without error.                                   | Accessibility |
| Type Consistency                   | Data Types                | All constants have the expected Python data types (int, float, tuple, str).                                    | Type Check    |
#### Test Results
##### Test 01
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
##### Test 02
![[Test Results - constants.py - test_02.html]]
The program passed 18/18 tests successfully after making the changes from [[#Test 01]].
## [[Game Class - Llama Game Decomposition]]

### Setup Game (`__init__`)
#### Component Planning
![[Game Class - Llama Game Decomposition#Setup Game (`__init__`)]]
#### Test Plan
| Test Case                                 | Input / Conditions                                       | Expected Output                                                                                                                                                                                                                                   | Test Type         |
| :---------------------------------------- | :------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :---------------- |
| Standard Initialization                   | `Game()` called                                          | Pygame initialized, window created, caption set, clock exists, state flags (`running`, `game_over`, etc.) set to defaults, sprite groups are empty initially, Llama & Scoreboard objects created, High scores list attempted load, Timer started. | Expected          |
| High Score File Exists                    | `high_scores.json` exists and contains valid JSON list   | `self.high_scores` populated with data from file.                                                                                                                                                                                                 | Expected          |
| High Score File Does Not Exist            | `high_scores.json` is missing                            | `self.high_scores` is initialized as an empty list. No error/crash.                                                                                                                                                                               | Edge Case         |
| High Score File Corrupted                 | `high_scores.json` exists but contains invalid JSON      | Error handled gracefully (e.g., exception caught), `self.high_scores` initialized as an empty list. No crash.                                                                                                                                     | Error Handling    |
| Missing Font Files (Fallback test)        | Default system font specified in `Scoreboard` is missing | Scoreboard initializes using the fallback system font without crashing.                                                                                                                                                                           | Error Handling    |
| Pygame Initialization Fails (Conceptual)  | e.g., Display system unavailable                         | Program exits gracefully with an error message (or handles failure appropriately based on `pygame.init()` return values).                                                                                                                         | Error Handling    |
| Timer Setup Fails (Conceptual - Unlikely) | `pygame.time.set_timer` fails                            | Program potentially logs error or exits, depending on error handling strategy.                                                                                                                                                                    | Error Handling    |
#### Test Results

### Run Game Loop (`run`)
#### Component Planning
![[Game Class - Llama Game Decomposition#Run Game Loop (`run`)]]
#### Test Plan
| Test Case                      | Input / Conditions                              | Expected Output                                                                                                                            | Test Type  |
| :----------------------------- | :---------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------- | :--------- |
| Normal Execution               | Game started, `self.running` is True          | Loop continues executing, calling `_handle_events`, `_update`, `_draw`, `clock.tick` repeatedly.                                           | Expected   |
| Game Quit via Event            | `_handle_events` sets `self.running` to False | Loop terminates after the current iteration completes. `pygame.quit()` is called.                                                        | Expected   |
| Game Over State Reached        | `_update` sets `self.game_over` to True       | Loop continues running, but `_update` logic might be skipped. `_draw` calls `_draw_high_scores_screen` (or relevant game over drawing logic). | Expected   |
| Clock Ticking                  | Loop running                                    | Game runs at approximately the target FPS (visual check, or timing check).                                                                 | Expected   |
| Exception within Loop (e.g., `_update`) | An uncaught exception occurs in a sub-method | Loop terminates abruptly, program likely crashes without calling `pygame.quit()` unless wrapped in a global try-except (not typical). | Error Case |
#### Test Results

### Handle Events (`_handle_events`)
#### Component Planning
![[Game Class - Llama Game Decomposition#Handle Events (`_handle_events`)]]
#### Test Plan
| Test Case                                   | Input / Conditions                                                  | Expected Output                                                                                                                    | Test Type        |
| :------------------------------------------ | :------------------------------------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------- | :--------------- |
| Quit Event (Window Close)                   | User clicks window 'X' button                                       | `pygame.QUIT` event detected, `self.running` set to False.                                                                         | Expected         |
| Jump Key Press (Playing)                    | SPACE or UP pressed while `game_over` is False                      | `llama.jump()` method is called.                                                                                                   | Expected         |
| Jump Key Press (Game Over)                  | SPACE or UP pressed while `game_over` is True                       | No action (jump not called).                                                                                                       | Expected         |
| Restart Key Press (Game Over)               | 'R' pressed while `game_over` is True                               | `_reset_game()` method is called.                                                                                                  | Expected         |
| Restart Key Press (Playing)                 | 'R' pressed while `game_over` is False                              | No action.                                                                                                                         | Expected         |
| Quit Key Press (Game Over)                  | 'Q' pressed while `game_over` is True                               | `self.running` set to False.                                                                                                       | Expected         |
| Quit Key Press (Playing)                    | 'Q' pressed while `game_over` is False                              | No action.                                                                                                                         | Expected         |
| Obstacle Spawn Event                        | `pygame.USEREVENT + 1` occurs while `game_over` is False            | `_spawn_obstacle()` method is called.                                                                                              | Expected         |
| Obstacle Spawn Event (Game Over)            | `pygame.USEREVENT + 1` occurs while `game_over` is True             | No action (`_spawn_obstacle` not called).                                                                                          | Expected         |
| Save Score Confirm (Y - Eligible)           | 'Y' pressed while `game_over` is True & score is eligible           | Game state changes to `entering_name`.                                                                                             | Expected         |
| Save Score Decline (N - Eligible)           | 'N' pressed while `game_over` is True & score is eligible           | Game state remains `game_over`, no name entry initiated.                                                                         | Expected         |
| Save Score Keys (Not Eligible)              | 'Y' or 'N' pressed while `game_over` is True & score not eligible | No action.                                                                                                                         | Expected         |
| View Scores Click (Game Over)               | Mouse click within "View High Scores" button rect                   | Game state changes to `showing_scores`.                                                                                            | Expected         |
| Mouse Click Elsewhere (Game Over)           | Mouse click outside button rect                                     | No action.                                                                                                                         | Expected         |
| Enter Name Keys (Entering Name State)       | Alphanumeric keys pressed                                           | Characters appended to temporary name string.                                                                                      | Expected         |
| Backspace Key (Entering Name State)         | BACKSPACE pressed                                                   | Last character removed from temporary name string.                                                                                 | Expected         |
| Enter Key (Entering Name State)             | ENTER pressed                                                       | `_add_high_score()` called with name/score, state changes back to `game_over`, high scores saved.                                 | Expected         |
| Escape Key (Showing Scores State)           | ESC pressed                                                         | Game state changes back to `game_over`.                                                                                            | Expected         |
| Unexpected Key Press (Playing)              | Any key other than SPACE/UP pressed                                 | No action.                                                                                                                         | Unexpected Input |
| Unexpected Key Press (Game Over - Standard) | Any key other than R, Q, Y, N pressed                               | No action.                                                                                                                         | Unexpected Input |
| Unexpected Key Press (Entering Name)        | Any key other than alphanum, backspace, enter pressed               | No action / character not added.                                                                                                   | Unexpected Input |
| Unexpected Key Press (Showing Scores)       | Any key other than ESC pressed                                      | No action.                                                                                                                         | Unexpected Input |
| Multiple Events Per Frame                   | e.g., Key press and Obstacle Spawn event in same frame              | Both events processed correctly in sequence within the loop iteration.                                                             | Edge Case        |
#### Test Results

### Update Game State (`_update`)
#### Component Planning
![[Game Class - Llama Game Decomposition#Update Game State (`_update`)]]
#### Test Plan
| Test Case                       | Input / Conditions                       | Expected Output                                                                                             | Test Type  |
| :------------------------------ | :--------------------------------------- | :---------------------------------------------------------------------------------------------------------- | :--------- |
| Update While Playing            | `game_over` is False                     | `all_sprites.update()`, `scoreboard.update()`, `_check_collisions()` are called.                            | Expected   |
| Update While Game Over          | `game_over` is True                      | Methods inside the `if not self.game_over:` block are skipped (sprites don't update, score doesn't increase). | Expected   |
| Collision Detected During Update| `_check_collisions()` returns collision  | `self.game_over` is set to True within the same update cycle.                                               | Expected   |
| Score Increments Over Time      | Multiple `_update` calls while playing | Scoreboard value increases monotonically based on elapsed time.                                             | Expected   |
| Difficulty Increase (Optional)  | Game played for extended period        | Obstacle speed (or other difficulty factor) increases gradually as implemented.                             | Expected   |
| No Sprites Present              | `all_sprites` group is empty             | `all_sprites.update()` runs without error.                                                                  | Edge Case  |
#### Test Results

### Draw Frame (`_draw`)
#### Component Planning
![[Game Class - Llama Game Decomposition#Draw Frame (`_draw`)]]
#### Test Plan
| Test Case                    | Input / Conditions                             | Expected Output                                                                                              | Test Type  |
| :--------------------------- | :--------------------------------------------- | :----------------------------------------------------------------------------------------------------------- | :--------- |
| Draw While Playing           | `game_over` is False, not entering/showing | Background, Ground, Sprites (`all_sprites.draw`), Scoreboard are drawn.                                      | Expected   |
| Draw While Game Over         | `game_over` is True, not entering/showing    | Background, Ground, Sprites (static), Scoreboard, Game Over text, Final Score, Instructions, View Scores button drawn. | Expected   |
| Draw Game Over (Eligible)    | `game_over` is True, score eligible          | Includes the "Save Score? (Y/N)" prompt in addition to standard Game Over elements.                           | Expected   |
| Draw Entering Name           | State is `entering_name`                       | Background, Static Sprites, "Enter Name:" prompt, current typed name are drawn.                              | Expected   |
| Draw Showing Scores          | State is `showing_scores`                      | Calls `_draw_high_scores_screen()` method.                                                                   | Expected   |
| Screen Update Called         | After all drawing elements                   | `pygame.display.flip()` is called to make drawing visible.                                                   | Expected   |
| Empty Sprite Group           | `all_sprites` is empty                       | `all_sprites.draw()` executes without error.                                                                 | Edge Case  |
| Font Rendering Fails (Conceptual) | Font object is None or invalid               | Relevant `font.render()` call raises an exception (should be handled, or will crash).                         | Error Case |
#### Test Results

### Spawn Obstacle (`_spawn_obstacle`)
#### Component Planning
![[Game Class - Llama Game Decomposition#Spawn Obstacle (`_spawn_obstacle`)]]
#### Test Plan
| Test Case                        | Input / Conditions               | Expected Output                                                                                    | Test Type  |
| :------------------------------- | :------------------------------- | :------------------------------------------------------------------------------------------------- | :--------- |
| Standard Spawn                   | Called from event handler        | New `Obstacle` instance created. Instance added to `self.all_sprites` and `self.obstacles` groups. | Expected   |
#### Test Results

### Check Collisions (`_check_collisions`)
#### Component Planning
![[Game Class - Llama Game Decomposition#Check Collisions (`_check_collisions`)]]
#### Test Plan
| Test Case                    | Input / Conditions                             | Expected Output                                                                                               | Test Type  |
| :--------------------------- | :--------------------------------------------- | :------------------------------------------------------------------------------------------------------------ | :--------- |
| No Collision                 | Llama sprite does not overlap obstacle sprites | `pygame.sprite.spritecollide` returns empty list. `self.game_over` remains False.                             | Expected   |
| Collision Occurs             | Llama sprite mask overlaps an obstacle mask    | `pygame.sprite.spritecollide` returns list containing the collided obstacle(s). `self.game_over` set to True. | Expected   |
| Multiple Obstacles Collision | Llama overlaps two obstacles simultaneously    | Collision detected, `self.game_over` set to True. (Result is same as single collision).                       | Edge Case  |
| No Obstacles Present         | `self.obstacles` group is empty                | `pygame.sprite.spritecollide` returns empty list. No error.                                                   | Edge Case  |
#### Test Results

### Reset Game (`_reset_game`)
#### Component Planning
![[Game Class - Llama Game Decomposition#Reset Game (`_reset_game`)]]
#### Test Plan
| Test Case                      | Input / Conditions                 | Expected Output                                                                                                      | Test Type  |
| :----------------------------- | :--------------------------------- | :------------------------------------------------------------------------------------------------------------------- | :--------- |
| Standard Reset                 | Called from Game Over state      | `self.game_over` is False, `start_time_ticks` reset, `scoreboard.reset()` called, `llama.reset()` called, obstacles group emptied, name input variables cleared. | Expected   |
| Reset with Existing Obstacles  | Obstacles exist on screen        | All obstacle sprites removed from `all_sprites` and `obstacles` groups.                                              | Expected   |
| Reset with Difficulty Increase | Obstacle speed was increased     | Obstacle speed (or other factors) reset to default values.                                                           | Expected   |
| Call Reset While Playing       | Called unexpectedly (debug?)     | Game state resets, potentially disrupting play but should not crash.                                                 | Unexpected |
#### Test Results

### Load High Scores (`_load_high_scores`)
#### Component Planning
![[Game Class - Llama Game Decomposition#Load High Scores (`_load_high_scores`)]]
#### Test Plan
| Test Case                      | Input / Conditions                                      | Expected Output                                                                                                                | Test Type      |
| :----------------------------- | :------------------------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------- | :------------- |
| File Exists, Valid JSON List   | `high_scores.json` contains `[{"name":"A","score":10}]` | Method returns the list `[{'name':'A', 'score':10}]`. `self.high_scores` (in `__init__`) stores this list.                     | Expected       |
| File Exists, Empty JSON List   | `high_scores.json` contains `[]`                        | Method returns `[]`. `self.high_scores` stores `[]`.                                                                           | Expected       |
| File Does Not Exist            | No `high_scores.json` file                              | `FileNotFoundError` caught, method returns `[]`. `self.high_scores` stores `[]`. No crash.                                     | Edge Case      |
| File Exists, Invalid JSON      | `high_scores.json` contains `"abc"`                     | `json.JSONDecodeError` caught, method returns `[]`. `self.high_scores` stores `[]`. No crash. Log message potentially printed. | Error Handling |
| File Exists, Not a List        | `high_scores.json` contains `{"name":"A","score":10}`   | Error during processing (e.g., `TypeError` if expecting list methods), handled gracefully, method returns `[]`.                | Error Handling |
| File Contains Non-Dict Items   | `high_scores.json` contains `[1, 2, 3]`                 | Potential error during sorting/accessing `['score']`, handled gracefully, method returns `[]` or partially processed list.     | Error Handling |
| File Contains Missing Keys     | `high_scores.json` contains `[{"name":"A"}]`            | Potential `KeyError` during sorting, handled gracefully, method returns `[]` or partially processed list.                      | Error Handling |
#### Test Results

### Save High Scores (`_save_high_scores`)
#### Component Planning
![[Game Class - Llama Game Decomposition#Save High Scores (`_save_high_scores`)]]
#### Test Plan
| Test Case            | Input / Conditions                                     | Expected Output                                                                                            | Test Type      |
| :------------------- | :----------------------------------------------------- | :--------------------------------------------------------------------------------------------------------- | :------------- |
| Save Valid List      | `self.high_scores` is `[{"name":"A","score":10}]`      | `high_scores.json` created/overwritten with the correct JSON representation of the list. No errors raised. | Expected       |
| Save Empty List      | `self.high_scores` is `[]`                             | `high_scores.json` created/overwritten with `[]`. No errors raised.                                        | Expected       |
| Invalid Data in List | `self.high_scores` contains non-JSON serializable data | `TypeError` during `json.dump`, caught, save fails gracefully. Log message potentially printed. No crash.  | Error Handling |
#### Test Results

### Check Score Eligibility (`_check_score_eligible`)
#### Component Planning
![[Game Class - Llama Game Decomposition#Check Score Eligibility (`_check_score_eligible`)]]
#### Test Plan
| Test Case                    | Input / Conditions                                                   | Expected Output                                                                                    | Test Type  |
| :--------------------------- | :------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------- | :--------- |
| List < 10, Any Score         | `len(self.high_scores)` is 5, `final_score` is 1                     | True                                                                                               | Expected   |
| List = 10, Score > 10th      | `len` is 10, 10th score is 50, `final_score` is 51                   | True                                                                                               | Expected   |
| List = 10, Score = 10th      | `len` is 10, 10th score is 50, `final_score` is 50                   | False                                                                                              | Boundary   |
| List = 10, Score < 10th      | `len` is 10, 10th score is 50, `final_score` is 49                   | False                                                                                              | Expected   |
| Empty List                   | `self.high_scores` is `[]`, `final_score` is 10                      | True                                                                                               | Edge Case  |
#### Test Results

### Add High Score (`_add_high_score`)
#### Component Planning
![[Game Class - Llama Game Decomposition#Add High Score (`_add_high_score`)]]
#### Test Plan
| Test Case                  | Input / Conditions                                                       | Expected Output                                                                                                                                  | Test Type        |
| :------------------------- | :----------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------- | :--------------- |
| Add to Empty List          | `name`="A", `score`=10, `high_scores`=`[]`                             | `self.high_scores` becomes `[{'name':'A', 'score':10}]`. `_save_high_scores()` called.                                                           | Expected         |
| Add to Short List          | `name`="B", `score`=5, `high_scores`=`[{'name':'A', 'score':10}]`       | `self.high_scores` becomes `[{'name':'A', 'score':10}, {'name':'B', 'score':5}]` (sorted). `_save_high_scores()` called.                         | Expected         |
| Add Higher Score           | `name`="C", `score`=15, `high_scores`=`[{'name':'A', 'score':10}]`       | `self.high_scores` becomes `[{'name':'C', 'score':15}, {'name':'A', 'score':10}]` (sorted). `_save_high_scores()` called.                         | Expected         |
| Add to Full List (Beats 10th) | `name`="New", `score`=55, `high_scores` has 10 items, 10th score is 50 | New score added, list sorted, list truncated back to 10 items (lowest score dropped). `_save_high_scores()` called.                              | Expected         |
| Add to Full List (Not Top 10)| `name`="Low", `score`=45, `high_scores` has 10 items, 10th score is 50 | (This function shouldn't be called if not eligible, but if called) Score added, list sorted, original 10th score dropped, list truncated to 10. | Defensive Test   |
| Add Duplicate Score        | `name`="D", `score`=10, `high_scores`=`[{'name':'A', 'score':10}]`       | New score added, order might depend on sort stability, list length increases by 1. `_save_high_scores()` called.                                | Edge Case        |
| Invalid Name/Score Input | `name`=None, `score`="abc"                                             | Potential `TypeError` during sorting or dictionary creation. Should ideally validate input before calling.                                     | Error Handling   |
#### Test Results

### Draw High Scores Screen (`_draw_high_scores_screen`)
#### Component Planning
![[Game Class - Llama Game Decomposition#Draw High Scores Screen (`_draw_high_scores_screen`)]]
#### Test Plan
| Test Case                         | Input / Conditions                           | Expected Output                                                                                                                       | Test Type  |
| :-------------------------------- | :------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------ | :--------- |
| Draw Full List (10)               | `self.high_scores` has 10 entries            | Screen cleared/background drawn. Title drawn. 10 score entries drawn (Rank, Name, Score). Return instruction drawn.                   | Expected   |
| Draw Partial List (<10)           | `self.high_scores` has 3 entries             | Screen cleared/background drawn. Title drawn. 3 score entries drawn correctly ranked. Return instruction drawn.                       | Expected   |
| Draw Empty List                   | `self.high_scores` is `[]`                   | Screen cleared/background drawn. Title drawn. No score entries drawn (or a "No scores yet" message). Return instruction drawn.        | Edge Case  |
| Long Names/Scores                 | Entries have very long names or large scores | Text may overflow expected area if not handled (e.g., by truncating or adjusting font size). Test appearance with plausible maximums. | Boundary   |
#### Test Results

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