from app.dto.PublicGameState import PublicGameState
from app.dto.PublicPlayer import PublicPlayer
from app.dto.ReturnDirections import ReturnDirections
from app.dto.HelperDTOs import PublicFields
from app.Pathfinder import Pathfinder

class PacHackSolver:
    initialised = False
    gameFieldsSplitPoint = 0
    isLeftOurHomeSide = True

    def setInitialState(self, gstate):
        self.gameFieldsSplitPoint = int(len(gstate.gameField[0]) / 2)
        ourXPosition = gstate.publicPlayers[gstate.agent_id]['position'][0]

        if (ourXPosition > self.gameFieldsSplitPoint):
            self.isLeftOurHomeSide = False

        print("==== Init game with params:")
        print("   splitpoint: " + str(self.gameFieldsSplitPoint))
        print("   ourSide: " + str(self.isLeftOurHomeSide))
        self.initialised = True

    def getNextDirection(self, gState):
        if (not self.initialised):
            self.setInitialState(gState)
        # prepare for calculation
        self.improveMap(gState)
        self.printStateNice(gState)

        ourPlayer = gState.publicPlayers[gState.agent_id]
        ourPosition = (int(ourPlayer['position'][0]), int(Pathfinder.reverseYCoordinate(len(gState.gameField), ourPlayer['position'][1])))

        target = self.findNearestEatableFood(gState)
        pathfinder = Pathfinder()
        path = pathfinder.find_path_astar(pathfinder.game2Maze(gState), ourPosition, target)
        
        print("Target path: " + str(path))

        return ReturnDirections.getDirectionForShortcut(path[0])

    def findNearestEatableFood(self, gState):
        # todo: better?
        if (self.isLeftOurHomeSide):
            for x in range(self.gameFieldsSplitPoint, len(gState.gameField[0])):
                for y in range(len(gState.gameField)):
                    if (PublicFields.FOOD == gState.gameField[y][x]):
                        print("Target field: " + str(x) + " " + str(y))
                        return (x, y)
        return None

    def improveMap(self, gState):
        # reverse map
        newMap = []
        newY = 0
        for y in reversed(range(len(gState.gameField))):
            newMap.append([])
            for x in range(len(gState.gameField[y])):
                newMap[newY].append(gState.gameField[y][x])
            newY = newY + 1
        gState.gameField = newMap

        # set our position
        ourselfe = gState.publicPlayers[gState.agent_id]
        ourX = ourselfe['position'][0]
        ourY = Pathfinder.reverseYCoordinate(len(gState.gameField), ourselfe['position'][1])
        gState.gameField[int(ourY)][int(ourX)] = "X"

        # set enemie positions
        for enemieId in range(len(gState.publicPlayers)):
            if (enemieId != gState.agent_id):
                enemie = gState.publicPlayers[enemieId]
                enemieX = enemie['position'][0]
                enemieY = Pathfinder.reverseYCoordinate(len(gState.gameField), enemie['position'][1])
                enemieSymbol = 'E'
                if (enemie['weakened']):
                    enemieSymbol = 'F'
                gState.gameField[int(enemieY)][int(enemieX)] = enemieSymbol

    def printStateNice(self, gState):
        print("Game State:")
        print("Field:")
        for y in range(len(gState.gameField)):
            for x in range(len(gState.gameField[y])):
                print(gState.gameField[y][x], end =" ")
            print()
