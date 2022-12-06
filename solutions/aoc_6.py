import itertools
import collections as c
import pandas as pd
import heapq
import bisect
import datetime as dt
import re


def one(lines):
    the_line = lines[0]
    for i in range(len(the_line)):
        cs = set(the_line[i:i+4])
        if (len(cs) == 4):
            return i+4


def two(lines):
    the_line = lines[0]
    for i in range(len(the_line)):
        cs = set(the_line[i:i+14])
        if (len(cs) == 14):
            return i+14
