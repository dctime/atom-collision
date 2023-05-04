import pygame
import block
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
blocks = set()
clock = pygame.time.Clock()

while running:

    screen.fill((0, 0, 0))
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()
            blocks.add(block.Block((x, y)))
                
        if event.type == pygame.QUIT:
            running = False
            
    # Draw shapes on the screen
    # Draw block
    for a_block in blocks:
        if isinstance(a_block, block.Block):
            a_block.render(screen, STONE_COLOR, False)
        

    # Update screen
    pygame.display.flip()
    clock.tick(120)

# Quit Pygame
pygame.quit()