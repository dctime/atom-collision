from block import Block
import weapons as wp
import game_statistics as stat


class DefenseBlock(Block):
    """
    Attribute:
        (1) _status: status of block, decided by hp ratio
        (2) _max_hp: block's max_hp
        (3) _init_color: initial color
        (4) _texture: texture of block
        (5) _arm: weapon of block
        (6) _rotation: angle of block with x-axis(in degree)
        and others in Block
    """

    def __init__(self, center_point: tuple, color: tuple, hp: int, mass: int, texture: str, arm=None, visible: bool = True, status: int = 3):
        self._status = status
        self._max_hp = hp
        self._init_color = color
        self._texture = texture
        self._rotation = 0
        self.set_arm(arm)

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

    def set_rotation(self, rotation: float):
        # Cannon rotates independently

        self._rotation = rotation
        arm = self.get_arm()
        arm_type = type(arm)
        if arm_type == wp.Sword or arm_type == wp.Hammer:
            arm.set_dir(rotation)

    def move(self, delta_pos):
        # Movement of block is not clear yet
        new_coor = tuple(map(lambda x, y: x+y, self.get_coor(), delta_pos))
        self.set_coor(new_coor)
    # Armed block

    def attack(self, opponent) -> None:
        # Unable to attack
        if self.get_status() == 0 or self.get_arm() == None:
            return

        arm = self.get_arm()
        arm.attack(opponent, self.get_coor())

    def get_arm(self):
        return self._arm

    def set_arm(self, arm_type: str) -> None:
        arm = None
        if arm_type == "sword":
            arm = wp.Sword(stat.sword_stat, self._rotation)
        elif arm_type == "hammer":
            arm = wp.Hammer(stat.hammer_stat, self._rotation)
        elif arm_type == "cannon":
            arm = wp.Cannon(stat.cannnon_stat, self._rotation)
