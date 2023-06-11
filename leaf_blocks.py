from defense_block import DefenseBlock
from block import Block
from color import Color


class WoodBlock(DefenseBlock):
    def __init__(self, center_point: tuple, arm=None, visible=True, status=4):
        self._max_hp = 100
        self._mass = 10
        self._init_color = (133, 94, 66)
        texture = "wood"

        super().__init__(center_point=center_point, color=self._init_color,
                         hp=self._max_hp, mass=self._mass, texture=texture, arm=arm, visible=visible, status=status)


class StoneBlock(DefenseBlock):
    def __init__(self, center_point: tuple, arm=None, visible=True, status=4):
        self._max_hp = 200
        self._mass = 50
        self._init_color = (136, 140, 141)
        texture = "stone"

        super().__init__(center_point=center_point, color=self._init_color,
                         hp=self._max_hp, mass=self._mass, texture=texture, arm=arm, visible=visible, status=status)


class CoreBlock(DefenseBlock):
    def __init__(self, center_point: tuple, visible: bool = True, status: int = 4):
        center_point = center_point
        hp = 1000
        color = Color.CORE_COLOR
        mass = 100
        arm = None
        texture = "steel"
        super().__init__(center_point, color=color,
                         hp=hp, mass=mass, texture=texture, arm=arm, visible=visible, status=status)

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
