from defense_block import DefenseBlock


class StoneBlock(DefenseBlock):
    def __init__(self, center_point: tuple, visible=True, status=3):
        super().__init__(center_point, visible, status)
        self._hp = 200
        self._mass = 100