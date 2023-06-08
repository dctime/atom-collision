import pygame
from block import Block
from leaf_blocks import CoreBlock, StoneBlock, WoodBlock
from block_assembly import BlockAssembly
from block_mechanism import BlockMechanism
import math
from game import Game
from color import Color

def change_normalized_into_real(zero_vector, unit_size, target_vector):
    return (target_vector[0]*unit_size+zero_vector[0], target_vector[1]*unit_size+zero_vector[1])

# Initialize Pygame
pygame.init()

# Create screen
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((1200, 800))
screen_x_size, screen_y_size = screen.get_size()
MID_SCREEN_POINT = (screen_x_size/2, screen_y_size/2)
UNIT_SIZE = 30
FRAMERATE = 500

# Set window title
pygame.display.set_caption("My Pygame Screen")

running = True

game = Game(screen)
player1 = BlockMechanism(CoreBlock((0, 0)))
player2 = BlockMechanism(CoreBlock((2, 2)))
player1.add_block(StoneBlock((0, 1)))
player1.add_block(WoodBlock((0, 2)))
player1.add_block(StoneBlock((1, 2)))
game.add_players(player1, player2)

clock = pygame.time.Clock()

while running:

    screen.fill((0, 0, 0))
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()
            print("Nothing happens")
                
        if event.type == pygame.QUIT:
            running = False
            
    # Draw shapes on the screen
    game.run(MID_SCREEN_POINT, UNIT_SIZE, 1/FRAMERATE)
    player1.add_force((10, 0), (0, 5), 1/FRAMERATE)

    # Draw debugging points on the screen
    pygame.draw.circle(screen, Color.MID_SCREEN_COLOR, MID_SCREEN_POINT, 3)

    # Draw center of mass of player1
    pygame.draw.circle(screen, Color.CENTER_OF_MASS_COLOR, change_normalized_into_real(MID_SCREEN_POINT, UNIT_SIZE, player1.get_center_of_mass_coor()), 3)
    # Draw center of mass of player2
    pygame.draw.circle(screen, Color.CENTER_OF_MASS_COLOR, change_normalized_into_real(MID_SCREEN_POINT, UNIT_SIZE, player2.get_center_of_mass_coor()), 3)
    # draw every blocks coor
    for _, block in player1.get_blocks().items():
        pygame.draw.circle(screen, Color.BLOCK_COOR_COLOR, change_normalized_into_real(MID_SCREEN_POINT, UNIT_SIZE, block.get_coor()), 2)

    # Update screen
    pygame.display.flip()
    clock.tick(FRAMERATE) # it doesnt not become super fast idk why

# Quit Pygame
pygame.quit()