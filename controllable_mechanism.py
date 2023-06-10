from block_mechanism import BlockMechanism
from leaf_blocks import CoreBlock
import pygame
from sound import Sounds

CORE_FORCE = 5000
class ControllableMechansim(BlockMechanism):
    def __init__(self, core_block: CoreBlock, momentum:tuple = (0, 0)):
        super().__init__(core_block, momentum)
        self._channel = pygame.mixer.find_channel()

    def core_move_up(self, time_between_frame:float) -> None:
        self.add_force((0, -CORE_FORCE), self.get_coor(), time_between_frame)
        if not self._channel.get_busy():
            self._channel.play(Sounds.THRUSTER_BURN)

    def core_move_down(self, time_between_frame:float) -> None:
        self.add_force((0, CORE_FORCE), self.get_coor(), time_between_frame)
        if not self._channel.get_busy():
            self._channel.play(Sounds.THRUSTER_BURN)

    def core_move_left(self, time_between_frame:float) -> None:
        self.add_force((-CORE_FORCE, 0), self.get_coor(), time_between_frame)
        if not self._channel.get_busy():
            self._channel.play(Sounds.THRUSTER_BURN)

    def core_move_right(self, time_between_frame:float) -> None:
        self.add_force((CORE_FORCE, 0), self.get_coor(), time_between_frame)
        if not self._channel.get_busy():
            self._channel.play(Sounds.THRUSTER_BURN)
