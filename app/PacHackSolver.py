from app.dto.PublicGameState import PublicGameState
from app.dto.PublicPlayer import PublicPlayer
from app.dto.ReturnDirections import ReturnDirections
from app.dto.PointOfInterest import PointOfInterest
from app.dto.HelperDTOs import PublicFields
from app.Pathfinder import Pathfinder

class PacHackSolver:
    initialised = False
    gameFieldsSplitPoint = 0
    isLeftOurHomeSide = True
    lastFoodTargetPosition = (0,0)
    eatedFood = 0

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

        self.improveMap(gState)
        self.printStateNice(gState)
        if (self.eatedFood > 0):
            print("Food in progress: " + str(self.eatedFood))
        
        # our position
        ourPlayer = gState.publicPlayers[gState.agent_id]
        ourPosition = (int(ourPlayer['position'][0]), int(Pathfinder.reverseYCoordinate(len(gState.gameField), ourPlayer['position'][1])))

        target = None
        pathToNearestFood = self.findNearestEatableFood(gState)
        pathToNearestAttackableEnemy = self.findNearestAttackableEnemie(gState)
        print("Path to nearest enemy: " + str(pathToNearestAttackableEnemy))
        if (self.isPositionInHome(ourPosition)):
            print("HOME MODE")
            self.eatedFood = 0
        if (ourPosition == self.lastFoodTargetPosition):
            self.eatedFood = self.eatedFood + 1
        if (self.eatedFood > 4 or not pathToNearestFood):
            target = self.findHome(gState)
            print("===== Target is now HOME!")
        else:
            if (type(pathToNearestFood) is PointOfInterest):
                self.lastFoodTargetPosition = (pathToNearestFood.x, pathToNearestFood.y)
                target = pathToNearestFood
                print("FOOD MODE")

        # attack mode
        if (pathToNearestAttackableEnemy is not None and 
                len(pathToNearestAttackableEnemy.path) < len(pathToNearestFood.path)):
            target = pathToNearestAttackableEnemy
            print("ATTACK MODE")

        pathfinder = Pathfinder()
        if (type(target) is PointOfInterest):
            path = target.path
        else:
            path = pathfinder.find_path_astar(pathfinder.game2Maze(gState), ourPosition, target)
        print("Target path: " + str(path))
        return ReturnDirections.getDirectionForShortcut(path[0])

    def findNearestEatableFood(self, gState):
        foods = []
        pathfinder = Pathfinder()
        generatedMaze = pathfinder.game2Maze(gState)
        ourPlayer = gState.publicPlayers[gState.agent_id]
        ourPosition = (int(ourPlayer['position'][0]), int(Pathfinder.reverseYCoordinate(len(gState.gameField), ourPlayer['position'][1])))

        if (self.isLeftOurHomeSide):
            for x in range(self.gameFieldsSplitPoint, len(gState.gameField[0])):
                for y in range(len(gState.gameField)):
                    if (PublicFields.FOOD == gState.gameField[y][x]):
                        food = PointOfInterest(x, y, pathfinder.find_path_astar(generatedMaze, ourPosition, (x,y)))
                        if (food.path is not None):
                            foods.append(food)
        else:
            for x in range(0, self.gameFieldsSplitPoint - 1):
                for y in range(len(gState.gameField)):
                    if (PublicFields.FOOD == gState.gameField[y][x]):
                        food = PointOfInterest(x, y, pathfinder.find_path_astar(generatedMaze, ourPosition, (x,y)))
                        if (food.path is not None):
                            foods.append(food)
        if (not foods):
            return None
        return min(foods, key=lambda x:len(x.path))

    def findHome(self, gState):
        homePoints = []
        pathfinder = Pathfinder()
        generatedMaze = pathfinder.game2Maze(gState)
        ourPlayer = gState.publicPlayers[gState.agent_id]
        ourPosition = (int(ourPlayer['position'][0]), int(Pathfinder.reverseYCoordinate(len(gState.gameField), ourPlayer['position'][1])))

        x = self.gameFieldsSplitPoint
        if (self.isLeftOurHomeSide):
            x = self.gameFieldsSplitPoint - 1
        
        for y in range(len(gState.gameField)):
            if (PublicFields.WALL != gState.gameField[y][x]):
                homePoint = PointOfInterest(x, y, pathfinder.find_path_astar(generatedMaze, ourPosition, (x, y)))
                homePoints.append(homePoint)

        if (not homePoints):
            return None
        return min(homePoints, key=lambda x:len(x.path))

    def findNearestAttackableEnemie(self, gState):
        enemies = []
        pathfinder = Pathfinder()
        generatedMaze = pathfinder.game2Maze(gState)
        ourPlayer = gState.publicPlayers[gState.agent_id]
        ourPosition = (int(ourPlayer['position'][0]), int(Pathfinder.reverseYCoordinate(len(gState.gameField), ourPlayer['position'][1])))

        if (self.isLeftOurHomeSide):
            for x in range(0, self.gameFieldsSplitPoint - 1):
                for y in range(len(gState.gameField)):
                    if (PublicFields.ENEMY == gState.gameField[y][x]):
                        enemie = PointOfInterest(x, y, pathfinder.find_path_astar(generatedMaze, ourPosition, (x,y)))
                        print("Enemie: " + str(enemie))
                        if (enemie.path is not None):
                            enemies.append(enemie)
        else:
            for x in range(self.gameFieldsSplitPoint, len(gState.gameField[0])):
                for y in range(len(gState.gameField)):
                   if (PublicFields.ENEMY == gState.gameField[y][x]):
                        enemie = PointOfInterest(x, y, pathfinder.find_path_astar(generatedMaze, ourPosition, (x,y)))
                        if (enemie.path is not None):
                            enemies.append(enemie)
            
        if (not enemies):
            return None
        return min(enemies, key=lambda x:len(x.path))

    def isPositionInHome(self, position):
        if (self.isLeftOurHomeSide):
            return position[0] < self.gameFieldsSplitPoint
        else:
            return position[0] >= self.gameFieldsSplitPoint

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
