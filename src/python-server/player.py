from object import Object
from bullet import Bullet
import constants

import math
import random

class Player(Object):
    def __init__(self, id, username, x, y):
        super().__init__(id=id, x=x, y=y, dir=random.random()*2*math.pi, speed=constants.PLAYER_SPEED)
        self.username = username
        self.hp = constants.PLAYER_MAX_HP
        self.fireCooldown = 0
        self.score = 0

    
    def update(self, dt):
        super().update(dt=dt)

        self.score += dt * constants.SCORE_PER_SECOND

        self.x = max(0, min(constants.MAP_SIZE, self.x))
        self.y = max(0, min(constants.MAP_SIZE, self.y))

        self.fireCooldown -= dt
        if self.fireCooldown <= 0:
            self.fireCooldown += constants.PLAYER_FIRE_COOLDOWN
            return Bullet(self.id, self.x, self.y, self.dir)


        return None

    def takeBulletDamage(self):
        self.hp -= constants.BULLET_DAMAGE
    
    def onDealtDamage(self):
        self.score += constants.SCORE_BULLET_HIT
    
    def serializeForUpdate(self):
        return {
            **super().serializeForUpdate(),
            'direction':self.dir,
            'hp':self.hp
        }
