---

kanban-plugin: board

---

## `__init__(self)`

- [ ] Call parent constructor (`super().__init__()`)
- [ ] Load obstacle image(s) (cactus, etc.) using `pygame.image.load().convert_alpha()`
- [ ] (Optional) Randomly select which obstacle image to use
- [ ] Set `self.image` to the chosen image
- [ ] Get `self.rect` from the image (`self.image.get_rect()`)
- [ ] Define initial position (off-screen right, correct height) (`self.rect.bottomleft = (SCREEN_WIDTH, GROUND_HEIGHT)`)
- [ ] Set movement speed (`self.speed = OBSTACLE_SPEED`) - *Consider passing speed from Game class if it changes*
- [ ] Create collision mask (`self.mask = pygame.mask.from_surface(self.image)`)


## `update(self)`

- [ ] Move the obstacle left (`self.rect.x -= self.speed`)
- [ ] Check if the obstacle is completely off-screen to the left (`self.rect.right < 0`)
- [ ] If off-screen, remove the sprite from groups (`self.kill()`)




%% kanban:settings
```
{"kanban-plugin":"board","list-collapse":[]}
```
%%