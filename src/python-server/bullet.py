from object import Object
import constants

import uuid

class Bullet(Object):
    def __init__(self, parentID, x, y, dir):
        super().__init__(uuid.uuid4(), x, y, dir, constants.BULLET_SPEED)
        self.parentID = parentID
    
    def update(self, dt):
        super.update(dt)
        return self.x < 0 or self.x > constants.MAP_SIZE or self.y < 0 or self.y > constants.MAP_SIZE
    