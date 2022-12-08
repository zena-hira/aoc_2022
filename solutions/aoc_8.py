import itertools
import collections as c
import pandas as pd
import heapq
import bisect
import datetime as dt
import re


def one(lines):
    grid = [list(map(int,l)) for l in lines]
    visible = {}
    h,w = len(lines),len(lines[0])

    for i in range(h):
        c = -1
        for j in range(w):
            if grid[i][j] > c:
                c = grid[i][j]
                visible[(i,j)] = True
        c = -1
        for j in range(w-1,-1,-1):
            if grid[i][j] > c:
                c = grid[i][j]
                visible[(i,j)] = True
        c = -1
        for j in range(w - 1, -1, -1):
            if grid[j][i] > c:
                c = grid[j][i]
                visible[(j, i)] = True
        c = -1
        for j in range(w):
            if grid[j][i] > c:
                c = grid[j][i]
                visible[(j, i)] = True
    return len(visible)


def score(grid, x, y, h):
    c = h
    total = 1

    ss = 0
    i = x+1
    while i < 99 and grid[i][y] < c:
        ss += 1
        i += 1
    if i < 99:
        ss += 1
    total *= ss

    ss = 0
    i = y+1
    while (i < 99) and grid[x][i] < c:
        ss += 1
        i += 1
    if i < 99:
        ss += 1
    total *= ss

    ss = 0
    i = x-1
    while i >= 0 and grid[i][y] < c:
        ss += 1
        i -= 1
    if i >= 0:
        ss += 1
    total *= ss

    ss = 0
    i = y-1
    while i >= 0 and grid[x][i] < c:
        ss += 1
        i -= 1
    if i >= 0:
        ss += 1
    total *= ss

    return total


def two(lines):
    grid = [list(map(int,l)) for l in lines]
    scenic_scores={}
    h,w = len(lines),len(lines[0])
    for i in range(h):
        for j in range(w):
            scenic_scores[(i,j)] = score(grid, i, j, grid[i][j])
    return max(scenic_scores.values())
