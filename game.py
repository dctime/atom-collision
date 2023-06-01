class game:
    def __init__(self, background: str = None) -> None:
        self._players = []  # list of players(BlockAssembly)
        self._objects = []   # list of objects(like bullet)
        self._phase = "build"
        self._background = background

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

    def draw(self) -> None:
        # Draw background, players and objects(follow the order)
        # render called below are all undefined yet

        self._background.render()
        for player in self._players:
            player.render()
        for object in self._objects:
            object.render()
        pass
