import itertools
import collections
import pandas as pd
import heapq
import bisect
import datetime as dt
import re

def parse(line):
    s = 0
    for x in line.strip():
        s *= 5

        if x == '2':
            s += 2
        if x == '1':
            s += 1
        if x == '0':
            pass
        if x == '-':
            s -= 1
        if x == '=':
            s -= 2
    return s

def one(lines):
    sample = """
    1=-0-2
    12111
    2=0=
    21
    2=01
    111
    20012
    112
    1=-1=
    1-12
    12
    1=
    122
    """
    #lines = sample.split()
    s = sum(map(parse,lines))
    print(s)
    return rev(s)

def rev(n):
    r = []
    while n > 0:
        nmf = n % 5
        if nmf == 0:
            r.insert(0, '0')
            n = n // 5
        elif nmf == 1:
            r.insert(0, '1')
            n = n // 5
        elif nmf == 2:
            r.insert(0, '2')
            n = n // 5
        elif nmf == 3:
            r.insert(0, '=')
            n = (n+2) // 5
        elif nmf == 4:
            r.insert(0, '-')
            n = (n+1) // 5
    return ''.join(r)

def two(lines):
    return ':)'
