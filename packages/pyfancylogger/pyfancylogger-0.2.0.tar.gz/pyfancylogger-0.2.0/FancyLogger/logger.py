from logging import Logger, Formatter, StreamHandler
from string import Template
from types import MappingProxyType
from typing import Optional, Literal, Union, Iterable, Callable

from .colors import *


def _format(string: str, values: Union[list, tuple, dict], style: Literal['%', '{', '$']):
    if style == '%':
        return string % values

    if style == '{':
        if isinstance(values, (list, tuple)):
            return string.format(*values)
        if isinstance(values, dict):
            return string.format(**values)

    if style == '$':
        if isinstance(values, dict):
            return Template(string).substitute(values)

    return string


class FancyStyle:
    @staticmethod
    def get(level):
        if isinstance(level, list) or isinstance(level, tuple):
            return FancyStyle(*level)

        return level if isinstance(level, FancyStyle) else FancyStyle(level) if isinstance(level, Color) else None

    def __init__(self, color: 'Color', background: 'Color' = None, underline: bool = False, bold: bool = False):
        self.color = color.text if isinstance(color, Color) else ''
        self.background = background.background if isinstance(background, Color) else ''
        self.others = ('\x1b[1m' if bold else '') + ('\x1b[4m' if underline else '')
        self.reset = Color.reset if self.color or self.background or self.others else ''

    def format(self, message):
        return self.color + self.background + self.others + message + Color.reset


class FancyFormatter(Formatter):
    DEBUG: Union[Color, FancyStyle, Iterable] = BRIGHT_WHITE
    INFO: Union[Color, FancyStyle, Iterable] = BRIGHT_WHITE
    WARNING: Union[Color, FancyStyle, Iterable] = YELLOW
    ERROR: Union[Color, FancyStyle, Iterable] = RED
    CRITICAL: Union[Color, FancyStyle, Iterable] = BRIGHT_WHITE, RED, True, True

    def __init__(self, fmt: Optional[str] = None, subname_fmt: Optional[str] = None, datefmt: Optional[str] = None, style: Literal['%', '{', '$'] = '%', validate: bool = True):
        super().__init__(fmt, datefmt, style, validate)

        self.original = MappingProxyType(dict(
            fmt=fmt,
            subname_fmt=subname_fmt,
            datefmt=datefmt,
            style=style,
            validate=validate,
        ))

        self.subname_fmt = subname_fmt or ('%(parent)s - %(name)s' if style == '%' else '$parent - $name' if style == '$' else '{parent} - {name}')

        self.formats = {
            10: FancyStyle.get(self.DEBUG),
            20: FancyStyle.get(self.INFO),
            30: FancyStyle.get(self.WARNING),
            40: FancyStyle.get(self.ERROR),
            50: FancyStyle.get(self.CRITICAL),
        }

    def format(self, record):
        message = super(FancyFormatter, self).format(record)
        formatter = self.formats.get(record.levelno, None)
        return message if formatter is None else formatter.format(message)

    def copy(self):
        return FancyFormatter(**self.original)


class FancyLogger(Logger):
    def __init__(self, name: str, formatter: FancyFormatter):
        super().__init__(name)

        self.formatter = formatter
        self._subs = {}

        import sys

        self.handler = StreamHandler(sys.stdout)
        self.handler.setFormatter(formatter)
        self.addHandler(self.handler)

    def setLevel(self, level):
        super(FancyLogger, self).setLevel(level)
        self.handler.setLevel(level)

    def sub(self, name):
        if name in self._subs:
            return self._subs[name]

        sub = SubFancyLogger(self, name)
        self._subs[name] = sub
        return sub


class SubFancyLogger(FancyLogger):
    def __init__(self, parent: 'FancyLogger', name: str):
        super().__init__(
            _format(parent.formatter.subname_fmt, {'parent': parent.name, 'name': name}, parent.formatter.original['style']),
            parent.formatter.copy()
        )

        self.parent = parent
        self.propagate = False
