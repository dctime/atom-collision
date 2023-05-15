from block import Block

STONE_COLOR = (125, 125, 125)

class BlockAssembly(Block):
    def __init__(self):
        self._core = Block((0, 0), 100)
        self._core_x = 0
        self._core_y = 0
        self.rotation = 0
        self._blocks = {(0, 0):self._core}
        self._texture = {(0, 0):STONE_COLOR}

    def render(self, screen):
        for coordinate, block in self._blocks.items():
            block.render(screen, self._texture[coordinate])