from enum import Enum as _Enum


class ColorType(_Enum):
    NoColor = 0
    Color8 = 1
    Color16 = 2
    Color256 = 3


class Color:
    reset = '\x1b[0m'

    def __init__(self, code: str, color_type: 'ColorType', fallback: 'Color' = None):
        self._text = f'\x1b[3{code}m'
        self._background = f'\x1b[4{code}m'

        self._type = color_type
        self._fallback = fallback

    @property
    def text(self):
        return self._text

    @property
    def back(self):
        return self._background

    @property
    def background(self):
        return self._background

    @property
    def type(self):
        return self._type

    @property
    def fallback(self):
        return self._fallback


# Color 8
BLACK   = Color('0', ColorType.Color8)
RED     = Color('1', ColorType.Color8)
GREEN   = Color('2', ColorType.Color8)
YELLOW  = Color('3', ColorType.Color8)
BLUE    = Color('4', ColorType.Color8)
MAGENTA = Color('5', ColorType.Color8)
CYAN    = Color('6', ColorType.Color8)
WHITE   = Color('7', ColorType.Color8)

# Color 16
BRIGHT_BLACK   = Color('0;1', ColorType.Color16, BLACK)
BRIGHT_RED     = Color('2;1', ColorType.Color16, RED)
BRIGHT_GREEN   = Color('3;1', ColorType.Color16, GREEN)
BRIGHT_YELLOW  = Color('4;1', ColorType.Color16, YELLOW)
BRIGHT_BLUE    = Color('5;1', ColorType.Color16, BLUE)
BRIGHT_MAGENTA = Color('6;1', ColorType.Color16, MAGENTA)
BRIGHT_CYAN    = Color('7;1', ColorType.Color16, CYAN)
BRIGHT_WHITE   = Color('8;1', ColorType.Color16, WHITE)

# Color 256
COLOR_256 = {
    i: Color(f'8;5;{i}', ColorType.Color256, None) for i in range(256)
}
