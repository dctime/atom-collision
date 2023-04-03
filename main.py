import pygame
import bone
import skin_bone
import random

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

# Make a skin bone
skin_bone_1 = skin_bone.SkinBone([(120, 120), (120, 150), (140, 170), (180, 190), (220, 190), (240, 170), (250, 140), (250, 100), (230, 80), (200, 80), (170, 100), (140, 100)])
    
# Game loop
running = True
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    pygame.draw.polygon(screen, STONE_COLOR, skin_bone_1.get_nodes(), 0)
    
    for node in skin_bone_1.get_nodes():
        pygame.draw.circle(screen, DEBUGGING_COLOR, node, 3)
        

    # Update screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()