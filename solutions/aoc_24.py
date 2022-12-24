import itertools
import collections
import pandas as pd
import heapq
import bisect
import datetime as dt
import re

def parse(lines):
    blizzards = set()
    for (y, line) in enumerate(lines):
        for (x, char) in enumerate(line):
            if char in "<>^v":
                blizzards.add(((x,y),char))
    return blizzards

len_x = 152
len_y = 22

start = (1, 0)
target = (150, 21)

def one(lines):
    blizzards = parse(lines)

    grid = collections.defaultdict(set)
    for ((x,y), b) in blizzards:
        grid[(x,y)].add(b)

    possible_me = set([start])

    i = 0
    while True:
        next_grid = move_blizzards(grid)
        next_me = move_me(possible_me)
        next_me.difference_update(next_grid.keys())
        i += 1
        if target in next_me:
            return i
        grid = next_grid
        possible_me = next_me

def move_me(possible_mes):
    nxt = set()
    for (x,y) in possible_mes:
        nxt.add((x,y))
        for (nx,ny) in [(x+1, y), (x-1,y), (x,y-1), (x,y+1)]:
            if (nx,ny) == target or (nx,ny) == start or (nx > 0 and nx < (len_x-1) and ny > 0 and ny < (len_y-1)):
                nxt.add((nx,ny))
    return nxt

def print_grid(grid, possible_me):
    for y in range(len_y):
        for x in range(len_x):
            if (x,y) == start or (x,y) == target:
                print(end='.')
            elif (x,y) in grid:
                if (x,y) in possible_me:
                    raise 'Oh no!'
                print(end=str(len(grid[(x,y)])))
            elif (x,y) in possible_me:
                print(end='*')
            elif x == 0 or x == len_x - 1 or y == 0 or y == len_y - 1:
                print(end='#')

            else:
                print(end='.')
        print()


def move_blizzards(grid):
    nxt_blizzards = collections.defaultdict(set)
    for ((x,y), bs) in grid.items():
        for b in bs:
            if b == '>':
                nx, ny = x + 1, y
            elif b == '<':
                nx, ny = x - 1, y
            elif b == '^':
                nx, ny = x, y - 1
            elif b == 'v':
                nx, ny = x, y + 1
            else:
                raise 'oops'
            if nx == 0:
                nx = len_x - 2
            if nx == len_x - 1:
                nx = 1
            if ny == 0:
                ny = len_y - 2
            if ny == len_y - 1:
                ny = 1
            nxt_blizzards[(nx,ny)].add(b)
    return nxt_blizzards

def two(lines):
    blizzards = parse(lines)

    grid = collections.defaultdict(set)
    for ((x, y), b) in blizzards:
        grid[(x, y)].add(b)

    possible_me = set([start])

    i = 0
    while True:
        #print_grid(grid, possible_me)
        next_grid = move_blizzards(grid)
        next_me = move_me(possible_me)
        next_me.difference_update(next_grid.keys())
        i += 1
        grid = next_grid
        possible_me = next_me
        if target in next_me:
            break

    possible_me = set([target])

    while True:
        next_grid = move_blizzards(grid)
        next_me = move_me(possible_me)
        next_me.difference_update(next_grid.keys())
        i += 1
        grid = next_grid
        possible_me = next_me
        if start in next_me:
            break

    possible_me = set([start])

    while True:
        next_grid = move_blizzards(grid)
        next_me = move_me(possible_me)
        next_me.difference_update(next_grid.keys())
        i += 1
        grid = next_grid
        possible_me = next_me
        if target in next_me:
            break
    return i
