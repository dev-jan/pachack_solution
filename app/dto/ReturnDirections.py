import random


class ReturnDirections():
    NORTH = '\"North\"'
    SOUTH = '\"South\"'
    EAST = '\"East\"'
    WEST = '\"West\"'
    STOP = '\"Stop\"'

    LEFT = {NORTH: WEST,
            SOUTH: EAST,
            EAST: NORTH,
            WEST: SOUTH,
            STOP: STOP}

    RIGHT = dict([(y, x) for x, y in LEFT.items()])

    REVERSE = {NORTH: SOUTH,
               SOUTH: NORTH,
               EAST: WEST,
               WEST: EAST,
               STOP: STOP}

    @classmethod
    def random(cls):
        return random.choice(
            [ReturnDirections.SOUTH, ReturnDirections.NORTH, ReturnDirections.EAST, ReturnDirections.WEST,
             ReturnDirections.STOP])

    # shortname = N, W, E, S
    @classmethod
    def getDirectionForShortcut(cls, shortname):
        switcher = {
            'N': ReturnDirections.NORTH,
            'S': ReturnDirections.SOUTH,
            'W': ReturnDirections.WEST,
            'E': ReturnDirections.EAST
        }
        return switcher.get(shortname, ReturnDirections.STOP)
