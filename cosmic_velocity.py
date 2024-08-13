from vector import Vector, projections
from log_parser import cut_log


class Cosmic_velocity(Vector):
    def __init__(self, x=0, y=-300, gravity=2000):
        super().__init__(x, y)
        self.base_values = [x, y, gravity]
        self.starting_point_x = 500
        self.starting_point_y = 500
        self.reset()

    def reset(self):#should be in every model
        self.setters_and_getters = {#should be in every model
            "setters": [
                "set_mass",
                "set_size",
                "set_speed",
                "set_height",
                "set_kinetic",
                "set_potential",
                "set_force",
                "set_velocity"
            ],
            "getters": [
                "get_mass",
                "get_size",
                "get_speed",
                "get_height",
                "get_kinetic",
                "get_potential",
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
                "0.01",
                "5",
                "20",
                "1",
                "10",
                "10",
                "1000",
                "150"
            ],
            "shifts": [
                "0",
                "0",
                "0",
                "0",
                "0",
                "400",
                "0",
                "0"
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
                'isDefined': []
            },
            "speed": {
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
        self.gravity = Gravity(0, 1, self)
        self.speed = Vector(2, 0, self)
        self.apogee = Vector(0, 0, self)
        self.apogeic_speed = Vector(0, 0)
        self.apogee.going_up = False
        self.apogee.previous_height = 10000
        self.apogee.isDefined = False
        self.speed.mark_forces(self.gravity)
        self.mark_forces(self.speed)
        self.planet_size = 20
        self.full_energy = 0
        self.sliders = ""
        self.count = 0

    def get_graph(self, data):#should be in every model, returns graph arrays for each slider
        parsed = data.split(" ")
        arr = []
        if data == "0":
            arr = self.log["gMm"].copy()
        elif data == "1":
            arr = self.log["size"].copy()
        elif data == "2":
            for i in range(len(self.log["speed"]["x"])):
                arr.append((self.log["speed"]["x"][i] ** 2 + self.log["speed"]["y"][i] ** 2) ** 0.5)
        elif data == "3":
            arr = self.log["self"]["length"]
        elif data == "4":
            for i in range(len(self.log["speed"]["x"])):
                arr.append((self.log["speed"]["x"][i] ** 2 + self.log["speed"]["y"][i] ** 2) / 2)
        elif data == "5":#potential
            for i in range(len(self.log["self"]["length"])):
                if self.log["self"]["length"][i] == 0:
                    arr.append(1000000)
                    continue
                arr.append(-self.log["gMm"][i] / self.log["self"]["length"][i])
        elif data == "6":
            for i in range(len(self.log["self"]["length"])):
                if self.log["self"]["length"][i] == 0:
                    arr.append(1000000)
                    continue
                arr.append(self.log["gMm"][i] / self.log["self"]["length"][i] ** 2)
        elif data == "7":
            for i in range(len(self.log["speed"]["x"])):
                if (self.log["speed"]["x"][i] ** 2 + self.log["speed"]["y"][i] ** 2) ** 0.5 >= (self.log["gMm"][i] / self.log["self"]["length"][i]) ** 0.5:
                    arr.append(2)
                    continue
                if (self.log["speed"]["x"][i] ** 2 + self.log["speed"]["y"][i] ** 2) ** 0.5 >= (self.log["gMm"][i] / self.log["self"]["length"][i] * 2) ** 0.5:
                    arr.append(1)
                    continue
                arr.append(0)
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
        self.log["self"]["length"].append(self.length())
        self.log["apogee"]["x"].append(self.apogee.x)
        self.log["apogee"]["y"].append(self.apogee.y)
        self.log["apogee"]["isDefined"].append(self.apogee.isDefined * 1)
        self.apogee.previous_height = self.length()
        self.log["speed"]["x"].append(self.speed.x)
        self.log["speed"]["y"].append(self.speed.y)
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
        draw_string += animator.planet(self.starting_point_x, self.starting_point_y, self.planet_size)
        draw_string += animator.ship(self.starting_point_x + self.x, self.starting_point_y + self.y, self.speed.x, self.speed.y)
        draw_string += animator.vector(self.starting_point_x + self.x, self.starting_point_y + self.y, self.starting_point_x + self.x + self.speed.x * 20, self.starting_point_y + self.y + self.speed.y * 20, "4", "green")
        draw_string += animator.vector(self.starting_point_x + self.x, self.starting_point_y + self.y, self.starting_point_x + self.x + self.gravity.x * 400, self.starting_point_y + self.y + self.gravity.y * 400, "3", "grey")
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
        return draw_string

    def get_working_vectors(self):#should be in every model
        return [self, self.gravity, self.speed]

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

    def get_height(self):
        return self.length()

    def set_height(self, height):
        self.time_without_interruption = self.time
        self.apogee.isDefined = False
        self.set_length(height)

    def get_speed(self):
        return self.speed.length()

    def set_speed(self, speed):
        self.time_without_interruption = self.time
        self.apogee.isDefined = False
        self.speed.set_length(speed)

    def get_mass(self):
        return self.gMm

    def set_mass(self, mass):
        self.time_without_interruption = self.time
        self.apogee.isDefined = False
        self.gMm = mass

    def get_kinetic(self):
        return self.speed.length() ** 2 / 2

    def set_kinetic(self, kin):#already included
        self.set_speed((2 * kin) ** 0.5)

    def softset_kinetic(self, kin):#does not count as intervention
        self.speed.set_length((2 * kin) ** 0.5)

    def get_potential(self):
        if self.length() == 0: return 0
        return -self.gMm / self.length()

    def set_potential(self, pot):#already included
        if pot == 0: return
        self.set_height(-self.gMm / pot)

    def softset_potential(self, pot):#does not count as intervention
        if pot == 0: return
        self.set_length(-self.gMm / pot)

    def get_size(self):
        return self.planet_size

    def set_size(self, size):
        self.planet_size = size

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
            if p < a[i]:
                going_up = True
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
