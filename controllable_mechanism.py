from block_mechanism import BlockMechanism
from leaf_blocks import CoreBlock

class ControllableMechansim(BlockMechanism):
    def __init__(self, core_block: CoreBlock, momentum:tuple = (0, 0)):
        super().__init__(core_block, momentum)

    def core_move_up(self, time_between_frame:float) -> None:
        self.add_force((0, -100), self.get_coor(), time_between_frame)

    def core_move_down(self, time_between_frame:float) -> None:
        self.add_force((0, 100), self.get_coor(), time_between_frame)

    def core_move_left(self, time_between_frame:float) -> None:
        self.add_force((-100, 0), self.get_coor(), time_between_frame)

    def core_move_right(self, time_between_frame:float) -> None:
        self.add_force((100, 0), self.get_coor(), time_between_frame) 
