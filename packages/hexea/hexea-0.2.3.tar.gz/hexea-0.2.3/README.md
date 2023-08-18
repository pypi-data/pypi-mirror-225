# Hexea

This is a simple library for working with the closely related connection games of Y and Hex.  This is not meant to be a standalone, playable game, but rather a set of tools one could use to implement such a game, train a machine learning model to play a game, and so forth.

## Basic Usage

All of the functionality currently available in the `hexea` module is in the `Yboard` and `Hexboard` classes, which both implement the `Board` protocol.  `Yboard` is implemented as a C++ extension using [`pybind11`](https://pybind11.readthedocs.io/en/stable/).  `Hexboard` is a Python wrapper that uses a `Yboard` under the hood, since [Hex is a special case of Y](https://www.cs.cornell.edu/~adith/docs/y_hex.pdf), and a Y board can be converted into a Hex board by selectively filling in hexes.

The `hexea` module also provides a `Marker` class, which is an enumeration class for representing the type of game marker inhabiting a hex:  `Marker.red`, `Marker.blue`, or `Marker.none`.  The `__str__` method of `Marker`  has been overridden to return a character representing the marker:  `X`, `O`, or `.`, respectively.

The following methods are available for both `Yboard` and `Hexboard`:

#### `get_next_player()`

Returns a `Marker` indicating which player is up next:  `Marker.red` for an empty board, and then alternating between `Marker.blue` and `Marker.red` as moves are played.  Note that this does not change even after a player has won; it is possible to keep placing moves as long as there are empty hexes, and even when the board is filled up, `get_next_player()` will return either `Marker.red` or `Marker.blue`.  If this behavior turns out to be undesirable in practice, code may be added in a future version to return `Marker.none` whenever the board represents a winning position for either player.

#### `move(col: int, row:int)`

Places a `Marker` representing the next player at the specified column and row.  Throws `IndexError` if the specified column and row do not exist, and `ValueError` if the specified location is already occupied.

`move()` returns `self` in order to allow daisy chaining like so:

``` python
b = (
    Hexboard(3)
    .move(0, 1)
    .move(1, 0)
    .move(1, 1)
`)

```

#### get_free_hexes()

Returns a list of 2-tuples, each of which contains the column and row of a hex that is not currently occupied.

#### get_winner()

Returns a `Marker` representing the current winning player, or `Marker.none` if the board is not yet in a winning state.

#### random_playout()

Performs a single random playout.  Starting with the current board state, markers for each player are alternately placed on a random hex until no empty hexes are left.  Does not stop when a winning position has been reached.  This is in the interest of speed:  Random playouts are typically done hundreds or thousands at a time, and checking for a winner after each turn would be slower than just filling up the board.

#### random_playouts_won(num_playouts: int)

Starting with the current board position, runs `num_playouts` random playouts.  Returns a dictionary whose keys are `Marker.red` and `Marker.blue`, and whose values are the number of wins each player has.

Since neither Hex nor Y can end in a draw, there is never a key for `Marker.none`.

#### get_dict()

Gets a dictionary whose keys are all strings representing a cell on the board (e.g. `cell0,0`) and whose values are `Marker` objects indicating the occupant of the cell.

This is admittedly an esoteric method.  I once used something similar when building a Y-playing AI using genetic programming:  Each gene represented a function that performed mathematical operations on the values of cells, and was evaluated using string subtitution (replacing `cell0,0` with the integer value of that cell).  There are undoubtedly better ways to do this, so expect this method to change or be deprecated soon.
