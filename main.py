import pygame
from block import Block
from leaf_blocks import CoreBlock, StoneBlock
from block_assembly import BlockAssembly
import math
from game import Game

# Initialize Pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Set window title
pygame.display.set_caption("My Pygame Screen")

DEBUGGING_COLOR = (255, 0, 0)

running = True


game = Game(screen)
player1 = BlockAssembly(CoreBlock((100, 100)), 0, 0)
player2 = BlockAssembly(CoreBlock((200, 100)), 0, 1)
player1.add_block(StoneBlock((100, 101)))
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
    game.draw()

    # Update screen
    pygame.display.flip()
    clock.tick(120)

# Quit Pygame
pygame.quit()