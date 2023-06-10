import pygame
from pygame import mixer
from leaf_blocks import CoreBlock, StoneBlock, WoodBlock
from controllable_mechanism import ControllableMechansim
import math
from game import Game
from color import Color

# Initialize Pygame
pygame.init()

screen = pygame.display.set_mode((1200, 800))
screen_x_size, screen_y_size = screen.get_size()
MID_SCREEN_POINT = (screen_x_size/2, screen_y_size/2)
UNIT_SIZE = 30
FRAMERATE = 500

# Set window title
pygame.display.set_caption("My Pygame Screen")

# set up the environment
game = Game(screen, 1/FRAMERATE, MID_SCREEN_POINT, UNIT_SIZE)
game.set_phase("battle")
player1 = ControllableMechansim(CoreBlock((0, 0)))
player2 = ControllableMechansim(CoreBlock((0, 0)))
player1.add_block(WoodBlock((1, 0)))
player1.add_block(StoneBlock((2, 0)))
player1.add_block(StoneBlock((3, 0)))
player1.add_block(StoneBlock((4, 0)))
player1.add_block(WoodBlock((1, 1)))
player1.add_block(StoneBlock((2, 1)))
player1.add_block(StoneBlock((3, 1)))
player1.add_block(StoneBlock((4, 1)))
player2.add_block(WoodBlock((0, 1)))
player2.add_block(WoodBlock((0, 2)))
player2.add_block(WoodBlock((0, 3)))
game.add_players(player1, player2)
player1.move_to((-5, 0))
player2.move_to((5, 0))

game.run()

