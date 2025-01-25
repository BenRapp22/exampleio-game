import math

class Object:
    def __init__(self,id, x, y, dir, speed):
        self.id=id
        self.x=x
        self.y=y
        self.dir=dir
        self.speed=speed

    def update(self, dt):
        self.x += dt * self.speed * math.sin(self.dir);
        self.y -= dt * self.speed * math.cos(self.dir);
    
    def distanceTo(self, obj):
        dx = self.x - obj.x
        dy = self.y - obj.y
        return math.sqrt(dx**2 + dy**2)

    def setDirection(self, dir):
        self.dir = dir
    
    def serializeForUpdate(self):
        return {
            'id': self.id,
            'x': self.x,
            'y': self.y,
        }
    
