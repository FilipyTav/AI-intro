from dataclasses import dataclass
import math


@dataclass
class Coordinate2D:
    x: int = 0
    y: int = 0


class Node:
    def __init__(self, position: Coordinate2D, parent=None):
        """
        A Node for the A* algorithm.
        :param position: The (x, y) position of the node in the grid.
        :param parent: The parent node (for path reconstruction).
        """
        self.position = position
        self.parent = parent  # Parent node reference
        self._g = 0  # Cost from the start node to this node
        self._h = 0  # Heuristic estimated cost from this node to the goal
        self.f = self._g + self._h  # Total cost (f = g + h)

    @property
    def g(self):
        """
        :return: g value (cost from start node).
        """
        return self._g

    @g.setter
    def g(self, value):
        """
        :param value: New g value.
        """
        self._g = value
        self.f = self._g + self._h  # Update f whenever g changes

    @property
    def h(self):
        """
        :return: h value (heuristic cost to goal).
        """
        return self._h

    @h.setter
    def h(self, value):
        """
        :param value: New h value.
        """
        self._h = value
        self.f = self._g + self._h  # Update f whenever h changes

    def __eq__(self, other):
        """
        Equality check for comparing two nodes based on their positions.
        :param other: Another Node object.
        :return: True if the nodes have the same position.
        """
        return self.position == other.position

    def __lt__(self, other):
        """
        Comparison operator for sorting nodes based on their f values (for priority queue).
        :param other: Another Node object.
        :return: True if this node's f value is less than the other node's f value.
        """
        return self.f < other.f

    def __repr__(self):
        """
        String representation of the node for debugging.
        :return: String format: (x, y)
        """
        return f"Node({self.position})"


def get_neighbours(pos: Coordinate2D, matrix_size: int) -> list[Coordinate2D]:
    neighbours: list[Coordinate2D] = []
    for i in range(-1, 2):
        xb: int = pos.x - 1
        xa: int = pos.x + 1
        y: int = pos.y + i
        if xb >= 0:
            if y >= 0 and y < matrix_size:
                neighbours.append(Coordinate2D(xb, y))
        if xa < matrix_size:
            if y >= 0 and y < matrix_size:
                neighbours.append(Coordinate2D(xa, y))

    if pos.y - 1 >= 0:
        neighbours.append(Coordinate2D(pos.x, pos.y - 1))
    if pos.y + 1 < matrix_size:
        neighbours.append(Coordinate2D(pos.x, pos.y + 1))
    return neighbours


def calc_heuristic(start: Coordinate2D, goal: Coordinate2D) -> int:
    return int(math.sqrt(abs(goal.x - start.x) ** 2 + abs(goal.y - start.y) ** 2) * 10)


def a_star_search(graph, start, goal):
    pass


matrix = [
    [0, 0, 0],
    [0, 9, 0],
    [0, 0, 0],
]

a = get_neighbours(Coordinate2D(0, 2), 3)
print(calc_heuristic(Coordinate2D(0, 0), Coordinate2D(2, 2)))
