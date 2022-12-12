import itertools
import collections
import pandas as pd
import heapq
import bisect
import datetime as dt
import re


def parse_one(char):
    if char == 'E':
        return -2
    elif char == 'S':
        return -1
    return ord(char) - ord('a')

def parse_row(line):
    return list(map(parse_one, line))

def parse(lines):
    grid = list(map(parse_row, lines))

    start = None
    end = None
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == -1:
                start = (i,j)
                grid[i][j] = 0
            if grid[i][j] == -2:
                end = (i,j)
                grid[i][j] = 25

    return grid, start, end


def one(lines):
    grid, start, end = parse(lines)

    todo = [(0,start)]
    lowest_costs = collections.defaultdict(lambda:99999999999999)

    while True:
        c_cost, (x,y) = heapq.heappop(todo)
        if (x,y) == end:
            return c_cost

        if lowest_costs[(x,y)] <= c_cost:
            continue

        lowest_costs[(x,y)] = c_cost

        c_height = grid[x][y]
        for (nx, ny) in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
            if nx < 0 or nx >= len(grid) or ny < 0 or ny >= len(grid[nx]):
                continue
            n_height = grid[nx][ny]
            if n_height > c_height + 1:
                continue
            if lowest_costs[(nx,ny)] > c_cost+1:
                heapq.heappush(todo, (c_cost+1, (nx, ny)))


def two(lines):
    lowest_costs = collections.defaultdict(lambda:99999999999999)
    grid, _, end = parse(lines)

    min_steps = 9999999999
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                min_steps = min(min_steps, search(grid, (i,j), end, lowest_costs))
    return min_steps


def search(grid, start, end, lowest_costs):

    todo = [(0,start)]
    while todo:
        c_cost, (x,y) = heapq.heappop(todo)
        if (x,y) == end:
            return c_cost

        if lowest_costs[(x,y)] <= c_cost:
            continue

        lowest_costs[(x,y)] = c_cost

        c_height = grid[x][y]
        for (nx, ny) in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
            if nx < 0 or nx >= len(grid) or ny < 0 or ny >= len(grid[nx]):
                continue
            n_height = grid[nx][ny]
            if n_height > c_height + 1:
                continue
            if lowest_costs[(nx,ny)] > c_cost+1:
                heapq.heappush(todo, (c_cost+1, (nx, ny)))
    return 9999999999