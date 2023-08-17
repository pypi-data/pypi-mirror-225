from typing import Dict, List
from coopstructs.geometry import Rectangle, Vector2
from coopstructs.grids.grid_base import Grid
import numpy as np
from cooptools.sectors import rect_utils as sec_u
from cooptools.coopEnum import CardinalPosition

class RectGrid(Grid):
    def __init__(self,
                 nRows: int,
                 nColumns: int,
                 values: np.array = None,
                 default_state: Dict = None):
        super().__init__(
            nRows=nRows,
            nColumns=nColumns,
            default_state=default_state,
            values=values)

    def grid_unit_shape(self, area_rect:Rectangle) -> (float, float):
        w, h, _, _ = sec_u.rect_sector_attributes(area_dims=(area_rect.width, area_rect.height),
                                                  sector_def=self.Shape)
        return w, h

    def grid_unit_width(self, area_rect:Rectangle) -> float:
        w, h = self.grid_unit_shape(area_rect)
        return w

    def grid_unit_height(self, area_rect: Rectangle) -> float:
        w, h = self.grid_unit_shape(area_rect)
        return h

    def coord_from_grid_pos(self, grid_pos: Vector2, area_rect: Rectangle, cardinal_pos: CardinalPosition= CardinalPosition.TOP_LEFT) -> Vector2:
        coord = sec_u.coord_of_sector(area_dims=(area_rect.width, area_rect.height),
                                      sector_def=self.Shape,
                                      sector=grid_pos.as_tuple(),
                                      cardinality=cardinal_pos)
        ret = Vector2.from_tuple(coord)
        return ret

    def grid_from_coord(self, coord: Vector2, area_rect: Rectangle) -> Vector2:
        grid_pos = sec_u.sector_from_coord(coord=coord.as_tuple(),
                                           area_dims=(area_rect.width, area_rect.height),
                                           sector_def=self.Shape)
        ret = Vector2.from_tuple(grid_pos)
        return ret

    def left_of(self, row: int, column: int, positions: int = 1):
        if column > positions:
            return self.grid[row][column - positions]
        else:
            return None

    def right_of(self, row: int, column: int, positions: int = 1):
        if column < self.grid.nColumns - positions:
            return self.grid[row][column + positions]
        else:
            return None

    def up_of(self, row: int, column: int, positions: int = 1):
        if row > positions:
            return self.grid[row - positions][column]
        else:
            return None

    def down_of(self, row: int, column: int, positions: int = 1):
        if row < self.grid.nRows - positions:
            return self.grid[row + positions][column]
        else:
            return None

if __name__ == "__main__":
    mygrid = RectGrid(10, 10, default_state={'a': 1})
    for ii in mygrid:
        if ii[0].x == 9:
            ii[1]['a'] = 2

    meets = mygrid.coords_with_condition([lambda x: x.get('a', None) == 2])
    [print(x) for x in meets]
