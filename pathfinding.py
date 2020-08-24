import heapq
import math
import window

from typing import List, Optional, Tuple

# Type definitions.
Cell_ID = int

ADJACENT_COST = 1


class Node:
    """ Holds important information about a Cell when calculating the shortest path.

    Instance Variables:
        came_from: Contains the Cell ID that came before the current cell on the path. Used to construct the path when
            the algorithm is complete.
        visited: Flag to keep track of if the node was checked.
        g_score: Exact time to get from the start to the current node
        f_score: Value to minimize; g_score + h_score is the estimated cost of the path from start to finish (h_score
            is a heuristic estimate of the time to get from the current node to the end).
    """
    visited: bool
    came_from: Optional[Cell_ID]
    g_score: float
    f_score: float

    def __init__(self) -> None:
        """ Initialize default node values. g_score must be set to infinity so any g_score from a cell to a newly
            discovered neighbour will be smaller than the default g_score of the neighbour.
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

    # List of all cells to easily retrieve information from. Heap will store the cell ID along with it's f_score.
    cells = [Node() for _ in range(window.get_num_cells())]
    heap = Heap()

    # Cost from start to start is 0; starting cell's cost is purely heuristic.
    cells[start].g_score = 0
    cells[start].f_score = h_score(window, start, end)
    heap.push((cells[start].f_score, start))

    while not heap.empty():
        # Get cell with the lowest f_score. Keep popping until either the heap is empty or we find an up to date node
        # (we can insert the same node multiple times but with different f_scores, so a node in the heap may have an
        # outdated f_score).
        while True:
            top = heap.pop()
            current_id = top[1]

            if heap.empty() or cells[current_id].f_score == top[0]:
                break

        # Found the path to the end.
        if current_id == end:
            return construct_path(start, current_id, cells)

        # Mark cell as visited and check its neighbours.
        cells[current_id].visited = True
        for neighbour_id in window.get_neighbours(current_id):
            if cells[neighbour_id].visited:
                continue

            # Update neighbour's information if a better path is found and add to the heap.
            new_g_score = cells[current_id].g_score + ADJACENT_COST
            if new_g_score < cells[neighbour_id].g_score:
                cells[neighbour_id].came_from = current_id
                cells[neighbour_id].g_score = new_g_score
                cells[neighbour_id].f_score = new_g_score + h_score(window, neighbour_id, end)

                heap.push((cells[neighbour_id].f_score, neighbour_id))

    # No solution, return empty path.
    return []


def h_score(window: window.Window, cell1: Cell_ID, cell2: Cell_ID) -> float:
    """ Calculate the heuristic for two cells (euclidian distance). """
    c1_coords = window.cell_id_to_cell(cell1)
    c2_coords = window.cell_id_to_cell(cell2)
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(c1_coords, c2_coords)]))


def construct_path(start: Cell_ID, end: Cell_ID, cells: List[Node]) -> List[Cell_ID]:
    """ Construct the shortest path taken from start to end. """
    if start == end:
        return []

    path = [end]

    # Create the path by working backwards.
    current = end
    while current is not start:
        came_from = cells[current].came_from
        assert came_from is not None

        path.append(came_from)
        current = came_from

    path.reverse()
    return path
