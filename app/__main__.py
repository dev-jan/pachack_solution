import random
import bottle
import os

from app.dto.PublicGameState import PublicGameState
from app.dto.PublicPlayer import PublicPlayer
from app.dto.ReturnDirections import ReturnDirections
from app.PacHackSolver import PacHackSolver

class State:
    solver = PacHackSolver()

@bottle.post('/start')
def start():
    State.solver = PacHackSolver()
    return "SoVollFancy"

@bottle.post('/chooseAction')
def move():
    data = PublicGameState(ext_dict=bottle.request.json)
    return State.solver.getNextDirection(data)

application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
