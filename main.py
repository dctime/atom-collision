import pygame
from block import Block
from block_assembly import BlockAssembly
import math

# Initialize Pygame
pygame.init()

# Set screen size
screen_size = (800, 600)

# Create screen
screen = pygame.display.set_mode(screen_size)

# Set window title
pygame.display.set_caption("My Pygame Screen")

DEBUGGING_COLOR = (255, 0, 0)
STONE_COLOR = (125, 125, 125)
CENTER_OF_MASS_COLOR = (255,77,255)

running = True
block_assembly = BlockAssembly()
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
    block_assembly.render(screen)

    # Update screen
    pygame.display.flip()
    clock.tick(120)

# Quit Pygame
pygame.quit()