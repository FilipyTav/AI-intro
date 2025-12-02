from dataclasses import dataclass
from typing import TypeAlias
import math
import random

AMOUNT_APTS: int = 4
AMOUNT_ACCEPTABLE: int = 30
# In percentage
PROB_MUTATION: int = 23


@dataclass
class Coord2D:
    x: int
    y: int


Matrix2D: TypeAlias = list[list[int]]
Indiv: TypeAlias = list[Coord2D]


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


def calc_heuristic(start: Coord2D, end: Coord2D) -> float:
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


possible_moves: list[int] = [0, 1, 2]


def gen_indivs(
    amount_indiv: int, amount_genes: int, initial_pos: Coord2D
) -> list[Indiv]:
    indivs: list[Indiv] = []
    for _ in range(amount_indiv):
        genes: list[Coord2D] = [Coord2D(initial_pos.x, initial_pos.y)]
        for _ in range(amount_genes - 1):
            genes.append(
                Coord2D(random.choice(possible_moves), random.choice(possible_moves))
            )
        indivs.append(genes)
    return indivs


def crossover(indiv1: Indiv, indiv2: Indiv):
    size: int = len(indiv1)
    children: list[Indiv] = []
    for i in range(1, size):
        # Gets first i of one and last (size - i) from other
        children.append(indiv1[:i] + indiv2[-(size - i) :])
        children.append(indiv2[:i] + indiv1[-(size - i) :])

    return children


def mutate(indiv: Indiv, matrix_size: int) -> Indiv:
    ind: Indiv = indiv.copy()

    random_index: int = random.randint(0, len(ind) - 1)
    pos_moves: list[int] = [1, -1]
    seed: int = random.randint(0, 1)

    if seed == 0:
        # print("Mutation on x")
        new_value: int = ind[random_index].x + random.choice(pos_moves)
        if new_value >= 0 and new_value < matrix_size:
            ind[random_index].x = new_value
    else:
        # print("Mutation on y")
        new_value: int = ind[random_index].y + random.choice(pos_moves)
        if new_value >= 0 and new_value < matrix_size:
            ind[random_index].y = new_value
    return ind


def is_valid_move(start: Coord2D, end: Coord2D) -> bool:
    return abs(start.x - end.x) <= 1 and abs(start.y - end.y) <= 1


def is_valid_indiv(indiv: Indiv, start_pos: Coord2D, correct_size: int) -> bool:
    if not indiv or indiv[0] != start_pos:
        return False

    if len(indiv) != correct_size:
        return False

    for i in range(len(indiv) - 1):
        if not is_valid_move(indiv[i], indiv[i + 1]):
            return False

    return True


def genetic_algo(
    matrix: Matrix2D, start: Coord2D, end: Coord2D, gens: int = 150, pop_size: int = 100
) -> Indiv:
    min_len = max(abs(start.x - end.x), abs(start.y - end.y)) + 1
    pop: list[Indiv] = gen_indivs(pop_size, min_len, start)

    for i in range(gens):
        scores: list[tuple[Indiv, float]] = []
        for indiv in pop:
            scores.append((indiv, calc_heuristic(indiv[-1], end)))

        scores.sort(key=lambda item: item[1])
        pop = [x for x, _ in scores]

        best = scores[0]
        best_indiv: Indiv = best[0]
        best_h: float = best[1]

        # print(
        #     f"Best: {best_indiv} --- Valid: {is_valid_indiv(best_indiv, start, min_len)}"
        # )

        if best_h == 0 and is_valid_indiv(best_indiv, start, min_len):
            print("Found solution!")
            return best_indiv

        # Elitism
        apts: list[Indiv] = pop[:AMOUNT_APTS]
        acceptables: list[Indiv] = pop[:AMOUNT_ACCEPTABLE]

        attempts = 0
        max_attempts = 1000  # arbitrary safe number
        while len(apts) < pop_size and attempts < max_attempts:
            attempts += 1
            dad: Indiv = random.choice(acceptables)
            mom: Indiv = random.choice(acceptables)

            children = crossover(dad, mom)
            for i in range(len(children)):
                if len(apts) >= pop_size:
                    break

                if random.random() < PROB_MUTATION / 100:
                    children[i] = mutate(children[i], min_len)

                if is_valid_indiv(children[i], start, min_len):
                    apts.append(children[i])

        pop = apts

    # No valid Individual found
    print("Could not find a valid path")
    return [Coord2D(-1, -1)]


# environment: list[list[int]] = [
#     [0, 2, 0, 2, 0],
#     [0, 2, 0, 2, 0],
#     [0, 0, 0, 2, 0],
#     [0, 2, 0, 2, 0],
#     [0, 2, 0, 0, 0],
# ]

environment: list[list[int]] = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 1],
]

pos = [0, 0]
# a = genetic_algo(environment, Coord2D(0, 0), Coord2D(2, 2))
# print("Best route: ", a)

# print(path)

while True:
    search_res: dict[str, int] = read_sensor(pos, environment)
    dirty: list[int] = [search_res["y"], search_res["x"]]

    # All clean
    if pos == dirty:
        break
    print("Trash in", dirty)

    path: list[Coord2D] = genetic_algo(
        environment, Coord2D(pos[1], pos[0]), Coord2D(search_res["x"], search_res["y"])
    )

    print("Path: ", path)

    pos = dirty

    clean_tile(pos, environment)
    print()
