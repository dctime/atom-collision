import pygame
import rigid_body

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
skin_bone_1 = rigid_body.Rigidbody(10)
running = True
physics_mode = False

clock = pygame.time.Clock()

while running:

    screen.fill((0, 0, 0))
    
    # Handle events
    if not physics_mode:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                skin_bone_1.add_node((x, y))
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    physics_mode = True
                if event.key == pygame.K_t:
                    skin_bone_1.fill_nodes()
                    
            if event.type == pygame.QUIT:
                running = False
            
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        skin_bone_1.move((3, -2))
        
    # Draw shapes on the screen
    if len(skin_bone_1.get_nodes()) == 1:
        pygame.draw.circle(screen, DEBUGGING_COLOR, skin_bone_1.get_nodes()[0], 3)
    elif len(skin_bone_1.get_nodes()) == 2:
        pygame.draw.line(screen, STONE_COLOR, skin_bone_1.get_nodes()[0], skin_bone_1.get_nodes()[1])
        pygame.draw.circle(screen, DEBUGGING_COLOR, skin_bone_1.get_nodes()[0], 3)
        pygame.draw.circle(screen, DEBUGGING_COLOR, skin_bone_1.get_nodes()[1], 3)
    elif len(skin_bone_1.get_nodes()) > 2:
        pygame.draw.polygon(screen, STONE_COLOR, skin_bone_1.get_nodes(), 0)
    
    for node in skin_bone_1.get_nodes():
        pygame.draw.circle(screen, DEBUGGING_COLOR, node, 3)
        

    # Update screen
    pygame.display.flip()
    clock.tick(120)

# Quit Pygame
pygame.quit()