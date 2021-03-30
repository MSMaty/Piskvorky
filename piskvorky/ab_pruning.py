import copy
from typing import Tuple
from game.board import Board

# Minmax algoritmus
def ab_pruning(board: Board, depth: int, alpha: int, beta: int, max_player: bool) -> Tuple[Board, int]:
    new_board: Board = None
    depth_limit = 5
    if depth == 0 or board.victory():
        return board, board.evaluate()
    elif max_player:
        value = -2**32
        for child in board.vedle():
            k, node_value = ab_pruning(child, depth - 1, alpha, beta, False)
            #alpha-beta pruning
            if node_value > value:
                value = node_value
                new_board = copy.deepcopy(child)
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return new_board, value
    else:
        value = 2**32
        for child in board.vedle():
            k, node_value = ab_pruning(child, depth - 1, alpha, beta, True)
            # alpha-beta pruning
            if node_value < value:
                value = node_value
                new_board = copy.deepcopy(child)
            beta = min(beta, value)
            if beta <= alpha:
                break
        return new_board, value
