import tkinter as tk

from typing import Dict, Tuple

# Type definitions.
Coordinate = Tuple[int, int]


class Window:
    """ This class defines all window-related behaviour, including updating the
    window with the algorithm's progress and allowing the user to create and
    destroy obstacles before running the algorithm.

    Class Variables:
        box_width: Width of a box in the grid.
        box_height: Height of a box in the grid.
        __obstacles: Dictionary of tkinter ID to box coordinates.
    """
    box_width: int = 25
    box_height: int = 25
    __obstacles: Dict[int, Coordinate] = {}

    def __init__(self, width: int = 500, height: int = 500) -> None:
        self.__root = tk.Tk()
        self.width = width
        self.height = height
        self.canvas = tk.Canvas(self.__root, width=width, height=height)

        self.__create_window()

    def __create_window(self) -> None:
        """ Draw the grid and register callback functions for when a user
        clicks the screen.
        """
        # Create vertical and horizontal lines that define the grid and draw
        # them on the canvas.
        for x in range(0, self.width, self.box_width):
            self.canvas.create_line([x, 0], [x, self.height])
        for y in range(0, self.height, self.box_height):
            self.canvas.create_line([0, y], [self.width, y])
        self.canvas.pack()

        button = tk.Button(self.__root, text="Start A*", height=2, width=10)
        button.pack(side=tk.LEFT)

        # Left mouse button should create an obstacle, right mouse button
        # should erase an obstacle.
        self.canvas.bind('<B1-Motion>', self.__draw_obstacle)
        self.canvas.bind('<Button-1>', self.__draw_obstacle)
        self.canvas.bind('<B3-Motion>', self.__erase_obstacle)
        self.canvas.bind('<Button-3>', self.__erase_obstacle)

    @property
    def root(self) -> tk.Tk:
        return self.__root

    @property
    def obstacles(self) -> Dict[int, Coordinate]:
        return self.__obstacles

    def __draw_obstacle(self, event: tk.Event) -> None:
        """ Draw an obstacle (a filled square) on the screen."""
        # Get the coordinates of the box that the user clicked.
        coords = self.abs_to_box_coords((event.x, event.y))

        # No need to draw the obstacle if it already exists or if the user
        # clicked in an area outside the grid.
        if coords in self.__obstacles.values() or self.out_of_bounds(coords):
            return

        # Compute corners of box and draw a rectangle on the canvas
        top_left, bottom_right = self.box_to_corner_coords(coords)

        id = self.canvas.create_rectangle(top_left, bottom_right, fill='black')
        self.canvas.pack()
        self.__obstacles[id] = coords

    def __erase_obstacle(self, event: tk.Event) -> None:
        """ Erase an obstacle (a filled square) on the screen."""
        # Get the IDs of all items overlapping where the user clicked.
        ids = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)

        # Make sure there is only one item where the user clicked (looking for
        # a box) and that the item is in the obstacles list (as it's possible
        # the user clicked on a line that defines the grid).
        if len(ids) == 1 and ids[0] in self.__obstacles.keys():
            self.canvas.delete(ids[0])
            del self.__obstacles[ids[0]]

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

    def abs_to_box_coords(self, abs_coords: Coordinate) -> Coordinate:
        """ Converts the absolute coordinates where the user clicked to the box
        in which they clicked.
        """
        return abs_coords[0] // self.box_width, abs_coords[1] // self.box_height

    def out_of_bounds(self, box_coords: Coordinate) -> bool:
        """ Return whether the coordinates of a box that the user clicked is
        outside the bounds of the grid.
        """
        if box_coords[0] > self.width // self.box_width - 1 or \
           box_coords[1] > self.height // self.box_height - 1:
            return True
        return False
