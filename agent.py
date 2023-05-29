import numpy as np


class Agent():
    def __init__(self, blocks: list) -> None:
        self.blocks = blocks

        # Whether the agent is able to speed up
        self.boost = any([bi._boost and bi._visible for bi in blocks])

        # Undefined
        self.speed = None

    def block_num(self) -> int:
        return sum([1 if bi.get_hp() > 0 else 0 for bi in self.blocks])

    def total_hp(self) -> float:
        return sum([bi.get_hp() for bi in self.blocks])

    def core_hp(self) -> float:
        return self.blocks[0].get_hp()

    def alive(self) -> bool:
        return self.blocks[0].get_hp() > 0

    def damaged(self, damage: list) -> None:
        blocks = self.blocks

        for i in range(len(blocks)):
            blocks[i].damage_block(damage[i])

    def move_x(self, right: bool = True) -> None:
        if right:
            self.pos[0] += self.speed
        else:
            self.pos[0] -= self.speed

    def move_y(self, down: bool = True) -> None:
        if down:
            self.pos[1] += self.speed
        else:
            self.pos[1] -= self.speed

    def attack(self, arm_type: str) -> None:
        block_index = np.where([bi.get_arm_type()
                               for bi in self.blocks] == arm_type)
        for bi in block_index:
            self.blocks[bi].attack()
