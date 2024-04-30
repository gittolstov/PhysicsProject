from vector import Vector

class Pendulum(Vector):#representation of pendulum in memory
    def __init__(self, x=500, y=500, gravity=0.05):
        super().__init__(0, y)
        self.starting_point_x = x
        self.starting_point_y = 0
        self.gravity = Vector(0, gravity, self)
        self.tension = Tension(0, -gravity, self)
        self.speed = Vector(0.5, 0, self)
        self.speed.mark_forces(self.gravity)
        self.speed.mark_forces(self.tension)
        self.mark_forces(self.speed)

    def draw(self, animator):
        print(self.x + self.starting_point_x, self.y + self.starting_point_y)
        #animator.goto(self.x + self.starting_point_x, self.y + self.starting_point_y)

    def tick2(self):
        self.model_implications()

    def model_implications(self):
        if self.y < self.starting_point_y:
            self.speed.zero_out()
        self.set_length(500)

    def get_working_vectors(self):
        return [self, self.gravity, self.tension, self.speed]


class Tension(Vector):
    def __init__(self, x, y, aux):
        super().__init__(x, y, aux)

    def tick2(self):
        self.turn_to_coordinate(
            self.backlink.starting_point_x,
            self.backlink.starting_point_y,
            self.backlink.x + self.backlink.starting_point_x,
            self.backlink.y + self.backlink.starting_point_y
        )


if __name__ == "__main__":
    PENDULUM = Pendulum()
