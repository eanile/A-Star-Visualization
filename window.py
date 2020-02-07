import tkinter as tk

from cell import Cell
from typing import Dict, Optional, Tuple

# Type definitions.
Coordinate = Tuple[int, int]
Cell_ID = int


class Window:
    """ This class defines all window-related behaviour, including updating the
    window with the algorithm's progress and allowing the user to create and
    destroy obstacles before running the algorithm.

    Class Variables:
        width: Width of the window (in pixels).
        height: Height of the window (in pixels).
        box_width: Width of a box in the grid (in pixels).
        box_height: Height of a box in the grid (in pixels).
        __root: Represents the tkinter window.
        __canvas: Displayed in the window and holds all elements drawn.
        __obstacles: Dictionary of cell ID to Cell structure. The cell ID is
            calculated based on the (x,y) position of the cell in the grid.
        __start: Cell that represents the starting point of the algorithm.
        __start: Cell that represents the ending point of the algorithm.
    """
    width: int
    height: int
    __root: tk.Tk
    __canvas: tk.Canvas
    __obstacles: Dict[int, Cell]
    __start: Optional[Cell]
    __end: Optional[Cell]

    box_width: int = 25
    box_height: int = 25

    def __init__(self, width: int = 500, height: int = 500) -> None:
        self.width = width
        self.height = height
        self.__obstacles = {}
        self.__start = None
        self.__end = None
        self.__root = tk.Tk()
        self.__canvas = tk.Canvas(self.__root, width=width, height=height)

        self.__create_window()

    def __create_window(self) -> None:
        """ Draw the grid and register callback functions for when a user
        clicks the screen.
        """
        # Create vertical and horizontal lines that define the grid and draw
        # them on the canvas.
        for x in range(0, self.width, self.box_width):
            self.__canvas.create_line([x, 0], [x, self.height])
        for y in range(0, self.height, self.box_height):
            self.__canvas.create_line([0, y], [self.width, y])
        self.__canvas.pack()

        # Place all buttons.
        buttons_text = ["Start A*", "Place Starting Point",
                        "Place Ending Point", "Place Obstacles"]
        for text in buttons_text:
            button = tk.Button(
                self.__root, text=text, wraplength=80, height=2, width=15)
            button.pack(side=tk.LEFT)

        # Left mouse button should create an obstacle, right mouse button
        # should erase an obstacle.
        self.__canvas.bind('<B1-Motion>', self.__draw_obstacle)
        self.__canvas.bind('<Button-1>', self.__draw_obstacle)
        self.__canvas.bind('<B3-Motion>', self.__erase_obstacle)
        self.__canvas.bind('<Button-3>', self.__erase_obstacle)

    @property
    def root(self) -> tk.Tk:
        return self.__root

    @property
    def obstacles(self) -> Dict[int, Cell]:
        return self.__obstacles

    @property
    def start(self) -> Optional[Cell]:
        return self.__start

    @property
    def end(self) -> Optional[Cell]:
        return self.__end

    def __draw_obstacle(self, event: tk.Event) -> None:
        """ Draw an obstacle (a filled square) on the screen."""
        # Get the box coordinates and cell ID that the user clicked on.
        box_coords = self.abs_to_box((event.x, event.y))
        cell_id = self.box_to_cell_id(box_coords)

        # No need to draw the obstacle if it already exists or if the user
        # clicked in an area outside the grid.
        if cell_id in self.__obstacles.keys() or self.out_of_bounds(box_coords):
            return

        # Compute corners of box and draw a rectangle on the canvas
        tk_id = self.__canvas.create_rectangle(
            self.box_to_corner_coords(box_coords), fill='black')
        self.__canvas.pack()
        assert not self.out_of_bounds(box_coords)
        self.__obstacles[cell_id] = Cell(tk_id, box_coords, 'black')

    def __erase_obstacle(self, event: tk.Event) -> None:
        """ Erase an obstacle (a filled square) on the screen."""
        cell_id = self.abs_to_cell_id((event.x, event.y))

        # Remove the obstacle if it exists from the screen and the data
        # structure keeping track of them all.
        if cell_id in self.__obstacles.keys():
            self.__canvas.delete(self.__obstacles[cell_id].tk_id)
            del self.__obstacles[cell_id]

    def box_to_corner_coords(self, box_coords: Coordinate) -> Tuple[Coordinate,
                                                                    Coordinate]:
        """ Converts a box's coordinates to the coordinates of it's top left
        and bottom right corners on the canvas.
        """

        top_left = (box_coords[0] * self.box_width,
                    box_coords[1] * self.box_height)
        bottom_right = (top_left[0] + self.box_width,
                        top_left[1] + self.box_height)

        return top_left, bottom_right

    def box_to_cell_id(self, box_coords: Coordinate) -> Cell_ID:
        """ Converts a box's coordinates to the cell ID that would exist in that
        position.
        """
        cell_id = box_coords[0] + (box_coords[1] * self.width // self.box_width)

        return cell_id

    def abs_to_box(self, abs_coords: Coordinate) -> Coordinate:
        """ Converts the absolute coordinates where the user clicked to the box
        in which they clicked.
        """
        box_coords = (abs_coords[0] // self.box_width,
                      abs_coords[1] // self.box_height)

        return box_coords

    def abs_to_cell_id(self, abs_coords: Coordinate) -> Cell_ID:
        """ Converts the absolute coordinates where the user clicked to the cell
        ID that would exist in that position.
        """
        return self.box_to_cell_id(self.abs_to_box(abs_coords))

    def out_of_bounds(self, box_coords: Coordinate) -> bool:
        """ Return whether the coordinates of a box that the user clicked is
        outside the bounds of the grid.
        """
        if box_coords[0] < 0 or box_coords[1] < 0 or \
           box_coords[0] > self.width // self.box_width - 1 or \
           box_coords[1] > self.height // self.box_height - 1:
            return True
        return False
