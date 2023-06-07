from block_assembly import BlockAssembly
from block_mechanism import BlockMechanism
class Game:
    def __init__(self, pygame_screen, background: str = None) -> None:
        self._players = []  # list of players(BlockAssembly)
        self._objects = []   # list of objects(like bullet)
        self._phase = "build"
        self._background = background
        self._screen = pygame_screen
    
    def add_players(self, player1:BlockMechanism, player2:BlockMechanism):
        self._players = []
        player1.set_oppo(player2)
        player2.set_oppo(player1)
        self._players.append(player1)
        self._players.append(player2)

    def get_player(self, index: int):
        # Return players[index](BlockAssembly)
        return self._players[index]

    def add_object(self, object) -> None:
        # Add object to objects
        self._objects.append(object)

    def remove_object(self, object) -> None:
        # Remove object from objects
        self._objects.remove(object)

    def run(self) -> None:
        # Call this in main loop
        pass

    def get_phase(self) -> str:
        return self._phase

    def set_phase(self, phase: str) -> None:
        self._phase = phase

    def is_valid(self, instruction) -> bool:
        # Check if the instruction is valid for current stage
        condition = None
        if condition:
            return False
        return True

    def act(self, player, action) -> None:
        # Apply action on the player
        pass

    def draw(self, zero_vector:tuple, unit_size:int) -> None:
        # Draw background, players and objects(follow the order)
        # render called below are all undefined yet

        # TODO: make background alive
        # self._background.render()

        for object in self._objects:
            # TODO: add zero vector and unit size so the game wont break
            object.render(self._screen)

        for player in self._players:
            player.render(self._screen, zero_vector, unit_size)
        
        pass
