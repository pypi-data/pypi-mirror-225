from coopstructs.vectors import Vector2
import cooptools.geometry as geo

class Line:
    def __init__(self, origin: Vector2, destination: Vector2):

        if origin == destination:
            raise ValueError(f"origin and destination cannot be equal: {origin}")

        self.origin = origin
        self.destination = destination

    @property
    def length(self):
        try:
            return (self.destination - self.origin).length()
        except Exception as e:
            print(f"Destination: {self.destination}\n"
                  f"Origin: {self.origin}\n"
                  f"{e}")
            raise

    def intersection(self, other_line, extend: bool = False) -> Vector2:
        if not type(other_line) == Line:
            raise TypeError(f"can only intersect with objects of type <Line> but type {type(other_line)} was provided")

        try:
            intersect = geo.line_intersection(line1=(self.origin.as_tuple(), self.destination.as_tuple()),
                                     line2=(other_line.origin.as_tuple(), other_line.destination.as_tuple()),
                                     extend=extend)

            return Vector2(intersect[0], intersect[1])

        except:
            return None