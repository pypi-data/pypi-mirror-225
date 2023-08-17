from .logger import geomLogger
from coopstructs.geometry.vectors.vectorN import Vector2

class DuplicatePointException(Exception):
    def __init__(self, point: Vector2):
        geomLogger.error(f"Unable to process the point {point} because it is a duplicate")
        super().__init__()

