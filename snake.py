#!/usr/bin/env python

import time
import random

class snake:
    size = 0
    pos = [] # list of (row,column) head is at position 0

    weight_target =2
    weight_selfd = -1

    def __init__(self,game):
        self.game=game

    def available_moves(self):
        # all moves from head than are not in pos
        s = self.pos[0]

        x = []
        x.append((s[0]+1,s[1]))
        x.append((s[0]-1,s[1]))
        x.append((s[0],s[1]+1))
        x.append((s[0],s[1]-1))

        x2 = []
        for xi in x:
            if ((xi not in self.pos) and 
                (xi[0] >= 0) and (xi[0] < self.game.grid_size[0]) and 
                (xi[1] >= 0) and (xi[1] < self.game.grid_size[1])):
                x2.append(xi)

        return x2

    def move(self,to):
        self.pos.pop()
        self.pos.insert(0,to)

    def grow_to(self,to):
        self.pos.insert(0,to)

    def weight_move(self,move):
        w = self.weight_target* self.game.score_X(move)
        return w + (self.weight_selfd*self.distance_score(move))

    def best_move(self):
        # returns -1 when no move, must have died, lost game.
        am = self.available_moves()
        if len(am)==0: return -1
        mw = []
        for move in self.available_moves():
            mw.append((self.weight_move(move),move))

        mw.sort()
        return mw[0][1]

    def distance_score(self,cell):
        # could be python one liner
        s =0
        for pos in self.pos:
            s += snake_game.distance_between(pos,cell)
        return s

    @classmethod
    def mate(game,s1,s2):
        child = snake(game)
        child.weight_target = float(s1.weight_target + s2.weight_target)/2
        child.weight_selfd = float(s1.weight_selfd + s2.weight_selfd)/2
        return child

class snake_game:
    grid_size = (10,10) #row,colum
    target = (5,5)

    def __init__(self):
        self.snake = snake(self)

    def draw_grid(self):
        print '----------'
        for r in range(self.grid_size[0]):
            for c in range(self.grid_size[1]):
                if (r,c)== self.target: print 'X',
                elif (r,c) in self.snake.pos: print 'S',
                else: print '.',
            print ''

    @staticmethod
    def distance_between(a,b):
        # a & b are (r,c) coordiniates
        rdiff = a[0]-b[0]
        cdiff = a[1]-b[1]
        return (rdiff*rdiff)+(cdiff*cdiff)

    def score_X(self,cell):
        return snake_game.distance_between(cell, self.target)

    def new_target(self):
        while 1:
            t = (random.randint(0,self.grid_size[0]),
                random.randint(0,self.grid_size[0]))
            if t not in self.snake.pos:
                return t

    def tick(self):
        # run one time_step
        m = self.snake.best_move()
        if m ==-1: return 'lose'
        if m != self.target:
            self.snake.move(m)
        else:
            self.snake.grow_to(m)
            return 'target'

        return ''

    def play(self):
        while 1:
            c = self.tick()
            if c == 'target':
                self.target = self.new_target()
                
            self.draw_grid()
            if c == 'lose': break
            time.sleep(0.3)


if __name__=='__main__':
    sg= snake_game()
    sg.snake.pos.append((1,1))
    sg.snake.pos.append((1,2))
    sg.play()
