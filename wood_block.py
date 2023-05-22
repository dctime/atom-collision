from defense_block import DefenseBlock


class WoodBlock(DefenseBlock):
    def __init__(self, center_point: tuple, visible=True, status=3):
        super().__init__(center_point, visible, status)
        self._hp = 50
        self._mass = 15

