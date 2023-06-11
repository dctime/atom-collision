from game_state import GameState


class minimaxAgent():
    def __init__(self, index: int = 1, depth="2") -> None:
        self._index = index
        self._depth = depth

        # 2 players by default
        self._oppo = 1 if self._index == 0 else 1

    def eval(self, gameState: GameState) -> float:
        player = self._index
        opponent = self._oppo

        block_num_diff = gameState.agent[player].block_num() - \
            gameState.agent[opponent].block_num()
        total_hp_diff = gameState.agent[player].total_hp() - \
            gameState.agent[opponent].total_hp()
        core_hp_diff = gameState.agent[player].core_hp() - \
            gameState.agent[opponent].core_hp()
        win = not gameState.agent[opponent].alive()
        lose = not gameState.agent[player].alive()

        weights = [1, 2, 10, 100, -100]
        features = [block_num_diff, total_hp_diff, core_hp_diff, win, lose]
        score = 0
        for i in range(len(weights)):
            score += weights[i]*features[i]
        return score

    def get_legal_action(self):
        pass

    def getAction(self, gameState):
        # Recursive minimax algorithm
        def minimax(gameState, depth, agent, agent_num):
            if agent >= agent_num:
                agent = 0
                depth -= 1

            if depth == 0 or gameState.isWin() or gameState.isLose():
                return (self.eval(gameState), "_")
            token_act = None
            val = None
            # Max layer
            if agent == 0:
                val = float("-inf")
                for act in gameState.getLegalActions(agent):
                    nxtState = gameState.getNextState(agent, act)
                    score, _ = minimax(nxtState, depth, (agent + 1), agent_num)
                    if score > val:
                        val = score
                        token_act = act
                return (val, token_act)

            # Min layer
            else:
                val = float("inf")
                for act in gameState.getLegalActions(agent):
                    nxtState = gameState.getNextState(agent, act)
                    score, _ = minimax(nxtState, depth, (agent + 1), agent_num)
                    if score < val:
                        val = score
                        token_act = act
                return (val, token_act)

        n = gameState.getNumAgents()
        _, best_act = minimax(gameState, self.depth, 0, n)

        return best_act
