from vector import Vector

class Pendulum:
    def __init__(self, x=500, y=500, gravity=0.05):
        self.x = x
        self.y = y
        self.gravity = Vector(0, gravity)
        self.tension = Vector(0, -gravity)
        self.speed = Vector(0.5, 0)
        self.speed.mark_forces(self.gravity)
        self.speed.mark_forces(self.tension)
        def a():
            self.turnToCoordinates(500, 0, PENDULUM.x, PENDULUM.y)
        self.tension.tick_move = a

PENDULUM = Pendulum()