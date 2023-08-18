"""Basic classes for plaques."""

from enum import Enum
from wcwidth import wcswidth
from os import get_terminal_size

class Color(Enum):
    """Basic colors for CharCell."""

    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7
    TRANSPARENT = 8
    NORMAL = 9

globals().update(Color.__members__)


class CharCell:
    """Representation of a single character-cell in terminal.

    Attributes:
    char: a character to be printed;
    color, bgcol: character and background colors (Color enum);
    bold, u[nder]lined, italic: styles.
    """

    __DEFAULTS = {
        "char": None,
        "color": NORMAL,
        "bgcol": NORMAL,
        "bold": False,
        "ulined": False,
        "italic": False,
    }

    def __init__(self, **kwargs) -> None:
        """Set provided attributes or the default ones."""
        kwargs = self.__DEFAULTS | kwargs
        for _key, _value in kwargs.items():
            self.__setattr__(_key, _value)

    def __setattr__(self, name: str, value: bool | str | Color | None) -> None:
        """Validate attributes.

        Raise ValueError if character is not 1 cell-wide or None.
        """
        if name == "char":
            if value is None:
                object.__setattr__(self, name, value)
            elif wcswidth(value) == 1:
                object.__setattr__(self, name, value)
            else:
                _msg = "CharCell.char must have printable length of 1"
                raise ValueError(_msg)
        elif name in ["color", "bgcol", "bold", "ulined", "italic"]:
            object.__setattr__(self, name, value)

    def __eq__(self, other: object) -> bool:
        """Compare 2 CharCells using `==`.

        This compares how CharCells look _visually_, so if char is space, bold
        and italic attributes are not compared since they are not visible.
        """
        if not isinstance(other, CharCell):
            return NotImplemented
        if self.bgcol != other.bgcol or self.ulined != other.ulined:
            return False
        if self.char in (" ", None) and other.char in (" ", None):
            return True #chars are spaces or None, no need to check further
        if self.char != other.char or self.bold != other.bold or self.ulined \
            != other.ulined or self.color != other.color:
            return False
        return True

    def __ne__(self, other: object) -> bool:
        """Compare 2 CharCells using `!=`.

        Refer to __eq__() for details on the logic.
        """
        if not isinstance(other, CharCell):
            return NotImplemented
        return not self == other

    def __repr__(self) -> str:
        """Show attributes."""
        return (
            f"<CharCell: char:{self.char}, color:{self.color}, "
            f"bgcol:{self.bgcol}, bold:{self.bold}, underlined:{self.ulined},"
            f" italic:{self.italic}>"
        )

    def __str__(self) -> str:
        """Get printable representation (mostly for testing purposes)."""
        return (CharCell().ansi_transition(self)
            + (self.char if self.char is not None else " ")
            + "\033[0m") #SGR normal

    def copy(self) -> "CharCell":
        """Return an identical CharCell."""
        return CharCell(
            char = self.char,
            color = self.color,
            bgcol = self.bgcol,
            bold = self.bold,
            ulined = self.ulined,
            italic = self.italic,
            )

    def overlay(self, other: "CharCell") -> "CharCell":
        """Copy all the attributes of another CharCell, except colors and char.

        Colors will remain the same if they have the value of TRANSPARENT.
        Character will remain the same if it's None.
        """
        return CharCell(
            char = other.char if other.char is not None else self.char,
            color = (other.color if other.color is not TRANSPARENT
                else self.color),
            bgcol = (other.bgcol if other.bgcol is not TRANSPARENT
                else self.bgcol),
            bold = other.bold,
            ulined = other.ulined,
            italic = other.italic,
            )

    def ansi_transition(self, other: "CharCell") -> str:
        """Change style and color between 2 CharCells.

        Return a sequence of ANSI SGR escape codes necessary to transition
        from the colors and styles of CharCell `self` to the colors and
        styles of CharCell `other`. The codes are to be printed in between
        the characters form char attributes of the CharCells.

        If the CharCell colors and styles are the same, an empty string is
        returned.

        See en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters
        for details.
        """
        _escseq = "\033["
        if self.color != other.color:
            _color = (other.color if other.color != TRANSPARENT else NORMAL)
            #return to normal color if the next char's color is transparent
            _escseq = _escseq + "3" + str(_color.value) + ";"
        if self.bgcol != other.bgcol:
            _bgcol = (other.bgcol if other.bgcol != TRANSPARENT else NORMAL)
            _escseq = _escseq + "4" + str(_bgcol.value) + ";"
        if self.bold != other.bold:
            _escseq = _escseq + "1;" if other.bold else _escseq + "21;"
        if self.ulined != other.ulined:
            _escseq = _escseq + "4;" if other.ulined else _escseq + "24;"
        if self.italic != other.italic:
            _escseq = _escseq + "3;" if other.italic else _escseq + "23;"
        if _escseq == "\033[": #if no colors and styles were changed,
            return ""          #return an empty string
        return _escseq[:-1] + "m" #replace the trailing semicolon with SGR `m`


class Pivot(Enum):
    """Defines several useful points on a Plaque (clockwise).

    1---2---3
    |       |
    |       |
    8   0   4
    |       |
    |       |
    7---6---5
    """

    CENTER_CENTER = 0
    TOP_LEFT = 1
    TOP_CENTER = 2
    TOP_RIGHT = 3
    CENTER_RIGHT = 4
    BOTTOM_RIGHT = 5
    BOTTOM_CENTER = 6
    BOTTOM_LEFT = 7
    CENTER_LEFT = 8

    def h_shift(self) -> float:
        """Tell what fraction of size should top-left corner be moved."""
        if self.value in [1, 8, 7]:
            return 0
        if self.value in [2, 0, 6]:
            return 0.5
        return 1

    def v_shift(self) -> int:
        """Tell what fraction of size should top-left corner be moved."""
        if self.value in [1, 2, 3]:
            return 0
        if self.value in [8, 0, 4]:
            return 0.5
        return 1

globals().update(Pivot.__members__)


class Plaque:
    """Plaque is the central concept of the module.

    It is a rectangular area defined by absolute (`abs`) and relative (`rel`)
    sizes.
    A plaque knows where it is by keeping position (`pos`) values, that
    can be relative and absolute too.
    It also has `pivot` attribute (Pivot enum), defining its origin point
    by which it is attached to its position.
    Sizes and positions start with `h` or `v`, for Horizontal or Vertical

    Absolute `pos`s and `size`s are integers representing exact number of
    terminal cells:
    `v_abs_pos = 2` means this Plaque must be positioned 2 rows below the top
    side of the "parent", the Plaque that contains it (the exact position
    depends on the `pivot` attribute).

    Relative `pos`s and `size`s are floats representing the values comparing
    to the size of the "parent":
    `h_rel_size = 0.5` means this Plaque will have the width (Horizontal size)
    of 50% of the Plaque that contains it.

    In the real position and size calculations absolute and relative
    attributes get combined:
    `v_rel_pos = 0.3`
    `v_abs_pos = -2`
    In this case, the origin point of the Plaque will be put at 30% of the
    parent's height minus 2 rows. Fore example, if the parent Plaque is
    30 rows high:
    30 * 0.3 + (-2) = 7
    Origin point will be placed on the 7th row.

    Plaque is the base class for any other end user-facing element in the
    module.
    """

    DEFAULTS = {
        "v_abs_pos": 0,
        "h_abs_pos": 0,
        "v_rel_pos": 0.0,
        "h_rel_pos": 0.0,
        "v_abs_size": 0,
        "h_abs_size": 0,
        "v_rel_size": 0.0,
        "h_rel_size": 0.0,
        "pivot": CENTER_CENTER,
        "h_move_to_fit": True,
        "v_move_to_fit": True,
        "h_resize_to_fit": True,
        "v_resize_to_fit": True,
        "fill": None,
        "visible": True,
    }

    BORDER = {
        "top": 0,
        "right": 0,
        "bottom": 0,
        "left": 0,
    }

    DEFAULT_ELEMENTS = []

    def __init__(self, **kwargs) -> None:
        """Set provided attributes or the default ones."""
        kwargs = self.DEFAULTS | kwargs
        for _key, _value in kwargs.items():
            if isinstance(_value, Plaque):
                self.__setattr__(_key, _value.copy())
            else:
                self.__setattr__(_key, _value)
        object.__setattr__(self, "content", [])

    def __setattr__(self, name: str, value) -> None:
        """Validate attributes."""
        if name == "fill" and value is None:
            object.__setattr__(self, "fill", CharCell())
            return
        object.__setattr__(self, name, value)

    def render(self, h_avail: int, v_avail: int) -> \
        tuple[list[list[CharCell]] | None, int, int]:
        """Get a table of CharCells.

        Returns 2-dimensional list of CharCells along with horizontal and
        vertical position.
        """
        h_exact_pos, h_exact_size, trim_left, trim_right = self.__calc(
            h_avail,
            self.pivot.h_shift(),
            self.h_move_to_fit,
            self.h_resize_to_fit,
            self.h_rel_size,
            self.h_abs_size,
            self.h_rel_pos,
            self.h_abs_pos,
            )
        v_exact_pos, v_exact_size, trim_top, trim_bottom = self.__calc(
            v_avail,
            self.pivot.v_shift(),
            self.v_move_to_fit,
            self.v_resize_to_fit,
            self.v_rel_size,
            self.v_abs_size,
            self.v_rel_pos,
            self.v_abs_pos,
            )
        if (trim_left >= h_exact_size or trim_right >= h_exact_size
            or trim_top >= v_exact_size or trim_bottom >= v_exact_size
            or h_exact_size <= 0 or v_exact_size <= 0):
            return None, 0, 0 # out of bounds or zero size
        char_table = self._get_char_table(h_exact_size, v_exact_size)
        for _element_name in self.DEFAULT_ELEMENTS:
            _element = getattr(self, _element_name)
            if _element.visible:
                elem_char_table, elem_h_pos, elem_v_pos = _element.render(
                    h_exact_size, v_exact_size
                    )
                if elem_char_table is not None:
                    self.__overlay_tables(char_table, elem_char_table,
                        elem_h_pos, elem_v_pos
                        )
        for _element in self.content:
            if _element.visible:
                elem_char_table, elem_h_pos, elem_v_pos = _element.render(
                    h_exact_size - self.BORDER["left"] - self.BORDER["right"],
                    v_exact_size - self.BORDER["top"] - self.BORDER["bottom"],
                    )
                if elem_char_table is not None:
                    self.__overlay_tables(char_table, elem_char_table,
                        elem_h_pos + self.BORDER["left"],
                        elem_v_pos + self.BORDER["top"]
                        )
        char_table = [_[trim_left:len(_) - trim_right] for _ in
            char_table[trim_top:len(char_table) - trim_bottom]]
        return char_table, h_exact_pos, v_exact_pos

    def _get_char_table(self, h_size: int, v_size: int
        ) -> list[list[CharCell]]:
        """Get empty canvas of right size."""
        return [
            [self.fill.copy() for _i in range(h_size)]
            for _j in range(v_size)
            ]

    def copy(self):
        """Make a copy of this plaque (without content)."""
        _dict = {_: self.__dict__[_] for _ in self.DEFAULTS.keys()}
        return type(self)(**_dict)

    def __repr__(self) -> str:
        """Show attributes."""
        return (
            f"<Plaque: size: {self.h_rel_size * 100}%+{self.h_abs_size} x "
            f"{self.v_rel_size * 100}%+{self.v_abs_size}, fill: "
            f"{self.fill.__repr__()}>"
        )

    def __str__(self) -> str:
        """Allow printing a plaque directly to console."""
        h_avail, v_avail = get_terminal_size()
        lines, _, _ = self.render(h_avail, v_avail)
        if lines == []:
            return ""
        return "\n".join([self.__ansi_char_line(_line) for _line in lines])

    @staticmethod
    def __calc(
        avail: int,
        shift: float,
        move_to_fit: bool,
        resize_to_fit: bool,
        rel_size: float,
        abs_size: int,
        rel_pos: float,
        abs_pos: int,
        ) -> tuple[int, int, int, int]:
        """Calculate exact size and position in one dimension.

        Returns real position, size and trim values.
        """
        exact_size = rel_size * avail + abs_size
        if exact_size <= 0:
            return 0, 0, 0, 0
        exact_pos = round(rel_pos * avail + abs_pos - shift * exact_size)
        exact_size = round(exact_size)
        trim_start = trim_end = 0
        if (_ := exact_pos + exact_size - avail) > 0:
            # plaque doesnt fit on the right or at the bottom
            if move_to_fit:
                exact_pos -= _
            else:
                trim_end += _
        if (_ := -exact_pos) > 0:
            # plaque doesnt fit on the left or at the top
            if move_to_fit:
                exact_pos += _
                if (_ := exact_pos + exact_size - avail) > 0:
                    if resize_to_fit:
                        exact_size -= _
                    else:
                        trim_end += _
            else:
                trim_start += _
        if resize_to_fit:
            exact_size -= (trim_start + trim_end)
            trim_start = trim_end = 0
        return exact_pos, exact_size, trim_start, trim_end

    @staticmethod
    def __overlay_tables(
        table1: list[list[CharCell]],
        table2: list[list[CharCell]],
        h_pos: int,
        v_pos: int,
        ) -> None:
        """Overlay one CharCell table on another at specified coordinates.

        For every CharCell, its `overlay()` method is used.
        """
        h_size = len(table2[0])
        v_size = len(table2)
        for _r1, _r2 in zip(table1[v_pos:v_pos + v_size], table2):
            _r1[h_pos:h_pos + h_size] = [_c1.overlay(_c2)
                for _c1, _c2 in zip(_r1[h_pos:h_pos + h_size], _r2)
                ]

    @staticmethod
    def __ansi_char_line(chars: list[CharCell]) -> str:
        """Get a printable representation of a list of CharCells."""
        chars = [CharCell()] + chars
        return "".join(
            [chars[i].ansi_transition(chars[i+1]) + 
                (chars[i+1].char if chars[i+1].char is not None else " ")
                for i in range(len(chars) - 1)
                ]
            ) + "\033[0m" #SGR normal
