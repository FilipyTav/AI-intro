def move(pos: tuple[int, int], destination: tuple[int, int], matrix_size: int):
    path = bfs_search((pos[1], pos[0]), (destination[1], destination[0]), matrix_size)
    print("Found the shortest path: ", path)
    return path[-1]


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
        if matrix[row][col]:
            return (row, col)
    return (-1, -1)


from collections import deque


def get_neighbours(pos: tuple[int, int], matrix_size: int) -> list[tuple[int, int]]:
    neighbours: list[tuple[int, int]] = []
    for i in range(-1, 2):
        xb: int = pos[0] - 1
        xa: int = pos[0] + 1
        y: int = pos[1] + i
        if xb >= 0:
            if y >= 0 and y < matrix_size:
                neighbours.append((xb, y))
        if xa < matrix_size:
            if y >= 0 and y < matrix_size:
                neighbours.append((xa, y))

    if pos[1] - 1 >= 0:
        neighbours.append((pos[0], pos[1] - 1))
    if pos[1] + 1 < matrix_size:
        neighbours.append((pos[0], pos[1] + 1))
    return neighbours


def bfs_search(start, goal, matrix_size) -> list[tuple[int, int]]:
    queue = deque([[start]])
    visited = set()

    while queue:
        path = queue.popleft()
        node = path[-1]

        print("Current node: ", node)
        print("Goal: ", goal)
        if node == goal:
            return path

        if node not in visited:
            visited.add(node)

            n = get_neighbours((node[0], node[1]), matrix_size)
            print("Neighbours: ", n)
            for neighbour in n:
                new_path = path + [neighbour]
                queue.append(new_path)
            print()

    return [(-1, -1)]


# (0, 1), (1, 0), (1, 1)
# environment: list[list[int]] = [
#     [0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 1],
#     [1, 0, 0, 0, 0],
#     [0, 0, 1, 1, 0],
#     [0, 1, 0, 0, 1],
# ]

environment: list[list[int]] = [
    [0, 0, 0],
    [0, 0, 1],
    [1, 1, 0],
]

pos: list[int] = [0, 1]

# start = (3, 0)
# goal = (4, 4)
# a = move(start, goal, 5)
# print("Res: ", a)

while True:
    search_res: dict[str, int] = read_sensor(pos, environment)
    dirty: list[int] = [search_res["y"], search_res["x"]]

    # All clean
    if pos == dirty:
        break

    move((pos[0], pos[1]), (dirty[0], dirty[1]), len(environment))
    pos = dirty
    clean_tile(pos, environment)
    print()
