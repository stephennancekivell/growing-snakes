#!/usr/bin/env python

import time
import random

class Snake:
    size = 0
    pos = [] # list of (row,column) head is at position 0

    def __str__(self):
        return "<%s> %s wt:%i ws%i" %(hex(id(self)),self.pos[0], self.weight_target,self.weight_selfd)

    def __init__(self,game):
        self.game=game
        self.pos = [(1,1),(1,2)]#.append((0,0))
        self.weight_target = random.uniform(0,5)
        self.weight_selfd = random.uniform(-5,0)

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

    def tick(self):
        m = self.best_move()
        if m ==-1: return 'lose'
        elif m == self.game.target:
            self.grow_to(m)
            return 'target'
        else:
            self.move(m)
            return ''

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

    @staticmethod
    def mate(s1,s2):
        if s1.game != s2.game:
            raise "Error mating snakes from different games"
        child = Snake(s1.game)
        child.pos = s1.pos # should i check the pos is the same?
        child.weight_target = float(s1.weight_target + s2.weight_target)/2
        child.weight_selfd = float(s1.weight_selfd + s2.weight_selfd)/2
        return child

class snake_game:
    grid_size = (10,10) #row,colum
    target = (5,5)

    def __init__(self):
        self.snake = Snake(self)

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
        # this will miss lots when the number of free cells is small
        while 1:
            t = (random.randint(0,self.grid_size[0]),
                random.randint(0,self.grid_size[1]))
            if t not in self.snake.pos:
                return t

    def tick(self):
        return self.snake.tick()
       
    def play(self):
        while 1:
            c = self.tick()
            if c == 'target':
                self.target = self.new_target()
                
            self.draw_grid()
            if c == 'lose': break
            time.sleep(0.3)

    def play_evolving(self,population_size):
        snakes = {self.snake: 0}
        for i in range(population_size):
            print Snake(self)
            snakes[Snake(self)] =0

        while 'playing game':
            for snake in snakes:
                play_count=0
                while play_count < 30:
                    play_count+=1
                    res = snake.tick()
                    if res == 'target':
                        snakes[snake]=play_count
                        break
                    elif res =='lose':
                        snakes[snake] = -1
                        break

            print snakes
            break
            #snakes = [mate snakes in tornament]

class e_pit:
    # the snake pit full of evolving snakes
    def __init__(self,size):
        self.game = snake_game()
        self.snakes = []
        for i in range(size):
            self.snakes.append(Snake(self.game))

    def tick(self):
        times = {}

        for snake in self.snakes:
            self.game.snake = snake
            print snake,snake.pos
            tick_count=0
            while tick_count <= 40:
                self.game.draw_grid()
                time.sleep(0.2)
                tick_count+=1
                res = snake.tick()
                if res == 'target':
                    times[snake]=tick_count
                    break
                elif res =='lose':
                    times[snake] = -1
                    break
        print times

        if len(times)==0:
            raise Exception('all snakes went extinct, nothing to evolve')

        # mating tornament
        snakes2=[]
        for i in range(len(self.snakes)):
            m1 = random.choice(times.keys())
            m2 = random.choice(times.keys())
            f1 = random.choice(times.keys())
            f2 = random.choice(times.keys())

            f = f1
            if times[f2] < times[f1]: f = f2
            m = m1
            if times[m2] < times[m1]: m = m2
    
            snakes2.append(Snake.mate(f,m))
        self.snakes = snakes2

if __name__=='__main__':
    #sg= snake_game()
    #sg.snake.pos.append((1,1))
    #sg.snake.pos.append((1,2))
    e = e_pit(3)
    e.tick()
    e.game.target = e.game.new_target()
    e.tick()


