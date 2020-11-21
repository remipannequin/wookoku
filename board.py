#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The board for the woodoku game.

the board is 9x9, with 9 3x3 zones.

At each turn new pieces appears, that the player must place on the board. Of
course a piece can be placed only in free spaces.

When a 3x3 zone, a vertical or horizontal line is completely occupied, it 
disapears.

The game ends when a piece cannot be placed on the board.

"""

import sys
from random import Random, randrange
from enum import Enum


__author__="Rémi Pannequin"
__copyright__ = "Copyright 2020"
__credits__ = ["Rémi Pannequin"]
__license__ = "GPL"
__maintainer__ = "Rémi Pannequin"
__email__ = "remi.pannequin@gmail.com"
__status__ = "Development"



class Board:
    """The game board.
    
    It is represented by a list of 9*9 boolean (True meaning that the cell is
    occupied)
    """

    def __init__(self, data=None):
        if data:
            self.cells = data
        else:
            self.cells = [False]*81
    
    def __str__(self):
        """Display the board state.
        
        >>> b = Board()
        >>> for i in range(9):
        ...     v = b._set(i,i)
       
        >>> print(b)
        +-----------------+
        |X                |
        |  X              |
        |    X            |
        |      X          |
        |        X        |
        |          X      |
        |            X    |
        |              X  |
        |                X|
        +-----------------+
        """
        
        line = '+-----------------+'
        r = line+'\n'
        for l in range(9):
            r +=('|%s|\n' % ' '.join(['X' if e else ' ' for e in self.line(l)]))
        r += line
        return r
        
    def _lineIdx(i):
        """Index of the cells of a line.
        """
        return range(i*9,(i+1)*9)
        
    def line(self, i):
        """Return a list of the 9 cells in the ith line of the board
        
        >>> b = Board()
        >>> for i in range(9):
        ...     v = b._set(i,i)
        >>> b.line(0)
        [True, False, False, False, False, False, False, False, False]
        >>> b.line(5)
        [False, False, False, False, False, True, False, False, False]
        """
        return [self.cells[k] for k in Board._lineIdx(i)]
    
    def clearLine(self, i):
        """Clear a line of the board
        >>> b = Board(data=[True]*81)
        >>> b.clearLine(5)
        >>> print(b)
        +-----------------+
        |X X X X X X X X X|
        |X X X X X X X X X|
        |X X X X X X X X X|
        |X X X X X X X X X|
        |X X X X X X X X X|
        |                 |
        |X X X X X X X X X|
        |X X X X X X X X X|
        |X X X X X X X X X|
        +-----------------+
        """
        for k in Board._lineIdx(i):
            self.cells[k] = False
    
    def _zoneIdx(i):
        """Index of cells in zone i
        """
        l = (i // 3) * 3
        c = ((i % 3) - 1) * 3
        return [e+(l*9)+c for e in [0, 1, 2, 9, 10, 11, 18, 19, 20]]
    
    def zone(self, i):
        """return the 9 cells in a zone.
        Zone 0 is at top right of the board, zone 8 is at bottom left.
        """
        return [self.cells[k] for k in Board._zoneIdx(i)]
        
    def clearZone(self, i):
        """clear a zone of the board
        >>> b = Board(data=[True]*81)
        >>> b.clearZone(4)
        >>> print(b)
        +-----------------+
        |X X X X X X X X X|
        |X X X X X X X X X|
        |X X X X X X X X X|
        |      X X X X X X|
        |      X X X X X X|
        |      X X X X X X|
        |X X X X X X X X X|
        |X X X X X X X X X|
        |X X X X X X X X X|
        +-----------------+
        """
        for k in Board._zoneIdx(i):
            self.cells[k] = False
    
    def _colIdx(i):
        """return cell indexes of column i
        """
        return [j*9+i for j in range(9)] 
    
    def column(self, i):
        """Return a list of the 9 cells in the ith line of the board
        """
        return [self.cells[k] for k in Board._colIdx(i)]

    def clearColumn(self, i):
        """clear a column of the board
        >>> b = Board(data=[True]*81)
        >>> b.clearColumn(3)
        >>> print(b)
        +-----------------+
        |X X X   X X X X X|
        |X X X   X X X X X|
        |X X X   X X X X X|
        |X X X   X X X X X|
        |X X X   X X X X X|
        |X X X   X X X X X|
        |X X X   X X X X X|
        |X X X   X X X X X|
        |X X X   X X X X X|
        +-----------------+
        """
        for k in Board._colIdx(i):
            self.cells[k] = False

    def at(self, i, j):
        """return True if the cell at line i, col j is occupied
        """
        return self.cells[i * 9 + j]
    
    def _set(self, i, j):
        """set the cell at line i and column j to occupied. This should only be
        called internally.
        :return: True if cell was previously free 
        """
        if i < 0 or i >= 9 or j < 0 or j >= 9:
            return False
        if not self.cells[i * 9 + j]: 
            self.cells[i * 9 + j] = True
            return True
        else:
            return False
    
    def fit(self, piece, i, j):
        """test whether a piece fit at a location
        >>> b = Board()
        >>> p = Piece([(0,0), (1,0), (2,0)])
        >>> b.fit(p, 6, 0)
        True
        >>> b.fit(p, 8, 0)
        False
        >>> p = Piece([(0,0), (0,1), (0,2)])
        >>> b.fit(p, 0, 7)
        False
        """
        for e in piece.elements:
            #print(i+ e[0], j+ e[1])
            if i + e[0] > 9 or j + e[1] > 9:
                return False
            if self.at(i + e[0], j + e[1]):
                return False
        return True
    
    def place(self, piece, i, j):
        """Add a piece on the board at line i and col j.
        
        :piece: the piece to add
        :return: True if the piece could be added, false otherwise
        
        >>> b = Board()
        >>> p = Piece([(0,0), (1, 0), (1,1), (2,1)])
        >>> b.place(p, 2, 5)
        True
        >>> print(b)
        +-----------------+
        |                 |
        |                 |
        |          X      |
        |          X X    |
        |            X    |
        |                 |
        |                 |
        |                 |
        |                 |
        +-----------------+
        """
        if not self.fit(piece, i, j):
            return False
        for e in piece.elements:
            self._set(i + e[0], j + e[1])
        return True
           
    def reduce(self):
        """finds complete lines, columns, or zone, and remove the piece
        elements there.
        
        If a line and a column (or a zone) are both complete, both are 
        removed.
        
        :return: the number of matches (lines, col or zones)
        
        >>> b = Board(data=[True]*81)
        >>> b.reduce()
        27
        >>> print(b)
        +-----------------+
        |                 |
        |                 |
        |                 |
        |                 |
        |                 |
        |                 |
        |                 |
        |                 |
        |                 |
        +-----------------+
    """
        lines =[]
        cols = []
        zones = []
        # First find them
        for i in range(9):
            l = self.line(i)
            if sum(l) >= 9:
                lines .append(i)
            c = self.column(i)
            if sum(c) >= 9:
                cols .append(i)
            z = self.zone(i)
            if sum(z) >= 9:
                zones.append(i)
        # Then remove them
        for l in lines:
            self.clearLine(l)
        for c in cols:
            self.clearColumn(c)
        for z in zones:
            self.clearZone(z)
        return len(lines)+len(cols)+len(zones)
        
        
class Piece:
    """A piece is represented by the list of its elements :
    each element is a tuple of (line, column coordinate). By convention,
    elements coordidinates are always positives (i.e. located wrt the lower 
    left element)
    """    
    
    def __init__(self, elements):
        self.elements = elements
        self.w = max([e[1] for e in self.elements])+1
        self.h = max([e[0] for e in self.elements])+1
        
    def __str__(self):
        """
        
        >>> p = Piece([(0,0), (0,1)])
        >>> print(p)
        X X
        >>> p = Piece([(1,0), (0,1), (1,1)])
        >>> print(p)
          X
        X X
        """
        elt = []
        for i in range(self.h):
            elt.append([' ']*self.w)
        for e in self.elements:
            elt[e[0]][e[1]] = 'X'
        return '\n'.join([' '.join(line) for line in elt])



if __name__ == '__main__':
    import doctest
    doctest.testmod()

