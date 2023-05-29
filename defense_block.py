from block import Block


class DefenseBlock(Block):
    def __init__(self, center_point: tuple, color: tuple, hp: int, mass: int, arm_type: str = None, visible: bool = True, status: int = 3):
        self._status = status
        self._max_hp = hp
        self._init_color = color
        self.set_arm_type(arm_type)

        super.__init__(center_point, hp, self._init_color, mass)

    def get_hp_ratio(self) -> float:
        return self._hp / self._max_hp

    def set_status(self, status: int):
        # status: 0(hp=0),1(hp<25%),2(hp<50%),3(hp<75%),4(hp>75%)
        if status < 0 or status > 4:
            raise Exception('In set_status: Value of status out of range')
        self._status = status
        if status == 0:
            self.break_animation()
            self._visible = False

    def get_status(self):
        return self._status

    def set_color(self):
        status = self._status
        match status:
            case 0:
                self._color = tuple(
                    map(lambda x, y: x+y, self._init_color, (100, 0, 0)))
            case 1:
                self._color = tuple(
                    map(lambda x, y: x+y, self._init_color, (75, 0, 0)))
            case 2:
                self._color = tuple(
                    map(lambda x, y: x+y, self._init_color, (50, 0, 0)))
            case 3:
                self._color = tuple(
                    map(lambda x, y: x+y, self._init_color, (25, 0, 0)))
            case 4:
                self._color = self._init_color
            case _:
                raise Exception('In set_color: Value of status out of range')

    def damage_block(self, value):
        super.damage_block(value)
        ratio = self.get_hp_ratio()
        if ratio == 0:
            self.set_status(0)
        elif ratio < 0.25:
            self.set_status(1)
        elif ratio < 0.50:
            self.set_status(2)
        elif ratio < 0.75:
            self.set_status(3)
        else:
            self.set_status(4)

    def break_animation(self):
        raise NotImplementedError

    # Armed block

    def attack(self) -> None:
        # Unable to attack
        if self.get_status() == 0 or self.get_arm_type() == None:
            return

        arm_type = self.get_arm_type()
        match arm_type:
            case "sword":
                raise NotImplementedError("Arm_type: sword not implemented")
            case "cannon":
                raise NotImplementedError("Arm_type: cannon not implemented")
            case "hammer":
                raise NotImplementedError("Arm_type: hammer not implemented")
            case _:
                raise Exception("No such arm type", arm_type)

    def get_arm_type(self) -> str:
        return self._arm_type

    def set_arm_type(self, arm_type) -> None:
        if arm_type == "sword" or arm_type == "cannon" or arm_type == "hammer":
            self._arm_type = arm_type
