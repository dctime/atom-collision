from skin_bone import SkinBone
import pygame
import numpy as np
import copy


class Block(SkinBone):
    def __init__(self, center_point: tuple, hp: int, color: tuple, mass: int, visible=True):
        super().__init__()
        self._hp = hp
        self._visible = visible
        self._block_size = 1 # normalized, set the render unit size to make it look big
        self._color = color
        self._mass = mass
        self._coor = center_point
        self._rotation = 0
        self._previous_coor = ()

        points = [] # sequential, tuple in list
        points.append(
            (center_point[0]-self._block_size/2, center_point[1]-self._block_size/2))
        points.append(
            (center_point[0]+self._block_size/2, center_point[1]-self._block_size/2))
        points.append(
            (center_point[0]+self._block_size/2, center_point[1]+self._block_size/2))
        points.append(
            (center_point[0]-self._block_size/2, center_point[1]+self._block_size/2))

        self.set_nodes(points)

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

    def get_previous_coor(self):
        return self._previous_coor

    def get_left_top(self) -> tuple:
        return self.get_nodes[0]

    def get_block_size(self) -> int:
        return self._block_size

    def get_coor(self) -> tuple:
        return self._coor
    
    def get_mass(self) -> int:
        return self._mass

    def set_coor(self, coor) -> None:
        self._previous_coor = copy.deepcopy(self.get_coor())
        self._coor = coor

    def move(self, dir_vector:tuple) -> None: 
        # Movement of block is not clear yet
        new_coor = tuple(map(lambda x, y: x+y, self.get_coor(), dir_vector))
        self.set_coor(new_coor)
        new_nodes = []
        for node in self.get_nodes():
            new_nodes.append((node[0]+dir_vector[0], node[1]+dir_vector[1]))
        self.set_nodes(new_nodes)
        # Armed block

    def rotate(self, pivot_point:tuple, theta:float) -> None:
        theta = theta % (2*np.pi)
        temp_nodes = []
        for node in self.get_nodes():
            temp_nodes.append([node[0]-pivot_point[0], node[1]-pivot_point[1]])

        temp_nodes = np.asarray(temp_nodes)
        temp_nodes = temp_nodes.transpose()
        rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)],
                                    [np.sin(theta),  np.cos(theta)]])
        temp_nodes = rotation_matrix @ temp_nodes
        temp_nodes = temp_nodes.transpose()
        
        return_nodes = []
        for node in temp_nodes:
            return_nodes.append([node[0]+pivot_point[0], node[1]+pivot_point[1]])

        self.set_nodes(return_nodes)

        temp_coor = self.get_coor()
        temp_coor = np.array((temp_coor[0]-pivot_point[0], temp_coor[1]-pivot_point[1]))
        temp_coor = rotation_matrix.dot(temp_coor)

        self.set_coor((temp_coor[0]+pivot_point[0], temp_coor[1]+pivot_point[1]))


    def render(self, screen, zero_vector:tuple, unit_size:int, is_debugging=False, debug_color=(255, 0, 0)):
        # draw ifself
        if self._visible:
            image_nodes = np.asarray(self.get_nodes())
            image_nodes *= unit_size
            image_nodes[:, 0] += zero_vector[0]
            image_nodes[:, 1] += zero_vector[1]
                    

            pygame.draw.polygon(screen, self._color, image_nodes, 0)

            # Draw corners
            if is_debugging:
                for node in image_nodes():
                    pygame.draw.circle(screen, debug_color, node, 3)
