from coopstructs.vectors import Vector2
import math
from typing import List
from .line import Line

class Circle:

    @classmethod
    def from_boundary_points(cls, point1: Vector2, point2: Vector2, point3: Vector2):
        lst = [point1, point2, point3]
        if not len(lst) == len(set(lst)):
            raise ValueError(
                f"All the points must be different for a circle to be created. {point1}, {point2}, {point3} were provided")

        # calculate midpoints
        m1 = point1 + (point2 - point1) / 2
        m2 = point2 + (point3 - point2) / 2

        # Generate perpendicular vectors
        perp_vector_m1 = Vector2(m1.x - point1.y + point2.y, m1.y + point1.x - point2.x)
        perp_line_m1 = Line(origin=Vector2(m1.x, m1.y), destination=perp_vector_m1)

        perp_vector_m2 = Vector2(m2.x - point2.y + point3.y, m2.y + point2.x - point3.x)
        perp_line_m2 = Line(origin=Vector2(m2.x, m2.y), destination=perp_vector_m2)

        # Circle center is where perpendicular vectors intersect
        circ_center = perp_line_m1.intersection(perp_line_m2, extend=True)

        # Radius is distance from center to one of the boundary points
        rad = (circ_center - point1).length()
        return Circle(circ_center, rad, known_boundary_points=[point1, point2, point3])

    def __init__(self, center: Vector2, radius: float, known_boundary_points: List[Vector2] = None):
        if type(radius) != float:
            raise TypeError(f"Radius must be of type float, but type {type(radius)} was provided")

        self.center = center
        self.radius = radius
        self.known_boundary_points = known_boundary_points if known_boundary_points else []

    def point_at_angle(self, radians: float) -> Vector2:
        x = (self.radius * math.cos(radians) + self.center.x)
        y = (self.radius * math.sin(radians) + self.center.y)
        return Vector2(x, y)

    def rads_of_point(self, point: Vector2):
        rads = math.atan2(point.y - self.center.y, point.x - self.center.x)

        if rads > 0:
            ret = rads
        else:
            ret = 2 * math.pi + rads

        return ret

    def rads_between_points(self, a: Vector2, b: Vector2):
        """Assumes a counter-clockwise orientation between the two points"""
        rad_d = self.rads_of_point(b)
        rad_o = self.rads_of_point(a)

        delta = rad_d - rad_o

        if rad_d > rad_o:
            return delta
        else:
            return 2 * math.pi + delta

    @property
    def Center(self):
        return self.center

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"Circle of radius {round(self.radius, 2)} centered at {self.center}"