from block_mechanism import BlockMechanism
from leaf_blocks import CoreBlock

class BlockMechanismWithCollision(BlockMechanism):
    def __init__(self, core_block: CoreBlock, momentum:tuple = (0, 0)):
        super().__init__(core_block, momentum)
