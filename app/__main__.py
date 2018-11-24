import random
import bottle
import os

from app.dto.PublicGameState import PublicGameState
from app.dto.PublicPlayer import PublicPlayer
from app.dto.ReturnDirections import ReturnDirections

bottle.post('/start')
def start():
    return "SoVollFancy"


@bottle.post('/chooseAction')
def move():
    data = PublicGameState(ext_dict=bottle.request.json)
    data.agent_id
    # print gamestate to console
    print("State: ")
    print(data)

    # TODO: Do things with data acces via data
    return ReturnDirections.random()

application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))