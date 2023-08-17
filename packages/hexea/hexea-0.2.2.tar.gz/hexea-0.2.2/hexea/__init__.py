from typing import Dict, List, Self, Protocol, Tuple, runtime_checkable
from hexea._board import (
    Board as Yboard,
    Marker,
)
from copy import deepcopy

def _marker_to_string(marker):
    if marker == Marker.red:
        return 'X'
    elif marker == Marker.blue:
        return 'O'
    else:
        return '.'

setattr(Marker, '__str__', _marker_to_string)

@runtime_checkable
class Board(Protocol):
    def __str__(self) -> str:
        ...

    def __copy__(self) -> Self:
        ...

    def get_next_player(self) -> Marker:
        ...

    def move(self, col : int, row : int) -> Self:
        ...

    def get_free_hexes(self) -> List[Tuple[int,int]]:
        ...

    def random_playout(self) -> Self:
        ...

    def get_dict(self) -> Dict[str, Marker]:
        ...

    def random_playouts_won(self, num_playouts : int) -> Dict[Marker, int]:
        ...

    def get_winner(self) -> Marker:
        ...


class Hexboard:
    def __init__(self, size):
        self.size = size
        self.yboard = Yboard(size * 2)
        for col in range(size):
            height = size - col
            for row in range(height):
                (
                    self.yboard
                    .move(col, row)
                    .move(col, (2 * size - col) - row - 1)
                )

    def _hex_to_y(self, col : int, row : int) -> Tuple[int, int]:
        return (
            col + row + 1,
            self.size - col - 1
        )

    def _y_to_hex(self, col : int, row : int) -> Tuple[int, int]:
        return (
            self.size - row - 1,
            (col - self.size) + row
        )

    def __getitem__(self, tup: Tuple[int,int]):
        x, y = tup
        return self.yboard[self._hex_to_y(x, y)]

    def __str__(self) -> str:
        board_width = (self.size * 4) - 1
        footer = ("x" * board_width)
        header = " " + footer + "\n"
        separator = "\no" + (" " * board_width) + "o\n"
        # first create rectangular result
        result = header + separator.join(
            [
                "o "
                + "   ".join([str(self[col, row]) for col in range(self.size)])
                + " o"
                for row in range(self.size)
            ]
        ) + "\n" + footer
        # now skew the result
        result = "\n" + "\n".join([
            (" " * (i-1)) + row
            for i, row in enumerate(result.split("\n"))
        ]) + "\n"
        return result


    def __copy__(self) -> Self:
        b = Hexboard(self.size)
        b.yboard.board = deepcopy(self.yboard.board)
        return b

    def get_next_player(self) -> Marker:
        return self.yboard.get_next_player()

    def move(self, col: int, row: int) -> Self:
        ycol, yrow = self._hex_to_y(col, row)
        self.yboard.move(ycol, yrow)
        return self

    def get_free_hexes(self):
        free_y_hexes = self.yboard.get_free_hexes()
        return [self._y_to_hex(*x) for x in free_y_hexes]

    def get_winner(self) -> Marker:
        return self.yboard.get_winner()

    def random_playout(self) -> Self:
        self.yboard.random_playout()
        return self

    def random_playouts_won(self, num_playouts : int) -> Dict[Marker, int]:
        return self.yboard.random_playouts_won(num_playouts)

    def get_dict(self) -> Dict[str, Marker]:
        hexes = [self._hex_to_y(x,y) for x in range(self.size) for y in range(self.size)]
        hex_dict = {hex:self.yboard.board[hex[0]][hex[1]] for hex in hexes}
        return {"cell{},{}".format(hex[0], hex[1]):hex_dict[hex] for hex in hex_dict}

    def __eq__(self, other) -> bool:
        return self.yboard == other.yboard
