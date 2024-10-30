import math

from vector import Vector, projections
from log_parser import cut_log
from math import sin, cos, asin, atan


class Pendulum(Vector):#representation of pendulum in memory
    def __init__(self, x=500, y=750, gravity=0.1):
        super().__init__(0, y)
        self.base_values = [x, y, gravity]
        self.starting_point_x = x
        self.starting_point_y = 0
        self.reset()

    def reset(self):#should be in every model
        self.setters_and_getters = {#should be in every model
            "setters": [
                "hardset_kinetic_energy",
                "set_speed",
                "set_base_length",
                "set_gravity",
                "set_potential_energy",
                "set_angle"
            ],
            "getters": [
                "get_kinetic_energy",
                "get_speed",
                "get_base_length",
                "get_gravity",
                "get_potential_energy",
                "get_angle"
            ],
            "names": [
                "Кинетическая энергия",
                "Скорость",
                "Длина",
                "Ускорение свободного падения",
                "Потенциальная энергия",
                "Угол отклонения (в градусах)"
            ],
            "modifiers": [
                "10",
                "20",
                "0.5",
                "2000",
                "10",
                "5"
            ],
            "shifts": [
                "0",
                "0",
                "0",
                "0",
                "0",
                "250"
            ]
        }
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
            "full_energy": [],
            "simulation_type": "Pendulum"
        }
        self.time = 0
        self.reset_forces()
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

    def get_graph(self, data):#should be in every model, returns graph arrays for each slider
        arr = []
        if data == "0":
            for i in range(len(self.log["speed"]["x"])):
                arr.append((self.log["speed"]["x"][i] ** 2 + self.log["speed"]["y"][i] ** 2) / 2)
        elif data == "1":
            for i in range(len(self.log["speed"]["x"])):
                arr.append((self.log["speed"]["x"][i] ** 2 + self.log["speed"]["y"][i] ** 2) ** 0.5)
        elif data == "2":
            for i in range(len(self.log["self"]["x"])):
                arr.append((self.log["self"]["x"][i] ** 2 + self.log["self"]["y"][i] ** 2) ** 0.5)
        elif data == "3":
            for i in range(len(self.log["gravity"]["x"])):
                arr.append((self.log["gravity"]["x"][i] ** 2 + self.log["gravity"]["y"][i] ** 2) ** 0.5)
        elif data == "4":
            for i in range(len(self.log["self"]["y"])):
                arr.append((self.log["gravity"]["x"][i] ** 2 + self.log["gravity"]["y"][i] ** 2) ** 0.5 * (self.starting_point_y + self.baseLength - self.log["self"]["y"][i]))
        elif data == "5":
            for i in range(len(self.log["self"]["x"])):
                arr.append(atan(self.log["self"]["x"][i] / self.log["self"]['y'][i]) * 180 / math.pi)
        for i in range(len(arr)):
            arr[i] *= float(self.setters_and_getters["modifiers"][int(data)])
            arr[i] = str(arr[i])
        return arr

    def log_state(self):#should be in every model
        if self.time < len(self.log["self"]["x"]):
            cut_log(self.log, self.time)
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

    def apply_log(self, log, frame):#should be in every model, applies frames from log
        print(log)
        if frame >= len(log["self"]["x"]):
            print("frame index out of range")
            return
        self.x = log["self"]["x"][frame]
        self.y = log["self"]["y"][frame]
        self.speed.x = log["speed"]["x"][frame]
        self.speed.y = log["speed"]["y"][frame]
        self.gravity.x = log["gravity"]["x"][frame]
        self.gravity.y = log["gravity"]["y"][frame]
        self.tension.x = log["tension"]["x"][frame]
        self.tension.y = log["tension"]["y"][frame]
        self.full_energy = log["full_energy"][frame]

    def draw(self, animator):#should be in every model
        self.store_sliders()
        #print(self.x + self.starting_point_x, self.y + self.starting_point_y)
        #animator.goto(self.x + self.starting_point_x, self.y + self.starting_point_y)
        draw_string = ""
        r = (self.baseLength ** 2 - ((self.full_energy / self.gravity.length()) - self.starting_point_y - self.baseLength) ** 2) ** 0.5
        draw_string += animator.circle(self.starting_point_x, self.starting_point_y + 500, r, "2", "lightgrey")
        y2 = self.starting_point_y + 500 + self.speed.x / abs(self.speed.x + 0.00001) * (r ** 2 - self.x ** 2) ** 0.5
        draw_string += animator.circle(self.starting_point_x + self.x, y2, 4, "8", "red")
        draw_string += animator.line(self.starting_point_x + self.x, y2, self.starting_point_x + self.x, self.starting_point_y + self.y, 1, "red")
        draw_string += animator.pendulum(self.starting_point_x + self.x, self.starting_point_y + self.y, 40)
        draw_string += animator.line(self.starting_point_x, self.starting_point_y, self.starting_point_x + self.x, self.starting_point_y + self.y, "3", "black")
        sc = self.gravity.x * self.speed.x + self.gravity.y * self.speed.y
        temp = projections(self.speed.x, self.speed.y, sc / self.speed.length())
        temp["x"] *= 1000
        temp["y"] *= 1000
        draw_string += animator.vector(self.starting_point_x + self.x, self.starting_point_y + self.y, self.starting_point_x + self.x + temp["x"], self.starting_point_y + self.y + temp["y"], "6", "lightblue")
        draw_string += animator.vector(self.starting_point_x + self.x, self.starting_point_y + self.y, self.starting_point_x + self.x + self.speed.x * 30, self.starting_point_y + self.y + self.speed.y * 30, "6", "green")
        draw_string += animator.vector(self.starting_point_x + self.x, self.starting_point_y + self.y, self.starting_point_x + self.x + self.tension.x * 1000, self.starting_point_y + self.y + self.tension.y * 1000, "4", "red")
        draw_string += animator.vector(self.starting_point_x + self.x, self.starting_point_y + self.y, self.starting_point_x + self.x + self.gravity.x * 1000, self.starting_point_y + self.y + self.gravity.y * 1000, "4", "blue")
        return draw_string

    def get_working_vectors(self):#should be in every model
        return [self, self.gravity, self.tension, self.speed]

    def react_click(self, x, y):#should be in every model
        self.x = x - self.starting_point_x
        self.y = y - self.starting_point_y
        self.set_base_length(((x - self.starting_point_x) ** 2 + (y - self.starting_point_y) ** 2) ** 0.5)
        pass

    def store_sliders(self):
        self.sliders = ""
        for i in self.setters_and_getters["getters"]:
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
        self.recalculate_full_energy()

    def hardset_kinetic_energy(self, num):
        self.speed.set_length(abs(num * 2) ** 0.5 * num/abs(num))
        self.recalculate_full_energy()

    def get_potential_energy(self):
        return self.gravity.length() * (self.starting_point_y + self.baseLength - self.y)

    def set_potential_energy(self, num):
        length = -(num / self.gravity.length()) + self.starting_point_y + self.baseLength
        if type(length) == type(0.0):
            self.y = length
            self.x = (self.baseLength ** 2 - length ** 2) ** 0.5
            self.recalculate_full_energy()

    def get_angle(self):
        try:
            return math.asin(self.x / self.baseLength) / math.pi * 180
        except:
            return 0

    def set_angle(self, angle):
        self.x = sin(angle / 180 * math.pi) * self.baseLength
        self.y = cos(angle / 180 * math.pi) * self.baseLength

    def tick1(self):
        self.model_implications()

    def tick2(self):
        self.apply_forces()
        self.log_state()

    def model_implications(self):
        if self.y < self.starting_point_y:
            self.speed.x = 0
            self.speed.y = -self.speed.y
            self.y = self.starting_point_y
            self.x = self.baseLength * self.x / abs(self.x)
            return
        self.set_length(self.baseLength)
        a = self.judge_speed_direction()
        self.speed.turn_to(-self.x, -self.y)
        self.speed.get_perpendicular(a)
        self.set_kinetic_energy(self.full_energy - self.get_potential_energy())

    def judge_speed_direction(self):
        if self.speed.length() > 0.005:
            return -(self.speed.x + 0.000001) / abs(self.speed.x + 0.000001)
        return int(self.x < 0) * 2 - 1


class Tension(Vector):
    def __init__(self, x, y, aux):
        super().__init__(x, y, aux)

    def tick2(self):
        a = projections(self.x, self.y, self.backlink.gravity.length())
        self.set_length(-a["y"] + self.backlink.speed.length() ** 2 / self.backlink.baseLength)
        self.turn_to(-self.backlink.x, -self.backlink.y)



if __name__ == "__main__":
    PENDULUM = Pendulum()
