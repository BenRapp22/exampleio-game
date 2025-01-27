from bullet import Bullet
from collisions import applyCollisions
from player import Player

import constants

def testApplyCollisions():
    distance_from_player = constants.BULLET_RADIUS + constants.PLAYER_RADIUS + 1
    players = [
        Player('1', 'guest1', 1000, 40),
        Player('2', 'guest2', 2000, 2000)
    ]
    bullets = [
        Bullet('2', 1000-distance_from_player, 40, 0),
        Bullet('2', 1000+distance_from_player, 40, 0)
    ]
    result = applyCollisions(players, bullets)
    assert len(result) == 0

def testNoSelfHarm():
    playerID = '1234'
    p = Player(playerID, 'guest', 40, 40)
    b = Bullet(playerID, 40, 40, 0)
    result = applyCollisions([p], [b])
    assert len(result) == 0

def testHarmOthers(mocker):
    p = Player('1', 'guest', 40, 40)
    b = Bullet('2', 40, 40 + constants.BULLET_RADIUS + constants.PLAYER_RADIUS, 0)

    spy = mocker.spy(p, 'takeBulletDamage')

    result = applyCollisions([p], [b])
    assert len(result) == 1
    assert b in result
    assert spy.call_count == 1
