from block import Block
from color import Color

class BlockAssembly(Block):
    def __init__(self):
        self._core = Block((200, 200), 100, Color.CORE_COLOR)
        self._core_x = 0
        self._core_y = 0
        self.rotation = 0
        self._blocks = {(0, 0):self._core}

    def render(self, screen):
        for coordinate, block in self._blocks.items():
            block.render(screen)

    def add_block(self, block:Block, location:tuple):
        self._blocks[location] = block

class Builder:
    def __init__(self, core_block, core_coor):
        self._size = 0

        # key=coor, value=block
        self._coor_block = {}

        # key=block, value = children(list)
        self._block_child = {}

        self.add_block(core_block, core_coor, core=True)

    def size(self):
        return self._size

    def get_block(self, coor):
        return self._coor_block.get(coor)

    def get_able(self, coor):
        # check if coor is able to add_block
        if self.get_block(coor) != None:
            return False
        neighbors = self.get_neighbors(coor)
        for neighbor in neighbors:
            if neighbor != None:
                return True
        return False

    def get_neighbors(self, coor):
        # return neighbors at coor(including None)
        x = coor[0]
        y = coor[1]

        # find neighbors
        neighbors = [self.get_block((x+1, y)), self.get_block((x-1, y)),
                     self.get_block((x, y+1)), self.get_block((x, y-1))]
        return neighbors

    def add_block(self, block, coor, core=False):
        if not core and not self.get_able(coor):
            raise print('Adding block in this coor is unavailable.')
            return
        self._size += 1
        self._coor_block[coor] = block
        self._block_child[block] = []

        neighbors = self.get_neighbors(coor)
        for neighbor in neighbors:
            if neighbor != None:
                self._block_child[neighbor].append(block)
        return self

    def add_blocks(coordinate_block:dict):
        pass
        
    def build() -> Block:
        pass 