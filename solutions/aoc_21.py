import itertools
import collections as c
import math

import pandas as pd
import heapq
import bisect
import datetime as dt
import re

def parse(lines):
    consts = {}
    instrs = {}
    for line in lines:
        monkey, defn = line.split(': ')
        if re.fullmatch(r'\d+', defn):
            consts[monkey] = int(defn)
        else:
            m1, cmd, m2 = defn.split(' ')
            instrs[monkey] = (m1, cmd, m2)
    return consts, instrs

def one(lines):
    consts, instrs = parse(lines)
    target = 'root'
    return search_const(target, consts, instrs)


def search_const(target, consts, instrs):
    q = [target]
    while q:
        curr = q.pop()
        if curr in consts:
            continue

        (m1, cmd, m2) = instrs[curr]
        if m1 in consts and m2 in consts:
            v1 = consts[m1]
            v2 = consts[m2]
            consts[curr] = eval(f"{v1} {cmd} {v2}")
        else:
            q.append(curr)
            if m1 not in consts:
                q.append(m1)
            if m2 not in consts:
                q.append(m2)

    return consts[target]

def two(lines):
    consts, instrs = parse(lines)
    del(consts['humn'])
    t1, _, t2 = instrs['root']
    t2_v = search_const(t2, consts.copy(), instrs)
    print(t2_v)

    needs_human = set(['humn'])
    q = [t1]
    while q:
        curr = q.pop()
        if curr in consts or curr in needs_human:
            continue
        (m1, cmd, m2) = instrs[curr]
        if m1 in needs_human or m2 in needs_human:
            needs_human.add(curr)
        if m1 in consts and m2 in consts:
            v1 = consts[m1]
            v2 = consts[m2]
            consts[curr] = eval(f"{v1} {cmd} {v2}")
        else:
            if curr not in needs_human:
                q.append(curr)
            if m1 not in consts and m1 not in needs_human:
                q.append(m1)
            if m2 not in consts and m2 not in needs_human:
                q.append(m2)

    q = [t1]
    target = t2_v
    while q:
        print(q)
        curr = q.pop()
        if curr == 'humn':
            return target
        if curr in consts:
            print(curr)
            raise 'Gone wrong'
        m1, cmd, m2 = instrs[curr]
        if m1 in consts and m2 in consts:
            raise 'Also gone wrong'
        if m1 in consts:
            if cmd == '+':
                target = target - consts[m1]
            elif cmd == '-':
                target = consts[m1] - target
            elif cmd == '*':
                target = target / consts[m1]
            elif cmd == '/':
                target = consts[m1] / target
            else:
                raise 'blugh'
            q.append(m2)

        if m2 in consts:
            if cmd == '+':
                target = target - consts[m2]
            elif cmd == '-':
                target = target + consts[m2]
            elif cmd == '*':
                target = target / consts[m2]
            elif cmd == '/':
                target = target * consts[m2]
            else:
                raise 'blugh2'
            q.append(m1)


