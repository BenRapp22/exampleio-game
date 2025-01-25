import math

from bullet import Bullet

DIRECTION_UP = 0
DIRECTION_DOWN = math.pi

def testDestroyedIfOffMap():
    bullet = Bullet('test-id', 1, 1, DIRECTION_UP)
    assert bullet.update(1) # Should return true if the bullet is off the map

def testLivesIfOnMap():
    bullet = Bullet('test-id', 1, 1, DIRECTION_DOWN)
    assert not bullet.update(1)