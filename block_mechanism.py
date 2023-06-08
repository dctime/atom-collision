from block_assembly import BlockAssembly
from leaf_blocks import CoreBlock
import pygame
import math
import numpy as np

class BlockMechanism(BlockAssembly):
    def __init__(self, core_block: CoreBlock, momentum:tuple = (0, 0)):
        self._momentum = momentum
        self._angular_momentum = 0
        self._momentum_of_inertia = 0
        self._mass = 0
        self._center_of_mass_coor = (0, 0)
        
        super().__init__(core_block)
        self.__update_mass()
        self.__update_center_of_mass_coor()
        self.__update_momentum_of_inertia()

    def render(self, screen, zero_vector:tuple, unit_size:int, is_debugging=False, debug_color=(255, 0, 0)):
        super().render(screen, zero_vector, unit_size)
    
    def add_force(self, force:tuple, location:tuple, time_between_frame:float):
        # FIXME: A little bit weird, use main again
        self._momentum = (self._momentum[0] + force[0]*time_between_frame, self._momentum[1] + force[1]*time_between_frame)

        momentum = self._momentum
        momentum_arm = [location[0]-self._center_of_mass_coor[0], location[1]-self._center_of_mass_coor[1]]
        momentum_arm.append(0)
        force = list(force)
        force.append(0)
        tau = np.cross(np.array(momentum_arm).transpose(), np.array(force).transpose()).transpose()
        self._angular_momentum += tau[2]
        
    def get_center_of_mass_coor(self):
        return self._center_of_mass_coor
    
    def move(self, time_between_frame:float) -> None:
        '''
        move stuff in a tick of time
        '''
        for coori, bi in self.get_blocks().items():
            bi.move((self._momentum[0]/self._mass*time_between_frame*100, self._momentum[1]/self._mass*time_between_frame*100))
            bi.rotate(self.get_center_of_mass_coor(), self._angular_momentum/self._momentum_of_inertia*time_between_frame)

    def __update_mass(self) -> None:
        total_mass = 0
        for _, block in self._blocks.items():
            total_mass += block.get_mass()

        self._mass = total_mass

    def __update_center_of_mass_coor(self) -> None:
        x_up = 0
        y_up = 0
        for _, block in self._blocks.items():
            x_up += block.get_coor()[0]*block.get_mass()
            y_up += block.get_coor()[1]*block.get_mass()
        
        self._center_of_mass_coor = (x_up/self._mass, y_up/self._mass)

    def __update_momentum_of_inertia(self) -> None:
        total_inertia = 0
        inertia = lambda mass, distance_to_center:(1/6)*mass+mass*distance_to_center**2
        distance = lambda x, y: ((x[0]-y[0])**2 + (x[1]-y[1])**2)**(1/2)
        for _, block in self._blocks.items():
            total_inertia += inertia(block.get_mass(), distance(block.get_coor(), self.get_center_of_mass_coor()))

        self._momentum_of_inertia = total_inertia

    def update(self, time_between_frame:float):
        # call this in main loop
        self.__update_mass()
        self.__update_center_of_mass_coor()
        self.__update_momentum_of_inertia()
        self.move(time_between_frame)