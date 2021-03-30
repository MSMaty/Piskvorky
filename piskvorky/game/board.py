import re
import os
import copy
from typing import Any, Iterable, List, Tuple


velikost = 15

hrac1_victory = re.compile(r"11111")
hrac2_victory = re.compile(r"22222")

min1 = re.compile(r"011112|211110")
min2 = re.compile(r"011110")
min3 = re.compile(r"01110")
min4 = re.compile(r"0011102|2011100")
min5 = re.compile(r"011010|010110")
min6 = re.compile(r"0110")

max1 = re.compile(r"022221|122220")
max2 = re.compile(r"022220")
max3 = re.compile(r"02220")
max4 = re.compile(r"0022201|1022200")
max5 = re.compile(r"022020|020220")
max6 = re.compile(r"0220")

def spiral_matrix(n: int) -> List[Tuple[int, int]]:
    wx, wy = 1, 0
    x, y = 0, 0
    #tvoreni matice jako interpretaci souradnic
    matrix = [[-1]*n for k in range(n)]
    for i in range(n**2):
        matrix[x][y] = i
        hx, hy = x + wx, y + wy
        if 0 <= hx < n and 0 <= hy < n and matrix[hx][hy] == -1:
            x, y = hx, hy
        else:
            wx, wy = -wy, wx
            x, y = x + wx, y + wy

    output = [(0, 0) for k in range(n**2)]
    for i in range(n):
        for j in range(n):
            output[matrix[i][j]] = (i, j)
    return output

spiral = spiral_matrix(velikost)[::-1]

def stringify(matrix: List[List[int]]) -> str:
    string = ""
    for line in matrix:
        string += "".join(map(str, line)) + "\n"
    return string

class Board():

    stones = {0: ' ', 1: 'x', 2: 'o'}

    def __init__(self, ai: int) -> None:
        self._board = [[0 for k in range(velikost)] for k in range(velikost)]
        self._human = 1
        self._ai = ai
        self._last_play: Tuple[str, int] = ('', 0)
    
    """def __str__(self) -> str:
        letter_row = "     " + " ".join(chr(i) for i in range(65, 65 + len(self._board[0]))) + '\n'
        top_row = '   ┏' + '━' * (2 * len(self._board[0]) + 1) + '┓\n'
        bottom_row = '   ┗' + '━' * (2 * len(self._board[0]) + 1) + '┛'
        mid_rows = ""

        for row, i in zip(self._board, range(len(self._board))):
            mid_rows += '{:02d} ┃ '.format(i + 1) + ' '.join(Board.stones[i] for i in row) + ' ┃ {:02d}\n'.format(i + 1)

        return letter_row + top_row + mid_rows + bottom_row + '\n' + letter_row"""
    #Umístění x nebo o
    def place_xo(self, position: Tuple[int, int]) -> None:
        x_pos, y_pos = position
        self._last_play = (chr(x_pos + 65), y_pos + 1)
        self._board[y_pos][x_pos] = self._human
        self._human = 1 if self._human == 2 else 2
    
    # Kontrola zda je pozice volná
    def free(self, position: Tuple[int, int]) -> bool:
        x_pos, y_pos = position
        return self._board[y_pos][x_pos] == 0
    
    @property
    def last_play(self) -> Tuple[str, int]:
        return self._last_play
    
    def _diagonals1(self) -> List[List[int]]:
        return [[self._board[velikost - c + v - 1][v] for v in range(max(c - velikost + 1, 0), min(c + 1, velikost))]for c in range(velikost + velikost - 1)]
    
    def _diagonals2(self) -> List[List[int]]:
        return [[self._board[c - v][v]for v in range(max(c - velikost + 1, 0), min(c + 1, velikost))]for c in range(velikost + velikost - 1)]

    def _columns(self) -> List[List[int]]:
        return [[self._board[i][j]for i in range(velikost)]for j in range(velikost)]
    
    def victory(self) -> bool:
        whole_board = "\n".join(map(stringify,[self._board,self._diagonals1(),self._diagonals2(),self._columns()]))

        victory1 = hrac1_victory.search(whole_board)
        victory2 = hrac2_victory.search(whole_board)

        if victory1 or victory2:
            return (victory1, victory2)

        return False

    def evaluate(self) -> int:
        # Funkce která ohodnotí stav hry
        whole_board = "\n".join(map(stringify,[self._board, self._diagonals1(), self._diagonals2(), self._columns()]))

        hrac1_val = 0
        hrac2_val = 0
        if hrac1_victory.search(whole_board):
            hrac1_val += 2**25
        elif hrac2_victory.search(whole_board):
            hrac2_val +=2 **25

        # Tato část vyhledává všechny ohodnocené variace v celé hře
        hrac1_val += 56*len(min1.findall(whole_board))
        hrac1_val += 37*56*len(min2.findall(whole_board))
        hrac1_val += 56*len(min3.findall(whole_board))
        hrac1_val += 56*len(min4.findall(whole_board))
        hrac1_val += 56*len(min5.findall(whole_board))
        hrac1_val += len(min6.findall(whole_board))
        
        hrac2_val += 56*len(max1.findall(whole_board))
        hrac2_val += 37*56*len(max2.findall(whole_board))
        hrac2_val += 56*len(max3.findall(whole_board))
        hrac2_val += 56*len(max4.findall(whole_board))
        hrac2_val += 56*len(max5.findall(whole_board))
        hrac2_val += len(max6.findall(whole_board))

        return hrac1_val - hrac2_val if self._ai == 1 else hrac2_val - hrac1_val
        
    def vedle(self) -> Iterable[Any]:
        board_now = copy.deepcopy(self)
        for i, j in spiral:
            if board_now.free((i, j)):
                board_now.place_xo((i, j))
                yield board_now
                board_now._human = 1 if board_now._human == 2 else 2
                board_now._board[j][i] = 0

    
