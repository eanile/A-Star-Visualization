import heapq
import math
import window

from typing import List

# Type definitions.
Cell_ID = int


class Node:
    """ Holds important information about a Cell when calculating the shortest
    path.
        Notes:
        f_score = g_score + h_score
        g_score: exact time to get from the start to the current node
        h_score: heuristic estimate of the time to get from the current node
                 to the end
        came_from is used to construct the path when the algorithm is complete
    """
    came_from: Cell_ID
    g_score: float
    f_score: float
    visited: bool

    def __init__(self):
        # Initialize g_score to infinity so any newly discovered node will have
        # a g_score less than the initialized one.
        self.came_from = None
        self.g_score = math.inf
        self.f_score = math.inf
        self.visited = False


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
