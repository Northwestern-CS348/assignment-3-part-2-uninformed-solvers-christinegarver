
from solver import *
from queue import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        #self.visits = []
        super().__init__(gameMaster, victoryCondition)


    @property
    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        old_state = self.currentState
        movables = self.gm.getMovables()
        current_depth = self.currentState.depth
        found = False
        i = 0

        if self.victoryCondition == self.currentState.state:
            return True

        while i < len(movables):
            next_move = movables[i]

            self.gm.makeMove(next_move)
            new_state = GameState(self.gm.getGameState(), current_depth + 1, next_move)

            new_state.parent = self.currentState
            self.currentState.children.append(new_state)

            self.gm.reverseMove(next_move)

            i += 1

        j = self.currentState.nextChildToVisit
        while j < len(self.currentState.children):
            child = self.currentState.children[self.currentState.nextChildToVisit]
            self.currentState.nextChildToVisit += 1
            if child not in self.visited:
                self.visited[child] = True
                self.gm.makeMove(child.requiredMovable)
                self.currentState = child
                found = True
                break
            j += 1

        if not found:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = old_state

        if self.victoryCondition == self.currentState.state:
            return True

        return False





class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        return True


