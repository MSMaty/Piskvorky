import pygame as pg

# Nastavení které umožnujě lehký přístup k věcím jako jsou například barvy

pg.font.init()

RESOLUTION = 800, 800
FPS = 30
CAPTION = "Piškvorky XOX"

BASE_BG_COLOR = (240, 240, 240)
BASE_FONT_COLOR = (10, 10, 10)
HOVER_FONT_COLOR = (50, 50, 50)
FONT = "fonts/Comfortaa-Regular.ttf"
FONT_BOLD = "fonts/Comfortaa-Bold.ttf"

class MenuSettings:
    TITLE_CENTER = RESOLUTION[0] // 2, RESOLUTION[1] // 2
    TITLE_KWARGS = {
        "text": "PIŠKVORKY",
        "color": BASE_FONT_COLOR,
        "font_family": FONT_BOLD,
        "font_size": 50,
        "external": True
    }
    SUBTITLE_CENTER = RESOLUTION[0] // 2, RESOLUTION[1] // 2 + 50
    SUBTITLE_KWARGS = {
        "text": "play against the AI",
        "color": BASE_FONT_COLOR,
        "font_family": FONT,
        "font_size": 25,
        "external": True
    }

    PLAY1_CENTER = RESOLUTION[0] // 2 - 150, RESOLUTION[1] // 2 + 150
    PLAY1_SIZE = (200, 50)
    PLAY1_KWARGS = {
        "text": "You start",
        "color": BASE_FONT_COLOR,
        "font_family": FONT,
        "font_size": 35,
        "external": True,
        "hover_color": HOVER_FONT_COLOR
    }

    PLAY2_CENTER = RESOLUTION[0] // 2 + 150, RESOLUTION[1] // 2 + 150
    PLAY2_SIZE = (200, 50)
    PLAY2_KWARGS = {
        "text": "AI starts",
        "color": BASE_FONT_COLOR,
        "font_family": FONT,
        "font_size": 35,
        "external": True,
        "hover_color": HOVER_FONT_COLOR
    }

    EASY_CENTER = RESOLUTION[0] // 2 - 150, RESOLUTION[1] // 2 + 220
    EASY_SIZE = (200, 50)
    EASY_KWARGS = {
        "text": "Easy",
        "color": BASE_FONT_COLOR,
        "font_family": FONT,
        "font_size": 25,
        "external": True,
        "hover_color": HOVER_FONT_COLOR
    }

    MEDIUM_CENTER = RESOLUTION[0] // 2, RESOLUTION[1] // 2 + 220
    MEDIUM_SIZE = (200, 50)
    MEDIUM_KWARGS = {
        "text": "Medium",
        "color": BASE_FONT_COLOR,
        "font_family": FONT,
        "font_size": 25,
        "external": True,
        "hover_color": HOVER_FONT_COLOR
    }

    HARD_CENTER = RESOLUTION[0] // 2 + 150, RESOLUTION[1] // 2 + 220
    HARD_SIZE = (200, 50)
    HARD_KWARGS = {
        "text": "Hard",
        "color": BASE_FONT_COLOR,
        "font_family": FONT,
        "font_size": 25,
        "external": True,
        "hover_color": HOVER_FONT_COLOR
    }

    QUIT_CENTER = RESOLUTION[0] // 2, RESOLUTION[1] // 2 + 280
    QUIT_SIZE = (80, 30)
    QUIT_KWARGS = {
        "text": "Quit",
        "color": BASE_FONT_COLOR,
        "font_family": FONT,
        "font_size": 25,
        "external": True,
        "hover_color": HOVER_FONT_COLOR,
    }

class GameUiSettings:
    TURN_CENTER = RESOLUTION[0] // 2, 50
    TURN_KWARGS = {
        "text": "",
        "color": BASE_FONT_COLOR,
        "font_family": FONT,
        "font_size": 25,
        "dynamic": True,
        "external": True
    }

    TURN_TEXT = ["The AI is thinking..", "Your turn"]

    ROWS = 15
    COLS = 15

    GRID_THICKNESS = 3, 1
    GRID_COLOR = [(10, 10, 10), (50, 50, 50)]
    GRID_SIZE = 600
    GRID_CELLSIZEX = GRID_SIZE // COLS
    GRID_CELLSIZEY = GRID_SIZE // ROWS

    GRID = (
        RESOLUTION[0] // 2 - GRID_SIZE // 2,
        RESOLUTION[1] // 2 - GRID_SIZE // 2,
        GRID_SIZE, GRID_SIZE
    )

    MARK_COLOR = [(30, 30, 30), (150, 150, 150)]
    MARK_FONT = pg.font.Font(FONT_BOLD, 35)
    CIRCLE_RADIUS = GRID_CELLSIZEX // 3, GRID_CELLSIZEX // 4