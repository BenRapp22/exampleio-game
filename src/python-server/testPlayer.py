from player import Player
from bullet import Bullet
import constants

def testGainScoreEachSecond():
    p = Player('123', 'guest', 1, 1)
    init_score = p.score

    p.update(1)

    assert p.score > init_score


def testFireBullet():
    p = Player('123', 'guest', 1, 1)
    assert isinstance(p.update(constants.PLAYER_FIRE_COOLDOWN/3), Bullet)


def testCooldown():
    p = Player('123', 'guest', 1, 1)
    p.update(constants.PLAYER_FIRE_COOLDOWN/3)
    assert p.update(constants.PLAYER_FIRE_COOLDOWN / 3) is None


def testTakeBulletDamage():
    p = Player('123', 'guest', 1, 1)
    init_hp = p.hp

    p.takeBulletDamage()

    assert p.hp < init_hp

def testOnDealtDamage():
    p = Player('123', 'guest', 1, 1)
    init_score = p.score

    p.onDealtDamage()

    assert p.score > init_score

def testSerializeForUpdate():
    p = Player('123', 'guest', 1, 1)
    serialized = p.serializeForUpdate()
    assert serialized.get('hp') == constants.PLAYER_MAX_HP and serialized.get('direction') is not None