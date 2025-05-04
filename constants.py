import pygame

WINDOW_WIDTH = 900  # Width of the game window
WINDOW_HEIGHT = 400  # Height of the game window
WINDOW_TITLE = "Llama Game - Joseph Surrey"  # Title of game window
FPS = 30  # Frames per second

# Custom pygame event
OBSTACLE_SPAWN_EVENT = pygame.USEREVENT + 1

GROUND_Y = 235  # Y position of the ground

GRAVITY = 1.5  # Acceleration due to gravity
JUMP_SPEED = -20  # Speed at which the player jumps

PLAYER_HORIZONTAL_POSITION = 100  # Starting horizontal position of the player

OBSTACLE_INITIAL_SPEED = 8  # Initial speed of obstacles
OBSTACLE_CREATION_INTERVAL = 2000  # Time interval between obstacle creations
# (in milliseconds)

# Standard colour values
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Image file locations
PLAYER_IMAGE = "images/Llama.png"
OBSTACLE_IMAGE = "images/cactus.png"
GROUND_IMAGE = "images/ground.png"
GAME_ICON = "images/llama_icon.png"
