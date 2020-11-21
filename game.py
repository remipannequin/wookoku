#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The main game logic for the woodoku game.

Game description:

the board is 9x9, with 9 3x3 zones.

At each turn new pieces appears, that the player must place on the board. Of
course a piece can be placed only in free spaces.

When a 3x3 zone, a vertical or horizontal line is completely occupied, it 
disapears.

The game ends when a piece cannot be placed on the board.

"""

from random import Random
from board import Board, Piece

PIECES = [
    [(0,0)],
    [(0,0), (0,1)],
    [(0,0), (1,0)],
    [(0,0), (1,1)],
    [(0,1), (1,0)],
    [(0,0), (0,1), (0,2)],
    [(0,0), (1,0), (2,0)],
    [(0,0), (0,1), (1,0)],
    [(0,0), (0,1), (1,1)],
    [(0,0), (1,0), (1,1)],
    [(1,0), (0,1), (1,1)],
    [(0,0), (1,1), (2,2)],
    [(0,2), (1,1), (2,0)],
    [(0,0), (1,0), (0,1), (1,1)],
    [(0,0), (1,0), (1,1), (1,2)],
    [(0,0), (1,0), (2,0), (0,1)],
    [(0,0), (0,1), (1,1), (2,1)],
    [(0,0), (1,0), (0,1), (0,2)],
    [(0,0), (0,1), (1,1), (1,2)],
    [(0,1), (0,2), (1,0), (1,1)],
    [(0,0), (1,0), (1,1), (2,1)],
    [(0,1), (1,1), (1,0), (2,0)],
    [(0,0), (0,1), (0,2), (1,1)],
    [(1,0), (1,1), (1,2), (0,1)],
    [(0,0), (1,0), (2,0), (1,1)],
    [(0,1), (1,1), (2,1), (1,0)],
    ]


class PiecesGenerator:
    def __init__(self, seed=None):
        """create a new pieces generator
        """
        self.rng = Random(seed)
    
    def next(self):
        """return the next piece
        """
        return Piece(self.rng.choice(PIECES))
        
        
class Game:
    def __init__(self, seed=None):
        """Create a new game instance
        """
        self.board = Board()
        self.gen = PiecesGenerator(seed)
        self.next = self.gen.next()
        self.score = 0
        self.n_rows = 9
        self.n_cols = 9
        
    def play(self, i, j):
        """place next piece at location i, j on the board
        :return: the list of cells that disapeared (if any)
        """
        if i not in range(9) or j not in range(9):
             return set()
        if not self.board.place(self.next, i, j):
            return set()
        (s, removed) = self.board.reduce()
        self.next = self.gen.next()
        self.score += s
        return {(e // 9, e % 9) for e in removed}
    
    def fit(self, i, j):
        """Test whether next piece fit at i, j
        """
        return self.board.fit(self.next, i, j)
    
    def over(self):
        """Return true if next piece cannot be placed
        """
        for i in range (9):
            for j in range(9):
                if self.board.fit(self.next, i, j):
                    return False
        return True
    
    def displayPossiblePieces():
        """Display all possible pieces, mainly for testing purpose
        >>> Game.displayPossiblePieces()
        """
        for c in PIECES:
            print(Piece(c))
            print('--------------')
        
        
if __name__ == '__main__':
    g = Game()
    while not g.over():
        print(g.board)
        print('score: %d' %g.score)
        print('Next piece:')
        print(g.next)
        loc = input('location ? ')
        i, j = [int(e)-1 for e in loc.split(',')]
        if g.fit(i, j):
            g.play(i, j)
        else:
            print('piece does not fit there')
