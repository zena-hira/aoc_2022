import itertools
import collections
import pandas as pd
import heapq
import bisect
import re
import math

def parse_monkey(lines):
    hdr, starting, op, test, tru, fal = lines
    get_int = lambda s: int(re.findall(r'\d+', s)[0])
    m = {
        'monkey': int(hdr[-2]),
        'items': list(map(int,re.findall(r'\d+', starting))),
        'op': eval("lambda old: " + op.split('=')[1]),
        'test_div': get_int(test),
        'true': get_int(tru),
        'false': get_int(fal)
    }
    return m

def parse(lines):
    return [parse_monkey(lines[i*7:(i*7) + 6]) for i in range(8)]

def one(lines):
    monkeys = parse(lines)

    counts = collections.Counter()
    for i in range(20):
        do_round(monkeys, counts)

    (m1,c1), (m2,c2) = counts.most_common(2)
    return c1 * c2

def do_round(monkeys, inspect_count, wd=3, m=None):
    for i in range(len(monkeys)):
        do_turn(monkeys[i], monkeys, inspect_count, wd, m)

def do_turn(monkey, monkeys, inspect_count, wd, m=None):
    items = monkey['items']
    monkey['items'] = []
    for worry in items:
        inspect_count[monkey['monkey']] += 1
        worry = (monkey['op'](worry))
        if m:
            worry = worry % m
        worry = worry // wd
        if worry % monkey['test_div'] == 0:
            monkeys[monkey['true']]['items'].append(worry)
        else:
            monkeys[monkey['false']]['items'].append(worry)

def two(lines):
    monkeys = parse(lines)

    d = math.prod(m['test_div'] for m in monkeys)
    counts = collections.Counter()
    for i in range(10000):
        do_round(monkeys, counts, 1, d)

    (m1,c1), (m2,c2) = counts.most_common(2)
    return c1 * c2