import itertools
import collections
import pandas as pd
import heapq
import bisect
import datetime as dt
import re
import ast
import functools as f

def parse(line):
    m = re.match(r'Sensor at x=([0-9-]+), y=([0-9-]+): closest beacon is at x=([0-9-]+), y=([0-9-]+)', line)
    sx, sy, bx, by = map(int, m.groups())
    return (sx, sy), (bx, by)


def one(lines):
    coords = map(parse, lines)

    target_y = 2000000
    # remember 4 beacons on target row

    covered_ranges = []
    beacons_on_row = set()
    for (s, b) in coords:
        d = distance(s, b)
        r = range_on_row(s, d)
        if r:
            covered_ranges.append(r)

        if beacon_on_row(b):
            beacons_on_row.add(b)

    coords = set()
    for (lo, hi) in covered_ranges:
        coords.update(range(lo, hi+1))

    return len(coords) - len(beacons_on_row)


def distance(s, b):
    (sx, sy), (bx, by) = s, b
    return abs(sx - bx) + abs(sy - by)

def range_on_row(s, d, ty=2000000):
    sx, sy = s

    min_distance_from_row = abs(ty - sy)

    if min_distance_from_row > d:
        return None

    dr = d - min_distance_from_row
    return sx - dr, sx + dr

def beacon_on_row(b, ty=2000000):
    bx, by = b
    return by == ty


def two(lines):
    coords = list(map(parse, lines))
    hi = 4000000
    for y in range(0, hi+1):
        if y % 10000 == 0:
            print(y)
        x = 0
        crs = get_covered_ranges(coords, y)
        for (l, h) in crs:
            if x >= l:
                x = max(x,h+1)
            else:
                return tuning_freq((x,y))

def get_covered_ranges(coords, ty):
    covered_ranges = []
    for (s, b) in coords:
        d = distance(s, b)
        r = range_on_row(s, d, ty=ty)
        if r:
            covered_ranges.append(r)

    return sorted(covered_ranges)

def tuning_freq(c):
    x,y = c
    return x * 4000000 + y