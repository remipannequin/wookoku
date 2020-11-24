#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""AI player

"""

import sys
import os
import random
from enum import Enum
from board import Board, Piece
from game import Game, PIECES
import pickle
import matplotlib.pyplot as plt
import numpy

__author__="Rémi Pannequin"
__copyright__ = "Copyright 2020"
__credits__ = ["Rémi Pannequin"]
__license__ = "GPL"
__maintainer__ = "Rémi Pannequin"
__email__ = "remi.pannequin@gmail.com"
__status__ = "Development"

GAMMA = 0.9
GAME_OVER_REWARD = -10



class Player:
    def __init__(self):
        self.game = Game()
        self.Pieces = [Piece(elt) for elt in PIECES]
    
    def loadValues(self):
        if not os.path.exists('values'):
            self.values = dict()
        else:
            self.values = pickle.load(open('values', 'rb'))
    
    def saveValues(self):
        with open('values', 'wb') as f:
            pickle.dump(self.values, f)
    
    def play(self):
        while not self.game.over():
            actions = self.game.actions()
            print(self.game.board)
            # choose action whose destination state has the highest value
            found = (None, -1)
            for (a, v) in evalActions2(actions).items():
                if v > found[1]:
                    found = (a, v)
            # print(found)
            (i, j) = found[0]
            self.game.play(i, j)
        return self.game.score
    
    
    def evalPolicy(self, actions):
        if len(actions) == 0:
            # No actions possibles : game over
            self.value[(h0, n)] = GAME_OVER_REWARD
            return
        for (a, reward, new_state) in actions:
            h1 = new_state.hash()
            h0 = self.game.board.hash()
            n0 = self.game.next_num
            for n1 in range(26): # All next piece have te same probability
                if h1 not in self.values:
                    self.values[h1] = dict(zip(range(26), [0]*26))
                if h0 not in self.values:
                    self.values[h0] = dict(zip(range(26), [0]*26))
                self.values[h0][n0] = (1/26) * (reward + GAMMA * self.values[h1][n1])
                    
         

def evalActions(self, actions, depth=0, n_act=10, n_next=10, max_depth=4):
    if depth >= max_depth:
        return {'': 0}
    r = dict()
    # For a subset of each actions
    for (a, reward, new_state) in random.choices(actions, k=min(n_act, len(actions))):
        # evaluate score for this state
        r[a] = 0
        # For a subset of each possible next piece
        for next in random.choices(self.Pieces , k=n_next):
            hlp = Helper(new_state, next)
            new_actions = hlp.actions()
            ev = self.evalActions(new_actions, depth+1, n_act // 2, n_next, max_depth)
            if len(ev):
                v = reward + sum(ev.values())/len(ev)
            else:
                v = reward
            r[a] += (v/n_next) 
    return r


def evalActions2(actions, n_rep = 100, depth = 10, n_act=20):
    r = dict()
    # For a subset of each actions
    for (a, reward, new_state) in random.choices(actions, k=min(n_act, len(actions))):
    # For each actions
    #for (a, reward, new_state) in actions:
        # evaluate score for the new state
        r[a] = reward
        # run random play for the next moves, eval score
        #create a new game initialez with this state
        for n in range(n_rep):
            g = Game(board=new_state)
            score = rnd_play(g, depth)
            r[a] += score / n_rep
            #print(r)
    return r


def rnd_play(game, max_moves):
    """Random play at most max moves, and return score
    """
    k = 0
    while k < max_moves:
        
        actions = game.actions()
        if len(actions) == 0:
            return GAME_OVER_REWARD
        (i, j) = random.choice([a[0] for a in actions])
        game.play(i, j)
        k += 1
        
    return game.score




    
if __name__ == '__main__':
    scores = []
    #pl = Player() # just to load the data
    for i in range(100):
        pl = Player()
        sc = pl.play()
        scores.append(sc)
        #mean[i%100] = sc
        print (i, sc)
    plt.plot(range(i+1), scores)
    plt.show()
    #pl.saveValues()
