import skin_bone
import pygame

class Block(skin_bone.SkinBone):
    def __init__(self, center_point:tuple, hp:int, visible=True):
        super().__init__()
        self._hp = hp
        self._visible = visible
        block_size = 30
        points = []
        points.append((center_point[0]-block_size/2, center_point[1]-block_size/2))
        points.append((center_point[0]+block_size/2, center_point[1]-block_size/2))
        points.append((center_point[0]+block_size/2, center_point[1]+block_size/2))
        points.append((center_point[0]-block_size/2, center_point[1]+block_size/2))

        self.set_nodes(points)
        
    def get_hp(self):
        return self._hp

    def set_hp(self, hp):
        self._hp = hp
    
    def damage_block(self, value):
        if self._hp - value < 0:
            self._hp = 0
        else:
            self._hp -= value
        
    def heal_block(self, value):
        self._hp += value
    

    def render(self, screen, color, is_debugging:bool, debug_color=(255, 0, 0)):
        # draw ifself
        if self._visible:
            pygame.draw.polygon(screen, color, self.get_nodes(), 0)

            # Draw corners
            if is_debugging:
                for node in self.get_nodes():
                    pygame.draw.circle(screen, debug_color, node, 3)
        

    
