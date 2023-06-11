import pygame
from pygame import mixer
from leaf_blocks import CoreBlock, StoneBlock, WoodBlock
from controllable_mechanism import ControllableMechansim
import math
from game import Game
from color import Color

WIDTH = 1200
HEIGHT = 800

# Initialize Pygame
pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_x_size, screen_y_size = screen.get_size()
MID_SCREEN_POINT = (screen_x_size/2, screen_y_size/2)
UNIT_SIZE = 30
FRAMERATE = 500

# Set window title
pygame.display.set_caption("My Pygame Screen")

# set up the environment
game = Game(screen, 1/FRAMERATE, MID_SCREEN_POINT, UNIT_SIZE)
game.run()

