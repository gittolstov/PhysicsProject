import math

from vector import Vector, projections
from log_parser import cut_log
from math import atan, sin, cos


class Cosmic_velocity(Vector):
    def __init__(self, x=0, y=-300, gravity=2000):
        super().__init__(x, y)
        self.base_values = [x, y, gravity]
        self.starting_point_x = 500
        self.starting_point_y = 500
        self.reset()
        self.gravitationalConstant = 3.5 * 10 ** (-22)
        self.length_multiplier = 31855
        self.speed_multiplier = 2.5

    def reset(self):#should be in every model
        self.setters_and_getters = {#should be in every model
            "setters": [
                "set_mass_public",
                "set_size",
                "set_speed_public",
                "set_height_public",
                "set_kinetic_public",
                "set_potential_public",
                "set_force",
                "set_velocity"
            ],
            "getters": [
                "get_mass_public",
                "get_size",
                "get_speed_public",
                "get_height_public",
                "get_kinetic_public",
                "get_potential_public",
                "get_force",
                "get_velocity"
            ],
            "names": [
                "Масса планеты",
                "Радиус планеты",
                "Скорость",
                "Высота",
                "Кинетическая энергия",
                "Потенциальная энергия",
                "Сила гравитации",
                "Космическая скорость (по индексу)"
            ],
            "modifiers": [
                "0.00000000000000000000002",
                "0.000025",
                "40",
                "0.00002",
                "4",
                "4",
                "10000",
                "200"
            ],
            "shifts": [
                "0",
                "0",
                "0",
                "0",
                "0",
                "400",
                "0",
                "25"
            ]
        }
        self.log = {
            "self": {
                'x': [],
                'y': [],
                'length': []
            },
            "apogee": {
                'x': [],
                'y': [],
                'going_up': [],
                'previous_height': [],
                'isDefined': []
            },
            "speed": {
                'x': [],
                'y': []
            },
            "gravity": {
                'x': [],
                'y': []
            },
            "gMm": [],
            "size": [],
            "full_energy": [],
            "simulation_type": "Cosmic_velocity"
        }
        self.time = 0
        self.reset_forces()
        self.time_without_interruption = self.time
        x = self.base_values[0]
        y = self.base_values[1]
        self.gMm = self.base_values[2]
        self.x = x
        self.y = y
        self.gravity = Gravity(0, 0.0001, self)
        self.speed = Vector(2.5, 0, self)
        self.apogee = Vector(0, 0, self)
        self.apogeic_speed = Vector(0, 0)
        self.apogee.going_up = False
        self.apogee.previous_height = 10000
        self.apogee.isDefined = False
        self.speed.mark_forces(self.gravity)
        self.mark_forces(self.speed)
        self.planet_size = 100
        self.full_energy = 0
        self.sliders = ""
        self.count = 0
        self.explosion_frame = 0
        self.orbit_marks = []

    def get_graph(self, data):#should be in every model, returns graph arrays for each slider
        parsed = data.split(" ")
        arr = []
        if data == "0":
            for i in range(len(self.log["gMm"])):
                arr.append(self.log["gMm"][i] / self.gravitationalConstant)
        elif data == "1":
            for i in range(len(self.log["size"])):
                arr.append(self.log["size"][i] * self.length_multiplier * 2)
        elif data == "2":
            for i in range(len(self.log["speed"]["x"])):
                arr.append((self.log["speed"]["x"][i] ** 2 + self.log["speed"]["y"][i] ** 2) ** 0.5 * self.speed_multiplier)
        elif data == "3":
            for i in range(len(self.log["self"]["length"])):
                arr.append(self.log["self"]["length"][i] * self.length_multiplier)
        elif data == "4":
            for i in range(len(self.log["speed"]["x"])):
                arr.append((self.log["speed"]["x"][i] ** 2 + self.log["speed"]["y"][i] ** 2) * self.speed_multiplier ** 2 / 2)
        elif data == "5":#potential
            for i in range(len(self.log["self"]["length"])):
                if self.log["self"]["length"][i] == 0:
                    arr.append(1000000)
                    continue
                arr.append(-self.log["gMm"][i] * self.speed_multiplier ** 2 / float(self.log["self"]["length"][i]))
        elif data == "6":
            for i in range(len(self.log["self"]["length"])):
                if self.log["self"]["length"][i] == 0:
                    arr.append(1000000)
                    continue
                arr.append(float(self.log["gMm"][i]) / float(self.log["self"]["length"][i]) ** 2)
        elif data == "7":
            for i in range(len(self.log["speed"]["x"])):
                if (float(self.log["speed"]["x"][i]) ** 2 + float(self.log["speed"]["y"][i]) ** 2) ** 0.5 >= (((self.log["gMm"][i] / float(self.log["self"]["length"][i])) * 2) ** 0.5):
                    arr.append(2)
                elif (float(self.log["speed"]["x"][i]) ** 2 + float(self.log["speed"]["y"][i]) ** 2) ** 0.5 >= ((self.log["gMm"][i] / float(self.log["self"]["length"][i])) ** 0.5):
                    arr.append(1)
                else:
                    arr.append(0)
        for i in range(len(arr)):
            arr[i] = float(arr[i])
            arr[i] *= float(self.setters_and_getters["modifiers"][int(data)])
            arr[i] = str(arr[i])
        return arr

    def log_state(self):#should be in every model
        if self.time < len(self.log["self"]["x"]):
            cut_log(self.log, self.time)
        self.time += 1
        self.log["self"]["x"].append(self.x)
        self.log["self"]["y"].append(self.y)
        self.log["self"]["length"].append(self.length())
        self.log["apogee"]["x"].append(self.apogee.x)
        self.log["apogee"]["y"].append(self.apogee.y)
        self.log["apogee"]["previous_height"].append(self.apogee.previous_height)
        self.log["apogee"]["going_up"].append(int(self.apogee.going_up))
        self.log["apogee"]["isDefined"].append(int(self.apogee.isDefined))
        self.apogee.previous_height = self.length()
        self.log["speed"]["x"].append(self.speed.x)
        self.log["speed"]["y"].append(self.speed.y)
        self.log["gravity"]["x"].append(self.gravity.x)
        self.log["gravity"]["y"].append(self.gravity.y)
        self.log["gMm"].append(self.gMm)
        self.log["size"].append(self.planet_size)
        self.log["full_energy"].append(self.full_energy)

    def apply_log(self, log, frame):#should be in every model, applies frames from log
        print(log)
        if frame >= len(log["self"]["x"]):
            print("frame index out of range")
            return
        self.x = log["self"]["x"][frame]
        self.y = log["self"]["y"][frame]
        self.apogee.y = log["apogee"]["y"][frame]
        self.apogee.x = log["apogee"]["x"][frame]
        self.apogee.going_up = bool(log["apogee"]["going_up"][frame])
        self.apogee.previous_height = log["apogee"]["previous_height"][frame]
        self.apogee.isDefined = bool(log["apogee"]["isDefined"][frame])
        self.speed.x = log["speed"]["x"][frame]
        self.speed.y = log["speed"]["y"][frame]
        self.gravity.x = log["gravity"]["x"][frame]
        self.gravity.y = log["gravity"]["y"][frame]
        self.full_energy = log["full_energy"][frame]
        self.gMm = log["gMm"][frame]
        self.planet_size = log["size"][frame]

    def draw(self, animator):#should be in every model
        self.store_sliders()
        draw_string = ""
        draw_string += animator.planet(self.starting_point_x, self.starting_point_y, self.planet_size * 1.1)
        draw_string += animator.ship(self.starting_point_x + self.x, self.starting_point_y + self.y, self.speed.x, self.speed.y)
        draw_string += animator.vector(self.starting_point_x + self.x, self.starting_point_y + self.y, self.starting_point_x + self.x + self.speed.x * 50, self.starting_point_y + self.y + self.speed.y * 50, "5", "green")
        draw_string += animator.vector(self.starting_point_x + self.x, self.starting_point_y + self.y, self.starting_point_x + self.x + self.gravity.x * 3000, self.starting_point_y + self.y + self.gravity.y * 3000, "5", "grey")
        for i in self.orbit_marks:
            draw_string += animator.line(self.starting_point_x + i[0], self.starting_point_y + i[1], self.starting_point_x + i[0] + 1, self.starting_point_y + i[1] + 1, 1, "blue")
        if self.apogee.isDefined:
            temp = Vector(1, 1)
            self.apogee.transfer(temp)
            temp.get_perpendicular(1)
            temp.set_length(8)
            draw_string += animator.line(
                self.starting_point_x + self.apogee.x + temp.x,
                self.starting_point_y + self.apogee.y + temp.y,
                self.starting_point_x + self.apogee.x - temp.x,
                self.starting_point_y + self.apogee.y - temp.y,
                2,
                "red"
            )
        #if self.apogee.going_up and self.apogee.previous_height > self.length() and self.apogee.isDefined:
        #    self.orbit_marks = []
        if self.length() < self.planet_size * 2 and self.explosion_frame < 80:
            draw_string += animator.ship_boom(self.starting_point_x + self.x - 40, self.starting_point_y + self.y - 40, 80, 80, int(self.explosion_frame / 10))
            self.explosion_frame += 1
        if self.length() > self.planet_size * 2:
            self.explosion_frame = 0
        return draw_string

    def get_working_vectors(self):#should be in every model
        return [self, self.gravity, self.speed]

    def react_click(self, x, y):#should be in every model
        angle_shift = atan((y - self.starting_point_y) / (x - self.starting_point_x + 0.01)) + math.pi * ((x - self.starting_point_y) < 0)
        angle0 = atan(self.y / (self.x + 0.01)) + math.pi * (self.x < 0)
        sp0x = self.speed.x
        sp0y = self.speed.y
        self.x = x - self.starting_point_x
        self.y = y - self.starting_point_y
        self.speed.x = cos(angle_shift - angle0) * sp0x - sin(angle_shift - angle0) * sp0y
        self.speed.y = sin(angle_shift - angle0) * sp0x + cos(angle_shift - angle0) * sp0y
        self.time_without_interruption = self.time
        self.apogee.isDefined = False
        self.gravity.tick2()

    def apply_forces(self):
        for a in self.force_applications:
            self.x += a.x
            self.y += a.y
            for b in a.force_applications:
                self.x += b.x ** 2 / 2
                self.y += b.y ** 2 / 2

    def cosmic_velocity1(self):
        return (-self.get_potential()) ** 0.5

    def cosmic_velocity2(self):
        return (self.get_potential() * -2) ** 0.5

    def get_velocity(self):
        if self.speed.length() >= self.cosmic_velocity2():
            return 2
        if self.speed.length() >= self.cosmic_velocity1():
            return 1
        return 0

    def set_velocity(self, num):
        a = round(num)
        if a == 0:
            self.set_speed(self.cosmic_velocity1() * 0.8)
        if a == 1:
            self.set_speed(self.cosmic_velocity1())
        if a == 2:
            self.set_speed(self.cosmic_velocity2())

    def get_height_public(self):
        return round(self.length() * self.length_multiplier)

    def set_height(self, height):
        self.time_without_interruption = self.time
        self.apogee.isDefined = False
        self.set_length(height)
    def set_height_public(self, height):
        self.time_without_interruption = self.time
        self.apogee.isDefined = False
        self.set_length(height / self.length_multiplier)

    def get_speed(self):
        return self.speed.length()
    def get_speed_public(self):
        return self.speed.length() * self.speed_multiplier

    def set_speed(self, speed):
        self.time_without_interruption = self.time
        self.apogee.isDefined = False
        self.speed.set_length(speed)
    def set_speed_public(self, speed):
        self.set_speed(speed / self.speed_multiplier)

    def get_mass(self):
        return self.gMm
    def get_mass_public(self):
        return self.gMm / self.gravitationalConstant

    def set_mass(self, mass):
        self.time_without_interruption = self.time
        self.apogee.isDefined = False
        self.gMm = mass
    def set_mass_public(self, mass):
        self.set_mass(mass * self.gravitationalConstant)

    def get_kinetic(self):
        return self.speed.length() ** 2 / 2
    def get_kinetic_public(self):
        return self.get_kinetic() * self.speed_multiplier ** 2

    def set_kinetic(self, kin):#already included
        self.set_speed((2 * kin) ** 0.5)
    def set_kinetic_public(self, kin):#already included
        self.set_kinetic(kin / self.speed_multiplier ** 2)

    def softset_kinetic(self, kin):#does not count as intervention
        self.speed.set_length((2 * kin) ** 0.5)

    def get_potential(self):
        if self.length() == 0: return 0
        return -self.gMm / self.length()
    def get_potential_public(self):
        if self.length() == 0: return 0
        return -self.gMm * self.speed_multiplier ** 2 / self.length()

    def set_potential(self, pot):#already included
        if pot == 0: return
        self.set_height(-self.gMm / pot)
    def set_potential_public(self, pot):#already included
        if pot == 0: return
        self.set_height(-self.gMm * self.speed_multiplier ** 2 / pot)

    # def softset_potential(self, pot):#does not count as intervention
    #     if pot == 0: return
    #     self.set_length(-self.gMm / pot)

    def get_size(self):#doesn't have other usage
        return self.planet_size * self.length_multiplier * 2

    def set_size(self, size):#doesn't have other usage
        self.planet_size = size / self.length_multiplier / 2

    def get_force(self):
        if self.length() == 0: return
        return self.gMm / self.length() ** 2

    def set_force(self, force):
        self.gMm = force * self.length() ** 2

    def tick2(self):
        self.model_implications()
        self.count += 1
        if self.count > 20:
            self.count = 0
            self.recalculate_apogee()
        self.log_state()

    def model_implications(self):
        self.orbit_marks.append((self.x, self.y))
        if self.length() < self.planet_size * 2:
            self.main.pause()
        if self.apogee.isDefined:
            self.softset_kinetic(self.full_energy - self.get_potential())
        a = self.length()
        if self.apogee.going_up and self.apogee.previous_height > a and self.apogee.isDefined:
            self.snap_to_apogee()
            self.apogee.going_up = False
            return
        if self.apogee.previous_height < a:
            self.apogee.going_up = True
        self.apogee.previous_height = a

    def snap_to_apogee(self):
        self.orbit_marks = []
        print("snapped! " + str(self.apogee.x) + " " + str(self.apogee.y))
        self.apogee.transfer(self)
        self.apogeic_speed.transfer(self.speed)

    def recalculate_apogee(self):
        if self.apogee.isDefined:
            return
        going_up = False
        a = self.log["self"]["length"]
        p = 1000
        for i in range(self.time_without_interruption, len(a)):
            if going_up and p > a[i]:
                self.apogee.x = self.log["self"]["x"][i]
                self.apogee.y = self.log["self"]["y"][i]
                self.apogeic_speed.x = self.log["speed"]["x"][i]
                self.apogeic_speed.y = self.log["speed"]["y"][i]
                self.full_energy = (self.apogeic_speed.x ** 2 + self.apogeic_speed.y ** 2) / 2 - self.gMm / a[i]
                self.apogee.isDefined = True
                return
            try:
                if p < a[i]:
                    going_up = True
            except:
                print("fatal error")
                print(a)
                print(a[i])
                a[i] = 100
            p = a[i]

    def store_sliders(self):#should be in every model
        self.sliders = ""
        for i in self.setters_and_getters["getters"]:
            self.sliders += i + " " + str(getattr(self, i)()) + ";"


class Gravity(Vector):
    def __init__(self, x, y, aux):
        super().__init__(x, y, aux)

    def tick2(self):
        if self.backlink.length() == 0: return
        self.set_length(self.backlink.gMm / self.backlink.length() ** 2)
        self.turn_to(-self.backlink.x, -self.backlink.y)
