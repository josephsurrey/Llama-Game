---

kanban-plugin: board

---

## Setup Scoreboard (`__init__`)

- [ ] Store the desired position and color for the score display.
- [ ] Load or prepare the font for rendering text.
- [ ] Set the initial score value to zero.
- [ ] Prepare variables to hold the rendered score text image and its position.
- [ ] Create the initial score text image (e.g., "Score: 0").


## Update Score (`update`)

- [ ] Calculate the current score based on how long the game has been running.
- [ ] Check if the calculated score is different from the currently displayed score.
- [ ] If the score has changed, store the new score value.
- [ ] If the score has changed, create a new text image for the updated score.
- [ ] If the score has changed, update the position rectangle for the new text image.


## Draw Score (`draw`)

- [ ] Draw the current score text image onto the main game screen.


## Reset Score (`reset`)

- [ ] Set the score value back to zero.
- [ ] Create the text image for the zero score.
- [ ] Update the position rectangle for the zero score text.




%% kanban:settings
```
{"kanban-plugin":"board","list-collapse":[]}
```
%%