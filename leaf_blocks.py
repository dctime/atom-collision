from defense_block import DefenseBlock
from block import Block
from color import Color


class WoodBlock(DefenseBlock):
    def __init__(self, center_point: tuple, arm=None, visible=True, status=3):
        self._max_hp = 50
        self._mass = 15
        self._init_color = (133, 94, 66)
        texture = "wood"

        super().__init__(center_point, self._init_color,
                         self._max_hp, self._mass, texture, arm, visible, status)


class StoneBlock(DefenseBlock):
    def __init__(self, center_point: tuple, arm=None, visible=True, status=3):
        self._max_hp = 200
        self._mass = 100
        self._init_color = (136, 140, 141)
        texture = "stone"

        super().__init__(center_point, self._init_color,
                         self._max_hp, self._mass, texture, arm, visible, status)


class CoreBlock(DefenseBlock):
    def __init__(self, center_point: tuple, hp: int, color: tuple, mass: int, visible: bool = True, status: int = 3):
        center_point = center_point
        hp = 100
        color = Color.CORE_COLOR
        mass = 200
        arm = None
        texture = "steel"
        super().__init__(center_point, hp, color, mass, texture, arm, visible, status)

    def set_arm(self, arm) -> None:
        raise Exception("Core has no arm")
