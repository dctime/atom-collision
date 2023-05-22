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
            print('Adding block in this coor is unavailable.')
            return
        self._size += 1
        self._coor_block[coor] = block
        self._block_child[block] = []

        neighbors = self.get_neighbors(coor)
        for neighbor in neighbors:
            if neighbor != None:
                self._block_child[neighbor].append(block)
