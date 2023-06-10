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

    def __init__(self, center_point: tuple, color: tuple, hp: int, mass: int, texture: str, arm=None, visible: bool = True, status: int = 4):
        self._status = status
        self._max_hp = hp
        self._init_color = color
        self._texture = texture
        self._arm = None
        if arm != None:
            self.set_arm(arm)

        super().__init__(center_point, hp, self._init_color, mass)

    def get_hp_ratio(self) -> float:
        return self._hp / self._max_hp

    def set_status(self):
        # status: 0(hp=0),1(hp<25%),2(hp<50%),3(hp<75%),4(hp>75%)
        ratio = self.get_hp_ratio()
        if ratio == 0:
            self._status = 0
            self._visible=False
        elif ratio < 0.25:
            self._status = 1
        elif ratio < 0.50:
            self._status = 2
        elif ratio < 0.75:
            self._status = 3
        else:
            self._status = 4

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
            
        self._color = tuple([min(ci,255) for ci in self._color])

    def damage_block(self, value):
        super().damage_block(value)
        self.set_status()
        self.set_color()

    def break_animation(self):
        raise NotImplementedError

    def set_rotation(self, rotation: float):
        # Cannon rotates independently

        self._rotation = rotation
        arm = self.get_arm()
        arm_type = type(arm)
        if arm_type == wp.Sword or arm_type == wp.Hammer:
            arm.set_dir(rotation)

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
        self._arm = arm


if __name__ == "__main__":
    coor = (100, 100)
    color = (255, 255, 255)
    hp = 100
    mass = 100
    texture = "whatever"

    db = DefenseBlock(coor, color, hp, mass, texture)

    print("\nSet arm:")
    db.set_arm("sword")
    print(type(db.get_arm()))

    print("\nmove:")
    db.move(coor)
    print(db.get_coor())

    print("\nSet rotation:")
    db.set_rotation(180)
    print(db._rotation)

    print("\nStatus:")
    print(db.get_status())
    db.damage_block(48)
    print(db.get_hp_ratio())
    print(db.get_status())
