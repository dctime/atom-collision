import pygame
from block import Block
from leaf_blocks import CoreBlock, StoneBlock, WoodBlock
from block_assembly import BlockAssembly
import math
from game import Game
from color import Color

# Initialize Pygame
pygame.init()

# Create screen
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((1200, 800))
screen_x_size, screen_y_size = screen.get_size()
mid_screen_point = (screen_x_size/2, screen_y_size/2)

# Set window title
pygame.display.set_caption("My Pygame Screen")

running = True

game = Game(screen)
player1 = BlockAssembly(CoreBlock((0, 0)), 0, 0)
player2 = BlockAssembly(CoreBlock((2, 2)), 0, 1)
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
    game.draw(mid_screen_point, 100)

    # Draw debugging points on the screen
    pygame.draw.circle(screen, Color.DEBUGGING_COLOR, (screen_x_size/2, screen_y_size/2), 3)
    

    # Update screen
    pygame.display.flip()
    clock.tick(120)

# Quit Pygame
pygame.quit()