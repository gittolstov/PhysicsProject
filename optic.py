from math import sin, cos, atan


class Optic:
    def __init__(self, x=500, y=500, length=400, angle=90):
        self.base_values = [x, y, length, angle]
        self.starting_point_x = x
        self.starting_point_y = y
        self.reset()

    def reset(self):#should be in every model
        self.setters_and_getters = {#should be in every model
            "setters": [
                "hardset_kinetic_energy",
                "set_speed",
                "set_base_length",
                "set_red",
                "set_green",
                "set_blue"
            ],
            "getters": [
                "get_red",
                "get_red",
                "get_red",
                "get_red",
                "get_green",
                "get_blue"
            ],
            "names": [
                "Угол падения (в градусах)",
                "Угол преломления",
                "Оптическая плотность - верх",
                "Оптическая плотность - низ",
                "Красный",
                "Зелёный",
                "Синий"
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
        self.angle = self.base_values[3]
        self.baseLength = self.base_values[2]
        self.sliders = ""
        self.red = 255
        self.green = 0
        self.blue = 0
        self.time = 0

    def get_color(self):
        return f"rgb({self.red}, {self.green}, {self.blue})"

    def get_red(self):
        return self.red / 255
    def get_green(self):
        return self.green / 255
    def get_blue(self):
        return self.blue / 255

    def set_red(self, num):
        self.red = num * 255
    def set_green(self, num):
        self.green = num * 255
    def set_blue(self, num):
        self.blue = num * 255

    def get_graph(self, data):#should be in every model, returns graph arrays for each slider
        return []

    def log_state(self):#should be in every model
        pass

    def apply_log(self, log, frame):#should be in every model, applies frames from log
        pass

    def draw(self, animator):#should be in every model
        draw_string = ""
        x = self.baseLength * cos(self.angle)
        y = -self.baseLength * sin(self.angle)
        draw_string += animator.circle(self.starting_point_x, self.starting_point_y, 150, "300", "blue")
        draw_string += animator.circle(self.starting_point_x + x, self.starting_point_y + y, 10, "20", "black")
        self.store_sliders()
        return draw_string

    def get_working_vectors(self):#should be in every model
        return []

    def react_click(self, x, y):#should be in every model
        x2 = x - self.starting_point_x
        y2 = y - self.starting_point_y
        self.angle = atan(-y2 / x2)

    def store_sliders(self):#should be in every model
        self.sliders = ""
        for i in self.setters_and_getters["getters"]:
            self.sliders += i + " " + str(getattr(self, i)()) + ";"
