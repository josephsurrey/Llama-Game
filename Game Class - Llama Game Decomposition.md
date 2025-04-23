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
- [ ] Set initial game status (e.g., game is running, game is not over).
- [ ] Record the time the game session started for scoring.
- [ ] Create containers (groups) to hold all game objects and obstacles.
- [ ] Create the player character (Llama).
- [ ] Add the player character to the container for all game objects.
- [ ] Create the scoreboard display.
- [ ] Load or prepare background and ground visuals.
- [ ] Define a unique signal (custom event) for when to create a new obstacle.
- [ ] Start a timer that sends the obstacle creation signal repeatedly.


## Run Game Loop (`run`)

- [ ] Begin the main loop that keeps the game running.
- [ ] Handle player input and game events within the loop.
- [ ] Update the state and position of all game objects within the loop.
- [ ] Draw everything onto the screen within the loop.
- [ ] Control the game's speed (frames per second) within the loop.
- [ ] Check if the game has ended after updating/drawing.
- [ ] If the game ended, display the game over screen.
- [ ] Clean up Pygame resources after the main loop finishes.


## Handle Events (`_handle_events`)

- [ ] Check for any user actions or game events that occurred.
- [ ] Check if the user tried to close the game window.
- [ ] Check if it's time to create a new obstacle (custom event).
- [ ] If it's time, trigger the obstacle creation process.
- [ ] Check if the user pressed a key down.
- [ ] If the jump key was pressed (and game is not over), make the player jump.
- [ ] If the restart key was pressed (and game is over), restart the game.


## Update Game State (`_update`)

- [ ] Check if the game is currently in the 'game over' state.
- [ ] If the game is still running, tell all game objects to update themselves (move, apply physics, etc.).
- [ ] If the game is still running, check if the player has collided with any obstacles.
- [ ] If the game is still running, update the score based on elapsed time.
- [ ] (Optional) Add logic to make the game harder over time (e.g., speed up obstacles).


## Draw Frame (`_draw`)

- [ ] Fill the game window with the background color.
- [ ] Draw the ground element.
- [ ] Draw all the active game objects (player, obstacles) onto the screen.
- [ ] Draw the current score onto the screen.
- [ ] Show the final image on the display.


## Spawn Obstacle (`_spawn_obstacle`)

- [ ] Create a new obstacle object.
- [ ] Add the new obstacle to the group of all active game objects.
- [ ] Add the new obstacle specifically to the group of obstacles (for collision checks).


## Check Collisions (`_check_collisions`)

- [ ] Check if the player object is touching any obstacle object.
- [ ] Use precise collision detection (checking actual shapes, not just boxes).
- [ ] If a collision happened, set the game state to 'game over'.
- [ ] (Optional) If a collision happened, play a sound effect.


## Reset Game (`_reset_game`)

- [ ] Set the game state back to 'not game over'.
- [ ] Reset the start time for the new game session.
- [ ] Reset the scoreboard to zero.
- [ ] Remove all obstacles currently on the screen.
- [ ] Put the player back in the starting position with reset physics.
- [ ] (Optional) Reset any difficulty scaling (like obstacle speed) back to default.


## Show Game Over Screen (`_show_game_over_screen`)

- [ ] Prepare the "Game Over" text to be displayed.
- [ ] Prepare the final score text to be displayed.
- [ ] Prepare the instructions text (Restart/Quit) to be displayed.
- [ ] Ensure this screen stays visible (drawing happens in `_draw`).
- [ ] (Input handling for this screen is in `_handle_events`).




%% kanban:settings
```
{"kanban-plugin":"board","list-collapse":[]}
```
%%