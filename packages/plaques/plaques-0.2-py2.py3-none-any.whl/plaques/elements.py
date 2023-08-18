"""More advanced UI elements."""

from enum import Enum
from .base import CharCell, Plaque
from .base import Color, Pivot
globals().update(Color.__members__)
globals().update(Pivot.__members__)


class Text(Plaque):
    """Caption box element."""

    DEFAULTS = Plaque.DEFAULTS | {
        "text": "",
        "align": CENTER_CENTER,
    }
    
    def _get_char_table(self, h_size: int, v_size: int
        ) -> list[list[CharCell]]:
        """Get a canvas of right size and render the words."""
        _canvas = [
            [self.fill.copy() for _i in range(h_size)]
            for _j in range(v_size)
            ]
        # TEST
        if self.text:
            _canvas[0][0].char = self.text[0]
        else:
            print(self.text)
            _canvas[0][0].char = "{"
        _canvas[0][-1].char = "}"
        return _canvas


class Frame(Enum):
    """Possible border styles for Window."""

    NO_FRAME = {
           TOP_LEFT: " ",    TOP_CENTER: " ",    TOP_RIGHT: " ",
        CENTER_LEFT: " ",                     CENTER_RIGHT: " ",
        BOTTOM_LEFT: " ", BOTTOM_CENTER: " ", BOTTOM_RIGHT: " ",
        }
    THIN = {
           TOP_LEFT: "┌",    TOP_CENTER: "─",    TOP_RIGHT: "┐",
        CENTER_LEFT: "│",                     CENTER_RIGHT: "│",
        BOTTOM_LEFT: "└", BOTTOM_CENTER: "─", BOTTOM_RIGHT: "┘",
        }
    THICK = {
           TOP_LEFT: "┏",    TOP_CENTER: "━",    TOP_RIGHT: "┓",
        CENTER_LEFT: "┃",                     CENTER_RIGHT: "┃",
        BOTTOM_LEFT: "┗", BOTTOM_CENTER: "━", BOTTOM_RIGHT: "┛",
        }
    DOUBLE = {
           TOP_LEFT: "╔",    TOP_CENTER: "═",    TOP_RIGHT: "╗",
        CENTER_LEFT: "║",                     CENTER_RIGHT: "║",
        BOTTOM_LEFT: "╚", BOTTOM_CENTER: "═", BOTTOM_RIGHT: "╝",
        }
    SMOOTH = {
           TOP_LEFT: "╭",    TOP_CENTER: "─",    TOP_RIGHT: "╮",
        CENTER_LEFT: "│",                     CENTER_RIGHT: "│",
        BOTTOM_LEFT: "╰", BOTTOM_CENTER: "─", BOTTOM_RIGHT: "╯",
        }
    OUTER_HALF = {
           TOP_LEFT: "▛",    TOP_CENTER: "▀",    TOP_RIGHT: "▜",
        CENTER_LEFT: "▌",                     CENTER_RIGHT: "▐",
        BOTTOM_LEFT: "▙", BOTTOM_CENTER: "▄", BOTTOM_RIGHT: "▟",
        }
    INNER_HALF = {
           TOP_LEFT: "▗",    TOP_CENTER: "▄",    TOP_RIGHT: "▖",
        CENTER_LEFT: "▐",                     CENTER_RIGHT: "▌",
        BOTTOM_LEFT: "▝", BOTTOM_CENTER: "▀", BOTTOM_RIGHT: "▘",
        }
    ASCII = {
           TOP_LEFT: "+",    TOP_CENTER: "-",    TOP_RIGHT: "+",
        CENTER_LEFT: "|",                     CENTER_RIGHT: "|",
        BOTTOM_LEFT: "+", BOTTOM_CENTER: "-", BOTTOM_RIGHT: "+",
        }
    SLC_OUTER = { # Unicode 13+ required!
           TOP_LEFT: "🭽",    TOP_CENTER: "▔",    TOP_RIGHT: "🭾",
        CENTER_LEFT: "▏",                     CENTER_RIGHT: "▕",
        BOTTOM_LEFT: "🭼", BOTTOM_CENTER: "▁", BOTTOM_RIGHT: "🭿",
        }

globals().update(Frame.__members__)


class Window(Plaque):
    """Groups other UI elements in a frame."""

    DEFAULTS = Plaque.DEFAULTS | {
        "title": Text(
            pivot = TOP_LEFT,
            h_abs_pos = 1,
            v_abs_size = 1,
            h_rel_size = 1.0,
            h_abs_size = -2,
            fill = CharCell(color = TRANSPARENT, bgcol = TRANSPARENT),
            ),
        "status": Text(
            pivot = BOTTOM_LEFT,
            h_abs_pos = 1,
            v_rel_pos = 1.0,
            v_abs_pos = 0,
            v_abs_size = 1,
            h_rel_size = 1.0,
            h_abs_size = -2,
            fill = CharCell(color = TRANSPARENT, bgcol = TRANSPARENT),
            ),
        "frame": Frame.THIN,
    }

    BORDER = {
        "top": 1,
        "right": 1,
        "bottom": 1,
        "left": 1,
    }

    DEFAULT_ELEMENTS = ["title", "status"]

    def _get_char_table(self, h_size: int, v_size: int
        ) -> list[list[CharCell]]:
        """Get a canvas of right size with frame."""
        _canvas = [
            [self.fill.copy() for _i in range(h_size)]
            for _j in range(v_size)
            ]
        _canvas[0][0].char = self.frame.value[TOP_LEFT]
        for _i in range(h_size - 2):
            _canvas[0][_i + 1].char = self.frame.value[TOP_CENTER]
        _canvas[0][-1].char = self.frame.value[TOP_RIGHT]
        for _i in range(v_size - 2):
            _canvas[_i + 1][-1].char = self.frame.value[CENTER_RIGHT]
        _canvas[-1][-1].char = self.frame.value[BOTTOM_RIGHT]
        for _i in range(h_size - 2):
            _canvas[-1][_i + 1].char = self.frame.value[BOTTOM_CENTER]
        _canvas[-1][0].char = self.frame.value[BOTTOM_LEFT]
        for _i in range(v_size - 2):
            _canvas[_i + 1][0].char = self.frame.value[CENTER_LEFT]
        return _canvas