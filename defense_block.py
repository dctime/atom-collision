class DefenseBlock:
    def __init__(self, center_point: tuple, hp: int, mass:int, visible=True, status=3):
        self._status = None
        self._init_color = (136, 140, 141)
        
        self.set_status(status)
        self.set_color()

        super.__init__(center_point, hp, self._color, mass)

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
        if self.hp == 0:
            self.set_status(0)
        elif self.hp < 25:
            self.set_status(1)
        elif self.hp < 50:
            self.set_status(2)
        elif self.hp < 75:
            self.set_status(3)
        else:
            self.set_status(4)

    def break_animation(self):
        raise NotImplementedError