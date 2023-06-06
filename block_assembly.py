from defense_block import DefenseBlock
import leaf_blocks as lb
import math


class BlockAssembly():
    # i.e. player
    def __init__(self, core_block: DefenseBlock, velocity: float, index: int = 0):
        self._core = core_block
        self._rotation = 0
        self._index = index
        self._velocity = velocity
        self._size = 0
        self._oppo = None

        # key=coor, value=block
        # Represents coordinate-block pairs
        self._blocks = {} # stores Block class objects

        # key=block, value = neighbors(list)
        # dictionary form of adjacency list
        self._block_neighbor = {}
        self.add_block(core_block, core=True)

    def render(self, screen, zero_vector:tuple, unit_size:int):
        for coordinate, block in self._blocks.items():
            block.render(screen, zero_vector, unit_size)
            arm = block.get_arm()
            if arm != None:
                arm.render(screen)

    def add_block(self, block: DefenseBlock, core: bool = False):
        coor = block.get_coor()
        if not core and not self.get_able(coor):
            print('Adding block in this coor is unavailable.')
            return
        self._size += 1
        self._blocks[coor] = block
        self._block_neighbor[block] = []

        neighbors = self.get_neighbors(coor)
        for neighbor in neighbors:
            if neighbor != None:
                self._block_neighbor[neighbor].append(block)
                self._block_neighbor[block].append(neighbor)
        return self

    def set_oppo(self, player):
        '''
        player is BlockAssembly's object
        '''
        self._oppo = player

    def get_blocks(self) -> dict:
        return self._blocks

    def get_block(self, coor: tuple) -> DefenseBlock:
        return self._blocks.get(coor)

    def get_able(self, coor: tuple) -> bool:
        # check if coor is able to add_block
        if self.get_block(coor) != None:
            return False
        neighbors = self.get_neighbors(coor)
        for neighbor in neighbors:
            if neighbor != None:
                return True
        return False

    def get_neighbors(self, coor: tuple) -> list:
        # return neighbors at coor(including None)
        x = coor[0]
        y = coor[1]

        # find neighbors
        neighbors = [self.get_block((x+1, y)), self.get_block((x-1, y)),
                     self.get_block((x, y+1)), self.get_block((x, y-1))]
        return neighbors

    def add_blocks(self, coordinate_block: dict) -> None:
        for coori, bi in coordinate_block:
            self.add_block(bi, coori)

    def build(self) -> DefenseBlock:
        pass

    def get_coor(self) -> tuple:
        return self._core.get_coor()

    def move(self, dir: tuple) -> None:
        delta_pos = (dir[0]*self._velocity, dir[1]*self._velocity)
        slope = dir[1]/dir[0]
        rad = math.atan(slope)

        # deg in [-90,90]
        deg = rad/math.pi*180

        # map deg to [0,360]
        if dir[0] < 0:
            deg += 180
        if deg < 0:
            deg += 360

        self.set_rotation(deg)
        for coori, bi in self.get_blocks():
            bi.move(delta_pos)
            bi.set_rotation(deg)

    def set_rotation(self, rotation: float) -> None:
        self._rotation = rotation

    def attack(self, arm_type) -> None:
        # Call this function in main
        # arm_type should be a subclass of weapon
        for coori, bi in self.get_blocks():
            armi = bi.get_arm()
            if type(armi) == arm_type:
                bi.attack(self._oppo)


if __name__ == "__main__":
    coor = (100, 100)
    core = lb.CoreBlock(coor)
    game = None
    plr = BlockAssembly(game, core, 4.8763)
