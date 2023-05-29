from defense_block import DefenseBlock


class StoneBlock(DefenseBlock):
    def __init__(self, center_point: tuple, arm_type: str = None, visible=True, status=3):
        self._max_hp = 200
        self._mass = 100
        self._init_color = (136, 140, 141)

        super().__init__(center_point, self._init_color,
                         self._max_hp, self._mass, arm_type, visible, status)
