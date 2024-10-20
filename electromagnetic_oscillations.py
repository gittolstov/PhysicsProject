import math
from math import sin, cos, asin, acos
from log_parser import cut_log


class Oscillations:
    def __init__(self, capacitance=200, inductance=200, charge=400, charge_count=15, x1=250, y1=250, x2=500, y2=500):
        self.wireLength = 1000
        self.image_size = {
            "x": x1,
            "y": y1,
            "x_size": x2,
            "y_size": y2
        }
        self.base_values = (capacitance, inductance, charge)
        self.charge_count = charge_count
        self.reset()

    def reset(self):#should be in every model
        self.setters_and_getters = {#should be in every model
            "setters": [
                "set_current",
                "set_period",
                "set_charge",
                "set_capacitance",
                "set_inductance"
            ],
            "getters": [
                "get_current",
                "get_period",
                "get_charge",
                "get_capacitance",
                "get_inductance"
            ],
            "names": [
                "Сила тока",
                "Период колебаний",
                "Заряд конденсатора",
                "Ёмкость конденсатора (C)",
                "Индуктивность катушки (L)"
            ],
            "modifiers": [
                "100",
                "0.2",
                "0.5",
                "1",
                "1"
            ],
            "shifts": [
                "200",
                "0",
                "200",
                "0",
                "0"
            ]
        }
        self.time = 0
        self.periodic_time = 0
        self.capacitance = self.base_values[0]
        self.inductance = self.base_values[1]
        self.charge = self.base_values[2]
        self.current = 0
        self.sliders = ""
        self.log = {
            "self": {
                "charge": [],
                "current": [],
                "periodic_time": [],
                "capacitance": [],
                "inductance": []
            },
            "simulation_type": "Oscillations"
        }
        self.charges = []
        for i in range(self.charge_count):
            self.charges.append(Charge(self, self.wireLength * i / self.charge_count))

    def get_graph(self, data):#should be in every model, returns graph arrays for each slider
        parsed = data.split(" ")
        arr = []
        if data == "0":
            arr = self.log["self"]["current"].copy()
        elif data == "1":
            for i in range(len(self.log["self"]["capacitance"])):
                arr.append(math.pi * 2 * (self.log["self"]["capacitance"][i] * self.log["self"]["inductance"][i]) ** 0.5)
        elif data == "2":
            arr = self.log["self"]["charge"].copy()
        elif data == "3":
            arr = self.log["self"]["capacitance"].copy()
        elif data == "4":
            arr = self.log["self"]["inductance"].copy()
        for i in range(len(arr)):
            arr[i] *= float(self.setters_and_getters["modifiers"][int(data)])
            arr[i] = str(arr[i])
        return arr

    def log_state(self):#should be in every model
        if self.time < len(self.log["self"]["charge"]):
            cut_log(self.log, self.time)
        self.time += 1
        self.log["self"]["charge"].append(self.get_charge())
        self.log["self"]["current"].append(self.current)
        self.log["self"]["periodic_time"].append(self.periodic_time)
        self.log["self"]["capacitance"].append(self.capacitance)
        self.log["self"]["inductance"].append(self.inductance)

    def apply_log(self, log, frame):#should be in every model, applies frames from log
        print(log)
        for i in self.charges:
            i.tick_move()
        if frame >= len(log["self"]["charge"]):
            print("frame index out of range")
            return
        self.charge = log["self"]["charge"][frame]
        self.current = log["self"]["current"][frame]
        self.periodic_time = log["self"]["periodic_time"][frame]
        self.capacitance = log["self"]["capacitance"][frame]
        self.inductance = log["self"]["inductance"][frame]
        self.current = self.calc_current()

    def draw(self, animator):#should be in every model
        self.store_sliders()
        draw_string = ""
        draw_string += animator.scheme()
        img = self.image_size
        shift = 2000 / self.capacitance
        draw_string += animator.line(img["x"], img["y"], img["x"], img["y"] + img['y_size'] / 2 - shift - 5, 4, "black")
        draw_string += animator.line(img["x"] - 45, img["y"] + img['y_size'] / 2 - shift - 5, img["x"] + 45, img["y"] + img['y_size'] / 2 - shift - 5, 4, "black")
        draw_string += animator.line(img["x"] - 45, img["y"] + img['y_size'] / 2 + shift + 5, img["x"] + 45, img["y"] + img['y_size'] / 2 + shift + 5, 4, "black")
        draw_string += animator.line(img["x"], img["y"] + img["y_size"], img["x"], img["y"] + img['y_size'] / 2 + shift + 5, 4, "black")
        draw_string += animator.line(img["x"] - 55, img['y'] + img['y_size'] / 2, img["x"] - 55, img['y'] + img['y_size'] / 2 + img["y_size"] * 0.4 * self.get_charge() / self.base_values[2], 20, "lightblue")
        draw_string += animator.vector(img["x"] + img["x_size"],
                                       img["y"] + img["y_size"] * (0.25 + 0.52 * (self.current >= 0)),
                                       img["x"] + img["x_size"],
                                       img["y"] + img['y_size'] * (0.25 + 0.52 * (self.current >= 0)) + -self.current * 40, 4,
                                       "blue")
        # draw_string += animator.vector(img["x"] + img["x_size"],
        #                                img["y"] + img["y_size"] * 0.5,
        #                                img["x"] + img["x_size"],
        #                                img["y"] + img['y_size'] * 0.5 + -self.current * 40, 4,
        #                                "blue")
        for i in self.charges:
            draw_string += i.draw(animator)
        return draw_string

    def get_working_vectors(self):#should be in every model
        arr = [self]
        for i in self.charges:
            arr.append(i)
        return arr

    def tick_move(self):
        self.log_state()
        self.periodic_time += 1
        self.current = self.calc_current()
        self.current += 0.005

    def calc_current(self):
        w = 2 * math.pi / self.get_period()
        return self.base_values[2] * w * sin(w * self.periodic_time)

    def get_current(self):
        return self.current

    def set_current(self, cur):
        try:
            w = 2 * math.pi / self.get_period()
            self.periodic_time = asin(cur / w / self.base_values[2]) / w
        except:
            pass
        self.current = self.calc_current()

    def get_charge(self):
        if self.get_period() == 0:
            return self.base_values[2]
        w = 2 * math.pi / self.get_period()
        return self.base_values[2] * cos(w * self.periodic_time)

    def set_charge(self, cur):
        try:
            w = 2 * math.pi / self.get_period()
            self.periodic_time = asin(cur / w / self.base_values[2]) / w
        except:
            pass

    def get_capacitance(self):
        return self.capacitance

    def set_capacitance(self, cap):
        self.capacitance = cap

    def get_inductance(self):
        return self.inductance

    def set_inductance(self, ind):
        self.inductance = ind

    def get_period(self):
        return math.pi * 2 * (self.capacitance * self.inductance) ** 0.5

    def set_period(self, per):
        self.capacitance = (per * 0.5 / math.pi) ** 2 / self.inductance

    def store_sliders(self):#should be in every model
        self.sliders = ""
        for i in self.setters_and_getters["getters"]:
            self.sliders += i + " " + str(getattr(self, i)()) + ";"

class Charge:
    def __init__(self, backlink, potential):
        self.potential = potential
        self.backlink = backlink

    def draw(self, animator):
        a = self.get_coordinates(self.potential)
        return animator.circle(a[0], a[1], 5, "10", "blue")

    def get_coordinates(self, pot):
        wl = self.backlink.wireLength
        sz = self.backlink.image_size
        x = 0
        y = 0
        if pot < wl * 0.125:
            x = sz["x"]
            y = sz["y"] + sz["y_size"] * 0.55 + pot / wl * 8 * sz["y_size"] * 0.45
        elif pot < wl * 0.375:
            y = sz["y"] + sz["y_size"]
            x = sz["x"] + (pot / wl - 0.125) * 4 * sz["x_size"]
        elif pot < wl * 0.625:
            x = sz["x"] + sz["x_size"] + (pot > wl * 0.4375 and pot < wl * 0.5625) * abs(sin((pot / wl - 0.4375) * 24 * math.pi)) * 70
            y = sz["y"] + sz["y_size"] - (pot / wl - 0.375) * 4 * sz["y_size"]
        elif pot < wl * 0.875:
            y = sz["y"]
            x = sz["x"] + sz["x_size"] - (pot / wl - 0.625) * 4 * sz["x_size"]
        else:
            x = sz["x"]
            y = sz["y"] + (pot / wl - 0.875) * 8 * sz["y_size"] * 0.45
        return (x, y)

    def tick_move(self):
        self.potential += self.backlink.current
        if self.potential >= self.backlink.wireLength:
            self.potential -= self.backlink.wireLength
        elif self.potential < 0:
            self.potential += self.backlink.wireLength
