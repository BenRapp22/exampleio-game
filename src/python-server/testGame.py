from game import Game
import constants
import datetime

def testUpdatesOnInterval(): 
    game = Game()

    game.lastUpdateTime = int(datetime.datetime.now().timestamp() * 1000) - 10
    initialCreatedTime = game.lastUpdateTime

    assert game.lastUpdated != initialCreatedTime

def testSendUpdatesOnSecondUpdate(mocker):
    game = Game()
    socket = {
        'id':'1234',
        'emit':mocker.patch()
    }
    game.addPlayer(socket, 'guest')
    ...

# TODO Need to replicate socket.emit behavior using a python class. Need to make Socket().