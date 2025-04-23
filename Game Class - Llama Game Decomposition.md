---

kanban-plugin: board

---

## Setup Game (`__init__`)

- [ ] Start up Pygame systems.
- [ ] Prepare the sound system (Optional: if using sound).
- [ ] Prepare the font system for displaying text.
- [ ] Create the main game window.
- [ ] Set the title displayed on the game window.
- [ ] Create a timer to control game speed (FPS).
- [ ] Set initial game status flags (e.g., running, game over, entering name, showing scores).
- [ ] Record the time the game session started for scoring.
- [ ] Create containers (groups) to hold all game objects and obstacles.
- [ ] Create the player character (Llama).
- [ ] Add the player character to the container for all game objects.
- [ ] Create the scoreboard display.
- [ ] Load or prepare background and ground visuals.
- [ ] Define a unique signal (custom event) for when to create a new obstacle.
- [ ] Start a timer that sends the obstacle creation signal repeatedly.
- [ ] Load high scores from the storage file (handle file not found).
- [ ] Prepare variables for player name input.
- [ ] Define the area/text for the "View High Scores" button.


## Run Game Loop (`run`)

- [ ] Begin the main loop that keeps the game running.
- [ ] Handle player input and game events within the loop based on current game state.
- [ ] Update the state and position of all game objects within the loop (if applicable to state).
- [ ] Draw everything onto the screen within the loop based on current game state.
- [ ] Control the game's speed (frames per second) within the loop.
- [ ] Check if the game has ended after updating/drawing (sets game over state).
- [ ] Clean up Pygame resources after the main loop finishes.


## Handle Events (`_handle_events`)

- [ ] Check for any user actions or game events that occurred.
- [ ] Check if the user tried to close the game window (always active).
- [ ] **If game is playing:**
	- [ ] Check if it's time to create a new obstacle.
	- [ ] If it's time, trigger the obstacle creation process.
	- [ ] Check if the user pressed the jump key; if so, make the player jump.
- [ ] **If game is over (and not entering name or showing scores):**
	- [ ] Check if score is eligible for saving; if so, listen for save confirmation (Y/N).
	- [ ] If 'Y' pressed, switch state to 'entering name'.
	- [ ] Check if the user pressed the restart key; if so, restart the game.
	- [ ] Check if the user pressed the quit key; if so, exit the game loop.
	- [ ] Check if the user clicked the "View High Scores" button; if so, switch state to 'showing scores'.
- [ ] **If entering name:**
	- [ ] Listen for letter/number key presses and update the temporary player name.
	- [ ] Listen for Backspace key to delete characters from the name.
	- [ ] Listen for Enter key to finalize name, save the score, and switch back to 'game over' state.
- [ ] **If showing scores:**
	- [ ] Listen for Escape key press to switch back to 'game over' state.


## Update Game State (`_update`)

- [ ] Check if the game is in the 'playing' state.
- [ ] If playing, tell all game objects to update themselves.
- [ ] If playing, check if the player has collided with any obstacles (sets game over state).
- [ ] If playing, update the score based on elapsed time.
- [ ] (Optional) Add logic to make the game harder over time.


## Draw Frame (`_draw`)

- [ ] Clear the screen or draw the main background.
- [ ] **If game is playing:**
	- [ ] Draw the ground element.
	- [ ] Draw all the active game objects (player, obstacles).
	- [ ] Draw the current score.
- [ ] **If game is over (and not entering name or showing scores):**
	- [ ] Draw the last frame of gameplay (ground, player, obstacles).
	- [ ] Draw the "Game Over" text.
	- [ ] Draw the final score text.
	- [ ] If score is eligible, draw the "Save Score? (Y/N)" prompt.
	- [ ] Draw the "View High Scores" button.
	* [ ] Draw the "Restart/Quit" instructions.
- [ ] **If entering name:**
	* [ ] Draw the last frame of gameplay (ground, player, obstacles).
	* [ ] Draw the "Enter Name: " prompt.
	* [ ] Draw the player name text as it's being typed.
- [ ] **If showing scores:**
	- [ ] Call the specific function to draw the high scores list.
- [ ] Show the final image on the display.


## Spawn Obstacle (`_spawn_obstacle`)

- [ ] Create a new obstacle object.
- [ ] Add the new obstacle to the group of all active game objects.
- [ ] Add the new obstacle specifically to the group of obstacles.


## Check Collisions (`_check_collisions`)

- [ ] Check if the player object is touching any obstacle object.
- [ ] Use precise collision detection.
- [ ] If a collision happened, set the game state to 'game over'.
- [ ] (Optional) If a collision happened, play a sound effect.


## Reset Game (`_reset_game`)

- [ ] Set the game state back to 'playing' (or appropriate initial state).
- [ ] Reset the start time for the new game session.
- [ ] Reset the scoreboard to zero.
- [ ] Remove all obstacles currently on the screen.
- [ ] Put the player back in the starting position with reset physics.
- [ ] Reset name input variables.
- [ ] (Optional) Reset any difficulty scaling back to default.


## Load High Scores (`_load_high_scores`)

- [ ] Define the filename for high scores storage.
- [ ] Try to open and read the high scores file using JSON.
- [ ] If successful, store the loaded list (ensure sorted).
- [ ] If file not found, create an empty list for high scores.
- [ ] Handle potential errors during file reading or JSON parsing.


## Save High Scores (`_save_high_scores`)

- [ ] Define the filename for high scores storage.
- [ ] Try to open the high scores file for writing.
- [ ] Convert the current high scores list to JSON format and write it to the file.
- [ ] Handle potential errors during file writing.


## Check Score Eligibility (`_check_score_eligible`)

- [ ] Get the player's final score.
- [ ] Compare the score against the loaded high scores list.
- [ ] Return true if the list has fewer than 10 scores OR if the player's score is higher than the 10th score. Otherwise, return false.


## Add High Score (`_add_high_score`)

- [ ] Take the player's name and final score as input.
- [ ] Create a new score entry (dictionary or object).
- [ ] Add the new entry to the main high scores list.
- [ ] Sort the list by score (highest first).
- [ ] Trim the list to keep only the top 10 entries.
- [ ] Call the function to save the updated high scores list to the file.


## Draw High Scores Screen (`_draw_high_scores_screen`)

- [ ] Clear the screen or draw a suitable background.
- [ ] Draw a title like "Top 10 High Scores".
- [ ] Loop through the loaded high scores list (up to 10).
- [ ] For each entry, format and draw the rank, name, and score.
- [ ] Draw instructions like "Press ESC to return".




%% kanban:settings
```
{"kanban-plugin":"board","list-collapse":[]}
```
%%