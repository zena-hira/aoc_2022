import itertools
import collections as c
import math

import pandas as pd
import heapq
import bisect
import datetime as dt
import re

def parse(lines : [str]):
    grid = {}
    x_edges = {}
    y_edges = {}
    instructions = None
    row = 0
    for line in lines:
        if '.' in line:
            row += 1
            col = 0
            for c in line:
                col += 1
                if c in ['.', '#']:
                    grid[(col, row)] = c

                    if col in x_edges:
                        x_edges[col][1] = row
                    else:
                        x_edges[col] = [row, row]

                    if row in y_edges:
                        y_edges[row][1] = col
                    else:
                        y_edges[row] = [col, col]

        elif '1' in line:
            instructions = [ (int(n) if n else d) for n, d in re.findall(r'(\d+)|([RL])', line) ]
            return grid, x_edges, y_edges, instructions


f_vals = '>v<^'

f_map = {   ('>', 'L'): '^' ,
            ('v', 'L'): '>' ,
            ('<', 'L'): 'v' ,
            ('^', 'L'): '<' ,
            ('>', 'R'): 'v' ,
            ('v', 'R'): '<' ,
            ('<', 'R'): '^' ,
            ('^', 'R'): '>'
          }

f_changes = { '>': (1, 0),
              '<': (-1, 0),
              '^': (0, -1),
              'v': (0, 1)
              }

edge_map = { -1: 1, 1: 0 }

def step(i, curr, grid, x_edges, y_edges):
    (col, row), facing = curr

    if i in set('LR'):
        return (col, row), f_map[(facing, i)]

    (m_x, m_y) = f_changes[facing]

    for _ in range(i):
        ncol = col + m_x
        nrow = row + m_y
        if (ncol, nrow) not in grid:
            if m_y == 0:
                ncol = y_edges[nrow][edge_map[m_x]]
            else:
                nrow = x_edges[ncol][edge_map[m_y]]

        if grid[(ncol, nrow)] == '#':
            return (col, row), facing
        col = ncol
        row = nrow

    return (col, row), facing


def one(lines):
    grid, x_edges, y_edges, instructions = parse(lines)

    start = ( (y_edges[1][0], 1), '>')

    if grid[start[0]] != '.':
        raise "oops"

    curr = start

    for i in instructions:
        curr = step(i, curr, grid, x_edges, y_edges)

    (f_col, f_row), f_dir = curr
    return (f_row * 1000) + (f_col * 4) + f_vals.index(f_dir)

def two(lines):
    grid, x_edges, y_edges, instructions = parse(lines)

    start = ( (y_edges[1][0], 1), '>')
    if grid[start[0]] != '.':
        raise "oops"

    curr = start

    for i in instructions:
        curr = step2(i, curr, grid, x_edges, y_edges)

    # print_grid(grid)

    (f_col, f_row), f_dir = curr
    return (f_row * 1000) + (f_col * 4) + f_vals.index(f_dir)

def print_grid(grid):
    for i in range(200):
        print()
        for j in range(150):
            if (j+1, i+1) in grid:
                print(end=grid[(j+1, i+1)])
            else:
                print(end=' ')

def step2(i, curr, grid, x_edges, y_edges):
    (col, row), facing = curr

    if i in set('LR'):
        return (col, row), f_map[(facing, i)]

    for _ in range(i):
        (m_x, m_y) = f_changes[facing]
        ncol = col + m_x
        nrow = row + m_y
        nfacing = facing
        if (ncol, nrow) not in grid:
            ncol, nrow, nfacing = calc_cube_next(col, row, m_x, m_y)

        if grid[(ncol, nrow)] == '#':
            return (col, row), facing

        col = ncol
        row = nrow
        facing = nfacing

    return (col, row), facing

face_map = {  ((0,2), (0,1)):  (1, 1, '>', True, False, False) # flip x-y, mirror x-after, mirror y after
            , ((0,2), (-1,2)): (1, 0, '>', False, False, True)
            , ((1,2), (2,2)):  (2, 0, '<', False, False, True)
            , ((1,2), (1,3)):  (0, 3, '<', True, False, False)
            , ((0,3), (-1,3)): (1, 0, 'v', True, False, False)
            , ((0,3), ( 0,4)): (2, 0, 'v', False, False, True)
            , ((0,3), ( 1,3)): (1, 2, '^', True, False, False)
            , ((1,1), (0,1)): (0,2, 'v', True, False, False)
            , ((1,1), (2,1)): (2,0, '^', True, False, False)
            , ((1, 0), (0, 0)): (0, 2, '>', False, False, True)
            , ((1, 0), (1, -1)): (0,3, '>', True, False, False)
            , ((2, 0), (2, -1)): (0,3, '^', False, False, True)
            , ((2, 0), (3, 0)): (1,2, '<', False, False, True)
            , ((2, 0), (2, 1)): (1,1 , '<', True, False, False)
            }

def calc_cube_next(col, row, m_x, m_y):
    ncol = col + m_x
    nrow = row + m_y

    c_face = ((col-1) // 50, (row-1) // 50)
    n_face = ((ncol-1) // 50, (nrow-1) // 50)

    col_off = (col - 1) % 50
    row_off = (row - 1) % 50

    fx, fy, ndir, flip, mirx, miry = face_map[(c_face, n_face)]
    if flip:
        row_off, col_off = col_off, row_off

    if mirx:
        col_off = 49 - col_off
    if miry:
        row_off = 49 - row_off

    ncol = fx * 50 + col_off + 1
    nrow = fy * 50 + row_off + 1

    return ncol, nrow, ndir