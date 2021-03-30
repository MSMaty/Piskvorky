import time
import _thread

from random import choice

import pygame as pg

from pygame import gfxdraw

from game.ui import *
from game.board import Board
from game.settings import *

from ab_pruning import ab_pruning

class Menu(View):
    # Class reprezentující vzhled menu
    def __init__(self, game, render_resolution):
        super().__init__(render_resolution)

        self.game = game

        self.labels = [
            Label(MenuSettings.TITLE_CENTER,
                **MenuSettings.TITLE_KWARGS),
            Label(MenuSettings.SUBTITLE_CENTER,
                **MenuSettings.SUBTITLE_KWARGS),
        ]

        self.buttons = [
            # Play first
            Button(MenuSettings.PLAY1_CENTER,
                   MenuSettings.PLAY1_SIZE,
                 **MenuSettings.PLAY1_KWARGS,
                   click_callback=lambda: self.game.play(True)),
            # Play second
            Button(MenuSettings.PLAY2_CENTER,
                   MenuSettings.PLAY2_SIZE,
                 **MenuSettings.PLAY2_KWARGS,
                   click_callback=lambda: self.game.play(False)),
            # Easy
            Button(MenuSettings.EASY_CENTER,
                   MenuSettings.EASY_SIZE,
                 **MenuSettings.EASY_KWARGS,
                   click_callback=lambda: self.game.choose_difficulty(1)),
            # Hard
            Button(MenuSettings.HARD_CENTER,
                   MenuSettings.HARD_SIZE,
                 **MenuSettings.HARD_KWARGS,
                   click_callback=lambda: self.game.choose_difficulty(2)),
            # Medium
            Button(MenuSettings.MEDIUM_CENTER,
                   MenuSettings.MEDIUM_SIZE,
                 **MenuSettings.MEDIUM_KWARGS,
                   click_callback=lambda: self.game.choose_difficulty(3)),
            # Quit
            Button(MenuSettings.QUIT_CENTER,
                   MenuSettings.QUIT_SIZE,
                 **MenuSettings.QUIT_KWARGS,
                   click_callback=self.game._quit)
        ]
    
    def _loop(self, dt):
        for b in self.buttons:
            b.down = False
        self.buttons[1 + self.game.difficulty].down = True

class GameUi(View):
    # Class s funkcemi pro vzhled hry
    def __init__(self, game, render_resolution):
        super().__init__(render_resolution)

        self.game = game

        self.labels = [
            Label(GameUiSettings.TURN_CENTER,
                **GameUiSettings.TURN_KWARGS)
        ]

        self.buttons = [
            # Tlačítko quit
            Button((MenuSettings.QUIT_CENTER[0], 750),
                   MenuSettings.QUIT_SIZE,
                 **MenuSettings.QUIT_KWARGS,
                   click_callback=self.game.to_menu)
        ]

        self.initialize_buttons()

        self.player_turn = True
        self.hovered = None
        self.victory = False

    def initialize_buttons(self):
        # Spustí tlačítka na hrací ploše
        cell_size = GameUiSettings.GRID_CELLSIZEX, GameUiSettings.GRID_CELLSIZEY
        for r in range(GameUiSettings.ROWS):
            for c in range(GameUiSettings.COLS):
                x = c * cell_size[0] + GameUiSettings.GRID[0]
                y = r * cell_size[1] + GameUiSettings.GRID[1]
                button = Button(
                    (x + cell_size[0] // 2, y + cell_size[1] // 2),
                    cell_size,
                    visible=False,
                    hover_callback=lambda o=(r, c): self.hover_cell(o),
                    click_callback=lambda p=(r, c): self.mark_cell(p)
                )
                self.buttons.append(button)

    def reset(self):
        # Připraví plochu na další hru
        self.board = Board(2)
        self.hovered = None
        self.victory = False
        self.match_running = False
        self.labels[0].update_text("")
        self.labels[0].update()
    
    def start_ai(self):
        _thread.start_new_thread(self.ai_move, ())

    def hover_cell(self, rowcol):
        self.hovered = rowcol
        
    def mark_cell(self, rowcol):
        row, col = rowcol
        if not self.victory and self.player_turn and self.board.free((col, row)):
            self.board.place_xo((col, row))
            self.player_turn = False
            
    def ai_move(self):
        # Funkce která nechává běžet pygame loop, mezitím co ai propočítává další tah
        while self.match_running and not self.victory:
            time.sleep(0.1)
            if not self.player_turn:
                depth = self.game.difficulty
                # Pokud hráč zvolí medium tak minmax náhodně vybírá mezi depth 1 a 2
                if depth == 3:
                    depth = choice([1, 2])
                if self.mark == "x":
                    board, k = ab_pruning(self.board, depth, -2**32, 2**32, True)
                else:
                    board, k = ab_pruning(self.board, depth, -2**32, 2**32, False)
                if not self.match_running:
                    break
                self.board = board
                self.player_turn = True

    def _loop(self, dt):
        # Hlavní loop hry
        self.victory = self.board.victory()
        if self.victory:
            if self.victory[1]:
                if self.mark == "x":
                    text = "AI wins!"
                else:
                    text = "You win!"
            else:
                if self.mark == "o":
                    text = "AI wins!"
                else:
                    text = "You win!"
        else:
            text = GameUiSettings.TURN_TEXT[int(self.player_turn)]

        if (self.victory or not self.player_turn) and \
                pg.mouse.get_pos()[1] < GameUiSettings.GRID[1] + GameUiSettings.GRID[3]:
            self.pointing_cursor = False
        
        # Updating top label
        self.labels[0].update_text(text)

    def draw_board(self):
        # Nakreslení 15x15 hracího pole na plochu
        grid_rect = GameUiSettings.GRID
        cell_size = GameUiSettings.GRID_CELLSIZEX, GameUiSettings.GRID_CELLSIZEY
        border_thick, inner_thick = GameUiSettings.GRID_THICKNESS
        border_color, inner_color = GameUiSettings.GRID_COLOR
        # Kreslení horizontálních čar
        for r in range(GameUiSettings.ROWS):
            y = r * cell_size[1]
            pg.draw.line(
                self.surface,
                inner_color,
                (grid_rect[0], grid_rect[1] + y),
                (grid_rect[0] + grid_rect[2], grid_rect[1] + y),
                inner_thick
            )
        # Kreslení verikálních čár
        for c in range(GameUiSettings.COLS):
            x = c * cell_size[0]
            pg.draw.line(
                self.surface,
                inner_color,
                (grid_rect[0] + x, grid_rect[1]),
                (grid_rect[0] + x, grid_rect[1] + grid_rect[3]),
                inner_thick
            )
        # Drawing frame
        pg.draw.rect(
            self.surface,
            border_color,
            GameUiSettings.GRID,
            border_thick)

    def draw_mark(self, mark, cell, color=GameUiSettings.MARK_COLOR[0]):
        # Nakreslí x nebo o do daného čtverečku
        row, col = cell
        grid = GameUiSettings.GRID
        cell_size = GameUiSettings.GRID_CELLSIZEX, GameUiSettings.GRID_CELLSIZEY
        outer_radius, inner_radius = GameUiSettings.CIRCLE_RADIUS
        color = color

        x = col * cell_size[0] + grid[0] + cell_size[0] // 2
        y = row * cell_size[1] + grid[1] + cell_size[1] // 2

        font = GameUiSettings.MARK_FONT
        mark_surf = font.render(mark, True, color)
        mark_rect = mark_surf.get_rect(center=(x, y))
        self.surface.blit(mark_surf, mark_rect)

    def draw_state(self):
        # Tato funkce kreslí x a o podle aktuálního stavu hry
        for r, row in enumerate(self.board._board):
            for c, cell in enumerate(row):
                if cell != 0:
                    self.draw_mark(self.board.stones[cell], (r, c))
                elif self.hovered == (r, c) and self.player_turn and not self.victory:
                    self.draw_mark(self.mark, (r, c), GameUiSettings.MARK_COLOR[1])
        
        self.hovered = None

    def _draw(self):
        self.surface.fill(BASE_BG_COLOR)
        self.draw_board()
        self.draw_state()

   