import window

from typing import List

# Type definitions.
Cell_ID = int


def a_star(window: window.Window) -> List[Cell_ID]:
    """ Calculate and return the shortest path from start to end. """
    # Confirm starting and ending points are defined.
    start = window.start
    end = window.end
    assert start
    assert end

    print(f"Executing A*: start={window.cells[start].coords},"
          f" end={window.cells[end].coords}")

    return []
