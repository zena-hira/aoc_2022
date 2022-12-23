import itertools
import collections
import pandas as pd
import heapq
import bisect
import datetime as dt
import re

def parse(lines):
    elves = set()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == '#':
                elves.add((x,y))
    return elves


def one(lines):
    elves = parse(lines)
    dirs_to_consider = collections.deque("NSWE")

    for _ in range(10):
        elf_proposals = collections.defaultdict(set)
        next_elves = set()

        for elf in elves:
            if not has_neighbour(elf, elves):
                next_elves.add(elf)
                continue
            if not make_proposal(elf, elves, elf_proposals, dirs_to_consider):
                next_elves.add(elf)
                continue

        for (dest, new_elves) in elf_proposals.items():
            if len(new_elves) == 1:
                next_elves.add(dest)
            else:
                next_elves.update(new_elves)

        if len(elves) != len(next_elves):
            raise 'Oh no!'
        elves = next_elves

        dirs_to_consider.rotate(-1)

    xs = [x for (x,y) in elves]
    ys = [y for (x,y) in elves]

    return ((1+ max(xs) - min(xs)) * (1 + max(ys) - min(ys))) - len(elves)

def has_neighbour(elf, elves):
    x,y = elf
    return any((x+a, y+b) in elves for a in [-1,0,1] for b in [-1,0,1] if not (a == 0 and b == 0))

dir_to_coords = {
    'N': ((0,-1), [(-1,-1), (0, -1), (1, -1)]),
    'S': ((0, 1), [(-1, 1), (0,  1), (1,  1)]),
    'E': ((1, 0), [(1,0), (1, -1), (1,1)]),
    'W': ((-1, 0), [(-1,0),(-1,-1),(-1,1)])
}

def make_proposal(elf, elves, elf_proposals, dirs_to_consider):
    x,y = elf
    for dir in dirs_to_consider:
        (da, db), offs = dir_to_coords[dir]
        if any((x+a, y+b) in elves for (a,b) in offs):
            continue
        elf_proposals[(x+da, y+db)].add(elf)
        return True
    return False

def two(lines):

    elves = parse(lines)
    dirs_to_consider = collections.deque("NSWE")

    i = 0
    while True:
        i = i + 1
        elf_proposals = collections.defaultdict(set)
        next_elves = set()

        for elf in elves:
            if not has_neighbour(elf, elves):
                next_elves.add(elf)
                continue
            if not make_proposal(elf, elves, elf_proposals, dirs_to_consider):
                next_elves.add(elf)
                continue

        moved = False
        for (dest, new_elves) in elf_proposals.items():
            if len(new_elves) == 1:
                moved = True
                next_elves.add(dest)
            else:
                next_elves.update(new_elves)

        if len(elves) != len(next_elves):
            raise 'Oh no!'
        elves = next_elves
        dirs_to_consider.rotate(-1)

        if not moved:
            return i
