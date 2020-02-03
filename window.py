import tkinter as tk


class Window:
    """ This class defines all window-related behaviour, including updating the
    window with the algorithm's progress and allowing the user to create and
    destroy obstacles before running the algorithm.

    Args:
        width {int}: width of new window grid.
        height {int}: height of new window grid.
    """
    box_width = 25
    box_height = 25

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

        # Left mouse button should create an obstacle, right mouse button.
        # should erase an obstacle.
        self.canvas.bind('<Button-1>', self._draw_obstacle)
        self.canvas.bind('<Button-3>', self._erase_obstacle)

    def _draw_obstacle(self, event: tk.Event) -> None:
        """ Draw an obstacle (in the form of a filled in square) on the screen.

        Args:
            event {tkinder.Event}: details from the triggered event

        Returns:
            None
        """
        # Get the box that the user clicked.
        box_x = event.x // self.box_width
        box_y = event.y // self.box_height

        # Compute corners of box and draw on the canvas
        top_left = [box_x * self.box_width,
                    box_y * self.box_height]
        bottom_right = [top_left[0] + self.box_width,
                        top_left[1] + self.box_height]

        self.canvas.create_rectangle(top_left, bottom_right, fill='black')
        self.canvas.pack()

    def _erase_obstacle(self, event):
        pass

    def activate(self):
        self.root.mainloop()
