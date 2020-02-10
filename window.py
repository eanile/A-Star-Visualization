import tkinter as tk

from enum import Enum
from cell import Cell
from typing import Dict, Optional, Tuple

# Type definitions.
Coordinate = Tuple[int, int]
Cell_ID = int


# Define the colours used in the window.
class Colours(Enum):
    OBSTACLE = 'black'
    START = 'blue'
    END = 'yellow'


class Window:
    """ This class defines all window-related behaviour, including updating the
    window with the algorithm's progress and allowing the user to create and
    destroy obstacles before running the algorithm.

    Class Variables:
        width: Width of the window (in pixels).
        height: Height of the window (in pixels).
        cell_width: Width of a cell in the grid (in pixels).
        cell_height: Height of a cell in the grid (in pixels).
        __root: Represents the tkinter window.
        __canvas: Displayed in the window and holds all elements drawn.
        __colour: Current colour chosen to draw cells with.
        __cells: Dictionary of Cell ID to Cell structure. The cell ID is
            calculated based on the (x,y) position of the cell in the grid.
        __start: Cell ID that represents the starting point of the algorithm.
        __end: Cell ID that represents the ending point of the algorithm.
    """
    width: int
    height: int
    __root: tk.Tk
    __canvas: tk.Canvas
    __colour: str
    __cells: Dict[Cell_ID, Cell]
    __start: Optional[Cell_ID]
    __end: Optional[Cell_ID]

    cell_width: int = 25
    cell_height: int = 25

    def __init__(self, width: int = 500, height: int = 500) -> None:
        self.width = width
        self.height = height
        self.__colour = Colours.OBSTACLE.value
        self.__cells = {}
        self.__start = None
        self.__end = None

        self.__root = tk.Tk()
        self.__canvas = tk.Canvas(
            self.__root, width=width+1, height=height+1, borderwidth=0,
            highlightthickness=0)
        self.__buttons = tk.Frame(self.__root, relief=tk.RAISED)

        self.__create_canvas()
        self.__create_buttons()

    def __create_canvas(self) -> None:
        """ Draw the grid and register callback functions for when a user
        clicks the screen.
        """
        # Create vertical and horizontal lines that define the grid and draw
        # them on the canvas.
        for x in range(0, self.width+1, self.cell_width):
            self.__canvas.create_line([x, 0], [x, self.height])
        for y in range(0, self.height+1, self.cell_height):
            self.__canvas.create_line([0, y], [self.width, y])
        self.__canvas.pack()

        # Left mouse button should create a cell, right mouse button should
        # erase a cell.
        self.__canvas.bind('<B1-Motion>', self.__draw_cell)
        self.__canvas.bind('<Button-1>', self.__draw_cell)
        self.__canvas.bind('<B3-Motion>', self.__erase_cell)
        self.__canvas.bind('<Button-3>', self.__erase_cell)

    def __create_buttons(self) -> None:
        """ Draw the buttons and register callback functions for when a user
        clicks each button.
        """
        button = tk.Button(
            self.__buttons, text="Place Obstacles",
            wraplength=80, height=2, width=15)
        button.configure(command=lambda b=button: self.__change_cell_colour(
            Colours.OBSTACLE.value, b))
        button.grid(row=0, column=0, padx=5, pady=5)
        # "Place Obstacles" button should be focused by default.
        button.focus()

        button = tk.Button(
            self.__buttons, text="Place Starting Point",
            wraplength=80, height=2, width=15)
        button.configure(command=lambda b=button: self.__change_cell_colour(
            Colours.START.value, b))
        button.grid(row=0, column=1, padx=5, pady=5)

        button = tk.Button(
            self.__buttons, text="Place Ending Point",
            wraplength=80, height=2, width=15)
        button.configure(command=lambda b=button: self.__change_cell_colour(
            Colours.END.value, b))
        button.grid(row=0, column=2, padx=5, pady=5)

        button = tk.Button(
            self.__buttons, text="Clear",
            wraplength=80, height=2, width=15)
        button.configure(command=lambda: self.__clear_canvas())
        button.grid(row=0, column=3, padx=5, pady=5)

        button = tk.Button(
            self.__buttons, text="Start A*",
            wraplength=80, height=2, width=15)
        button.grid(row=1, column=0, columnspan=4, sticky=tk.W+tk.E,
                    padx=5, pady=5)

        self.__buttons.pack()

    @property
    def root(self) -> tk.Tk:
        return self.__root

    @property
    def cells(self) -> Dict[int, Cell]:
        return self.__cells

    @property
    def start(self) -> Optional[Cell_ID]:
        return self.__start

    @property
    def end(self) -> Optional[Cell_ID]:
        return self.__end

    def __change_cell_colour(self, colour: str, button: tk.Button) -> None:
        """ Change the colour of the cells being drawn on-screen. This method
        also changes the focused button the one clicked.
        """
        # Confirm the colour is expected before changing it.
        assert colour in set(colour.value for colour in Colours)
        button.focus()
        self.__colour = colour

    def __draw_cell(self, event: tk.Event) -> None:
        """ Draw a cell (a filled square) on the screen. """
        # Get the cell coordinates and cell ID that the user clicked on.
        cell_coords = self.abs_to_cell((event.x, event.y))
        cell_id = self.cell_to_cell_id(cell_coords)

        # Don't draw the cell if a cell already exists, the user clicked in an
        # area outside the grid, or the user is drawing a start/end cell when
        # a start/end cell already exists.
        if self.cell_exists(cell_id) or \
           self.out_of_bounds(cell_coords) or \
           (self.__end is not None and self.__colour == Colours.END.value) or \
           (self.__start is not None and self.__colour == Colours.START.value):
            return

        # Compute corners of cell and draw it on the canvas.
        tk_id = self.__canvas.create_rectangle(
            self.cell_to_corner_coords(cell_coords), fill=self.__colour)
        self.__canvas.pack()
        self.__cells[cell_id] = Cell(tk_id, cell_coords, self.__colour)

        # Make note if a start/end cell is drawn.
        if self.__colour == Colours.START.value:
            self.__start = cell_id
        elif self.__colour == Colours.END.value:
            self.__end = cell_id

    def __erase_cell(self, event: tk.Event) -> None:
        """ Erase a cell (a filled square) on the screen. """
        cell_id = self.abs_to_cell_id((event.x, event.y))

        if self.cell_exists(cell_id):
            # Make note if a start/end point is removed.
            if self.__cells[cell_id].colour == Colours.START.value:
                self.__start = None
            elif self.__cells[cell_id].colour == Colours.END.value:
                self.__end = None

            # Remove from screen and stop keeping track of the cell.
            self.__canvas.delete(self.__cells[cell_id].tk_id)
            del self.__cells[cell_id]

    def __clear_canvas(self) -> None:
        """ Remove all drawn cells from the grid. """
        for cell in self.__cells.values():
            self.__canvas.delete(cell.tk_id)

        self.__cells.clear()
        self.__start = None
        self.__end = None

    def cell_exists(self, cell_id: Cell_ID) -> bool:
        """ Return if a cell already exists in the specified cell. """
        return cell_id in self.__cells.keys()

    def cell_to_corner_coords(
       self, cell_coords: Coordinate) -> Tuple[Coordinate, Coordinate]:
        """ Converts a cell's coordinates to the coordinates of it's top left
        and bottom right corners on the canvas.
        """
        top_left = (cell_coords[0] * self.cell_width,
                    cell_coords[1] * self.cell_height)
        bottom_right = (top_left[0] + self.cell_width,
                        top_left[1] + self.cell_height)

        return top_left, bottom_right

    def cell_to_cell_id(self, cell_coords: Coordinate) -> Cell_ID:
        """ Convert's a cell's position on the grid to its cell ID. """
        cell_id = cell_coords[0] + \
            (cell_coords[1] * self.width // self.cell_width)

        return cell_id

    def abs_to_cell(self, abs_coords: Coordinate) -> Coordinate:
        """ Converts absolute coordinates on the grid to the cell coordinates
        at that position.
        """
        cell_coords = (abs_coords[0] // self.cell_width,
                       abs_coords[1] // self.cell_height)

        return cell_coords

    def abs_to_cell_id(self, abs_coords: Coordinate) -> Cell_ID:
        """ Converts absolute coordinates on the grid to the cell ID at that
        position.
        """
        return self.cell_to_cell_id(self.abs_to_cell(abs_coords))

    def out_of_bounds(self, cell_coords: Coordinate) -> bool:
        """ Return whether the coordinates of a cell that the user clicked is
        outside the bounds of the grid.
        """
        if cell_coords[0] < 0 or cell_coords[1] < 0 or \
           cell_coords[0] > self.width // self.cell_width - 1 or \
           cell_coords[1] > self.height // self.cell_height - 1:
            return True
        return False
