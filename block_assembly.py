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

    