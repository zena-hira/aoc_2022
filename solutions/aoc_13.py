import itertools
import collections
import pandas as pd
import heapq
import bisect
import datetime as dt
import re
import ast
import functools as f

def parse(lines):
    res = {}
    for i in range(len(lines)//3 + 1):
        a = ast.literal_eval(lines[i*3])
        b = ast.literal_eval(lines[i*3 + 1])
        res[i+1] = (a,b)
    return res

def one(lines):
    keyed_pairs = parse(lines)

    return sum([i for (i,(l,r)) in keyed_pairs.items() if compare(l,r) < 0])


def compare(l, r):
    if type(l) is int and type(r) is int:
        return l - r

    if type(l) is list and type(r) is list:
        for (a,b) in zip(l,r):
            c = compare(a,b)
            if c != 0:
                return c
        return len(l) - len(r)

    if type(l) is int:
        return compare([l], r)

    return compare(l, [r])

def two(lines):

    all_items = []
    k0 = [[2]]
    k1 = [[6]]
    for p in parse(lines).values():
        all_items.extend(p)
    all_items.extend([k0, k1])

    xs = sorted(all_items, key=f.cmp_to_key(compare))

    return (xs.index(k0) + 1) * (xs.index(k1) + 1)