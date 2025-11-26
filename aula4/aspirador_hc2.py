import math

ambiente = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 1],
]


def lerSensor(pos):
    x, y = pos

    for r in range(1, 3):
        for i in range(x - r, x + r + 1):
            for j in range(y - r, y + r + 1):
                if i < 0 or i > 2 or j < 0 or j > 2:
                    continue

                if ambiente[i][j] == 1:
                    ambiente[i][j] = 0
                    x, y = i, j

                    return i, j


def calc_heuristic(start, end):
    return math.sqrt(abs(start[0] - end[0]) ** 2 + abs(start[1] - end[1]) ** 2)


def get_neighbours(pos, matrix):
    y, x = pos
    neighbours = []
    rows, cols = len(matrix), len(matrix[0])

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue

            yi, xj = y + i, x + j

            if 0 <= yi < rows and 0 <= xj < cols:
                neighbours.append((yi, xj))

    return neighbours


def pensar(start, end, matrix):
    path = [start]
    current_pos = start
    current_h = calc_heuristic(current_pos, end)

    while True:
        if current_pos[0] == end[0] and current_pos[1] == end[1]:
            break

        info = []
        neighbours = get_neighbours(current_pos, matrix)
        for n in neighbours:
            info.append(
                {
                    "coords": n,
                    "heuristic": calc_heuristic(n, end),
                }
            )

        best: dict = min(info, key=lambda x: x["heuristic"])
        if best["heuristic"] >= current_h:
            print("No better path - stopped")
            break

        print(f"Moving to {best['coords']}")
        current_pos = best["coords"]
        current_h = best["heuristic"]

        path.append(current_pos)

    return path


pos = (0, 0)
i, j = lerSensor(pos)

print("Sujeira detectada em:", (i, j))
print("Posição aspirador:", pos)
movimentos = pensar(pos, [i, j], ambiente)
print("Movimentos:", movimentos)
