from coopstructs.vectors import Vector2
from typing import Tuple
from cooptools.coopEnum import CoopEnum, auto

class AlignmentType(CoopEnum):
    TOPLEFT = auto()
    TOPRIGHT = auto()
    TOPCENTER = auto()
    BOTTOMLEFT = auto()
    BOTTOMRIGHT = auto()
    RIGHTCENTER = auto()
    BOTTOMCENTER = auto()
    LEFTCENTER = auto()
    CENTER = auto()

def top_left_from_alignment(dims: Vector2,
                            anchor: Vector2,
                            alignment: AlignmentType) -> Vector2:
    switch = {
        AlignmentType.TOPLEFT: lambda vec: vec,
        AlignmentType.TOPRIGHT: lambda vec: vec.with_(x=anchor.x - dims.x),
        AlignmentType.TOPCENTER: lambda vec: vec.with_(x=anchor.x - dims.x / 2),
        AlignmentType.BOTTOMLEFT: lambda vec: vec.with_(y=anchor.y - dims.y),
        AlignmentType.BOTTOMRIGHT: lambda vec: vec.with_(x=anchor.x - dims.x, y=anchor.y - dims.y),
        AlignmentType.RIGHTCENTER: lambda vec: vec.with_(x=anchor.x - dims.x, y=anchor.y - dims.y / 2),
        AlignmentType.BOTTOMCENTER: lambda vec: vec.with_(x=anchor.x - dims.x/2, y=anchor.y - dims.y),
        AlignmentType.LEFTCENTER: lambda vec: vec.with_(y=anchor.y - dims.y / 2),
        AlignmentType.CENTER: lambda vec: vec.with_(x=anchor.x - dims.x / 2, y=anchor.y - dims.y / 2),
    }

    return switch.get(alignment)(anchor)


class Rectangle:

    @classmethod
    def from_tuple(cls, rect: Tuple[float, float, float, float]):
        return Rectangle(rect[0], rect[1], rect[2], rect[3])

    def __init__(self, x, y, height, width):
        self.top_left: Vector2 = Vector2(x, y)
        self.dims: Vector2 = Vector2(width, height)

    def points_tuple(self):
        return ((self.x, self.y), (self.x + self.width, self.y), (self.x + self.width, self.y + self.height),
                (self.x, self.y + self.height))

    def contains_point(self, point: Vector2):
        return self.x <= point.x <= self.x + self.width and \
               self.y <= point.y <= self.y + self.height

    def overlaps(self, other):
        if not type(other) == Rectangle:
            raise TypeError(f"Cannot compare object of type {type(other)} to Rectangle for overlaps()")

        return any(self.contains_point(x) for x in other.Corners) or any(other.contains_point(x) for x in self.Corners)

    def align(self, anchor: Vector2, alignment: AlignmentType):
        self.top_left = top_left_from_alignment(dims=self.dims, anchor=anchor, alignment=alignment)

    @property
    def Center(self) -> Vector2:
        return Vector2(self.x + self.width / 2, self.y + self.height / 2)

    @property
    def TopRight(self) -> Vector2:
        return Vector2(self.x + self.width, self.y)

    @property
    def TopLeft(self) -> Vector2:
        return Vector2(self.x, self.y)

    @property
    def BottomRight(self) -> Vector2:
        return Vector2(self.x + self.width, self.y + self.height)

    @property
    def BottomLeft(self) -> Vector2:
        return Vector2(self.x, self.y + self.height)

    @property
    def TopCenter(self) -> Vector2:
        return Vector2(self.x + self.width / 2, self.y)

    @property
    def BottomCenter(self) -> Vector2:
        return Vector2(self.x + self.width / 2, self.y + self.height)

    @property
    def RightCenter(self) -> Vector2:
        return Vector2(self.x + self.width, self.y + self.height / 2)

    @property
    def LeftCenter(self) -> Vector2:
        return Vector2(self.x, self.y + self.height / 2)

    @property
    def Corners(self):
        return [
            self.TopLeft,
            self.TopRight,
            self.BottomRight,
            self.BottomLeft
        ]

    @property
    def CornerTuples(self):
        return [x.as_tuple() for x in self.Corners]

    def as_tuple(self):
        return (self.x, self.y, self.height, self.width)

    @property
    def x(self):
        return self.top_left.x

    @property
    def y(self):
        return self.top_left.y

    @property
    def width(self):
        return self.dims.x

    @property
    def height(self):
        return self.dims.y

    def __str__(self):
        return f"TopLeft: <{self.x}, {self.y}>, Size: H{self.height} x W{self.width}"







