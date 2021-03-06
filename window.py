import tkinter as tk
import tkinter.messagebox as messagebox

from cell import Cell
from enum import Enum
from idlelib import tooltip
from typing import Dict, List, Optional, Tuple

# Type definitions.
Coordinate = Tuple[int, int]
Cell_ID = int

# Colours for UI elements.
CANVAS_BG_COLOUR = '#f0f0f0'
FRAME_BG_COLOUR = '#cfcfcf'
BUTTON_BG_PLACE_OBSTACLES = '#e3e3e3'
BUTTON_BG_PLACE_START = '#e8fffc'
BUTTON_BG_PLACE_END = '#fff2fe'
BUTTON_BG_CLEAR = '#fff'
BUTTON_BG_START_ALGORITHM = '#f2fff4'

# Strings for buttons.
BUTTON_TEXT_PLACE_OBSTACLES = "Place Obstacles"
BUTTON_TEXT_PLACE_START = "Place Starting Point"
BUTTON_TEXT_PLACE_END = "Place Ending Point"
BUTTON_TEXT_CLEAR = "Clear"
BUTTON_TEXT_START_ALGORITHM = "Start Pathfinding Algorithm"


class Colours(Enum):
    """ This class defines all valid colours that can be used to draw cells on the window's grid. """
    OBSTACLE = 'grey'
    START = 'cyan'
    END = 'magenta'
    PATH = 'green'


class Window:
    """ This class defines all window-related behaviour, including updating the window with the algorithm's progress and
    allowing the user to create and destroy obstacles before running the algorithm.

    Class Variables:
        cell_width: Width of a cell in the grid (in pixels).
        cell_height: Height of a cell in the grid (in pixels).

    Instance Variables:
        width: Width of the window (in pixels).
        height: Height of the window (in pixels).
        __root: Represents the tkinter window.
        __canvas: Displayed in the window and holds all elements drawn.
        __colour: Current colour chosen to draw cells with.
        __cells: Dictionary of Cell ID to Cell structure. The cell ID is calculated based on the (x,y) position of the
            cell in the grid.
        __start: Cell ID that represents the starting point of the algorithm.
        __end: Cell ID that represents the ending point of the algorithm.
        __shortest_path: Dictionary of Cell ID to Cell structure. These cells are excluded from the other cells
            dictionary because they are cleared at different times.
    """
    cell_width: int = 25
    cell_height: int = 25

    width: int
    height: int
    __root: tk.Tk
    __canvas: tk.Canvas
    __colour: str
    __cells: Dict[Cell_ID, Cell]
    __start: Optional[Cell_ID]
    __end: Optional[Cell_ID]
    __shortest_path: Dict[Cell_ID, Cell]

    def __init__(self, width: int = 500, height: int = 500) -> None:
        self.width = width
        self.height = height
        self.__colour = Colours.OBSTACLE.value
        self.__cells = {}
        self.__start = None
        self.__end = None
        self.__shortest_path = {}

        # Initialize window sections that interactive elements will live.
        self.__root = tk.Tk()
        self.__root.title("A* Pathfinding Visualization")
        self.__canvas = tk.Canvas(
            self.__root, width=width+1, height=height+1, borderwidth=0, highlightthickness=0, bg=CANVAS_BG_COLOUR)
        self.__controls = tk.Frame(self.__root, bg=FRAME_BG_COLOUR)

        self.__create_canvas()
        self.__create_controls()

    def __create_canvas(self) -> None:
        """ Draw the grid and register callback functions for when a user clicks the screen. """
        # Create vertical and horizontal lines that define the grid and draw them on the canvas.
        for x in range(0, self.width+1, self.cell_width):
            self.__canvas.create_line([x, 0], [x, self.height])
        for y in range(0, self.height+1, self.cell_height):
            self.__canvas.create_line([0, y], [self.width, y])
        self.__canvas.pack()

        # Left mouse button should create a cell, right mouse button should erase a cell.
        self.__canvas.bind('<B1-Motion>', self.__draw_callback)
        self.__canvas.bind('<Button-1>', self.__draw_callback)
        self.__canvas.bind('<B3-Motion>', self.__erase_callback)
        self.__canvas.bind('<Button-3>', self.__erase_callback)

    def __create_controls(self) -> None:
        """ Draw the buttons/tooltips and register callback functions for when a user clicks each button. """
        button = tk.Button(
            self.__controls,
            text=BUTTON_TEXT_PLACE_OBSTACLES,
            wraplength=80,
            height=2,
            width=15,
            bg=BUTTON_BG_PLACE_OBSTACLES)
        button.configure(command=lambda b=button: self.__change_cell_colour(Colours.OBSTACLE.value, b))
        button.grid(row=0, column=0, padx=5, pady=(10, 2.5))

        # "Place Obstacles" button should be focused by default.
        button.focus()

        button = tk.Button(
            self.__controls,
            text=BUTTON_TEXT_PLACE_START,
            wraplength=80,
            height=2,
            width=15,
            bg=BUTTON_BG_PLACE_START)
        button.configure(command=lambda b=button: self.__change_cell_colour(Colours.START.value, b))
        button.grid(row=0, column=1, padx=5, pady=(10, 2.5))

        button = tk.Button(
            self.__controls,
            text=BUTTON_TEXT_PLACE_END,
            wraplength=80,
            height=2,
            width=15,
            bg=BUTTON_BG_PLACE_END)
        button.configure(command=lambda b=button: self.__change_cell_colour(Colours.END.value, b))
        button.grid(row=0, column=2, padx=5, pady=(10, 2.5))

        button = tk.Button(
            self.__controls,
            text=BUTTON_TEXT_CLEAR,
            wraplength=80,
            height=2,
            width=15,
            bg=BUTTON_BG_CLEAR)
        button.configure(command=lambda: self.__clear_canvas())
        button.grid(row=0, column=3, padx=5, pady=(10, 2.5))

        button = tk.Button(
            self.__controls,
            text=BUTTON_TEXT_START_ALGORITHM,
            height=2,
            bg=BUTTON_BG_START_ALGORITHM)
        button.configure(command=lambda: self.__find_shortest_path())
        button.grid(row=1, column=0, columnspan=4, sticky=tk.W+tk.E, padx=5, pady=(2.5, 2.5))

        # Create a label in the buttom right corner of the screen that, when hovered over, displays information about
        # how to use the program.
        tooltip_label = tk.Label(self.__controls, text="?", bg=FRAME_BG_COLOUR)
        tooltip_label.grid(row=2, column=3, padx=5, pady=(0, 2.5), sticky=tk.E)
        tooltip.Hovertip(tooltip_label, hover_delay=100,
                         text=('Left-Click is used to select buttons and draw squares on the grid.\n'
                               'Right-Click is used to erase squares from the grid.'))

        self.__controls.pack()

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
        """ Change the colour of the cells being drawn on-screen. This method also changes the focused button to the one
        that was clicked.
        """
        # Confirm the colour is expected before changing it.
        assert colour in [colour.value for colour in Colours]
        button.focus()
        self.__colour = colour

    def __draw_callback(self, event: tk.Event) -> None:
        """ Draw a cell (a filled square) on the screen. """
        # Cannot draw if a path is drawn on the screen.
        if self.__shortest_path:
            return

        cell_id = self.abs_to_cell_id((event.x, event.y))

        # Don't draw the cell if a cell already exists, the user clicked in an area outside the grid, or the user is
        # drawing a start/end cell when a start/end cell already exists.
        if self.cell_exists(cell_id) or \
           self.out_of_bounds(self.abs_to_cell((event.x, event.y))) or \
           (self.__end is not None and self.__colour == Colours.END.value) or \
           (self.__start is not None and self.__colour == Colours.START.value):
            return

        self.draw_cell(cell_id, self.__colour, self.__cells)

        # Make note if a start/end cell is drawn.
        if self.__colour == Colours.START.value:
            self.__start = cell_id
        elif self.__colour == Colours.END.value:
            self.__end = cell_id

    def __erase_callback(self, event: tk.Event) -> None:
        """ Erase a cell (a filled square) on the screen. """
        # Cannot erase if a path is drawn on the screen.
        if self.__shortest_path:
            return

        cell_id = self.abs_to_cell_id((event.x, event.y))

        if not self.cell_exists(cell_id) or self.out_of_bounds(self.abs_to_cell((event.x, event.y))):
            return

        # Make note if a start/end point is removed.
        if self.__cells[cell_id].colour == Colours.START.value:
            self.__start = None
        elif self.__cells[cell_id].colour == Colours.END.value:
            self.__end = None

        # Remove from screen and stop keeping track of the cell.
        self.__canvas.delete(self.__cells[cell_id].tk_id)
        del self.__cells[cell_id]

    def __clear_canvas(self) -> None:
        """ Remove all drawn cells from the grid. If a shortest path is drawn, it is removed first. """
        if self.__shortest_path:
            for cell in self.__shortest_path.values():
                self.__canvas.delete(cell.tk_id)
            self.__shortest_path.clear()

            # Re-enable non-clear buttons after the path has been cleared from the screen.
            self.__set_non_clear_buttons_state(tk.NORMAL)

            return

        for cell in self.__cells.values():
            self.__canvas.delete(cell.tk_id)

        self.__cells.clear()
        self.__start = None
        self.__end = None

    def __find_shortest_path(self) -> None:
        """ Callback function to find the shortest path. Displays an error message if a starting and ending point
        are not selected.
        """
        if self.__start is None or self.__end is None:
            messagebox.showerror("Error", "Please select both a starting and ending point before running the"
                                          " pathfinding algorithm!")
        else:
            import pathfinding
            path = pathfinding.a_star(self)

            if not path:
                messagebox.showinfo("Info", "No path found!")
                return
            self.__draw_shortest_path(path)

    def __draw_shortest_path(self, path: List[Cell_ID]) -> None:
        """ Draw the shortest path on the grid. """
        # Start and end points are already drawn, no need to draw over them.
        for cell_id in path[1:-1]:
            self.draw_cell(cell_id, Colours.PATH.value, self.__shortest_path)

        # Disable every button except for the clear button to force the user to clear the path before making
        # modifications to the grid.
        self.__set_non_clear_buttons_state(tk.DISABLED)

    def __set_non_clear_buttons_state(self, new_state: str) -> None:
        """ Sets the state of all non-clear buttons in the window controls. """
        for widget in self.__controls.winfo_children():
            if widget.winfo_class().upper() == "BUTTON":
                if widget.config("text")[-1] != BUTTON_TEXT_CLEAR:
                    widget.config(state=new_state)

    def draw_cell(self, cell_id: Cell_ID, colour: str,
                  cells_dict: Dict[Cell_ID, Cell]) -> None:
        """ Draw a cell on the grid with the specified colour. The cells_dict is the dictionary the new cell should be
        tracked in.
        """
        assert colour in [colour.value for colour in Colours]

        cell_coords = self.cell_id_to_cell(cell_id)
        tk_id = self.__canvas.create_rectangle(self.cell_to_corner_coords(cell_coords), fill=colour)
        self.__canvas.pack()

        cells_dict[cell_id] = Cell(tk_id, cell_coords, colour)

    def cell_exists(self, cell_id: Cell_ID) -> bool:
        """ Return if a cell already exists in the specified cell. """
        return cell_id in self.__cells.keys()

    def obstacle_exists(self, cell_id: Cell_ID) -> bool:
        """ Return if an obstacle exists in the specified cell. """
        return (cell_id in self.__cells.keys() and self.__cells[cell_id].colour == Colours.OBSTACLE.value)

    def cell_to_corner_coords(self, cell_coords: Coordinate) -> Tuple[Coordinate, Coordinate]:
        """ Converts a cell's coordinates to the coordinates of it's top left and bottom right corners
        on the canvas.
        """
        top_left = (cell_coords[0] * self.cell_width, cell_coords[1] * self.cell_height)
        bottom_right = (top_left[0] + self.cell_width, top_left[1] + self.cell_height)

        return top_left, bottom_right

    def cell_to_cell_id(self, cell_coords: Coordinate) -> Cell_ID:
        """ Convert's a cell's position on the grid to its cell ID. Note: this function may return an unexpected Cell
        ID depending on the length and width of the grid. For example, if the grid is 20x20, (5,1) and (25,0) have the
        same Cell ID: 25. It is up to the caller of this function to determine whether the Cell ID makes sense (for
        example, by checking if the coordinate is in bounds.
        """
        return cell_coords[0] + (cell_coords[1] * self.width // self.cell_width)

    def cell_id_to_cell(self, cell_id: Cell_ID) -> Coordinate:
        """ Convert's a cell ID to its position on the grid. """
        return (cell_id % (self.width // self.cell_width), cell_id // (self.width // self.cell_width))

    def abs_to_cell(self, abs_coords: Coordinate) -> Coordinate:
        """ Converts absolute coordinates on the grid to the cell coordinates at that position. """
        return (abs_coords[0] // self.cell_width, abs_coords[1] // self.cell_height)

    def abs_to_cell_id(self, abs_coords: Coordinate) -> Cell_ID:
        """ Converts absolute coordinates on the grid to the cell ID at that position. """
        return self.cell_to_cell_id(self.abs_to_cell(abs_coords))

    def out_of_bounds(self, cell_coords: Coordinate) -> bool:
        """ Return whether the coordinates of a cell that the user clicked is outside the bounds of the grid. """
        if cell_coords[0] < 0 or cell_coords[1] < 0 or \
           cell_coords[0] > self.width // self.cell_width - 1 or \
           cell_coords[1] > self.height // self.cell_height - 1:
            return True
        return False

    def get_num_cells(self) -> int:
        """ Get the number of cells on the grid. """
        return (self.width // self.cell_width) * (self.height // self.cell_height)

    def get_neighbours(self, cell_id: Cell_ID) -> List[Cell_ID]:
        """ Get surrounding cells (N,E,S,W). """
        cell = self.cell_id_to_cell(cell_id)

        north = (cell[0], cell[1]-1)
        east = (cell[0]+1, cell[1])
        south = (cell[0], cell[1]+1)
        west = (cell[0]-1, cell[1])

        return [self.cell_to_cell_id(coords)
                for coords in [north, east, south, west]
                if not self.out_of_bounds(coords) and
                not self.obstacle_exists(self.cell_to_cell_id(coords))]
