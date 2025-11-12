def cleanTile(pos: list[int], env: list[list[int]]) -> None:
    env[pos[0]][pos[1]] = 0


def readSensor(pos: list[int], env: list[list[int]]) -> list[int]:
    y, x = pos
    print("position: (y, x)", y, x)
    matrix_size: int = len(env[0])
    radius: int = 0
    found: bool = False
    for i in range(matrix_size - 1):
        if found:
            break
        radius = i + 1
        print("radius: ", radius)

        cols, rows = get_axes((y, x), radius, matrix_size)
        print(cols, rows)

        # TODO: Eliminate redundancy: there's an overlap on the search of the rows and cols
        for colx in cols:
            if found:
                break

            upper, lower = determine_bounds(y, radius, matrix_size)
            for i in range(upper, lower):
                col, row = colx, i
                print("coords: ", row, col, ": ", env[row][col])

                if env[row][col]:
                    x = col
                    y = row
                    found = True
                    break

        for rowy in rows:
            if found:
                break

            upper, lower = determine_bounds(x, radius, matrix_size)
            for i in range(upper, lower):
                col, row = i, rowy
                print("coords: ", row, col, ": ", env[row][col])

                if env[row][col]:
                    x = col
                    y = row
                    found = True
                    break

            print("")

    return [y, x, radius]


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


# (0, 1), (1, 0), (1, 1)
environment: list[list[int]] = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0],
]

# environment: list[list[int]] = [
#     [9, 0, 0],
#     [0, 0, 0],
#     [0, 0, 0],
# ]

pos: list[int] = [0, 2]

a = readSensor(pos, environment)
print("sujo: ", a)

