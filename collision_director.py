from block_mechanism import BlockMechanism
from leaf_blocks import CoreBlock
from block import Block

class CollisionDirector():
    def is_collide(self,block_mechanism_1:BlockMechanism, block_mechanism_2:BlockMechanism):
        for _, block1 in block_mechanism_1._blocks:
            for _, block2 in block_mechanism_2.get_blocks():
                if self.is_block_collide(block1, block2):
                    return True
        return False
                
    def is_block_collide(self, block1:Block, block2:Block):
        for node in block2.get_nodes():
            if self.is_node_in_block(node, block1):
                return True
        return False

    def is_node_in_block(node:tuple, block:Block):
        nodes = block.get_nodes()
        ma = (nodes[0][1]-nodes[1][1])/(nodes[0][0]-nodes[1][0])
        b1 = nodes[1][1]-ma*nodes[1][0]
        b2 = nodes[2][1]-ma*nodes[2][0]
        bt = node[1]-ma*node[0]
        if not ((b2 >= bt and bt >= b1) or (b1 >= bt and bt >= b2)):
            return False

        mb = ((nodes[2][1]-nodes[1][1])/(nodes[2][0]-nodes[1][0]))
        b3 = nodes[3][1]-mb*nodes[3][0]
        b0 = nodes[0][1]-mb*nodes[0][0]
        btt = node[1]-mb*node[0]
        if not ((b3 >= btt and btt >= b0) or (b0 >= btt and btt >= b3)):
            return False
        
        return True