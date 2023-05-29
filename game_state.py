class GameState():
    def __init__(self) -> None:
        self.agents = []
        self.x_upper_bound, self.x_lower_bound = [100, 0]
        self.y_upper_bound, self.y_lower_bound = [100, 0]

    def getLegalActions(self, agentIndex: int) -> list:
        agent = self.agents[agentIndex]
        move_x = ["right", "left"]
        move_y = ["down", "up"]
        attack = ["sword", "cannon", "hammer"]
        pass

    def getNextState(self, gameState: GameState, action: tuple) -> GameState:
        pass

    def getNumAgents(self) -> int:
        return len(self.agents)

    def addAgents(self, agent) -> None:
        self.agents.append(agent)

    def isEnd(self) -> bool:
        return not self.agents[0].alive or not self.agents[1].alive
