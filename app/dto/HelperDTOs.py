#Do not use this Directions cause it is only for receiving purposes
class Directions:
    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'
    STOP = 'Stop'

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

class PublicFields:
    EMPTY = " "
    WALL = "%"
    FOOD = "°"
    CAPSULE = "o"
    ENEMY = "E"
    ENEMY_WEAK = "L"
    OURBOT = "X"

