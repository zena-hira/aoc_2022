import itertools
import collections as col
import pandas as pd
import heapq
import bisect
import datetime as dt
import re

def parse(line):
    return tuple(map(int,line.split(',')))

def one(lines):
    cubes = list(map(parse, map(str.strip,lines)))
    xy = col.defaultdict(set)
    xz = col.defaultdict(set)
    yz = col.defaultdict(set)

    for (x,y,z) in cubes:
        xy[(x,y)].add(z)
        xz[(x,z)].add(y)
        yz[(y,z)].add(x)


    exposed_sides = 0
    for d in [xy, xz, yz]:
        for c, cs in d.items():
            exposed_sides += 2
            c_a = sorted(cs)
            c_b = c_a[1:]
            exposed_sides += sum(2 for (n,m) in zip(c_a, c_b) if m > (n+1))

    return exposed_sides

test_lines = '''2,2,2
                1,2,2
                3,2,2
                2,1,2
                2,3,2
                2,2,1
                2,2,3
                2,2,4
                2,2,6
                1,2,5
                3,2,5
                2,1,5
                2,3,5'''.split('\n')

def two(lines):
    cubes = set(map(parse, map(str.strip,lines)))

    seen = set()

    for start in itertools.product(range(25), range(25), range(25)):
        if start in cubes or start in seen:
            continue

        visited = set()
        is_outside = False
        q = [start]
        while q:
            curr = q.pop(0)
            if curr in visited:
                continue
            visited.add(curr)

            (x, y, z) = curr
            if x < 0 or x >= 25 or y < 0 or y >= 25 or z < 0 or z >= 25:
                is_outside = True
                continue

            for next in [(x-1,y,z),(x+1,y,z),(x,y-1,z),(x,y+1,z),(x,y,z-1),(x,y,z+1)]:
                if next in cubes or next in visited:
                    continue
                q.append(next)

        seen.update(visited)
        if is_outside:
            pass
        else:
            cubes.update(visited)

    xy = col.defaultdict(set)
    xz = col.defaultdict(set)
    yz = col.defaultdict(set)

    for (x, y, z) in cubes:
        xy[(x, y)].add(z)
        xz[(x, z)].add(y)
        yz[(y, z)].add(x)


    exposed_sides = 0
    for d in [xy, xz, yz]:
        for c, cs in d.items():
            exposed_sides += 2
            c_a = sorted(cs)
            c_b = c_a[1:]
            exposed_sides += sum(2 for (n, m) in zip(c_a, c_b) if m > (n + 1))

    return exposed_sides
