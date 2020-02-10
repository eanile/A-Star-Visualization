import window

from typing import List

# Type definitions.
Cell_ID = int


def a_star(window: window.Window) -> List[Cell_ID]:
    """ Calculate and return the shortest path from start to end. """
    print(f"Executing A*: start={window.cells[window.start].coords},"
          f" end={window.cells[window.end].coords}")
