from block_assembly import BlockAssembly
from leaf_blocks import CoreBlock
import math

class BlockMechanism(BlockAssembly):
    def __init__(self, core_block: CoreBlock, velocity:float):
        self._velocity = velocity 
        self._rotation = 0
        
        super().__init__(core_block)

    def move(self, dir: tuple) -> None:
        delta_pos = (dir[0]*self._velocity, dir[1]*self._velocity)
        slope = dir[1]/dir[0]
        rad = math.atan(slope)

        # deg in [-90,90]
        deg = rad/math.pi*180

        # map deg to [0,360]
        if dir[0] < 0:
            deg += 180
        if deg < 0:
            deg += 360

        self.set_rotation(deg)
        for coori, bi in self.get_blocks():
            bi.move(delta_pos)
            bi.set_rotation(deg)