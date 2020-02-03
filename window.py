import tkinter as tk

from typing import Tuple


class Window:
    """ This class defines all window-related behaviour, including updating the
    window with the algorithm's progress and allowing the user to create and
    destroy obstacles before running the algorithm.

    Args:
        width {int}: width of new window grid.
        height {int}: height of new window grid.
    """
    box_width = 25   # Width of a box in the grid.
    box_height = 25  # Height of a box in the grid.
    obstacles = {}   # Dictionary of tkinter id to box coordinates.

    def __init__(self, width: int = 500, height: int = 500) -> None:
        """ Initialize the window, including drawing the grid and registering
        callback functions for when a user clicks the screen.

        Args:
            width {int}: width of the new window grid.
            height {int}: height of new window grid.

        Returns:
            None.
        """
        self.root = tk.Tk()
        self.width = width
        self.height = height
        self.canvas = tk.Canvas(self.root, width=width, height=height)

        # Create vertical and horizontal lines that define the grid and draw
        # them on the canvas.
        for x in range(0, width, self.box_width):
            self.canvas.create_line([x, 0], [x, height])
        for y in range(0, height, self.box_height):
            self.canvas.create_line([0, y], [width, y])
        self.canvas.pack()

        button = tk.Button(self.root, text="Start A*", height=2, width=10)
        button.pack(side=tk.LEFT)

        # Left mouse button should create an obstacle, right mouse button
        # should erase an obstacle.
        self.canvas.bind('<B1-Motion>', self.__draw_obstacle)
        self.canvas.bind('<Button-1>', self.__draw_obstacle)
        self.canvas.bind('<B3-Motion>', self.__erase_obstacle)
        self.canvas.bind('<Button-3>', self.__erase_obstacle)

    def __draw_obstacle(self, event: tk.Event) -> None:
        """ Draw an obstacle (in the form of a filled in square) on the screen.

        Args:
            event {tkinder.Event}: details from the triggered event

        Returns:
            None
        """
        # Get the box that the user clicked.
        box_x, box_y = self.abs_to_box(event.x, event.y)

        # No need to draw the obstacle if it already exists
        if (box_x, box_y) in self.obstacles.values():
            return

        # Compute corners of box and draw a rectangle on the canvas
        top_left, bottom_right = self.box_to_corner_coords(box_x, box_y)

        id = self.canvas.create_rectangle(top_left, bottom_right, fill='black')
        self.canvas.pack()
        self.obstacles[id] = box_x, box_y

    def __erase_obstacle(self, event: tk.Event) -> None:
        """ Erase an obstacle (in the form of a filled in square) on the screen.

        Args:
            event {tkinder.Event}: details from the triggered event

        Returns:
            None
        """
        # Get the IDs of all items overlapping where the user clicked.
        ids = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)

        # Make sure there is only one item where the user clicked (looking for
        # a box) and that the item is in the obstacles list (as it's possible
        # the user clicked on a line that defines the grid).
        if len(ids) == 1 and ids[0] in self.obstacles.keys():
            self.canvas.delete(ids[0])
            del self.obstacles[ids[0]]

    def box_to_corner_coords(self, x: int, y: int) -> Tuple[Tuple, Tuple]:
        """ Converts a box's coordinates to the coordinates of it's top left
        and bottom right corners on the canvas.

            Args:
                x {int}: x coordinate of the box.
                y {int}: y coordinate of the box.

            Returns:
                Tuple[int, int]: top_left corner of the box.
                Tuple[int, int]: bottom_right corner of the box.
        """
        top_left = (x * self.box_width,
                    y * self.box_height)
        bottom_right = (top_left[0] + self.box_width,
                        top_left[1] + self.box_height)

        return top_left, bottom_right

    def abs_to_box(self, x: int, y: int) -> Tuple:
        """ Converts absolute coordinates where the user clicked to the box in
        which they clicked.

            Args:
                x {int}: x coordinate of the user's click.
                y {int}: y coordinate of the user's click.

            Returns:
                Tuple[int, int]: coordinates of the box.
        """
        box_x = x // self.box_width
        box_y = y // self.box_height

        return box_x, box_y

    def activate(self):
        self.root.mainloop()
