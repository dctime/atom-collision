import pygame
import materials
import random

# Initialize Pygame
pygame.init()

# Set screen size
screen_size = (800, 600)

# Create screen
screen = pygame.display.set_mode(screen_size)

# Set window title
pygame.display.set_caption("My Pygame Screen")

DOT_COLOR = (125, 125, 125)
LINE_COLOR = (120, 255, 255)
bone = materials.Bone(200, 200, 12, 9, 25, 49)
bone.print_dots()

for _ in range(30):
    bone.remove_dot(random.randint(0, len(bone.get_dots())))
    
# Game loop
running = True
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        
    for location in bone.get_dots():
        pygame.draw.circle(screen, DOT_COLOR, [location[0], location[1]], 5)


    for line in bone.get_lines():
        pygame.draw.line(screen, LINE_COLOR, line[0], line[1])

    # Update screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()