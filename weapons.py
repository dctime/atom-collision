import time
import pygame
import math

# For melee, weapon turn with the block
# For ranged, weapon turn independently
# opponent or player is BlockAssembly


class Weapon():
    # Parent class of weapons
    def __init__(self, statistic: dict, rotation: float, credit: str = None) -> None:
        """
        Statistic definition:

        (1) damage: Damage per hit
        (2) range: Range of attack
        (3) frequency: Frequency of attack
        (4) velocity: Velocity of the fired bullet(only in cannon)
        (5) radius: Radius of bullet(only in cannon)

        """

        self._statistic = statistic
        self._available = True
        self._credit = credit
        self.set_dir(rotation)

    def set_dir(self, rotation) -> None:
        # Set direction_melee
        rotation %= 360
        if rotation >= 45 and rotation < 135:
            self._dir_melee = "up"
        elif rotation >= 135 and rotation < 225:
            self._dir_melee = "left"
        elif rotation >= 225 and rotation < 315:
            self._dir_melee = "down"
        else:
            self._dir_melee = "right"
        # Set direction_ranged
        rad = rotation/180*math.pi
        dir_x = math.sin(rad)
        dir_y = math.cos(rad)
        self._dir_ranged = (dir_x, dir_y)

    def get_stat(self) -> dict:
        return self._statistic

    def buff_stat(self, stat_to_buff: dict) -> None:
        # Update stat by adding or subbing
        for name, delta in stat_to_buff:
            self._statistic[name] += delta

    def change_stat(self, stat_to_change: dict) -> None:
        # Update stat by replacing
        for name, val in stat_to_change:
            self._statistic[name] = val

    def attack(self) -> None:
        # Virtual function
        # Do NOT call this function rightaway, we need to check if the block is broken first
        if not self._available:
            return
        self.attack_animation()

    def cool_down(self) -> None:
        self._available = False
        time.sleep(1/self._statistic["frequency"])
        self._available = True

    def find_hit(self, player, area: pygame.Rect):
        """
        Returns:
            The block in the area & closet to pos
        """
        area_center = area.center
        dist = float('inf')
        hit_block = None

        for block_center, block in player.get_blocks():
            left, top = block.get_left_top()
            size = block.get_block_size()
            rect_block = pygame.Rect(left, top, size, size)
            collide = area.colliderect(rect_block)
            if not collide:
                continue
            dist_temp = ((area_center[0]-block_center[0])
                         ** 2) + ((area_center[1]-block_center[1])**2)
            if dist_temp < dist:
                dist = dist_temp
                hit_block = block

        return hit_block

    def hit(self, block) -> None:
        dmg = self._statistic["damage"]
        if block._texture == self._credit:
            dmg *= 2
        block.damage_block(dmg)

    def attack_animation(self) -> None:
        # Virtual function
        pass

    def render(self, screen) -> None:
        # Virtual function
        pass


class Sword(Weapon):
    """
    Usually with high frequency
    Good at destroy wood blocks
    """

    def __init__(self, statistic: dict, rotation: float) -> None:

        credit = "wood"
        super().__init__(statistic, rotation, credit=credit)

    def get_attack_area(self, pos: tuple) -> pygame.Rect:
        # Return area of attack
        r = self._statistic["range"]
        dir = self._dir_melee
        if dir == "left":
            left = pos[0] - r
            top = pos[1] - r
            width = r
            height = 2*r
        elif dir == "right":
            left = pos[0]
            top = pos[1] + r
            width = r
            height = 2*r
        elif dir == "up":
            left = pos[0] - r
            top = pos[1] - r
            width = 2*r
            height = r
        elif dir == "down":
            left = pos[0] - r
            top = pos[1]
            width = 2*r
            height = r
        else:
            raise Exception("No such direction", dir)
        return pygame.Rect(left, top, width, height)

    def attack(self, opponent, pos: tuple) -> None:
        super().attack()
        area = self.get_attack_area(pos)
        block_hit = self.find_hit(opponent, area)
        if block_hit != None:
            self.hit(block_hit)
        self.cool_down()

    def attack_animation(self) -> None:
        pass


class Hammer(Weapon):
    """
    2 hit zones: close & far with damage low & high respectively
    Usually with low frequency
    Good at destroying steel(core) blocks 
    """

    def __init__(self, statistic: dict, rotation: float) -> None:

        credit = "steel"
        super().__init__(statistic, rotation, credit=credit)

    def get_attack_area(self, pos: tuple) -> list:
        # Return list of Rect

        # Rect_1: less dmg
        # Rect_2: more dmg
        r = self._statistic["range"]
        dir = self._dir_melee
        reserved_dist = r/2
        if dir == "left":
            left_1 = pos[0]-reserved_dist
            top_1 = pos[1]-r
            width_1 = reserved_dist
            height_1 = 2*r

            left_2 = pos[0] - r
            top_2 = pos[1] - r
            width_2 = r - reserved_dist
            height_2 = 2*r

        elif dir == "right":
            left_1 = pos[0]
            top_1 = pos[1]+r
            width_1 = reserved_dist
            height_1 = 2*r

            left_2 = pos[0]+reserved_dist
            top_2 = pos[1] + r
            width_2 = r-reserved_dist
            height_2 = 2*r
        elif dir == "up":
            left_1 = pos[0]-r
            top_1 = pos[1]+reserved_dist
            width_1 = 2*r
            height_1 = reserved_dist

            left_2 = pos[0] - r
            top_2 = pos[1] - r
            width_2 = 2*r
            height_2 = r-reserved_dist
        elif dir == "down":
            left_1 = pos[0]-r
            top_1 = pos[1]
            width_1 = 2*r
            height_1 = reserved_dist

            left_2 = pos[0] - r
            top_2 = pos[1]+reserved_dist
            width_2 = 2*r
            height_2 = r-reserved_dist
        else:
            raise Exception("No such direction", dir)
        rect_1 = pygame.Rect(left_1, top_1, width_1, height_1)
        rect_2 = pygame.Rect(left_2, top_2, width_2, height_2)
        return [rect_1, rect_2]

    def attack(self, opponent, pos: tuple) -> None:
        super().attack()
        area = self.get_attack_area(pos)
        block_hit = self.find_hit(opponent, area[1])  # more dmg zone first
        if block_hit != None:
            self.hit(block_hit)
        else:
            block_hit = self.find_hit(opponent, area[0])
            if block_hit != None:
                self.hit(block_hit)
        self.cool_down()

    def attack_animation(self) -> None:
        pass


class Cannon(Weapon):
    """
    Usually with lowest frequency 
    Good at destroying stone blocks
    """

    def __init__(self, statistic: dict, rotation: float) -> None:
        credit = "stone"
        super().__init__(statistic, rotation, credit=credit)

    def attack(self, opponent, pos: tuple) -> None:
        super().attack()

        stat = self.get_stat()
        r = stat["range"]
        dist_x = r * self._dir_ranged[0]
        dist_y = r*self._dir_ranged[1]

        bullet_pos = (pos[0]+dist_x, pos[1]+dist_y)
        bullet = Bullet(bullet_pos, stat["velocity"],
                        self._dir_ranged, stat["radius"], opponent)

        # game.add_object() hasn't been defined yet
        # We can define game as global varrible, so that it won't be necessary to be passed into this function
        game.add_object(bullet)
        self.cool_down()

    def attack_animation(self) -> None:
        pass


class Bullet():
    def __init__(self, damage: float, pos: tuple, velocity: float, dir: tuple, radius: float, opponent, credit: str = "stone") -> None:
        self._damage = damage
        self._pos = list(pos)
        self._velocity = velocity
        self._dir = dir
        self._radius = radius
        self._opponent = opponent
        self._credit = credit

    def move(self) -> None:
        # game will call this if the bullet exists

        self._pos[0] += self._velocity*self._dir[0]
        self._pos[1] += self._velocity*self._dir[1]
        area = self.get_attack_area()
        block_hit = self.find_hit(self._opponent, area)
        if block_hit != None:
            self.hit(block_hit)

    def get_attack_area(self) -> tuple:
        """
        Returns:
            tuple: 
                (1) center of circle(tuple)
                (2) radius
        """
        return (tuple(self._pos), self._radius)

    def intersects(self, rect: pygame.rect,  center: tuple, r: float):
        circle_distance_x = abs(center[0]-rect.centerx)
        circle_distance_y = abs(center[1]-rect.centery)
        if circle_distance_x > rect.w/2.0+r or circle_distance_y > rect.h/2.0+r:
            return False
        if circle_distance_x <= rect.w/2.0 or circle_distance_y <= rect.h/2.0:
            return True
        corner_x = circle_distance_x-rect.w/2.0
        corner_y = circle_distance_y-rect.h/2.0
        corner_distance_sq = corner_x**2.0 + corner_y**2.0
        return corner_distance_sq <= r**2.0

    def find_hit(self, player, area: tuple):
        """
        player is a BlockAssembly
        Returns:
            The block in the area & closet to pos
        """
        area_center = area[0]
        area_radius = area[1]
        dist = float('inf')
        hit_block = None

        for block_center, block in player.get_blocks():
            left, top = block.get_left_top()
            size = block.get_block_size()
            rect_block = pygame.Rect(left, top, size, size)
            collide = self.intersects(rect_block, area_center, area_radius)
            if not collide:
                continue
            dist_temp = ((area_center[0]-block_center[0])
                         ** 2) + ((area_center[1]-block_center[1])**2)
            if dist_temp < dist:
                dist = dist_temp
                hit_block = block

        return hit_block

    def hit(self, block) -> None:
        dmg = self._damage
        if block._texture == self._credit:
            dmg *= 2
        block.damage_block(dmg)
        self.explode_animation()

        # Not defined yet
        game.remove_object(self)

    def explode_animation(self) -> None:
        raise NotImplementedError("Explode animation not implemented yet")


if __name__ == "__main__":
    stat = {"range": 10}
    sword = Sword(stat, 0)
    hammer = Hammer(stat, 0)

    print("\nGet attack area:")
    area = sword.get_attack_area((100, 100))
    print(area)
    area = hammer.get_attack_area((100, 100))
    print(area)
