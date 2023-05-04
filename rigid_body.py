import skin_bone
import numpy as np
import math
# Deprecated
class Rigidbody(skin_bone.SkinBone):
    def __init__(self, nodes_max_length):
        '''
        nodes_max_length: the distance between the two points when calls the fill_nodes method
        think it as how much the bone can resist the punch
        high value -> metal, low value -> clay
        '''
        super().__init__(nodes_max_length)
        self._center_of_mass = (0, 0)

    def move(self, velocity_vector:tuple):
        for index in range(len(self.nodes)):
            self.nodes[index] = (self.nodes[index][0]+velocity_vector[0], self.nodes[index][1]+velocity_vector[1])

    def rotate(self, radian, pivot_point=tuple()) -> None:
        '''
        radian > 0: counterclockwise
        radian < 0: clockwise

        valid pivot_point => use that point
        unvalid: use the object's center of mass
        '''
        if len(pivot_point) != 2:
            pivot_point = self._center_of_mass

        normalized_nodes = list((node[0]-pivot_point[0], node[1]-pivot_point[1]) for node in self.nodes)
        normalized_nodes_numpy = np.array(normalized_nodes).transpose()
        rotate_matrix = np.array([[math.cos(radian), -math.sin(radian)], [math.sin(radian), math.cos(radian)]])
        # print(rotate_matrix, normalized_nodes_numpy)
        normalized_nodes = (rotate_matrix @ normalized_nodes_numpy).transpose().tolist()

        for normalized_nodes_index in range(len(normalized_nodes)):
            # add center vector back
            normalized_nodes[normalized_nodes_index][0] += pivot_point[0] 
            normalized_nodes[normalized_nodes_index][1] += pivot_point[1]

            normalized_nodes[normalized_nodes_index] = tuple(normalized_nodes[normalized_nodes_index]) # turn every node in tuple

        self.nodes = normalized_nodes  

    def get_center_of_mass(self):
        self._update_center_of_mass()
        # print(self._center_of_mass)
        return self._center_of_mass

    def _update_center_of_mass(self):
        points = self.nodes
        center_x = None
        center_y = None
        all_x = list(point[0] for point in points)
        all_y = list(point[1] for point in points)
        try:
            # print(f"all_x={all_x}")
            # print(f"all_y={all_y}")
            center_x = sum(all_x) / len(all_x)
            center_y = sum(all_y) / len(all_y)
        except ZeroDivisionError:
            print("No node, no center")

        self._center_of_mass = center_x, center_y