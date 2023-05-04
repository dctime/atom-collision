import pygame
import skin_bone
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

# Make a skin bone
rigidbody1 = skin_bone.SkinBone(10)
running = True
physics_mode = False

clock = pygame.time.Clock()

while running:

    screen.fill((0, 0, 0))
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()
            rigidbody1.add_node((x, y))
            
        # polygon ready
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                rigidbody1.fill_nodes()
                
        if event.type == pygame.QUIT:
            running = False
            
    # Draw shapes on the screen
    # Draw polygon
    if len(rigidbody1.get_nodes()) == 1:
        pygame.draw.circle(screen, DEBUGGING_COLOR, rigidbody1.get_nodes()[0], 3)
    elif len(rigidbody1.get_nodes()) == 2:
        pygame.draw.line(screen, STONE_COLOR, rigidbody1.get_nodes()[0], rigidbody1.get_nodes()[1])
        pygame.draw.circle(screen, DEBUGGING_COLOR, rigidbody1.get_nodes()[0], 3)
        pygame.draw.circle(screen, DEBUGGING_COLOR, rigidbody1.get_nodes()[1], 3)
    elif len(rigidbody1.get_nodes()) > 2:
        pygame.draw.polygon(screen, STONE_COLOR, rigidbody1.get_nodes(), 0)
    
    # Draw corners
    for node in rigidbody1.get_nodes():
        pygame.draw.circle(screen, DEBUGGING_COLOR, node, 3)


    
        

    # Update screen
    pygame.display.flip()
    clock.tick(120)

# Quit Pygame
pygame.quit()