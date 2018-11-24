from app.dto.PublicGameState import PublicGameState
from app.dto.PublicPlayer import PublicPlayer
from app.dto.ReturnDirections import ReturnDirections

class PacHackSolver:
    initialised = False
    gameFieldsSplitPoint = 0
    gameOurSide = 0

    def setInitialState(self, gstate):
        gameFieldsSplitPoint = len(gstate.gameField[0]) / 2
        ourXPosition = gstate.publicPlayers[gstate.agent_id]['position'][0]

        if (ourXPosition > gameFieldsSplitPoint):
            gameOurSide = 1

        print("==== Init game with params:")
        print("   splitpoint: " + str(gameFieldsSplitPoint))
        print("   ourSide: " + str(gameOurSide))
        self.initialised = True

    def getNextDirection(self, gState):
        self.improveMap(gState)
        self.printStateNice(gState)
        if (not self.initialised):
            self.setInitialState(gState)
        return ReturnDirections.random()

    def improveMap(self, gState):
        # set our position
        ourselfe = gState.publicPlayers[gState.agent_id]
        ourX = ourselfe['position'][0]
        ourY = ourselfe['position'][1]
        gState.gameField[int(ourY)][int(ourX)] = "X"

        # set enemie positions
        for enemieId in range(len(gState.publicPlayers)):
            if (enemieId != gState.agent_id):
                enemie = gState.publicPlayers[enemieId]
                enemieX = enemie['position'][0]
                enemieY = enemie['position'][1]
                enemieSymbol = 'E'
                if (enemie['weakend']):
                    enemieSymbol = 'F'
                gState.gameField[int(enemieY)][int(enemieX)] = enemieSymbol

    def printStateNice(self, gState):
        print("Game State:")
        print("Field:")
        for x in reversed(range(len(gState.gameField))):
            for y in range(len(gState.gameField[x])):
                print(gState.gameField[x][y], end =" ")
            print()
