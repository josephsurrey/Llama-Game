---

kanban-plugin: board

---

## `__init__(self)`

- [ ] Initialize Pygame (`pygame.init()`)
- [ ] Initialize Pygame mixer (`pygame.mixer.init()`) (Optional: if using sound)
- [ ] Initialize Pygame font (`pygame.font.init()`)
- [ ] Create the game window/screen (`pygame.display.set_mode`)
- [ ] Set the window caption (`pygame.display.set_caption`)
- [ ] Create a Pygame Clock (`pygame.time.Clock`)
- [ ] Initialize game state variables (`self.running = True`, `self.game_over = False`)
- [ ] Store game start time (`self.start_time = pygame.time.get_ticks()`)
- [ ] Create sprite groups (`self.all_sprites = pygame.sprite.Group()`, `self.obstacles = pygame.sprite.Group()`)
- [ ] Instantiate the Llama (`self.llama = Llama()`)
- [ ] Add Llama instance to `self.all_sprites` group
- [ ] Instantiate the Scoreboard (`self.scoreboard = Scoreboard()`)
- [ ] Load/prepare background and ground graphics/positions
- [ ] Define custom event for obstacle spawning (`OBSTACLE_SPAWN_EVENT = pygame.USEREVENT + 1`)
- [ ] Set timer for obstacle spawning (`pygame.time.set_timer(OBSTACLE_SPAWN_EVENT, obstacle_spawn_rate_ms)`)


## `run(self)`

- [ ] Start the main game loop (`while self.running:`)
- [ ] Call `self._handle_events()` inside the loop
- [ ] Call `self._update()` inside the loop
- [ ] Call `self._draw()` inside the loop
- [ ] Tick the clock (`self.clock.tick(FPS)`) inside the loop
- [ ] Check if `self.game_over` is True after update/draw
- [ ] If game over, call `self._show_game_over_screen()`
- [ ] Call `pygame.quit()` after the main loop finishes


## `_handle_events(self)`

- [ ] Start event loop (`for event in pygame.event.get():`)
- [ ] Check for `pygame.QUIT` event to set `self.running = False`
- [ ] Check for custom obstacle spawn event (`event.type == OBSTACLE_SPAWN_EVENT`)
- [ ] If spawn event, call `self._spawn_obstacle()`
- [ ] Check for keydown events (`event.type == pygame.KEYDOWN`)
- [ ] If jump key (SPACE or UP) pressed and `not self.game_over`, call `self.llama.jump()`
- [ ] If restart key ('R') pressed and `self.game_over`, call `self._reset_game()`


## `_update(self)`

- [ ] Check if `self.game_over` is False
- [ ] If game is running, update all sprites (`self.all_sprites.update()`)
- [ ] If game is running, check for collisions (`self._check_collisions()`)
- [ ] If game is running, update the scoreboard (`self.scoreboard.update(pygame.time.get_ticks(), self.start_time)`)
- [ ] (Optional) Implement logic to increase difficulty (e.g., increase obstacle speed over time)


## `_draw(self)`

- [ ] Fill the screen with background color (`self.screen.fill(COLOR)`)
- [ ] Draw the ground/static background elements
- [ ] Draw all sprites onto the screen (`self.all_sprites.draw(self.screen)`)
- [ ] Draw the scoreboard (`self.scoreboard.draw(self.screen)`)
- [ ] Update the display (`pygame.display.flip()`)


## `_spawn_obstacle(self)`

- [ ] Create a new `Obstacle()` instance
- [ ] Add the new obstacle to `self.all_sprites` group
- [ ] Add the new obstacle to `self.obstacles` group


## `_check_collisions(self)`

- [ ] Use `pygame.sprite.spritecollide()` to check for collisions between `self.llama` and `self.obstacles` group
- [ ] Use mask collision (`pygame.sprite.collide_mask`) for pixel-perfect detection
- [ ] If collision detected, set `self.game_over = True`
- [ ] (Optional) If collision, play a sound effect


## `_reset_game(self)`

- [ ] Reset game state (`self.game_over = False`)
- [ ] Reset the game start time (`self.start_time = pygame.time.get_ticks()`)
- [ ] Reset the scoreboard (`self.scoreboard.reset(self.start_time)`)
- [ ] Remove all existing obstacles from all groups (`self.obstacles.empty()`, iterate `self.all_sprites` or recreate groups)
- [ ] Reset llama's position and physics state (`self.llama.reset()`) - *Requires adding a reset method to Llama*
- [ ] (Optional) Reset obstacle speed/spawn rate if difficulty increases


## `_show_game_over_screen(self)`

- [ ] Display "Game Over" text on screen
- [ ] Display final score (possibly retrieve from `self.scoreboard`)
- [ ] Display instructions to restart or quit
- [ ] Keep updating the display (`pygame.display.flip()`)
- [ ] Loop here, waiting for events (`pygame.event.wait()` or handle events)
- [ ] Check for Quit event to set `self.running = False`
- [ ] Check for Restart key ('R') to call `self._reset_game()` and break this loop




%% kanban:settings
```
{"kanban-plugin":"board","list-collapse":[]}
```
%%