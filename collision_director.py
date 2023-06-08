from block_mechanism import BlockMechanism
from leaf_blocks import CoreBlock
from block import Block

class CollisionDirector():
    # TODO: do force to block_mecha1 and block_mecha2 
    def is_collide(self,block_mechanism_1:BlockMechanism, block_mechanism_2:BlockMechanism):
        for _, block1 in block_mechanism_1.get_blocks().items():
            for _, block2 in block_mechanism_2.get_blocks().items():
                if self.is_block_collide(block1, block2):
                    print(block1, block2)
                    return True
        return False
                
    def is_block_collide(self, block1:Block, block2:Block):
        for node in block2.get_nodes():
            if self.is_node_in_block(node, block1):
                return True
        return False

    def is_node_in_block(self, node:tuple, block:Block):
        nodes = block.get_nodes()
        if not ((nodes[0][0]-nodes[1][0]) == 0 or (nodes[2][0]-nodes[1][0]) == 0):
            ma = (nodes[0][1]-nodes[1][1])/(nodes[0][0]-nodes[1][0])
            b1 = nodes[1][1]-ma*nodes[1][0]
            b2 = nodes[2][1]-ma*nodes[2][0]
            bt = node[1]-ma*node[0]
            if not ((b2 >= bt and bt >= b1) or (b1 >= bt and bt >= b2)):
                return False
            
            mb = ((nodes[2][1]-nodes[1][1])/(nodes[2][0]-nodes[1][0]))
            b1 = nodes[1][1]-mb*nodes[1][0]
            b0 = nodes[0][1]-mb*nodes[0][0]
            btt = node[1]-mb*node[0]
            if not ((b1 >= btt and btt >= b0) or (b0 >= btt and btt >= b1)):
                return False
        
            print(nodes, node)
            return True
        else:
            # x coor
            if not ((nodes[1][0] >= node[0] and node[0] >= nodes[3][0]) or (nodes[3][0] >= node[0] and node[0] >= nodes[1][0])):
                return False
            
            # y coor
            if not ((nodes[1][1] >= node[1] and node[1] >= nodes[3][1]) or (nodes[3][1] >= node[1] and node[1] >= nodes[1][1])):
                return False
            
            print(nodes, node)
            return True