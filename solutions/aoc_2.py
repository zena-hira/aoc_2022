import itertools
import collections
import pandas as pd
import heapq
import bisect
import datetime as dt
import re

def parse(line):
    opp, me = line.split(' ')
    return opp, me

scores = {  ('A', 'X') : 1 + 3,
            ('A', 'Y') : 2 + 6,
            ('A', 'Z') : 3 + 0,
            ('B', 'X') : 1 + 0,
            ('B', 'Y') : 2 + 3,
            ('B', 'Z') : 3 + 6,
            ('C', 'X') : 1 + 6,
            ('C', 'Y') : 2 + 0,
            ('C', 'Z') : 3 + 3 }

def score(part):
    return scores[part]


def one(lines):
    moves = map(parse, lines)
    results = map(score, moves)
    return sum(results)


scores2 = { ('A', 'X') : scores[('A', 'Z')],
            ('A', 'Y') : scores[('A', 'X')],
            ('A', 'Z') : scores[('A', 'Y')],
            ('B', 'X') : scores[('B', 'X')],
            ('B', 'Y') : scores[('B', 'Y')],
            ('B', 'Z') : scores[('B', 'Z')],
            ('C', 'X') : scores[('C', 'Y')],
            ('C', 'Y') : scores[('C', 'Z')],
            ('C', 'Z') : scores[('C', 'X')] }

def score2(part):
    return scores2[part]

def two(lines):
    moves = map(parse, lines)
    results = map(score2, moves)
    return sum(results)