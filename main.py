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
            (constants.WINDOW_WIDTH,constants.WINDOW_HEIGHT))
        # Set the window caption
        pygame.display.set_caption(constants.WINDOW_TITLE)

        # Start game clock
        self.Clock = pygame.time.Clock

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
                f" {constants.GROUND_IMAGE} - {e}")
            print("Falling back to solid color ground.")
            self.background_image = None
        except FileNotFoundError:
            # If file isn't found, fall back to solid colour ground
            print(
                f"Ground image file not found:"
                f" {constants.GROUND_IMAGE}")
            print("Falling back to solid color ground.")
            self.background_image = None

        # Set timer for obstacle spawning
        pygame.time.set_timer(constants.OBSTACLE_SPAWN_EVENT,
                              constants.OBSTACLE_CREATION_INTERVAL)

        # Load high scores
        self._load_high_scores()

        # Prepare variable for player name
        self.player_name = ""

        # Define fonts
        self.score_font = pygame.font.SysFont(None, 36)
        self.game_over_font = pygame.font.SysFont(None, 74)
        self.button_font = pygame.font.SysFont(None, 24)
        self.input_font = pygame.font.SysFont(None, 36)

    def run(self):
        pass

    def _handle_events(self):
        pass

    def _update(self):
        pass

    def _draw(self):
        pass

    def _spawn_obstacle(self):
        pass

    def _check_collisions(self):
        pass

    def _reset_game(self):
        pass

    def _load_high_scores(self):
        pass

    def _save_high_scores(self):
        pass

    def _check_score_eligible(self):
        pass

    def _add_high_score(self):
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
    def __init__(self):
        super().__init__()

    def update(self):
        pass

class Scoreboard:
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def reset(self):
        pass

if __name__ == "__main__":
    pass