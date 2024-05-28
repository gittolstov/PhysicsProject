class Vector:
    def __init__(self, x, y, backlink=None):
        if backlink is not None:
            self.backlink = backlink
        self.x = x
        self.y = y
        self.force_applications = []#all vectors in this list will be added to current vector every tick AKA force

    def draw(self, animator):
        pass

    def tick_move(self):
        self.tick1()
        self.tick2()
        self.tick3()
        self.tick4()

    def tick1(self):
        self.apply_forces()

    def tick2(self):
        pass

    def tick3(self):
        pass

    def tick4(self):
        pass

    def zero_out(self):
        self.x = 0
        self.y = 0

    def copy_coordinates(self):
        return Vector(self.x, self.y)

    def transfer(self, another_vector):
        another_vector.x = self.x
        another_vector.y = self.y

    def mark_forces(self, other):
        self.force_applications.append(other)

    def apply_forces(self):
        for a in self.force_applications:
            self.x += a.x
            self.y += a.y
            for b in a.force_applications:
                self.x += b.x ** 2 / 2
                self.y += b.y ** 2 / 2

    def length(self):
        return (self.x ** 2 + self.y ** 2)**0.5

    def set_length(self, length):
        a = projections(self.x, self.y, length)
        self.x = a["x"]
        self.y = a["y"]

    def turn_to(self, x, y):
        a = projections(x, y, self.length())
        self.x = a["x"]
        self.y = a["y"]

    def turn_to_coordinate(self, x, y, self_x, self_y):
        a = projections(x - self_x, y - self_y, self.length())
        self.x = a["x"]
        self.y = a["y"]

    def get_perpendicular(self, direction):#if direction = 1 spins vector counterclockwise, if -1 - clockwise
        aux = self.x
        self.x = self.y * direction
        self.y = -aux * direction


def projections(a, b, hypothesis):
    if a == 0 and b == 0:
        return {"x": 0, "y": 0}
    if a == 0:
        return {"x": 0, "y": hypothesis * b / abs(b)}
    if b == 0:
        return {"y": 0, "x": hypothesis * a / abs(a)}
    y = hypothesis * b / abs(b) / (a ** 2 / b ** 2 + 1)**0.5
    return {
        "x": y * a / b,
        "y": y
    }
