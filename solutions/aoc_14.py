import itertools
import collections
import pandas as pd
import heapq
import bisect
import datetime as dt
import re
import ast
import functools as f

def parse_coord(coord_raw):
    return list(map(int,coord_raw.split(',')))

def parse_line(line):
    rocks = set()
    corners = list(map(parse_coord, line.split(' -> ')))
    for p in zip(corners, corners[1:]):
        (ax, ay), (bx, by) = sorted(p)
        if ay == by:
            for x in range(ax, bx+1):
                rocks.add((x, ay))
        else:
            for y in range(ay, by+1):
                rocks.add((ax, y))
    return rocks

def parse(lines):
    return set().union(*map(parse_line, lines))



def one(lines):
    rocks = parse(lines)
    xs = [c[0] for c in rocks]
    ys = [c[1] for c in rocks]

    x_min = min(xs)
    x_max = max(xs)
    y_max = max(ys)

    sand = set()

    i = 0
    while c := drop_one((500,0), x_min, x_max, y_max, rocks | sand):
        sand.add(c)
        i += 1

    return i

def drop_one(s, x_min, x_max, y_max, blocked):
    cx, cy = s
    while True:
        if cx < x_min or cx > x_max or cy > y_max:
            return False
        if (cx, cy+1) not in blocked:
            cy = cy+1
        elif (cx-1, cy+1) not in blocked:
            cx = cx - 1
            cy = cy + 1
        elif (cx+1, cy+1) not in blocked:
            cx = cx + 1
            cy = cy + 1
        else:
            return (cx, cy)

def two(lines):
    rocks = parse(lines)
    ys = [c[1] for c in rocks]
    y_max = max(ys)
    sand = set()

    i = 0
    while True:
        c = drop_one_2((500, 0), y_max + 2, rocks | sand)
        sand.add(c)
        i += 1
        if c == (500,0):
            break
    return i

def drop_one_2(s, y_floor, blocked):
    cx, cy = s
    while True:
        if (cy+1) == y_floor:
            return (cx, cy)
        if (cx, cy+1) not in blocked:
            cy = cy+1
        elif (cx-1, cy+1) not in blocked:
            cx = cx - 1
            cy = cy + 1
        elif (cx+1, cy+1) not in blocked:
            cx = cx + 1
            cy = cy + 1
        else:
            return (cx, cy)