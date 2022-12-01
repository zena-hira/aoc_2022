import itertools
import collections
import pandas as pd
import heapq
import bisect
import datetime as dt
import re


def one(_input):
    sum_1 = 0
    sums = []
    for line in _input:
        if line == "":
            sums.append(sum_1)
            sum_1 = 0
        else:
            sum_1 += int(line)

    return (max(sums))


def two(_input):
    sum_1 = 0
    sums = []
    for line in _input:
        if line == "":
            sums.append(sum_1)
            sum_1 = 0
        else:
            sum_1 += int(line)

    return sum(sorted(sums, reverse=True)[0:3])
