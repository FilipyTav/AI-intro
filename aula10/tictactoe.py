from typing import TypeAlias
from dataclasses import dataclass

@dataclass
class Coord2D:
    x: int
    y: int

Matrix2D: TypeAlias = list[list[int]]

NEUTRAL_TILE: int = 0

class Node:
    def __init__(self, state: Matrix2D, score: int = 0):
        self.children: list[Node] = []
        self.state: Matrix2D = state
        self.score: int = score

    def gen_children(self, player: int):
            for r in range(len(self.state)):
                for c in range(len(self.state[r])):
                    if self.state[r][c] == NEUTRAL_TILE:
                        new_state = [row[:] for row in self.state]  # Deep copy of the board
                        new_state[r][c] = player

                        self.children.append(Node(new_state)) 

    def calc_score(self, player: int, multiplier: int = 10) -> float:
        board: Matrix2D = self.state
        # Diagonal 1
        if board[0][0] == board[1][1] == board[2][2] == player:
            return multiplier

        # Diagonal 2
        if board[0][2] == board[1][1] == board[2][0] == player:
            return multiplier

        for i in range(len(board)):
            # Horizontal
            row: list[int] = board[i] 
            if row[0] == row[1] == row[2] == player:
                return multiplier

            # Vertical
            if board[0][i] == board[1][i] == board[2][i] == player:
                return multiplier

        # If no winner, return 0 (game is ongoing or draw)
        return 0

    def is_leaf(self):
        return len(self.children) == 0


p1: int = 1
p2: int = 2

board: Matrix2D = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

def minimax():
    pass


# Checks for winner
def check_board(board: Matrix2D, player: int, multiplier: int = 10) -> float:
    # Diagonal 1
    if board[0][0] == board[1][1] == board[2][2] == player:
        return multiplier

    # Diagonal 2
    if board[0][2] == board[1][1] == board[2][0] == player:
        return multiplier

    for i in range(len(board)):
        # Horizontal
        row: list[int] = board[i] 
        if row[0] == row[1] == row[2] == player:
            return multiplier

        # Vertical
        if board[0][i] == board[1][i] == board[2][i] == player:
            return multiplier

    # If no winner, return 0 (game is ongoing or draw)
    return 0


def tictactoe():
    pass

def print_matrix(matrix: Matrix2D):
    for row in matrix:
        print(" ".join(str(x) for x in row))

root: Node = Node(board)
root.gen_children(p1)

for c in root.children:
    print_matrix(c.state)
    print()
