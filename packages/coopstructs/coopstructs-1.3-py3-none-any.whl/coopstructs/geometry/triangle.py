from coopstructs.vectors import Vector2
import math

class Triangle:
    def __init__(self, a: Vector2, b: Vector2, c: Vector2):
        self.area = a.x * (b.y - c.y) + b.x * (c.y - a.y) * c.x * (a.y - b.y)
        if math.isclose(self.area, 0):
            raise ValueError(f"The points [{a}, {b}, {c}] are collinear, the triangle definition is not valid")

        self.points = [a, b, c]

    @property
    def a(self):
        return self.points[0]

    @property
    def b(self):
        return self.points[1]

    @property
    def c(self):
        return self.points[2]

    def incentre(self):
        len_ab = (self.a - self.b).length()
        len_bc = (self.b - self.c).length()
        len_ca = (self.c - self.a).length()

        return (len_bc * self.a + len_ab * self.c + len_ca * self.b) / (len_bc + len_ca + len_ab)