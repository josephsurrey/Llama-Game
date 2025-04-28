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
        self.running

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

class Llama:
    def __init__(self):
        pass

    def update(self):
        pass

    def jump(self):
        pass

    def reset(self):
        pass

class Obstacle:
    def __init__(self):
        pass

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