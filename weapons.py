from block import Block
from block_assembly import BlockAssembly
import time
import pygame
import math


class Weapon():
    # Parent class of weapons
    def __init__(self, statistic: dict, pos: tuple, dir_melee: str, dir_ranged: tuple) -> None:
        """
        Statistic definition:

        (1) damage: Damage per hit
        (2) range: Range of attack
        (3) frequency: Frequency of attack
        (4) velocity: Velocity of the fired bullet(only in cannon)
        (5) radius: Radius of bullet(only in cannon)

        """

        self._statistic = statistic
        self._pos = pos
        self._dir_melee = dir_melee
        self._dir_ranged = dir_ranged
        self._available = True

    def set_dir(self, dir) -> None:
        # Set direction
        if type(dir) == str:
            self._dir_melee = dir
        else:
            self._dir_ranged = dir

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
        # For melee class
        if not self._available:
            return

    def cool_down(self) -> None:
        self._available = False
        time.sleep(1/self._statistic["frequency"])
        self._available = True

    def find_hit(self, player: BlockAssembly, area: pygame.Rect) -> Block:
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

    def hit(self, block: Block) -> None:
        dmg = self._statistic["damage"]
        block.damage_block(dmg)

# __init__ of sub classes are as same as weapon


class Sword(Weapon):
    def get_attack_area(self) -> pygame.Rect:
        # Return area of attack
        r = self._statistic["range"]
        dir = self._dir_melee
        if dir == "left":
            left = self._pos[0] - r
            top = self._pos[1] - r
            width = r
            height = 2*r
        elif dir == "right":
            left = self._pos[0]
            top = self._pos[1] + r
            width = r
            height = 2*r
        elif dir == "up":
            left = self._pos[0] - r
            top = self._pos[1] - r
            width = 2*r
            height = r
        elif dir == "down":
            left = self._pos[0] - r
            top = self._pos[1]
            width = 2*r
            height = r
        else:
            raise Exception("No such direction", dir)
        return pygame.Rect(left, top, width, height)

    def attack(self, opponent) -> None:
        super().attack()
        area = self.get_attack_area()
        block_hit = self.find_hit(opponent, area)
        if block_hit != None:
            self.hit(block_hit)


class Hammer(Weapon):
    def get_attack_area(self) -> list:
        # Return list of Rect

        # Rect_1: less dmg
        # Rect_2: more dmg
        r = self._statistic["range"]
        dir = self._dir_melee
        reserved_dist = r/2
        if dir == "left":
            left_1 = self._pos[0]-reserved_dist
            top_1 = self._pos[1]-r
            width_1 = reserved_dist
            height_1 = 2*r

            left_2 = self._pos[0] - r
            top_2 = self._pos[1] - r
            width_2 = r - reserved_dist
            height_2 = 2*r

        elif dir == "right":
            left_1 = self._pos[0]
            top_1 = self._pos[1]+r
            width_1 = reserved_dist
            height_1 = 2*r

            left_2 = self._pos[0]+reserved_dist
            top_2 = self._pos[1] + r
            width_2 = r-reserved_dist
            height_2 = 2*r
        elif dir == "up":
            left_1 = self._pos[0]-r
            top_1 = self._pos[1]+reserved_dist
            width_1 = 2*r
            height_1 = reserved_dist

            left_2 = self._pos[0] - r
            top_2 = self._pos[1] - r
            width_2 = 2*r
            height_2 = r-reserved_dist
        elif dir == "down":
            left_1 = self._pos[0]-r
            top_1 = self._pos[1]
            width_1 = 2*r
            height_1 = reserved_dist

            left_2 = self._pos[0] - r
            top_2 = self._pos[1]+reserved_dist
            width_2 = 2*r
            height_2 = r-reserved_dist
        else:
            raise Exception("No such direction", dir)
        rect_1 = pygame.Rect(left_1, top_1, width_1, height_1)
        rect_2 = pygame.Rect(left_2, top_2, width_2, height_2)
        return [rect_1, rect_2]

    def attack(self, opponent) -> None:
        super().attack()
        area = self.get_attack_area()
        block_hit = self.find_hit(opponent, area[1])  # more dmg zone first
        if block_hit != None:
            self.hit(block_hit)
            return
        block_hit = self.find_hit(opponent, area[0])
        if block_hit != None:
            self.hit(block_hit)


class Cannon(Weapon):

    def attack(self, game, opponent) -> None:
        super().attack()
        stat = self.get_stat()
        bullet = Bullet(self._pos, stat["velocity"],
                        self._dir_ranged, stat["radius"], opponent)

        # game.add_object() hasn't been defined yet
        # We can define game as global varrible, so that it won't be necessary to be passed into this function
        game.add_object(bullet)


class Bullet():
    def __init__(self, damage: float, pos: tuple, velocity: float, dir: tuple, radius: float, opponent: BlockAssembly) -> None:
        self._damage = damage
        self._pos = list(pos)
        self._velocity = velocity
        self._dir = dir
        self._radius = radius
        self._opponent = opponent

    def move(self) -> None:
        # Call this only
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

    def find_hit(self, player: BlockAssembly, area: tuple) -> Block:
        """
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

    def hit(self, block: Block) -> None:
        block.damage_block(self._damage)
        self.explode_animation()

        # Not defined yet
        game.remove_object(self)

    def explode_animation(self) -> None:
        raise NotImplementedError
