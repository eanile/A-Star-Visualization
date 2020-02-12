import heapq
import math
import window

from typing import List, Optional, Tuple

# Type definitions.
Cell_ID = int


class Node:
    """ Holds important information about a Cell when calculating the shortest
    path.

    Instance Variables:
        came_from: Contains the Cell ID that came before the current cell on
            the path. Used to construct the path when the algorithm is
            complete.
        visited: Flag to keep track of if the node was checked.
        g_score: Exact time to get from the start to the current node
        f_score: Value to minimize; g_score + h_score is the estimated cost of
            the path from start to finish (h_score is a heuristic estimate of
            the time to get from the current node to the end).
    """
    visited: bool
    came_from: Optional[Cell_ID]
    g_score: float
    f_score: float

    def __init__(self) -> None:
        """ Initialize default node values. g_score must be set to infinity so
            any g_score from a cell to a newly discovered neighbour will be
            smaller than the default g_score of the neighbour.
        """
        self.came_from = None
        self.g_score = math.inf
        self.f_score = math.inf
        self.visited = False


class Heap:
    """ Wrapper class that implements heapq in an OOP fasion.

        Instance Variables:
            __data: Data structure used for the heap (in this case, a list).
    """
    def __init__(self, data: List[Tuple[float, Cell_ID]] = []) -> None:
        self.__data = data
        heapq.heapify(self.__data)

    def push(self, item: Tuple[float, Cell_ID]) -> None:
        heapq.heappush(self.__data, item)

    def pop(self) -> Tuple[float, Cell_ID]:
        return heapq.heappop(self.__data)

    def empty(self) -> bool:
        return not self.__data


def a_star(window: window.Window) -> List[Cell_ID]:
    """ Calculate and return the shortest path from start to end. """
    # Confirm starting and ending points are defined.
    start = window.start
    end = window.end
    assert start is not None
    assert end is not None

    print(f"Executing A*: start={window.cells[start].coords},"
          f" end={window.cells[end].coords}")
    exit()

    # List of all cells to easily retrieve information from.
    # Heap will store the cell ID along with it's f_score.
    cells = [Node()] * window.get_num_cells()
    heap = Heap()

    # Cost from start to start is 0; starting cell's cost is purely heuristic.
    cells[start].g_score = 0
    cells[start].f_score = h_score(window, start, end)
    heap.push((cells[start].f_score, start))

    while not heap.empty():
        # Get cell with the lowest f_score.
        top = heap.pop()
        current_id = top[1]

        # Found the path to the end.
        if current_id == end:
            return construct_path(start, current_id, cells)

        # Mark cell as visited and check its neighbours.
        cells[current_id].visited = True
        for neighbour in window.get_neighbours(current_id):
            if cells[neighbour].visited:
                continue

    return []


def h_score(window: window.Window, cell1: Cell_ID, cell2: Cell_ID) -> float:
    """ Calculate the heuristic for two cells (euclidian distance). """
    c1_coords = window.cell_id_to_cell(cell1)
    c2_coords = window.cell_id_to_cell(cell2)
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(c1_coords, c2_coords)]))


def construct_path(start: Cell_ID, end: Cell_ID,
                   cells: List[Node]) -> List[Cell_ID]:
    """ Construct the shortest path taken from start to end. """
    print("TODO implement construct_path")
    return []
