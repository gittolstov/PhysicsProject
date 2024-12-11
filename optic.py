from math import sin, cos, atan, pi, asin


class Optic:
    def __init__(self, x=500, y=500, length=430, angle=0):
        self.base_values = [x, y, length, angle]
        self.starting_point_x = x
        self.starting_point_y = y
        self.reset()

    def reset(self):#should be in every model
        self.setters_and_getters = {#should be in every model
            "setters": [
                "set_angle",
                "set_refraction",
                "set_optic1",
                "set_optic2",
                "set_red",
                "set_green",
                "set_blue"
            ],
            "getters": [
                "get_angle",
                "get_refraction_public",
                "get_optic1",
                "get_optic2",
                "get_red",
                "get_green",
                "get_blue"
            ],
            "names": [
                "Угол падения (в градусах)",
                "Угол преломления",
                "Оптическая плотность - верх (1)",
                "Оптическая плотность - низ (2)",
                "Красный",
                "Зелёный",
                "Синий"
            ],
            "modifiers": [
                "2.5",
                "2.5",
                "400",
                "400",
                "500",
                "500",
                "500"
            ],
            "shifts": [
                "250",
                "250",
                "-400",
                "-400",
                "0",
                "0",
                "0"
            ]
        }
        self.angle = self.base_values[3]
        self.baseLength = self.base_values[2]
        self.sliders = ""
        self.red = 255
        self.green = 0
        self.blue = 0
        self.optic1 = 1
        self.optic2 = 1
        self.time = 0

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
        angl = self.get_refraction() / 180 * pi
        x2 = 1000 * cos(angl)
        y2 = -1000 * sin(angl)
        draw_string += animator.angle(self.starting_point_x, self.starting_point_y, 735)
        draw_string += animator.semicircle(self.starting_point_x, self.starting_point_y, 300, 0, self.optic1)
        draw_string += animator.semicircle(self.starting_point_x, self.starting_point_y, 300, 0.5, self.optic2)
        draw_string += animator.line(self.starting_point_x + x,
                                     self.starting_point_y + y,
                                     self.starting_point_x,
                                     self.starting_point_y, 4,
                                     self.get_color())
        draw_string += animator.line(self.starting_point_x + x2,
                                     self.starting_point_y + y2,
                                     self.starting_point_x,
                                     self.starting_point_y, 4,
                                     self.get_color())
        # draw_string += animator.laserpointer(self.starting_point_x + x, self.starting_point_y + y, self.angle, 90)
        for i in range(25):
            draw_string += animator.line(self.starting_point_x - 500 + 40 * i,
                                         self.starting_point_y,
                                         self.starting_point_x - 480 + 40 * i,
                                         self.starting_point_y, 3,
                                         "grey")
        draw_string += animator.laserpointer(self.starting_point_x + self.baseLength * cos(self.angle + pi/2),
                                             self.starting_point_y - self.baseLength * sin(self.angle + pi/2),
                                             self.angle + pi/2, 90)
        self.store_sliders()
        return draw_string

    def get_working_vectors(self):  # should be in every model
        return []

    def react_click(self, x, y):  # should be in every model
        x2 = x - self.starting_point_x
        y2 = y - self.starting_point_y
        if y2 <= 0:
            self.angle = atan(x2 / y2)
        else:
            self.set_refraction(atan(-x2 / y2) / pi * 180 + 180)

    def store_sliders(self):  # should be in every model
        self.sliders = ""
        for i in self.setters_and_getters["getters"]:
            self.sliders += i + " " + str(getattr(self, i)()) + ";"

    def get_color(self):
        return f"rgb({self.red}:{self.green}:{self.blue})"

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

    def get_angle(self):
        return self.angle * 180 / pi

    def set_angle(self, num):#deg
        if abs(num) <= 90:
            self.angle = num * pi / 180

    def get_refraction(self):
        if abs(sin(self.angle) / self.optic2 * self.optic1) >= 1:
            a = -self.angle
        else:
            a = asin(sin(self.angle) / self.optic2 * self.optic1) + pi
        return a * 180 / pi #deg

    def get_refraction_public(self):
        return self.get_refraction() - 180

    def set_refraction(self, num):#deg
        try:
            self.angle = asin(sin(num / 180 * pi) / self.optic1 * self.optic2)
        except:
            pass

    def get_optic1(self):
        return self.optic1

    def set_optic1(self, num):
        self.optic1 = num

    def get_optic2(self):
        return self.optic2

    def set_optic2(self, num):
        self.optic2 = num
