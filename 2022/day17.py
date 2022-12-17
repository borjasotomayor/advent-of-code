"""
Day 17
https://adventofcode.com/2022/day/17

1st star: 01:19:51
2nd star: 02:53:04

Part 1 of this problem turned out to be a fun exercise in
object-oriented design (as well as ensuring that every
small detail was right). Keeping the code well organized
(and testing each method as I went along) meant that,
when all the pieces (ha!) came together, I got the right
answer for Part 1 with minimal debugging.

As for Part 2... clearly I couldn't simulate a bajillion
pieces, so I tried to see whether there was any patterns
I could exploit. Eventually, I tried printing the height 
of the rocks every time I made a full pass through all 
the movements (before you cycle back to the start), and 
it turned out the rocks actually grow by the same amount 
each cycle. I ended up using that information to manually
compute the answer, but I'll eventually get around
to adding code that finds out that value automatically.
"""

import util
import math
import sys
import re

from util import log


class Tetris:
    """
    Class for keeping track of a Tetris game
    """

    PIECE1 = [["#", "#", "#", "#"]]

    PIECE2 = [[".", "#", "."],
              ["#", "#", "#"],
              [".", "#", "."]]

    PIECE3 = [[".", ".", "#"],
              [".", ".", "#"],
              ["#", "#", "#"]]

    PIECE4 = [["#"],
              ["#"],
              ["#"],
              ["#"]]

    PIECE5 = [["#", "#"],
              ["#", "#"]]

    PIECES=[PIECE1, PIECE2, PIECE3, PIECE4, PIECE5]


    def __init__(self, width, height):
        """
        Constructor
        """
        # Create an empty Grid to represent the game
        # Note: in my Grid class, the upper-left corner
        # is position (0,0).
        self.grid = util.Grid.empty(width, height+1, ".")
        self.height = height
        self.width = width

        # The tallest rock (initially the ground)
        self.tallest_y = height+1

        # Index into the PIECES array
        self.piece_i = 0

        # The current piece (the piece that is currently
        # falling)
        self.cur_piece = None

    def new_piece(self):
        """
        Start dropping a new piece.
        """
        assert self.cur_piece is None

        # Compute initial coordinates
        piece_y = self.tallest_y - 3 - len(Tetris.PIECES[self.piece_i])
        piece_x = 2

        # Create the Piece object
        p = Piece(self, Tetris.PIECES[self.piece_i], piece_x, piece_y)
        self.cur_piece = p
        self.piece_i = (self.piece_i + 1) % len(Tetris.PIECES)

        # Draw it into the grid
        p.draw()

    def move_piece(self, move):
        """
        Moves a piece left ("<"), right (">"), or down ("v")
        """
        x = self.cur_piece.x
        y = self.cur_piece.y

        # Compute the updated coordinates, but don't
        # change the piece yet
        if move == "<":
            x -= 1
        elif move == ">":
            x += 1
        elif move == "v":
            y += 1

        # Let's make sure this move is valid
        if not self.cur_piece.validate(x, y):
            return False
        else:
            # If it is, "undraw" the piece from its current
            # location, and draw it in the new location.
            self.cur_piece.undraw()
            self.cur_piece.x = x
            self.cur_piece.y = y
            self.cur_piece.draw()
            return True

    def stop_piece(self):
        """
        Update the state of the game to reflect that the current
        piece has come to a stop.
        """
        self.cur_piece.stopped = True
        self.cur_piece.draw()
        self.tallest_y = min(self.cur_piece.y, self.tallest_y)
        self.cur_piece = None

    def play_game(self, n_pieces, moves):
        """
        Play one game of Tetris
        """
        moves_i = 0

        for _ in range(n_pieces):
            # Drop a new piece
            self.new_piece()

            # Keep moving it until it stops
            while True:
                # Move the piece left/right according
                # to the provided movements
                next_move = moves[moves_i]
                moves_i = (moves_i + 1) % len(moves)
                self.move_piece(next_move)

                # Move the piece down. If it doesn't move,
                # we're done with this piece
                moved = self.move_piece("v")
                if not moved:
                    self.stop_piece()
                    break


    def render(self, n=8):
        """
        Print the bottom n rows of the game
        """
        rows = ["".join(str(x) for x in row) for row in self.grid._grid[self.grid.max_y-n:]]
        print("\n".join(rows))
        print("-" * self.width)
        print()


class Piece:
    """
    Class for keeping track an individual piece.
    """

    def __init__(self, tetris, pattern, x, y):
        self.tetris = tetris
        
        # The pattern attribute is effectively a pointed into
        # a specific pattern in the Tetris.PIECES list.
        self.pattern = pattern
        
        # The x and y coordinates refer to the top-left corner
        # of the piece.
        self.x = x
        self.y = y
        self.width = len(self.pattern[0])
        self.height = len(self.pattern)
        self.stopped = False

    def draw(self):
        """
        Draw the piece on the game grid
        """
        y = self.y
        for row in self.pattern:
            x = self.x
            for c in row:
                if c == "#":
                    if self.stopped:
                        self.tetris.grid.set(x, y, "#")
                    else:
                        self.tetris.grid.set(x, y, "@")
                x += 1
            y += 1

    def undraw(self):
        """
        Remove the piece from the game grid
        """
        y = self.y
        for row in self.pattern:
            x = self.x
            for c in row:
                if c == "#":
                    self.tetris.grid.set(x, y, ".")
                x += 1
            y += 1            

    def validate(self, x, y):
        """
        Validate that the piece can be moved
        """
        # Make sure the left edge of the piece
        # is inside the game grid
        if x < 0 or x > self.tetris.width:
            return False

        # Make sure the right edge of the piece
        # is inside the game grid
        if x + self.width > self.tetris.width:
            return False

        # Make sure the bottom of the piece is
        # inside the game grid
        if y + self.height > self.tetris.height+1:
            return False

        # Do some rudimentary collision detection
        # to check whether we would overlap with other
        # pieces.
        iy = y
        for row in self.pattern:
            ix = x
            for c in row:
                if c == "#" and self.tetris.grid.get(ix, iy) == "#":
                    return False
                ix += 1
            iy += 1

        return True        
        

def task1(n_pieces, moves):
    # Maximum possible height (all vertical pieces stacked
    # on top of each other)
    height = (n_pieces * 4) + 1

    # Create the game and play it
    tetris = Tetris(7, height)
    tetris.play_game(2022, moves)

    return height - tetris.tallest_y + 1


if __name__ == "__main__":
    util.set_debug(False)

    sample = list(util.read_strs("input/sample/17.in", sep="\n")[0])
    input = list(util.read_strs("input/17.in", sep="\n")[0])

    print("TASK 1")
    util.call_and_print(task1, 2022, sample)
    util.call_and_print(task1, 2022, input)
