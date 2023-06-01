from defense_block import DefenseBlock
from block import Block
from color import Color


class WoodBlock(DefenseBlock):
    def __init__(self, center_point: tuple, arm=None, visible=True, status=4):
        self._max_hp = 50
        self._mass = 15
        self._init_color = (133, 94, 66)
        texture = "wood"

        super().__init__(center_point, self._init_color,
                         self._max_hp, self._mass, texture, arm, visible, status)


class StoneBlock(DefenseBlock):
    def __init__(self, center_point: tuple, arm=None, visible=True, status=4):
        self._max_hp = 200
        self._mass = 100
        self._init_color = (136, 140, 141)
        texture = "stone"

        super().__init__(center_point, self._init_color,
                         self._max_hp, self._mass, texture, arm, visible, status)


class CoreBlock(DefenseBlock):
    def __init__(self, center_point: tuple, visible: bool = True, status: int = 4):
        center_point = center_point
        hp = 100
        color = Color.CORE_COLOR
        mass = 200
        arm = None
        texture = "steel"
        super().__init__(center_point, hp, color, mass, texture, arm, visible, status)

    def set_arm(self, arm) -> None:
        print("Core has no arm")


if __name__ == "__main__":
    coor = (100, 100)

    core = CoreBlock(coor)
    wood = WoodBlock(coor)
    stone = StoneBlock(coor)
    print("texture of core is", core._texture)
    print("texture of wood is", wood._texture)
    print("texture of stone is", stone._texture)
