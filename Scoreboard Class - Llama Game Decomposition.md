---

kanban-plugin: board

---

## `__init__(self, x=10, y=10, font_size=30, color=BLACK)`

- [ ] Store position (`self.x`, `self.y`), color (`self.color`)
- [ ] Load/create the font (`self.font = pygame.font.Font(None, font_size)`)
- [ ] Initialize score value (`self.score = 0`)
- [ ] Initialize `self.image` and `self.rect` for rendering (`self.image = None`, `self.rect = None`)
- [ ] Render initial score text surface


## `update(self, current_time, game_start_time)`

- [ ] Calculate current score based on elapsed time (`score = (current_time - game_start_time) // 1000`)
- [ ] Check if calculated score is different from stored `self.score`
- [ ] If score changed, update `self.score = score`
- [ ] If score changed, re-render the text surface (`self.image = self.font.render(...)`)
- [ ] If score changed, update the text rect (`self.rect = self.image.get_rect()`, set position `self.rect.topleft = (self.x, self.y)`)


## `draw(self, screen)`

- [ ] Blit the current score surface onto the screen (`screen.blit(self.image, self.rect)`)


## `reset(self, game_start_time)`

- [ ] Reset score value (`self.score = 0`)
- [ ] Re-render the score text surface for the score '0'
- [ ] Update the text rect




%% kanban:settings
```
{"kanban-plugin":"board","list-collapse":[]}
```
%%