import sys
import random
import pygame

import constants


class Game:
    def __init__(self):
        # Initialise pygame
        pygame.init()
        # Initialise pygame sound
        pygame.mixer.init()
        # Initialise pygame font
        pygame.font.init()

        # Set the display mode with defined constants for width and height
        self.screen = pygame.display.set_mode(
            (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)
        )
        # Set the window caption
        pygame.display.set_caption(constants.WINDOW_TITLE)

        # Start game clock
        self.clock = pygame.time.Clock()

        # Set initial game states
        self.running = True
        self.game_over = False

        # Get start time
        self.start_time = pygame.time.get_ticks()

        # Create groups to hold game sprites
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()

        # Create player sprite (Llama)
        self.llama = Llama()
        self.llama.reset()

        # Add player sprite to all_sprites group
        self.all_sprites.add(self.llama)

        # Create scoreboard
        self.scoreboard = Scoreboard()

        # Load ground image
        self.scaled_ground_image = None
        try:
            # Load the original image
            original_ground_surf = pygame.image.load(
                constants.GROUND_IMAGE
            ).convert_alpha()

            # Get original dimensions
            original_width = original_ground_surf.get_width()
            original_height = original_ground_surf.get_height()

            # Calculate the desired height based on GROUND_Y and window height
            target_height = constants.WINDOW_HEIGHT

            # Check if original dimensions and target height are valid
            if (
                original_width > 0
                and original_height > 0
                and target_height > 0
            ):
                # Calculate the aspect ratio
                aspect_ratio = float(original_width) / float(original_height)

                # Calculate the target width
                target_width = int(aspect_ratio * target_height)

                # Ensure target_width is at least 1 pixel
                if target_width < 1:
                    target_width = 1

                # Scale the image using transform.scale
                self.scaled_ground_image = pygame.transform.scale(
                    original_ground_surf,
                    (
                        target_width,
                        target_height,
                    ),  # Scale to calculated width, target height
                )

            else:
                self.scaled_ground_image = None

        except pygame.error as e:
            print(
                f"Error loading or scaling ground image:"
                f" {constants.GROUND_IMAGE} - {e}"
            )
            self.scaled_ground_image = None
        except FileNotFoundError:
            print(f"Ground image file not found: {constants.GROUND_IMAGE}")
            self.scaled_ground_image = None

        # Set timer for obstacle spawning
        pygame.time.set_timer(
            constants.OBSTACLE_SPAWN_EVENT,
            constants.OBSTACLE_CREATION_INTERVAL,
        )

        # Define fonts
        self.score_font = pygame.font.SysFont(None, 36)
        self.game_over_font = pygame.font.SysFont(None, 74)
        self.instruction_font = pygame.font.SysFont(None, 36)
        self.button_font = pygame.font.SysFont(None, 24)

    def run(self):
        # Begin main loop
        while self.running:
            # Handle player input and game events based on current game state
            self._handle_events()
            # Update the state and position of game objects
            self._update()
            # Draw everything onto the screen
            self._draw()
            # Control the game's FPS
            # Used clock.tick_busy_loop which uses more CPU than clock.tick to
            # ensure that the FPS timing is more accurate
            self.clock.tick_busy_loop(constants.FPS)

        # Exit after main loop finishes
        pygame.quit()
        sys.exit()

    def _handle_events(self):
        # Check for any user actions or game events
        for event in pygame.event.get():
            # Check if the user tried to close the game window
            if event.type == pygame.QUIT:
                self.running = False

            # Events during gameplay
            if not self.game_over:
                # Check if it's time to create new obstacle
                if event.type == constants.OBSTACLE_SPAWN_EVENT:
                    self._spawn_obstacle()
                # Check if the user pressed the jump key
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        self.llama.jump()

            # Events during game over
            elif self.game_over:
                if event.type == pygame.KEYDOWN:
                    # Check if the user pressed the restart key
                    if event.key == pygame.K_r:
                        self._reset_game()
                    # Check if the user pressed the quit key
                    elif event.key == pygame.K_q:
                        self.running = False

    def _update(self):
        # Check if the game is playing
        if not self.game_over:
            # Updates all game objects
            self.all_sprites.update()
            # Update the score based on  time
            self.scoreboard.update(pygame.time.get_ticks(), self.start_time)
            # Check for collisions
            self._check_collisions()

    def _draw(self):
        # Draw background
        self.screen.fill(constants.WHITE)

        # Draw gameplay elements
        if self.scaled_ground_image:
            scaled_width = self.scaled_ground_image.get_width()
            draw_y = 0

            if scaled_width > 0:
                draw_x = 0
                while draw_x < constants.WINDOW_WIDTH:
                    self.screen.blit(
                        self.scaled_ground_image, (draw_x, draw_y)
                    )
                    draw_x += scaled_width
            else:
                # Fallback if scaled_width is 0
                print(
                    "Warning: Scaled ground image width is zero,"
                    " drawing fallback."
                )
                ground_rect = pygame.Rect(
                    0,
                    constants.GROUND_Y,
                    constants.WINDOW_WIDTH,
                    constants.WINDOW_HEIGHT - constants.GROUND_Y,
                )
                pygame.draw.rect(self.screen, constants.GREY, ground_rect)

        else:
            # Fallback: Draw solid ground rectangle if image failed to load
            ground_rect = pygame.Rect(
                0,
                constants.GROUND_Y,
                constants.WINDOW_WIDTH,
                constants.WINDOW_HEIGHT - constants.GROUND_Y,
            )
            pygame.draw.rect(self.screen, constants.GREY, ground_rect)

        # Draw all active game objects
        self.all_sprites.draw(self.screen)
        # Draw score
        self.scoreboard.draw(self.screen)

        # Draw game over elements
        if self.game_over:
            # Draw "Game Over" text
            go_text_surf = self.game_over_font.render(
                "GAME OVER", True, constants.BLACK
            )
            go_text_rect = go_text_surf.get_rect(
                center=(
                    constants.WINDOW_WIDTH // 2,
                    constants.WINDOW_HEIGHT // 2 - 50,
                )
            )
            self.screen.blit(go_text_surf, go_text_rect)

            # Draw the final score text
            final_score_surf = (
                self.instruction_font.render(  # Using instruction font size
                    f"Final Score: {self.scoreboard.score}",
                    True,
                    constants.BLACK,
                )
            )
            final_score_rect = final_score_surf.get_rect(
                center=(
                    constants.WINDOW_WIDTH // 2,
                    constants.WINDOW_HEIGHT // 2,
                )
            )
            self.screen.blit(final_score_surf, final_score_rect)

            # Draw the "Restart/Quit" instructions
            instr_surf = self.instruction_font.render(
                "Press 'R' to Restart or 'Q' to Quit", True, constants.BLACK
            )
            instr_rect = instr_surf.get_rect(
                center=(
                    constants.WINDOW_WIDTH // 2,
                    constants.WINDOW_HEIGHT // 2 + 80,  # Adjusted position
                )
            )
            self.screen.blit(instr_surf, instr_rect)

        # Show final image
        pygame.display.flip()

    def _spawn_obstacle(self):
        # Create a new obstacle object.
        obstacle = Obstacle(constants.OBSTACLE_INITIAL_SPEED)
        # Add the new obstacle to the group of all active game objects.
        self.all_sprites.add(obstacle)
        # Add the new obstacle specifically to the group of obstacles.
        self.obstacles.add(obstacle)

    def _check_collisions(self):
        # Check if the player object is touching an obstacle
        collisions = pygame.sprite.spritecollide(
            self.llama, self.obstacles, False, pygame.sprite.collide_mask
        )
        # If a collision happened, set game state to 'game over'
        if collisions:
            self.game_over = True
            # Stop obstacle timer
            pygame.time.set_timer(constants.OBSTACLE_SPAWN_EVENT, 0)

    def _reset_game(self):
        # Set the game state back to playing
        self.game_over = False

        # Reset the start time for the new game
        self.start_time = pygame.time.get_ticks()

        # Reset the scoreboard
        self.scoreboard.reset()

        # Remove all obstacles
        self.obstacles.empty()

        self.all_sprites.empty()
        self.all_sprites.add(self.llama)

        # Put the player back in the starting position
        self.llama.reset()

        # Restart obstacle timer
        pygame.time.set_timer(
            constants.OBSTACLE_SPAWN_EVENT,
            constants.OBSTACLE_CREATION_INTERVAL,
        )


class Llama(pygame.sprite.Sprite):
    def __init__(self):
        # Initialize base Sprite class
        super().__init__()
        # Load the player image, convert for performance
        try:
            self.image = pygame.image.load(
                constants.PLAYER_IMAGE
            ).convert_alpha()
        except Exception as e:
            # Fallback to shape if image load fails
            print(f"Error loading player image: {e}. Creating fallback shape.")
            self.image = pygame.Surface([40, 60])
            self.image.fill(constants.RED)

        # Get rectangle from image dimensions
        self.rect = self.image.get_rect()
        # Create collision mask from image alpha
        self.mask = pygame.mask.from_surface(self.image)

        # Physics variables
        self.velocity_y = 0
        self.is_jumping = False

        self.initial_pos = (
            constants.PLAYER_HORIZONTAL_POSITION,
            constants.GROUND_Y - self.rect.height,
        )

    def update(self):
        # Apply gravity to vertical velocity
        self.velocity_y += constants.GRAVITY
        # Update vertical position based on velocity
        self.rect.y += int(self.velocity_y)

        # Check for ground collision
        if self.rect.bottom >= constants.GROUND_Y:
            # Snap to ground level
            self.rect.bottom = constants.GROUND_Y
            # Stop vertical movement
            self.velocity_y = 0
            # Update jumping state
            self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            # Apply upward velocity
            self.velocity_y = constants.JUMP_SPEED
            # Set jumping state
            self.is_jumping = True

    def reset(self):
        # Reset position using the stored initial position
        self.rect.topleft = self.initial_pos
        # Reset physics variables
        self.velocity_y = 0
        self.is_jumping = False


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        # Load the obstacle image, convert for performance
        try:
            self.image = pygame.image.load(
                constants.OBSTACLE_IMAGE
            ).convert_alpha()
        except Exception as e:
            # Fallback to shape if image load fails
            print(
                f"Error loading obstacle image: {e}. Creating fallback shape."
            )
            self.image = pygame.Surface([25, 50])  # Example fallback size
            self.image.fill(constants.GREEN)  # Example fallback color

            # Get rectangle from image dimensions
        self.rect = self.image.get_rect()
        # Create collision mask from image alpha
        self.mask = pygame.mask.from_surface(self.image)

        # Set initial position off-screen right
        self.rect.bottomleft = (
            constants.WINDOW_WIDTH + random.randint(50, 200),
            constants.GROUND_Y,
        )

        # Store movement speed
        self.speed = speed

    def update(self):
        # Move obstacle left based on speed
        self.rect.x -= self.speed
        # Remove sprite if it goes completely off-screen left
        if self.rect.right < 0:
            self.kill()  # Removes sprite from all groups


class Scoreboard:
    def __init__(self, x=10, y=10, font_size=36, color=constants.BLACK):
        # Store display properties
        self.x = x
        self.y = y
        self.color = color

        # Initialize font
        self.font = pygame.font.SysFont(None, font_size)

        # Initialize score
        self.score = 0
        # Initial render of score text
        self.image = self.font.render(f"Score: {self.score}", True, self.color)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self, current_time_ticks, game_start_time_ticks):
        # Calculate score based on elapsed whole seconds
        new_score = (current_time_ticks - game_start_time_ticks) // 10
        # Only re-render if score has actually changed
        if new_score != self.score:
            self.score = new_score
            self.image = self.font.render(
                f"Score: {self.score}", True, self.color
            )
            # Update rect position in case text size  (unlikely here)
            self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        # Draw the pre-rendered score surface onto the main screen
        screen.blit(self.image, self.rect)

    def reset(self):
        # Reset score value to zero
        self.score = 0
        # Re-render the score text for "Score: 0"
        self.image = self.font.render(f"Score: {self.score}", True, self.color)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))


if __name__ == "__main__":
    # Instantiate the Game class
    game = Game()
    # Start the main game loop
    game.run()
