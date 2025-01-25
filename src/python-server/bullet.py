from object import Object
import constants

import uuid

class Bullet(Object):
    def __init__(self, parentID, x, y, dir):
        super().__init__(uuid.uuid4(), x, y, dir, constants.BULLET_SPEED)
        self.parentID = parentID
    
    def update(self, dt):
        """Returns true if the bullet should be destroyed
            dt: delta value for update
        """
        super().update(dt)
        return self.x < 0 or self.x > constants.MAP_SIZE or self.y < 0 or self.y > constants.MAP_SIZE
    

if __name__ == '__main__':
    import math
    bullet = Bullet('test-id', 1, 1, math.pi)
    bullet.update(1)