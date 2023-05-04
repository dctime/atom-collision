import skin_bone
import pygame

class Block(skin_bone.SkinBone):
    
    def __init__(self, center_point:tuple):
        super().__init__()

        block_size = 30
        points = []
        points.append((center_point[0]-block_size/2, center_point[1]-block_size/2))
        points.append((center_point[0]+block_size/2, center_point[1]-block_size/2))
        points.append((center_point[0]+block_size/2, center_point[1]+block_size/2))
        points.append((center_point[0]-block_size/2, center_point[1]+block_size/2))

        self.set_nodes(points)

    def render(self, screen, color, is_debugging:bool, debug_color=(255, 0, 0)):
        # draw ifself
        pygame.draw.polygon(screen, color, self.get_nodes(), 0)

        # Draw corners
        if is_debugging:
            for node in self.get_nodes():
                pygame.draw.circle(screen, debug_color, node, 3)
        

    
