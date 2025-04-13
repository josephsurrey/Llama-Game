---
kanban-plugin: board
---

## `__init__(self)`

- [ ] Call parent constructor (`super().__init__()`)
- [ ] Load llama image(s) (e.g., running, jumping) using `pygame.image.load().convert_alpha()`
- [ ] Set initial `self.image`
- [ ] Get `self.rect` from the image (`self.image.get_rect()`)
- [ ] Define initial position (`self.rect.bottomleft = (LLAMA_START_X, GROUND_HEIGHT)`)
- [ ] Store initial position for reset (`self.initial_pos = self.rect.bottomleft`)
- [ ] Initialize physics variables (`self.velocity_y = 0`)
- [ ] Create collision mask (`self.mask = pygame.mask.from_surface(self.image)`)
- [ ] (Optional) Store animation frames and index if animating


## `update(self)`

- [ ] Apply gravity to `self.velocity_y` (`self.velocity_y += GRAVITY`)
- [ ] Update `self.rect.y` based on `self.velocity_y`
- [ ] Check if llama hit or went below ground level (`self.rect.bottom >= GROUND_HEIGHT`)
- [ ] If on/below ground, set `self.rect.bottom = GROUND_HEIGHT` and `self.velocity_y = 0`
- [ ] (Optional) Update animation frame based on state (jumping/running)
- [ ] (Optional) If animation frame changed, update `self.mask`


## `jump(self)`

- [ ] Check if llama is on the ground (`self.rect.bottom == GROUND_HEIGHT`)
- [ ] If on ground, set `self.velocity_y = -JUMP_STRENGTH`
- [ ] (Optional) Change image/animation state to jumping


## `reset(self)`

- [ ] Reset position to initial position (`self.rect.bottomleft = self.initial_pos`)
- [ ] Reset velocity (`self.velocity_y = 0`)
- [ ] Reset animation state to default (running)




%% kanban:settings
```
{"kanban-plugin":"board","list-collapse":[]}
```
%%