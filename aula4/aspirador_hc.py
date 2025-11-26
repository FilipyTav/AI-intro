from dataclasses import dataclass
from typing import TypeAlias
import math
import random

Matrix2D: TypeAlias = list[list[int]]


@dataclass
class Coord2D:
    x: int
    y: int


def move(pos: tuple[int, int], destination: tuple[int, int], matrix_size: int):
    # path = bfs_search((pos[1], pos[0]), (destination[1], destination[0]), matrix_size)
    # print("Found the shortest path: ", path)
    # return path[-1]
    pass


def clean_tile(pos: list[int], matrix: list[list[int]]) -> None:
    matrix[pos[0]][pos[1]] = 0
    print(f"cleaned ({pos[0]}, {(pos[1])})")


def read_sensor(pos: list[int], env: list[list[int]]) -> dict[str, int]:
    y, x = pos
    print("position: (y, x)", y, x)
    # The matrix is bi-dimensional and squared
    matrix_size: int = len(env[0])
    radius: int = 0
    found: bool = False
    for i in range(matrix_size - 1):
        if found:
            break
        radius = i + 1
        # print("radius: ", radius)

        cols, rows = get_axes((y, x), radius, matrix_size)
        # print(cols, rows)

        # TODO: Eliminate redundancy: there's an overlap between the searchs of rows and cols
        for colx in cols:
            row, col = search_matrix(env, colx, "col", y, radius)
            if not (row < 0 or col < 0):
                found = True
                x = col
                y = row
                break

        for rowy in rows:
            row, col = search_matrix(env, rowy, "row", x, radius)
            if not (row < 0 or col < 0):
                found = True
                x = col
                y = row
                break

    return {"y": y, "x": x, "radius": radius}


def determine_bounds(axis_val: int, radius: int, matrix_size: int) -> tuple[int, int]:
    upper: int = axis_val - radius if axis_val != 0 else axis_val
    lower: int = axis_val + radius + 1 if axis_val != matrix_size - 1 else axis_val + 1
    upper = upper if upper > 0 else 0
    lower = lower if lower < matrix_size else matrix_size
    return (upper, lower)


# Coords as y, x
def get_axes(
    coords: tuple[int, int], radius: int, matrix_size: int
) -> tuple[list[int], list[int]]:
    form: tuple[int, int] = (-radius, radius)
    y, x = coords

    # X axis
    cols: list[int] = []
    # Y axis
    rows: list[int] = []
    for i in form:
        col: int = x + i
        if not (col < 0 or col >= matrix_size):
            cols.append(col)

        row: int = y + i
        if not (row < 0 or row >= matrix_size):
            rows.append(row)

    return (cols, rows)


# Return (y, x) if found, (-1, -1) otherwise
def search_matrix(
    matrix: list[list[int]],
    axis: int,
    axis_name: str,
    axis_val: int,
    radius: int,
) -> tuple[int, int]:
    matrix_size: int = len(matrix)
    upper, lower = determine_bounds(axis_val, radius, matrix_size)
    for i in range(upper, lower):
        col = row = -1
        if axis_name == "col":
            col, row = axis, i
        elif axis_name == "row":
            col, row = i, axis

        # print("coords: ", row, col, ": ", matrix[row][col])

        # x = col
        # y = row
        if matrix[row][col] == 1:
            return (row, col)
    return (-1, -1)


def calc_hc_heuristic(start: Coord2D, end: Coord2D) -> float:
    # Euclidian distance
    return math.sqrt(abs(start.x - end.x) ** 2 + abs(start.y - end.y) ** 2) * 10


def get_neighbours(pos: Coord2D, matrix_size: int) -> list[Coord2D]:
    neighbours: list[Coord2D] = []
    for i in range(-1, 2):
        xb: int = pos.x - 1
        xa: int = pos.x + 1
        y: int = pos.y + i
        if xb >= 0:
            if y >= 0 and y < matrix_size:
                neighbours.append(Coord2D(xb, y))
        if xa < matrix_size:
            if y >= 0 and y < matrix_size:
                neighbours.append(Coord2D(xa, y))

    if pos.y - 1 >= 0:
        neighbours.append(Coord2D(pos.x, pos.y - 1))
    if pos.y + 1 < matrix_size:
        neighbours.append(Coord2D(pos.x, pos.y + 1))
    return neighbours


def get_hc_neighbours(pos: Coord2D, matrix: Matrix2D) -> list[Coord2D]:
    n: list[Coord2D] = get_neighbours(pos, len(matrix))
    return list(filter(lambda p: matrix[p.y][p.x] != 2, n))


def hill_climbing(start: Coord2D, end: Coord2D, matrix: Matrix2D, prints=False):
    # Start
    current_tile = start
    path: list[Coord2D] = [start]

    # Calc current heuristic
    current_h = calc_hc_heuristic(current_tile, end)

    while True:
        if current_tile == end:
            break

        # Get neighbours
        neighbours: list[Coord2D] = get_hc_neighbours(current_tile, matrix)
        n_info: list[dict] = []

        # Calc heuristic for neighbours
        for n in neighbours:
            n_info.append(
                {
                    "coords": n,
                    "heuristic": calc_hc_heuristic(n, end),
                }
            )

        # Choose best neighbour
        best_n: dict = min(n_info, key=lambda x: x["heuristic"])
        random_n: dict = n_info[random.randint(0, len(n_info) - 1)]

        if prints:
            print(current_tile, current_h)
            print(f"Best n {best_n}")
            print(f"Random n: {random_n}")

        p: float = min(1, math.exp((current_h - random_n["heuristic"]) / 10))
        if prints:
            print(f"P: {p}")

        # Go to random tile, with a probability
        if random.random() < p:
            if prints:
                print("Taking random path...")
            current_h = random_n["heuristic"]
            current_tile = random_n["coords"]

        elif best_n["heuristic"] < current_h:
            current_h = best_n["heuristic"]
            current_tile = best_n["coords"]

        if prints:
            print("Next: ", current_tile)
            print()

        path.append(current_tile)
    return path


# environment: list[list[int]] = [
#     [0, 2, 0, 2, 0],
#     [0, 2, 0, 2, 0],
#     [0, 0, 0, 2, 0],
#     [0, 2, 0, 2, 0],
#     [0, 2, 0, 0, 0],
# ]

environment: list[list[int]] = [
    [0, 2, 1],
    [0, 2, 0],
    [0, 0, 1],
]

pos = [0, 0]
# path: list[Coord2D] = hill_climbing(Coord2D(0, 0), Coord2D(2, 0), environment)

# print(path)

while True:
    search_res: dict[str, int] = read_sensor(pos, environment)
    dirty: list[int] = [search_res["y"], search_res["x"]]

    # All clean
    if pos == dirty:
        break
    print("Trash in", dirty)

    # Avoids obstacles - stochastic
    path: list[Coord2D] = hill_climbing(
        Coord2D(pos[1], pos[0]),
        Coord2D(search_res["x"], search_res["y"]),
        environment,
        # for more info on the path
        # True,
    )
    print("Path: ", path)

    pos = dirty

    clean_tile(pos, environment)
    print()
