from vector import Vector, projections


class Pendulum(Vector):#representation of pendulum in memory
    def __init__(self, x=500, y=500, gravity=0.1):
        super().__init__(0, y)
        self.starting_point_x = x
        self.starting_point_y = 0
        self.gravity = Vector(0, gravity, self)
        self.tension = Tension(0, -gravity, self)
        self.speed = Vector(5, 0, self)
        self.speed.mark_forces(self.gravity)
        self.speed.mark_forces(self.tension)
        self.mark_forces(self.speed)
        self.full_energy = self.get_kinetic_energy() + self.get_potential_energy()

    def draw(self, animator):
        #print(self.x + self.starting_point_x, self.y + self.starting_point_y)
        #animator.goto(self.x + self.starting_point_x, self.y + self.starting_point_y)
        draw_string = ""
        draw_string += animator.circle(self.starting_point_x + self.x, self.starting_point_y + self.y, 25, "3", "black")
        draw_string += animator.line(self.starting_point_x, self.starting_point_y, self.starting_point_x + self.x, self.starting_point_y + self.y, "3", "black")
        draw_string += animator.line(self.starting_point_x + self.x, self.starting_point_y + self.y, self.starting_point_x + self.x + self.speed.x * 10, self.starting_point_y + self.y + self.speed.y * 10, "4", "green")
        draw_string += animator.line(self.starting_point_x + self.x, self.starting_point_y + self.y, self.starting_point_x + self.x + self.tension.x * 200, self.starting_point_y + self.y + self.tension.y * 200, "3", "red")
        draw_string += animator.line(self.starting_point_x + self.x, self.starting_point_y + self.y, self.starting_point_x + self.x + self.gravity.x * 200, self.starting_point_y + self.y + self.gravity.y * 200, "3", "red")
        return draw_string

    def get_kinetic_energy(self):
        return self.speed.length() ** 2 / 2

    def set_kinetic_energy(self, num):
        self.speed.set_length(abs(num * 2) ** 0.5 * num/abs(num))

    def get_potential_energy(self):
        return self.gravity.length() * (self.starting_point_y + 500 - self.y)

    def tick1(self):
        self.model_implications()

    def tick2(self):
        self.apply_forces()

    def model_implications(self):
        if self.y < self.starting_point_y:
            self.speed.zero_out()
        self.set_length(500)
        a = self.judge_speed_direction()
        self.speed.turn_to(-self.x, -self.y)
        self.speed.get_perpendicular(a)
        self.set_kinetic_energy(self.full_energy - self.get_potential_energy())


    def judge_speed_direction(self):
        if self.speed.length() > 0.005:
            return -(self.speed.x + 0.000001) / abs(self.speed.x + 0.000001)
        return int(self.x < 0) * 2 - 1


    def get_working_vectors(self):
        return [self, self.gravity, self.tension, self.speed]


class Tension(Vector):
    def __init__(self, x, y, aux):
        super().__init__(x, y, aux)

    def tick2(self):
        a = projections(self.x, self.y, self.backlink.gravity.length())
        self.set_length(-a["y"])
        self.turn_to(-self.backlink.x, -self.backlink.y)


if __name__ == "__main__":
    PENDULUM = Pendulum()
