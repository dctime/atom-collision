import pygame
from leaf_blocks import CoreBlock, StoneBlock, WoodBlock
from block_mechanism import BlockMechanism
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
game = Game(screen)
player1 = BlockMechanism(CoreBlock((0, 0)))
player2 = BlockMechanism(CoreBlock((0, 0)))
player1.add_block(WoodBlock((1, 0)))
player1.add_block(StoneBlock((2, 0)))
player1.add_block(StoneBlock((3, 0)))
player1.add_block(StoneBlock((4, 0)))
player2.add_block(WoodBlock((0, 1)))
player2.add_block(StoneBlock((0, 2)))
player2.add_block(StoneBlock((0, 3)))
game.add_players(player1, player2)
player1.move_to((-5, 0))
player2.move_to((5, 0))

game.run(MID_SCREEN_POINT, UNIT_SIZE, 1/FRAMERATE)

