import sys
import random
import json
import os
from pathlib import Path
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
        self.clock = pygame.time.Clock

        # Set initial game states
        self.running = True
        self.game_over = False
        self.entering_name = False
        self.displaying_scores = False
        self.score_eligible_for_save = False

        # Get start time
        self.start_time = pygame.time.get_ticks()

        # Create groups to hold game sprites
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()

        # Create player sprite (Llama)
        self.llama = Llama()

        # Add player sprite to all_sprites group
        self.all_sprites.add(self.llama)

        # Create scoreboard
        self.scoreboard = Scoreboard()

        # Load ground image
        try:
            ground_image = pygame.image.load(constants.GROUND_IMAGE)
            self.ground_image = ground_image.convert()
        except pygame.error as e:
            # If an error occurs when loading ground image,
            # fall back to solid colour ground
            print(
                f"Error loading ground image:"
                f" {constants.GROUND_IMAGE} - {e}"
            )
            print("Falling back to solid color ground.")
            self.ground_image = None
        except FileNotFoundError:
            # If file isn't found, fall back to solid colour ground
            print(f"Ground image file not found:" f" {constants.GROUND_IMAGE}")
            print("Falling back to solid color ground.")
            self.ground_image = None

        # Set timer for obstacle spawning
        pygame.time.set_timer(
            constants.OBSTACLE_SPAWN_EVENT,
            constants.OBSTACLE_CREATION_INTERVAL,
        )

        # Load high scores file
        self.high_score_file = "high_scores.json"

        # Load high scores
        self.high_scores = self._load_high_scores()

        # Prepare variable for player name
        self.player_name = ""

        # Define fonts
        self.score_font = pygame.font.SysFont(None, 36)
        self.game_over_font = pygame.font.SysFont(None, 74)
        self.button_font = pygame.font.SysFont(None, 24)
        self.input_font = pygame.font.SysFont(None, 36)
        self.final_score_font = pygame.font.SysFont(None, 48)

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
            if (
                not self.game_over
                and not self.entering_name
                and not self.displaying_scores
            ):
                # Check if it's time to create new obstacle
                if event.type == constants.OBSTACLE_SPAWN_EVENT:
                    self._spawn_obstacle()
                # Check if the user pressed the jump key
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        self.llama.jump()

            # Events during game over
            elif (
                self.game_over
                and not self.entering_name
                and not self.displaying_scores
            ):
                if event.type == pygame.KEYDOWN:
                    # Check if the user pressed the restart key
                    if event.key == pygame.K_r:
                        self._reset_game()
                    # Check if the user pressed the quit key
                    elif event.key == pygame.K_q:
                        self.running = False
                    # Check if score is eligible and user confirms save
                    elif (
                        event.key == pygame.K_y
                        and self.score_eligible_for_save
                    ):
                        self.entering_name = True
                        self.player_name = ""
                    # Check if score is eligible and user declines save
                    elif (
                        event.key == pygame.K_n
                        and self.score_eligible_for_save
                    ):
                        self.score_eligible_for_save = False

            # Events while entering name
            elif self.entering_name:
                if event.type == pygame.KEYDOWN:
                    # Listen for Backspace key to delete characters
                    if event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    # Listen for Enter key to save name
                    elif event.key == pygame.K_RETURN:
                        if self.player_name:
                            self._add_high_score(
                                self.player_name, self.scoreboard.score
                            )
                        self.entering_name = False
                        self.score_eligible_for_save = False
                    # Listen for key presses
                    elif event.unicode.isalnum() or event.unicode in [" "]:
                        # Limit name length
                        if len(self.player_name) < 6:
                            self.player_name += event.unicode

            # Events while displaying scores
            elif self.displaying_scores:
                if event.type == pygame.KEYDOWN:
                    # Listen for Escape key press to return
                    if event.key == pygame.K_ESCAPE:
                        self.displaying_scores = False

    def _update(self):
        # Check if the game is playing
        if (
            not self.game_over
            and not self.entering_name
            and not self.displaying_scores
        ):
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
        if not self.displaying_scores and not self.entering_name:
            # Draw the ground
            if self.ground_image:
                (
                    self.screen.blit(
                        self.ground_image,
                        (
                            0,
                            constants.WINDOW_HEIGHT
                            - self.ground_image.get_height(),
                        ),
                    )
                )
            else:
                # Draw solid ground rectangle
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
        if (
            self.game_over
            and not self.entering_name
            and not self.displaying_scores
        ):
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
            final_score_surf = self.final_score_font.render(
                f"Final Score: {self.scoreboard.score}", True, constants.BLACK
            )
            final_score_rect = final_score_surf.get_rect(
                center=(
                    constants.WINDOW_WIDTH // 2,
                    constants.WINDOW_HEIGHT // 2,
                )
            )
            self.screen.blit(final_score_surf, final_score_rect)

            # If score is eligible, draw "Save Score? (Y/N)" prompt
            if self.score_eligible_for_save:
                save_prompt_surf = self.final_score_font.render(
                    "High Score! Save? (Y/N)", True, constants.RED
                )
                save_prompt_rect = save_prompt_surf.get_rect(
                    center=(
                        constants.WINDOW_WIDTH // 2,
                        constants.WINDOW_HEIGHT // 2 + 40,
                    )
                )
                self.screen.blit(save_prompt_surf, save_prompt_rect)

            # Draw the "Restart/Quit" instructions
            instr_surf = self.final_score_font.render(
                "Press 'R' to Restart or 'Q' to Quit", True, constants.BLACK
            )
            instr_rect = instr_surf.get_rect(
                center=(
                    constants.WINDOW_WIDTH // 2,
                    constants.WINDOW_HEIGHT // 2 + 120,
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
            self.score_eligible_for_save = (
                self._check_score_eligible()
            )  # Check eligibility upon game over
            # Stop obstacle timer
            pygame.time.set_timer(constants.OBSTACLE_SPAWN_EVENT, 0)

    def _reset_game(self):
        # Set the game state back to playing
        self.game_over = False
        self.entering_name = False
        self.displaying_scores = False
        self.score_eligible_for_save = False

        # Reset the start time for the new game
        self.start_time_ticks = pygame.time.get_ticks()

        # Reset the scoreboard
        self.scoreboard.reset()

        # Remove all obstacles
        self.obstacles.empty()

        self.all_sprites.empty()
        self.all_sprites.add(self.llama)

        # Put the player back in the starting position with reset physics.
        self.llama.reset()  # Assumes llama object exists

        # Reset name input variables
        self.player_name = ""

        # Restart obstacle timer
        pygame.time.set_timer(
            constants.OBSTACLE_SPAWN_EVENT,
            constants.OBSTACLE_CREATION_INTERVAL,
        )

    def _load_high_scores(self):
        # Define the filename for high scores file
        file_path = Path(self.high_score_file)
        scores = []
        # Try to open and read the high scores file
        if file_path.is_file():
            try:
                with open(file_path, "r") as f:
                    scores = json.load(f)
                # Ensure scores are sorted upon loading
                scores.sort(
                    key=lambda item: item.get("score", 0), reverse=True
                )
            except FileNotFoundError:
                print(
                    f"High score file '{self.high_score_file}' not found."
                    f" Creating new list."
                )
            except json.JSONDecodeError:
                print(
                    f"Error decoding JSON from '{self.high_score_file}'."
                    f" Starting with empty list."
                )
            except Exception as e:
                print(f"An unexpected error occurred loading high scores: {e}")
        # Return sorted list or empty list
        return scores[:10]

    def _save_high_scores(self):
        file_path = Path(self.high_score_file)
        # Try to open the high scores file
        try:
            with open(file_path, 'w') as f:
                # Convert the current high scores list to JSON
                json.dump(self.high_scores, f, indent=4)
        except IOError as e:
            print(f"Error writing high scores to '{self.high_score_file}': {e}")
        except Exception as e:
            print(f"An unexpected error occurred saving high scores: {e}")

    def _check_score_eligible(self):
        # Get the player's final score
        final_score = self.scoreboard.score
        # Return true if the list has < than 10 scores OR score > 10th score
        if len(self.high_scores) < 10:
            return True
        # Check against 10th score (index 9) if list is full
        elif final_score > self.high_scores[-1].get('score', 0):
            return True
        return False

    def _add_high_score(self, name, score):
        pass

    def _draw_high_scores_screen(self):
        pass


class Llama(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def update(self):
        pass

    def jump(self):
        pass

    def reset(self):
        pass


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()

    def update(self):
        pass


class Scoreboard:
    def __init__(self):
        pass

    def update(self, current_time_ticks, game_start_time_ticks):
        pass

    def draw(self):
        pass

    def reset(self):
        pass


if __name__ == "__main__":
    pass
