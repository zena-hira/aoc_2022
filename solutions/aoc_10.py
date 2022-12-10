import itertools
import collections
import pandas as pd
import heapq
import bisect
import datetime as dt
import re

def parse(line):
    if line == "noop":
        return (1,0)
    _,x = line.split()
    return (2, int(x))

def one(lines):
    instrs = list(map(parse,lines))

    targets = {20,60,100,140,180,220}

    ss = 0

    i = 1
    x = 1
    while i < 225:
        (n, amt) = instrs.pop(0)
        for _ in range(n):
            if i in targets:
                ss += (i * x)
            i += 1
        x += amt

    return ss


def two(lines):
    instrs = list(map(parse, lines))

    out_lines = []
    i = 1
    x = 1
    c = 0
    while i < 241:
        (n, amt) = instrs.pop(0)
        for _ in range(n):
            if c == 0:
                out_lines.append([])
            out_lines[-1].append([' ','#'][c in range(x-1, x+2)])
            c = (c + 1) % 40
            i += 1
        x += amt

    for l in out_lines:
        print(''.join(l))