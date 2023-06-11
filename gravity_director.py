from block_mechanism import BlockMechanism
G = 6.674*(10**(-11))
class GravityDirector():
    def __init__(self, mass:float, loc:tuple, time_between_frame:float):
        self.__mass = mass
        self.__loc = loc
        self.__time_between_frame = time_between_frame

    def add_gravity(self, player:BlockMechanism):
        force = None
        player_loc = player.get_center_of_mass_coor()
        relative_loc = ((player_loc[0]-self.__loc[0]), (player_loc[1]-self.__loc[1]))
        distance = (relative_loc[0]**2+relative_loc[1]**2)**(1/2)
        #print("distance", distance)

        if distance == 0:
            force = (0, 0)
        else:
            unit_relative_force = (-relative_loc[0]/distance, -relative_loc[1]/distance)
            force_scalar = G*self.__mass*player.get_mass()*(distance**2)
            force = (force_scalar*unit_relative_force[0], force_scalar*unit_relative_force[1])

        player.add_force(force, player.get_center_of_mass_coor(), self.__time_between_frame)

    def set_mass(self, mass:float):
        self.__mass = mass

    def get_mass(self):
        return self.__mass

        