#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Interactive interface for the game and automatic player agent

Usage:
    fiver.py [--seed=<n>]
    fiver.py (-h | --help | --version)
    
Options:
    -h, --help      Display help
    --seed=<n>      Random seed to use
"""

import sys
from docopt import docopt
import pygame

from game import Game

_author__="Rémi Pannequin"
__copyright__ = "Copyright 2020"
__credits__ = ["Rémi Pannequin"]
__license__ = "GPL"
__maintainer__ = "Rémi Pannequin"
__email__ = "remi.pannequin@gmail.com"
__status__ = "Development"


#couleur des pieces
WHITE = 255, 255, 255
P_COLOR = 255,255,255
P_HOVER_COLOR = 75, 75, 75
ZONE_COLOR = 125,125,125
REM_COLOR = pygame.color.THECOLORS['gold']
REMOVE_TICK = 3

class Window:

    def __init__(self, seed = None):
        pygame.init()
        pygame.font.init()
        #variables
        self.seed = seed
        self.reset()
        self.compute_size()
        self.removed = set()
        self.removed_ts = 0

    def compute_size(self):
        height = 800
        width = round(height*(9/(9+1.5)))+20
        self.l = round((width-20)/9)
        self.win = pygame.display.set_mode((width, height))
        self.font = pygame.font.SysFont("arial", 36)
        self.font_big = pygame.font.SysFont("arial", 70)


    def reset(self):
        self.game_over = False
        self.g = Game(seed = self.seed)


    def pix(self, r):
        return int(10 + r*self.l)


    def grid(self, x):
        return (x-10)//self.l


    def text_centered(self, msg, x, y, big=False):
        if big:
            text = self.font_big.render(msg, 1, WHITE)
        else:
            text = self.font.render(msg, 1, WHITE)
        textpos = text.get_rect()
        textpos.centerx = x
        textpos.centery = y
        self.win.blit(text, textpos)
        
    
    def text_left(self, msg, height):
        text = self.font.render(msg, True, WHITE)
        textpos = text.get_rect()
        textpos.left = self.pix(0)
        textpos.centery = height
        self.win.blit(text, textpos)
        return textpos.right
    
    
    def draw_game(self):
        background = pygame.Surface(self.win.get_size())
        self.win.blit(background, (0, 0))
        
        # Display score
        self.text_left("Score : %d"%self.g.score, self.pix(9+0.5))
        
        
        # Draw zones
        for r, c in [(0,0), (0,6), (3,3), (6,0), (6,6)]:
            x = self.pix(c)
            y = self.pix(r)
            w = self.pix(c+3) - x
            h = self.pix(r+3) - y
            self.win.fill(ZONE_COLOR, [x, y, w, h])
        # Draw lines
        for col in range(10):
            pygame.draw.line(self.win,
                    WHITE, 
                    [self.pix(col), self.pix(0)],
                    [self.pix(col), self.pix(9)])
        for row in range(10):
            pygame.draw.line(self.win,
                    WHITE, 
                    [self.pix(0), self.pix(row)],
                    [self.pix(9), self.pix(row)])
        
        # Draw Pieces
        for row in range(9):
            for col in range(9):
                if self.g.board.at(row, col):
                    x = self.pix(col) + 1
                    y = self.pix(row) + 1
                    w = self.pix(col+1) - x -1
                    h = self.pix(row+1) - y - 1
                    self.win.fill(P_COLOR, [x, y, w, h])
        
        # Draw next
        next_surf = pygame.Surface((80, 80))
        next_p = self.g.next
        for e in next_p.elements:
            next_surf.fill(WHITE, [e[1]*20+1, e[0]*20+1, 18, 18])
        self.win.blit(next_surf, (self.pix(4.5), self.pix(9.1)))
        
        # Display current piece position
        x,y = pygame.mouse.get_pos()
        #savoir dans quelle case se situe le clic
        if x > self.pix(0) and y > self.pix(0) and x <  self.pix(9) and y < self.pix(9):
            base_c = self.grid(x)
            base_r = self.grid(y)
            if self.g.fit(base_r, base_c):
                for e in next_p.elements:
                    c = base_c + e[1]
                    r = base_r + e[0] 
                    x = self.pix(c) + 1
                    y = self.pix(r) + 1
                    w = self.pix(c+1) - x -1
                    h = self.pix(r+1) - y - 1
                    self.win.fill(P_HOVER_COLOR, [x, y, w, h])
        
        # Draw removed pieces
        for (r, c) in self.removed:
            x = self.pix(c) + 1
            y = self.pix(r) + 1
            w = self.pix(c+1) - x -1
            h = self.pix(r+1) - y - 1
            self.win.fill(REM_COLOR, [x, y, w, h])
        if self.removed_ts == 0:
            self.removed.clear()
        else:
            self.removed_ts -= 1
        
        #Display game over / play again
        if self.game_over:
            self.text_centered("GAME OVER", self.pix(9/2), self.pix(9/2), True)
            
            self.replay_bt = pygame.draw.rect(self.win, 
                                           WHITE, 
                                           [self.pix(9-2.5), 
                                            self.pix(9+0.5), 
                                            self.l*2.5, 
                                            self.l//2], 2)
            self.text_centered("play again", self.replay_bt.centerx, self.replay_bt.centery)


    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x,y = event.pos
                #savoir dans quelle case se situe le clic
                if x > self.pix(0) and y > self.pix(0) and x <  self.pix(9) and y < self.pix(9):
                    col = self.grid(x)
                    row = self.grid(y)
                    self.removed = self.g.play(row, col)
                    self.removed_ts = REMOVE_TICK
                    
                elif self.replay_bt.collidepoint(event.pos):
                    self.reset()


    def loop(self):
        clock = pygame.time.Clock()
        while self.loop:
            self.draw_game()
            self.process_events()
            if not self.game_over and self.g.over():
                self.game_over = True
            # Actualisation de l'affichage
            pygame.display.flip() 
            # 10 fps
            clock.tick(10)
        

if __name__=='__main__':
    
    args = docopt(__doc__)
    
    if args['--seed']:
        s = int(args['--seed'])
    else:
        s = None
    w = Window(seed = s)
    w.loop()
    

