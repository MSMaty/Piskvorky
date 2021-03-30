import pygame as pg

from game.settings import *

class Label:
    DEFAULTS = {
        "text": "",
        "color": "black",
        "font_family": "Calibri",
        "font_size": 20,
        "external": False,
        "dynamic": False,
        "left_aligned": False
    }
    def __init__(self, center, **kwargs):

        self.center = center
        self.text = kwargs.get("text", self.DEFAULTS["text"])
        self.color = kwargs.get("color", self.DEFAULTS["color"])
        font_family = kwargs.get("font_family", self.DEFAULTS["font_family"])
        font_size = kwargs.get("font_size", self.DEFAULTS["font_size"])
        external = kwargs.get("external", self.DEFAULTS["external"])
        self.dynamic = kwargs.get("dynamic", self.DEFAULTS["dynamic"])
        self.left_aligned = kwargs.get("left_aligned", self.DEFAULTS["left_aligned"])

        # Zvolení typu textu
        font_type = pg.font.Font if external else pg.font.SysFont
        self.font = font_type(font_family, font_size)

        self.render()

    def update_text(self, text):
        # Aktualizuje vzhled textu
        self.text = text

    def update(self):
        if self.dynamic:
            self.render()

    def render(self):
        self.surface = self.font.render(self.text, True, self.color)
        if self.left_aligned:
            center = self.center[0] + self.surface.get_size()[0] // 2, self.center[1]
        else:
            center = self.center
        self.rect = self.surface.get_rect(center=center)
    
    def draw(self, view):
        view.blit(self.surface, self.rect)

class Button(Label):
    BTN_DEFAULTS = {
        "visible": True,
        "hover_color": (100, 100, 100),
        "hover_callback": lambda: None,
        "click_callback": lambda: print("click")
    }
    def __init__(self, center, size, **kwargs):
        self.width, self.height = size
        self.x = center[0] - self.width // 2
        self.y = center[1] - self.height // 2
        super().__init__(center, **kwargs)
        self.base_color = self.color

        self.visible = kwargs.get("visible", self.BTN_DEFAULTS["visible"])
        self.hover_color = kwargs.get(
            "hover_callback", self.BTN_DEFAULTS["hover_color"])
        self.hover_callback = kwargs.get(
            "hover_callback", self.BTN_DEFAULTS["hover_callback"])
        self.click_callback = kwargs.get(
            "click_callback", self.BTN_DEFAULTS["click_callback"])

        self.dynamic = True if self.visible else False

        self.hovered = False
        self.down = False
        self.clicked = False
        self.released = False
    
    def check_input(self, mousepos, mouseclick):
        # Kontroluje zda je nad tlačítkem myš, nebo zda není stisknuto
        self.is_hovered(mousepos)
        self.is_pressed(mouseclick)

    def is_hovered(self, mousepos):
        # Vrátí true pokud je nad tlačítkem myš
        self.hovered = False
        mousex, mousey = mousepos[0], mousepos[1]
        xcollide = self.x < mousex < self.x + self.width
        ycollide = self.y < mousey < self.y + self.height
        if xcollide and ycollide:
            self.hovered = True

    def is_pressed(self, mouseclick):
        # Vrátí true, pokud bylo tlačítko ztisknuto
        self.released = False
        if mouseclick:
            self.clicked = True
        else:
            if self.clicked:
                self.released = True
                self.clicked = False            

        if self.hovered and self.released:
            self.click_callback()

    def update(self, view):
        # Aktualizuje vzhled tlačítek a jejich barvu
        self.color = self.base_color
        if self.down:
            self.color = self.hover_color
        if self.hovered:
            self.color = self.hover_color
            self.hover_callback()
            view.pointing_cursor = True
        if self.dynamic:
            self.render()

class View:
    # Class reprezentující vzhled
    def __init__(self, render_resolution):
        # Spustí surface, vzhled a tlačítka
        self.surface = pg.Surface(render_resolution)
        self.labels = []
        self.buttons = []
        self.pointing_cursor = False

    def check_events(self, event):
        pass

    def update_labels(self):
        for label in self.labels:
            label.update()

    def update_buttons(self):
        # Aktualizuje vzhled tlačítek, akontroluej jejich zmáčknutí

        # Kontroluje imput myši
        mousepos, mouseclick = pg.mouse.get_pos(), pg.mouse.get_pressed()[0]
        for btn in self.buttons:
            btn.check_input(mousepos, mouseclick)
        self.pointing_cursor = False
        for button in self.buttons:
            button.update(self)

    def update(self, dt):
        # Aktualizuje view(vzhled)
        self.update_labels()
        self.update_buttons()
        self._loop(dt)

    def _loop(self, dt):
        pass

    def _draw(self):
        self.surface.fill(BASE_BG_COLOR)

    def draw_labels(self):
        for label in self.labels:
            label.draw(self.surface)

    def draw_buttons(self):
        for button in self.buttons:
            button.draw(self.surface)

    def render(self):
        self._draw()
        self.draw_labels()
        self.draw_buttons()
        return self.surface