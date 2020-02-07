from typing import Tuple

# Type definitions.
Coordinate = Tuple[int, int]


class Cell:
    def __init__(self, tk_id: int, coords: Coordinate, colour: str) -> None:
        self.__tk_id = tk_id
        self.__coords = coords
        self.__colour = colour

    @property
    def tk_id(self) -> int:
        return self.__tk_id

    @property
    def coords(self) -> Coordinate:
        return self.__coords

    @property
    def colour(self) -> str:
        return self.__colour
