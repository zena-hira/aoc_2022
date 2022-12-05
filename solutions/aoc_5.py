import itertools
import collections as c
import pandas as pd
import heapq
import bisect
import datetime as dt
import re

def parse_picture(lines):
    stack_state = c.defaultdict(list)
    bs = list(reversed(lines))

    for b in bs:
        for i in range(1,10):
            x = b[((i - 1) * 4)+1]
            if x != " ":
                stack_state[i].append(x)
    return stack_state


def parse_instr(line):
    (count, fr, to) = map(int, re.match(r'move (\d+) from (\d) to (\d)', line).groups())
    return (count, fr, to)


def parse(lines):
    s = lines.index("")
    picture = lines[0:s-1]
    instrs = lines[s+1:]

    stack_state = parse_picture(picture)

    iss = map(parse_instr, instrs)
    return stack_state, iss



def one(lines):
    ss, instrs = parse(lines)

    for (count, fr, to) in instrs:
        for i in range(count):
            x = ss[fr].pop()
            ss[to].append(x)

    out = []
    for i in range(1,10):
        out.append(ss[i][-1])

    return ''.join(out)




def two(lines):
    ss, instrs = parse(lines)

    for (count, fr, to) in instrs:
        t = []
        for i in range(count):
            x = ss[fr].pop()
            t.append(x)
        for i in range(count):
            x = t.pop()
            ss[to].append(x)

    out = []
    for i in range(1,10):
        out.append(ss[i][-1])

    return ''.join(out)