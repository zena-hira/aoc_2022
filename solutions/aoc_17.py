import itertools
import collections
import pandas as pd
import heapq
import bisect
import datetime as dt
import re


shapes = [
    [(0,0), (1,0), (2,0), (3,0)],         # -
    [(0,1), (1,2), (1,0), (1,1), (2,1)],  # +
    [(0,0), (1,0), (2,0), (2,1), (2,2)],  # flipped L
    [(0,0), (0,1), (0,2), (0,3)],         # |
    [(0,0), (0,1), (1,0), (1,1)],         # []
]

def one(lines):
    jets = lines[0]

    chamber = collections.defaultdict(set)
    # y -> (rock x coords)

    highest_rock = -1
    chamber[-1] = set(range(7))          # x coords are 0-6

    shape_it = itertools.cycle(shapes)
    jet_it = itertools.cycle(jets)

    for _ in range(2022):
        shape = next(shape_it)
        shape_off = (2, highest_rock+4)

        c_f = True
        while c_f:
            jet = next(jet_it)
            shape_off, c_f = move(shape, jet, chamber, shape_off)
        highest_rock = max(highest_rock, add_to_chamber(shape, chamber, shape_off))

    return highest_rock+1

# move lr, then move down.
def move(shape, jet, chamber, shape_offs):
    (o_x, o_y) = shape_offs
    j_o = -1 if jet == '<' else 1

    # can we move l/r:
    can_shift = True
    for (x,y) in shape:
        t_x = x+o_x+j_o
        t_y = y+o_y
        if 0 <= t_x < 7 and (t_y not in chamber or t_x not in chamber[t_y]):
            continue
        can_shift = False
        break

    if can_shift:
        o_x += j_o

    # can we fall?
    if can_fall(shape, chamber, (o_x, o_y)):
        return (o_x, o_y-1), True
    return (o_x, o_y), False


def can_fall(shape, chamber, shape_offs):
    (o_x, o_y) = shape_offs
    for (x,y) in shape:
        t_y = y+o_y-1
        if t_y in chamber and x+o_x in chamber[t_y]:
            return False
    return True


def add_to_chamber(shape, chamber, shape_off):
    max_seen = -1
    o_x, o_y = shape_off
    for (x,y) in shape:
        yv = y+o_y
        chamber[yv].add(x + o_x)
        max_seen = max(yv, max_seen)
    return max_seen


def add_to_chamber2(shape, chamber, shape_off):
    max_seen = -1
    o_x, o_y = shape_off
    cs_to_check = set()
    for (x,y) in shape:
        yv = y+o_y
        xv = x+o_x
        if yv in chamber:
            chamber[yv] = chamber[yv] | {xv}
        else:
            chamber[yv] = frozenset([xv])
            cs_to_check.add((xv, yv))
        max_seen = max(yv, max_seen)

    l_b = find_hoz_path(cs_to_check, chamber)
    if l_b:
        chamber_2 = {}
        for (y, xs) in chamber.items():
            if y >= l_b:
                chamber_2[y-l_b] = chamber[y]
        return max_seen, chamber_2, l_b
    return max_seen, chamber, 0

def find_hoz_path(to_check, chamber):
    all_visited = set()
    path_visited = set()

    for c in to_check:
        if c in all_visited:
            continue
        has_path, visited = find_hoz_connections(c, chamber)
        all_visited.update(visited)
        if has_path:
            path_visited.update(visited)

    if len(path_visited) > 0:
        return min(y for (_,y) in path_visited)
    return None

ns = [(x,y) for x in [-1,0,1] for y in [-1,0,1] if x != 0 or y != 0]

def find_hoz_connections(item, chamber):
    visited = set()
    xs = set()
    q = [item]
    while q:
        c = q.pop()
        if c in visited:
            continue
        visited.add(c)
        (x,y) = c
        xs.add(x)
        if len(xs) == 7:
            return True, visited

        for (x_o, y_o) in ns:
            nx = x + x_o
            ny = y + y_o
            if 0 <= nx < 7 and ny in chamber and nx in chamber[ny] and (nx, ny) not in visited:
                q.append((nx,ny))
    return False, visited

def two(lines):
    jets = lines[0]
    chamber = {}
    # y -> (rock x coords)

    v_floor = 0                  # v_floor + highest_rock == actual highest_rock
    highest_rock = -1            # highest y in chamber
    chamber[-1] = frozenset(range(7))  # x coords are 0-6

    shape_it = itertools.cycle(zip(shapes, range(len(shapes))))
    jet_it = itertools.cycle(zip(jets, range(len(jets))))

    seen_states = {}
    it_heights = {}

    # find the loop point, recording max height per step
    current_it = 0
    while True:

        shape, shape_i = next(shape_it)
        shape_off = (2, highest_rock + 4)
        jet_i = None
        c_f = True
        while c_f:
            jet, jet_i = next(jet_it)
            shape_off, c_f = move(shape, jet, chamber, shape_off)

        max_seen, chamber, v_shift = add_to_chamber2(shape, chamber, shape_off)
        highest_rock = max(highest_rock - v_shift, max_seen - v_shift)
        v_floor += v_shift

        if v_shift:
            f_c = frozenset(chamber.items())
            state = (f_c, shape_i, jet_i)
            if state in seen_states:
                p_it, p_floor, p_hr = seen_states[state]
                its_per_loop = current_it - p_it
                height_per_loop = (v_floor+highest_rock) - (p_floor+p_hr)

                target = 1_000_000_000_000
                target_minus_init = target - p_it
                num_loops = target_minus_init // its_per_loop
                leftovers = target_minus_init % its_per_loop


                x_floor, x_hr = it_heights[p_it + leftovers - 1]

                total_height = height_per_loop * num_loops + x_floor + x_hr + 1

                return total_height
            else:
                seen_states[state] = (current_it, v_floor, highest_rock)
        it_heights[current_it] = (v_floor, highest_rock)
        current_it += 1