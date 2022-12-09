import itertools
import collections
import pandas as pd
import heapq
import bisect
import datetime as dt
import re

def parse(line):
    dir, raw_amount = line.split()
    return (dir, int(raw_amount))

def one(lines):
    instrs = map(parse, lines)

    h=(0,0)
    t=(0,0)
    seen = { (0,0) }

    for dir, amount in instrs:
        for _ in range(amount):
            h = move(dir, h)
            t = move_toward(h, t)
            seen.add(t)
    return len(seen)

dirs = { 'U': (0,1),
         'D': (0,-1),
         'L': (-1,0),
         'R': (1,0) }

def move(dir, v):
    x,y = v
    a,b = dirs[dir]
    return (x+a, y+b)

def move_toward(h, t):
    hx,hy = h
    tx,ty = t

    rx=0
    ry=0

    xd = abs(hx - tx)
    yd = abs(hy - ty)

    m = (xd+yd) > 2

    if m or xd > 1:
        rx = [-1, 1][hx > tx]
    if m or yd > 1:
        ry = [-1, 1][hy > ty]

    return (tx+rx, ty+ry)

def two(lines):
    instrs = map(parse, lines)

    rope=[(0,0)]*10
    tail_seen = { (0,0) }

    for dir, amount in instrs:
        for _ in range(amount):
            n_rope=[]
            h = move(dir, rope[0])
            for t in rope[1:]:
                n_rope.append(h)
                h = move_toward(h, t)
            n_rope.append(h)
            tail_seen.add(h)
            rope = n_rope
    return len(tail_seen)