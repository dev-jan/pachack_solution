from heapq import heappop, heappush
from app.dto.HelperDTOs import PublicFields

class Pathfinder:
    # MAZE:
    #  0 = Empty field
    #  1 = Impossible field (wall)
    #  example for position start = (1, 1)
    def find_path_astar(self, maze, start, goal):
        print("Start: " + str(start))
        print("End: " + str(goal))
        start = (start[1], start[0])
        goal = (goal[1], goal[0])
        pr_queue = []
        heappush(pr_queue, (0 + self.heuristic(start, goal), 0, "", start))
        visited = set()
        graph = self.maze2graph(maze)
        while pr_queue:
            _, cost, path, current = heappop(pr_queue)
            if current == goal:
                return path
            if current in visited:
                continue
            visited.add(current)
            for direction, neighbour in graph[current]:
                heappush(pr_queue, (cost + self.heuristic(neighbour, goal), cost + 1,
                                    path + direction, neighbour))
        return None

    def game2Maze(self, gState):
        maze = []
        newY = 0
        for y in range(len(gState.gameField)):
            maze.append([])
            for x in range(len(gState.gameField[y])):
                field = gState.gameField[y][x]
                switcher = {
                    PublicFields.WALL: 1,
                    PublicFields.EMPTY: 0,
                    PublicFields.FOOD: 0,
                    PublicFields.CAPSULE: 0,
                    'X': 0,
                    'L': 1,
                    'E': 1
                }
                maze[newY].append(switcher.get(field, 1))
            newY = newY + 1
        print("MAZE: ")
        for y in range(len(maze)):
            for x in range(len(maze[y])):
                print(maze[y][x], end =" ")
            print("")
        return maze

    def maze2graph(self, maze):
        height = len(maze)
        width = len(maze[0]) if height else 0
        graph = {(i, j): [] for j in range(width) for i in range(height) if not maze[i][j]}
        for row, col in graph.keys():
            if row < height - 1 and not maze[row + 1][col]:
                graph[(row, col)].append(("S", (row + 1, col)))
                graph[(row + 1, col)].append(("N", (row, col)))
            if col < width - 1 and not maze[row][col + 1]:
                graph[(row, col)].append(("E", (row, col + 1)))
                graph[(row, col + 1)].append(("W", (row, col)))
        return graph

    def heuristic(self, cell, goal):
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

    @classmethod
    def reverseYCoordinate(cls, mazeSize, originalY):
        return mazeSize - originalY - 1