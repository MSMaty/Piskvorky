import ctypes
import pygame as pg

from game.views import Menu, GameUi
from game.settings import *

class Game:
    """A class to handle the game."""
    def __init__(self):
        # Spuštení game window, hodiny(FPS) a views
        ctypes.windll.user32.SetProcessDPIAware()

        self.screen = pg.display.set_mode(RESOLUTION)
        pg.display.set_caption(CAPTION)

        pg.font.init()
        self.clock = pg.time.Clock()

        # Spuštení views
        self.menu = Menu(self, RESOLUTION)
        self.gameui = GameUi(self, RESOLUTION)

        self.difficulty = 1
        self.to_menu()

    def set_cursor(self, pointing):
        if pointing:
            pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_HAND)
        else:
            pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_ARROW)

    def run(self):
        # Hlavní game loop
        self.running = True
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.check_events()
            self.update(dt)
            self.draw()
            self.set_cursor(self.curr_view.pointing_cursor)

    def _quit(self):
        # Ukončení hry
        self.running = False

    def choose_difficulty(self, difficulty):
        # Nastavení obtížnosti pro další hru
        self.difficulty = difficulty        

    def play(self, player_starts):
        # Spuštení hry
        if not player_starts:
            self.gameui.player_turn = False
            self.gameui.mark = "o"
        else:
            self.gameui.player_turn = True
            self.gameui.mark = "x"
        self.gameui.match_running = True
        self.gameui.start_ai()
        self.curr_view = self.gameui

    def to_menu(self):
        # Vrácení zpět do menu
        self.gameui.reset()
        self.curr_view = self.menu

    def check_events(self):
        # Kontroluje zda uživatel neprovedl nějaku akci
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._quit()
            
            self.curr_view.check_events(event)

    def update(self, dt):
        # Aktualizace nynějšího view(vzhledu)
        self.curr_view.update(dt)

    def draw(self):
        # Kreslení nynějšího view(vzhledu) na plochu
        view_surface = self.curr_view.render()
        self.screen.blit(view_surface, (0, 0))
        pg.display.flip()