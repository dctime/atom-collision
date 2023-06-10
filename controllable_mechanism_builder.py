from block_mechanism import BlockMechanism
from controllable_mechanism import ControllableMechansim
import pygame
import leaf_blocks as lb

class ControllableMechansimBuilder(BlockMechanism):
    def __init__(self):
        core = lb.CoreBlock((0,0))
        super().__init__(core)

        # Relative position of current block
        self._cursor = (0,0)

        # Texture of block to add
        self._block_type = "wood"

    def set_block_type(self,block_type:str)->None:
        self._block_type = block_type

    def move_cursor(self,direction:str)->None:

        pos = None
        if direction=="up":
            pos = (self._cursor[0],self._cursor[1]-1)
        elif direction=="down":
            pos = (self._cursor[0],self._cursor[1]+1)
        elif direction=="left":
            pos = (self._cursor[0]-1,self._cursor[1])
        elif direction=="right":
            pos = (self._cursor[0]+1,self._cursor[1])

        if self.get_block(pos) != None:
            self._cursor=pos

    def add_block_dir(self, direction:str)->None:
        # Set coor
        coor = list(self._cursor)
        if direction=="up":
            coor[1] -= 1
        elif direction=="down":
            coor[1] += 1
        elif direction=="left":
            coor[0] -= 1
        elif direction=="right":
            coor[0] += 1

        coor = tuple(coor)
        block = None
        if self._block_type == "wood":
            block = lb.WoodBlock(coor)
        elif self._block_type =="stone":
            block = lb.StoneBlock(coor)
        
        if block != None:
            self.add_block(block)

    def build(self) -> ControllableMechansim:
        player = ControllableMechansim(self._core)
        for ci,bi in self.get_blocks().items():
            player.add_block(bi)
        return player
    
    def render(self, screen, zero_vector:tuple, unit_size:int, center:tuple)->None:
        super().render(screen, zero_vector, unit_size)

        color = (127,0,0)
        pygame.draw.circle(screen, color, center, 2)
