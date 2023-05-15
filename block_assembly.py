from block import Block

class BlockAssembly(Block):
    def __init__(self):
        self._core = Block((0, 0), 100)
        self._core_x = 0
        self._core_y = 0
        self.rotation = 0
        self._blocks = {(0, 0):self.core}