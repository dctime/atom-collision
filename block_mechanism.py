from block_assembly import BlockAssembly
from leaf_blocks import CoreBlock
import math

class BlockMechanism(BlockAssembly):
    def __init__(self, core_block: CoreBlock, momentum:tuple = (0, 0)):
        self._momentum = momentum
        self._angular_momentum = 0
        self._mass = 0
        
        super().__init__(core_block)
        self.__update_mass()
    
    def add_force(self, force:tuple, location:tuple, time_between_frame:float):
        self._momentum = (self._momentum[0] + force[0]*time_between_frame, self._momentum[1] + force[1]*time_between_frame)

    def move(self) -> None:
        for coori, bi in self.get_blocks().items():
            bi.move((self._momentum[0]/self._mass, self._momentum[1]/self._mass))

    def __update_mass(self) -> None:
        total_mass = 0
        for _, block in self._blocks.items():
            total_mass += block._mass

        self._mass = total_mass

    def update(self):
        # call this in main loop
        self.move()