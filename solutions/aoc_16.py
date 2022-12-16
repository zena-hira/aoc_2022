import itertools
import collections
import pandas as pd
import heapq
import bisect
import datetime as dt
import re

def parse(line):
    m = re.match(r'Valve (..) has flow rate=(\d+); tunnel(?:s?) lead(?:s?) to valve(?:s?) (.*)', line)
    valve, raw_rate, out_valves = m.groups()
    return { 'valve': valve,
             'rate': int(raw_rate),
             'next_valves': out_valves.split(', ') }

def build_graph(instrs):
    graph = {}
    for instr in instrs:
        graph[instr['valve']] = (instr['rate'], set(instr['next_valves']))
    return graph

def one(lines):
    caves = list(map(parse, lines))
    graph = build_graph(caves)

    init_state = ( 0             # time now
                 , 'AA'          # where we are
                 , frozenset()   # open valves by name
                 , 0             # current flow per timestep
                 , 0             # total flow
                 )

    q = [(0,init_state)]

    seen = collections.defaultdict(set)
    pressure_at_end = 0

    max_possible_flow_rate = sum(c['rate'] for c in caves)

    while q:
        _, s = heapq.heappop(q)

        if has_seen(s, seen):
            continue

        add_seen(s, seen)

        if (s[4] + (max_possible_flow_rate*(30-s[0]))) < pressure_at_end:
            continue

        if s[0] == 30:
            pressure_at_end = max(pressure_at_end, s[4])
            continue

        if s[3] == max_possible_flow_rate:
            pressure_at_end = max(pressure_at_end, s[4] + (max_possible_flow_rate * (30 - s[0])))
            continue

        for p_s in get_next_states(s, graph):
            if has_seen(p_s, seen):
                continue
            heapq.heappush(q, (-p_s[4], p_s))

    return pressure_at_end

def has_seen(s, seen):
    simpl_s = s[1:]
    for i in range(s[0]+1):
        if simpl_s in seen[i]:
            return True
    return False


def add_seen(s, seen):
    simpl_s = s[1:]
    seen[s[0]].add(simpl_s)


def get_next_states(s, graph):
    time, here, opens, flow_per_step, total_flow = s

    if time >= 30:
        return  # nowhere to go

    rate, nexts = graph[here]

    if rate > 0 and here not in opens:
        a_s = (time + 1, here, opens | {here}, flow_per_step + rate, total_flow + flow_per_step)
        yield from get_next_states(a_s, graph)

    for n in nexts:
        yield time+1, n, opens, flow_per_step, total_flow+flow_per_step

def simpl_graph(graph):
    nodes_we_care_about = ['AA'] + [node for node, (rate, nexts) in graph.items() if rate > 0]

    nodes_to_keep = set()
    for node in nodes_we_care_about:
        for target in nodes_we_care_about:
            if (target > node):
                continue
            nodes_to_keep.update(path_from_to(node, target, graph))

    res = {}
    for node in nodes_to_keep:
        rate, nexts = graph[node]
        res[node] = (rate, nexts & nodes_to_keep)
    return res

def path_from_to(node, target, graph):
    s = (node, set([node]))
    q = [(0, s)]
    while True:
        _, (curr, visited) = heapq.heappop(q)
        if curr == target:
            return visited | {target}

        _, nexts = graph[curr]
        for n in nexts:
            if n not in visited:
                heapq.heappush(q, (-len(visited)+1, (n, visited | {n})))

def two(lines):

    caves = list(map(parse, lines))
    graph = build_graph(caves)
    graph = simpl_graph(graph)
    init_state =  (0  # time now
                  , frozenset(['AA']) # where we both are
                  , frozenset()  # open valves by name
                  , 0 # current flow per timestep
                  , 0 # total flow
                  )

    q = [(0, init_state)]

    seen = collections.defaultdict(dict)
    pressure_at_end = 0

    max_possible_flow_rate = sum(c['rate'] for c in caves)

    while q:
        _, s = heapq.heappop(q)

        if has_seen2(s, seen):
            continue
        add_seen2(s, seen)

        if (s[4] + (max_possible_flow_rate * (26 - s[0]))) < pressure_at_end:
            continue

        if s[0] == 26:
            pressure_at_end = max(pressure_at_end, s[4])
            continue

        if s[3] == max_possible_flow_rate:
            pressure_at_end = max(pressure_at_end, s[4] + (max_possible_flow_rate * (26 - s[0])))
            continue

        for p_s in get_next_states2(s, graph):
            if has_seen2(p_s, seen):
                continue
            heapq.heappush(q, (-p_s[4], p_s))

    return pressure_at_end


def add_seen2(s, seen):
    simpl_s = s[1:3]
    seen[s[0]][simpl_s] = s[4]

def has_seen2(s, seen):
    simpl_s = s[1:3]
    for i in range(s[0], -1, -1):
        v = seen[i].get(simpl_s, -1)
        if v >= s[4]:
            return True
    return False

def get_next_states2(s, graph):
    time, here, opens, flow_per_step, total_flow = s

    if time >= 26:
        return  # nowhere to go

    if len(here) == 1:
        # both in same place
        us = list(here)[0]
        rate, nexts = graph[us]
        if rate > 0 and us not in opens:
            # one stays and opens, one moves
            for n in nexts:
                yield (time + 1, here | {n}, opens | {us}, flow_per_step + rate, total_flow + flow_per_step)

        # both move
        for n in set(map(frozenset,itertools.product(nexts, nexts))):
            yield (time + 1, n, opens, flow_per_step, total_flow + flow_per_step)

    if len(here) == 2:
        us, ele = list(here)
        us_rate, us_nexts = graph[us]
        ele_rate, ele_nexts = graph[ele]

        us_open = us_rate > 0 and us not in opens
        ele_open = ele_rate > 0 and ele not in opens

        if us_open and ele_open:
            yield (time + 1, here, opens | {us, ele}, flow_per_step + us_rate + ele_rate, total_flow + flow_per_step)

        if us_open:
            # we stay, ele moves
            for n in ele_nexts:
                yield (time + 1, frozenset([us, n]), opens | {us}, flow_per_step + us_rate, total_flow + flow_per_step)

        if ele_open:
            # we move, ele opens
            for n in us_nexts:
                yield (time + 1, frozenset([ele, n]), opens | {ele}, flow_per_step + ele_rate, total_flow + flow_per_step)

        # both move:
        for n in set(map(frozenset, itertools.product(us_nexts, ele_nexts))):
            yield (time + 1, n, opens, flow_per_step, total_flow + flow_per_step)

