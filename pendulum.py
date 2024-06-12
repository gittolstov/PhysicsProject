from vector import Vector, projections


class Pendulum(Vector):#representation of pendulum in memory
    def __init__(self, x=500, y=500, gravity=0.1):
        self.time = 0
        self.log = {
            "self": {
                'x': [],
                'y': []
            },
            "speed": {
                'x': [],
                'y': []
            },
            "gravity": {
                'x': [],
                'y': []
            },
            "tension": {
                'x': [],
                'y': []
            },
            "full_energy": []
        }
        super().__init__(0, y)
        self.base_values = [x, y, gravity]
        self.starting_point_x = x
        self.starting_point_y = 0
        self.reset()

    def log_state(self):
        self.time += 1
        self.log["self"]["x"].append(self.x)
        self.log["self"]["y"].append(self.y)
        self.log["speed"]["x"].append(self.speed.x)
        self.log["speed"]["y"].append(self.speed.y)
        self.log["gravity"]["x"].append(self.gravity.x)
        self.log["gravity"]["y"].append(self.gravity.y)
        self.log["tension"]["x"].append(self.tension.x)
        self.log["tension"]["y"].append(self.tension.y)
        self.log["full_energy"].append(self.full_energy)

    def draw(self, animator):#should be in every model
        self.store_sliders()
        #print(self.x + self.starting_point_x, self.y + self.starting_point_y)
        #animator.goto(self.x + self.starting_point_x, self.y + self.starting_point_y)
        draw_string = ""
        draw_string += animator.circle(self.starting_point_x + self.x, self.starting_point_y + self.y, 40, "6", "red")
        draw_string += animator.line(self.starting_point_x, self.starting_point_y, self.starting_point_x + self.x, self.starting_point_y + self.y, "3", "black")
        draw_string += animator.line(self.starting_point_x + self.x, self.starting_point_y + self.y, self.starting_point_x + self.x + self.speed.x * 10, self.starting_point_y + self.y + self.speed.y * 10, "4", "green")
        draw_string += animator.line(self.starting_point_x + self.x, self.starting_point_y + self.y, self.starting_point_x + self.x + self.tension.x * 200, self.starting_point_y + self.y + self.tension.y * 200, "3", "red")
        draw_string += animator.line(self.starting_point_x + self.x, self.starting_point_y + self.y, self.starting_point_x + self.x + self.gravity.x * 200, self.starting_point_y + self.y + self.gravity.y * 200, "3", "red")
        return draw_string

    def reset(self):#should be in every model
        x = self.base_values[0]
        y = self.base_values[1]
        gravity = self.base_values[2]
        self.x = 0
        self.y = y
        self.baseLength = self.length()
        self.gravity = Vector(0, gravity, self)
        self.tension = Tension(0, -gravity, self)
        self.speed = Vector(5, 0, self)
        self.speed.mark_forces(self.gravity)
        self.speed.mark_forces(self.tension)
        self.mark_forces(self.speed)
        self.full_energy = 0
        self.recalculate_full_energy()
        self.sliders = ""

    def store_sliders(self):
        self.sliders = ""
        a = [
            "get_kinetic_energy",
            "get_speed",
            "get_base_length",
            "get_gravity"
        ]
        for i in a:
            self.sliders += i + " " + str(getattr(self, i)()) + ";"

    def recalculate_full_energy(self):
        self.full_energy = self.get_kinetic_energy() + self.get_potential_energy()

    def get_kinetic_energy(self):
        return self.speed.length() ** 2 / 2

    def set_kinetic_energy(self, num):
        self.speed.set_length(abs(num * 2) ** 0.5 * num/abs(num))

    def get_speed(self):
        return self.speed.length()

    def set_speed(self, num):
        self.speed.set_length(num)
        self.recalculate_full_energy()

    def get_base_length(self):
        return self.length()

    def set_base_length(self, num):
        self.baseLength = num
        self.model_implications()
        self.recalculate_full_energy()

    def get_gravity(self):
        return self.gravity.length()

    def set_gravity(self, num):
        self.gravity.y = num

    def hardset_kinetic_energy(self, num):
        self.speed.set_length(abs(num * 2) ** 0.5 * num/abs(num))
        self.recalculate_full_energy()

    def get_potential_energy(self):
        return self.gravity.length() * (self.starting_point_y + self.baseLength - self.y)

    def tick1(self):
        self.model_implications()

    def tick2(self):
        self.apply_forces()
        self.log_state()

    def model_implications(self):
        if self.y < self.starting_point_y:
            self.speed.zero_out()
        self.set_length(self.baseLength)
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
