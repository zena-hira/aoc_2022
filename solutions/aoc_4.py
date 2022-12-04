import itertools
import collections
import pandas as pd
import heapq
import bisect
import datetime as dt
import re

def parse(line):
    a, b = line.split(',')
    return list(map(int, [*a.split('-'), *b.split('-')]))

def contains(l):
    a, b, c, d = l
    if a <= c and b >= d or c <= a and d >= b:
        return 1
    return 0

def contains_2(l):
    a, b, c, d = l
    if len(set(range(a, b+1)).intersection(set(range(c,d+1)))) > 0:
        return 1
    return 0


def one(lines):
    return sum(map(contains, (map(parse, lines))))



def two(lines):
    return sum(map(contains_2, (map(parse, lines))))
