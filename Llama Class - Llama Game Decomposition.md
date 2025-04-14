---

kanban-plugin: board

---

## Setup Player (`__init__`)

- [ ] Initialize the base Sprite features.
- [ ] Load the player's visual appearance (image or shape).
- [ ] Set the initial visual appearance.
- [ ] Get the rectangle representing the player's position and size.
- [ ] Set the player's starting position on the screen.
- [ ] Remember the starting position for resetting later.
- [ ] Initialize physics variables (like vertical speed).
- [ ] Create a precise outline (mask) for collision detection.
- [ ] (Optional) Prepare frames for player animation.


## Update Player State (`update`)

- [ ] Apply the effect of gravity to the player's vertical speed.
- [ ] Change the player's vertical position based on its current speed.
- [ ] Check if the player has landed on or fallen below the ground.
- [ ] If on the ground, stop downward movement and reset vertical speed.
- [ ] (Optional) Change the player's visual appearance based on state (jumping/running).
- [ ] (Optional) Update the collision mask if the visual appearance changed.


## Perform Jump (`jump`)

- [ ] Check if the player is currently on the ground.
- [ ] If on the ground, give the player an upward vertical speed boost.
- [ ] (Optional) Change the player's visual appearance to jumping state.


## Reset Player (`reset`)

- [ ] Move the player back to its initial starting position.
- [ ] Reset the player's vertical speed to zero.
- [ ] (Optional) Reset the player's visual appearance to the default (running) state.




%% kanban:settings
```
{"kanban-plugin":"board","list-collapse":[]}
```
%%