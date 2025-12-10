from typing import TypeAlias
from dataclasses import dataclass


MAX_PLAYER: int = 1
MIN_PLAYER: int = 2


@dataclass
class Coord2D:
    x: int
    y: int


Matrix2D: TypeAlias = list[list[int]]

NEUTRAL_TILE: int = 0


class Node:
    def __init__(self, state: Matrix2D, score: float = 0):
        self.children: list[Node] = []
        self.state: Matrix2D = state
        self.score: float = score

    def gen_children(self, player: int, opponent: int, is_max: bool):
        for r in range(len(self.state)):
            for c in range(len(self.state[r])):
                if self.state[r][c] == NEUTRAL_TILE:
                    new_state = [row[:] for row in self.state]  # Deep copy of the board
                    new_state[r][c] = player

                    new_node: Node = Node(new_state)
                    new_node.score = (
                        new_node.calc_score(player, opponent)
                        if is_max
                        else new_node.calc_score(opponent, player)
                    )

                    self.children.append(new_node)

                    if not new_node.is_full() and new_node.score == 0:
                        new_node.gen_children(opponent, player, not is_max)

    # Checks for winner
    def calc_score(self, max: int, min: int, multiplier: int = 10) -> float:
        board = self.state
        # Diagonal 1
        if board[0][0] == board[1][1] == board[2][2] == max:
            return multiplier
        if board[0][0] == board[1][1] == board[2][2] == min:
            return -multiplier

        # Diagonal 2
        if board[0][2] == board[1][1] == board[2][0] == max:
            return multiplier
        if board[0][2] == board[1][1] == board[2][0] == min:
            return -multiplier

        for i in range(len(board)):
            # Horizontal
            row: list[int] = board[i]
            if row[0] == row[1] == row[2] == max:
                return multiplier
            if row[0] == row[1] == row[2] == min:
                return -multiplier

            # Vertical
            if board[0][i] == board[1][i] == board[2][i] == max:
                return multiplier
            if board[0][i] == board[1][i] == board[2][i] == min:
                return -multiplier

        # If no winner, return 0 (game is ongoing or draw)
        return 0

    def is_leaf(self):
        return len(self.children) == 0

    def is_full(self) -> bool:
        for row in self.state:
            if NEUTRAL_TILE in row:
                return False
        return True

    def __repr__(self):
        """Return a string representation of the board and its score."""
        board_str = "\n".join([" ".join(str(x) for x in row) for row in self.state])
        return f"Board:\n{board_str}\nScore: {self.score}"


def minimax(
    node: Node, player: int, opponent: int, is_max: bool = True
) -> tuple[float, Node]:
    score = node.score

    # If a player has won, return the score
    if score != 0:
        return score, node

    if is_max:
        best_score = float("-inf")
        best_move = None
        for c in node.children:
            move_score, _ = minimax(c, player, opponent, not is_max)
            if move_score > best_score:
                best_score = move_score
                best_move = c
        return (best_score, best_move)
    else:
        best_score = float("inf")
        best_move = None
        for c in node.children:
            move_score, _ = minimax(c, player, opponent, not is_max)
            if move_score < best_score:
                best_score = move_score
                best_move = c
        return (best_score, best_move)


def print_matrix(matrix: Matrix2D):
    for row in matrix:
        print(" ".join(str(x) for x in row))


# Visualize the tree of nodes and their children
def visualize_tree(node: Node, depth: int = 0):
    """Recursively visualize the tree of nodes"""
    # Indentation for tree structure visualization
    indent = " " * (depth * 4)
    print(f"{indent}Node Score: {node.score}")
    print(f"{indent}State:")
    print_matrix(node.state)
    print()

    # Recursively visualize each child node
    def __lt__(self, n: "Node") -> bool:
        return self.score < n.score

    for child in node.children:
        visualize_tree(child, depth + 1)


if __name__ == "__main__":
    board: Matrix2D = [
        [1, 0, 0],
        [0, 1, 0],
        [2, 0, 2],
    ]

    root: Node = Node(board)
    root.score = root.calc_score(MAX_PLAYER, MIN_PLAYER)
    root.gen_children(MAX_PLAYER, MIN_PLAYER, True)

    # Only calculates the next best move
    best_score, best_move = minimax(root, MAX_PLAYER, MIN_PLAYER)
    print(f"Best score: {best_score} ")
    print(f"Best move:\n{best_move}")
