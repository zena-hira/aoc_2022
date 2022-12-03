import itertools
import collections
import pandas as pd
import heapq
import bisect
import datetime as dt
import re

def score(line):
    mid = len(line) // 2
    c1 = line[0:mid]
    c2 = line[mid:]
    common = list((set(c1).intersection(set(c2))))[0]
    p = prio(common)
    return p

def prio(letter):
    if letter >= 'a' and letter <= 'z':
        return 1 + ord(letter) - ord('a')

    return 1 + ord(letter) - ord('A') + 26

def one(lines):
    scores = map(score, lines)
    return sum(scores)

def two(lines):
    i = 0
    found_badges = []
    group = None
    for line in lines:
        if i % 3 == 0:
            if group:
                found_badges.extend(i for i, c in group.items() if c == 3)
            group = collections.Counter()
        i = i + 1
        group.update({ i for i, c in collections.Counter(line).items() if c == 1 })
    return sum(map(prio, found_badges))

def two(lines):
    i = 0
    found_badges = []
    group = []
    for line in lines:
        if i % 3 == 0:
            if group:
                a,b,c = group
                found_badges.extend(a.intersection(b).intersection(c))
            group = []
        i = i + 1
        group.append(set(line))

    a, b, c = group
    found_badges.extend(a.intersection(b).intersection(c))

    return sum(map(prio, found_badges))