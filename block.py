import skin_bone
import pygame

STONE_COLOR = (125, 125, 125)


class Block(skin_bone.SkinBone):
    def __init__(self, center_point: tuple, hp: int, color: tuple, mass: int, visible=True):
        super().__init__()
        self._hp = hp
        self._visible = visible
        self._block_size = 30
        self._color = color
        self._points = []
        self._mass = mass
        self._points.append(
            (center_point[0]-self._block_size/2, center_point[1]-self._block_size/2))
        self._points.append(
            (center_point[0]+self._block_size/2, center_point[1]-self._block_size/2))
        self._points.append(
            (center_point[0]+self._block_size/2, center_point[1]+self._block_size/2))
        self._points.append(
            (center_point[0]-self._block_size/2, center_point[1]+self._block_size/2))

        self.set_nodes(self._points)

    def get_hp(self):
        return self._hp

    def set_hp(self, hp):
        self._hp = hp

    def damage_block(self, value):
        if self._hp - value < 0:
            self._hp = 0
        else:
            self._hp -= value

    def heal_block(self, value):
        self._hp += value

    def get_left_top(self) -> tuple:
        return self._points[0]

    def get_block_size(self) -> int:
        return self._block_size

    def render(self, screen, is_debugging=False, debug_color=(255, 0, 0)):
        # draw ifself
        if self._visible:
            pygame.draw.polygon(screen, self._color, self.get_nodes(), 0)

            # Draw corners
            if is_debugging:
                for node in self.get_nodes():
                    pygame.draw.circle(screen, debug_color, node, 3)
