import itertools
import collections
import pandas as pd
import heapq
import bisect
import datetime as dt
import re


def one(lines):
    filesystem = collections.defaultdict(collections.Counter)
    current_path = []
    for line in lines:
        l = line.split()
        if line.startswith("$ cd"):
            if l[2] == '/':
                current_path = []
            elif l[2] == '..':
                current_path.pop()
            else:
                current_path.append(l[2])
        elif line.startswith("$ ls"):
            pass
        elif line.startswith("dir"):
            pass
        else:
            size = int(l[0])
            name = l[1]
            filesystem[tuple(current_path)][name] = size
    totals = collections.defaultdict(int)
    for path, counter in filesystem.items():
        for j in range(len(path), -1, -1):
            p = path[0:j]
            totals[(p, )] += sum(counter.values())
    return sum([x for x in totals.values() if x < 100000])



def two(lines):
    filesystem = collections.defaultdict(collections.Counter)
    current_path = []
    for line in lines:
        l = line.split()
        if line.startswith("$ cd"):
            if l[2] == '/':
                current_path = []
            elif l[2] == '..':
                current_path.pop()
            else:
                current_path.append(l[2])
        elif line.startswith("$ ls"):
            pass
        elif line.startswith("dir"):
            pass
        else:
            size = int(l[0])
            name = l[1]
            filesystem[tuple(current_path)][name] = size
    totals = collections.defaultdict(int)
    for path, counter in filesystem.items():
        for j in range(len(path), -1, -1):
            p = path[0:j]
            totals[(p, )] += sum(counter.values())
    root = totals[((),)]
    free = 70000000 - root
    need = 30000000 - free
    return min([x for x in totals.values() if x > need])
