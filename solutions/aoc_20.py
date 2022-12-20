import itertools
import collections as c
import math

import pandas as pd
import heapq
import bisect
import datetime as dt
import re


def one(lines):
    ns = list(map(int, lines))
    #ns = [1,2,-3,3,-2,0,4]
    #ns = [-3,1,2]
    ns_with_id = list(enumerate(ns))

    mx = len(ns)

    for p in list(ns_with_id):
        #print(p)
        #print(ns_with_id)
        id, n = p
        idx = ns_with_id.index(p)

        if n == 0:
            continue

        n_idx = (idx + n) % (mx-1)

        ns_with_id.remove(p)
        ns_with_id.insert(n_idx, p)

    z_idx = ns.index(0)
    z_pos = ns_with_id.index((z_idx,0))
    sns = [ns_with_id[(i+z_pos)%mx][1] for i in [1000, 2000, 3000]]
    return sum(sns)


def two(lines):
    key = 811589153
    ns = [int(l) * key for l in lines]
    #ns = [v * key for v in [1,2,-3,3,-2,0,4]]

    ns_with_id = list(enumerate(ns))
    mx = len(ns)

    orig = list(ns_with_id)

    for _ in range(10):
        for p in orig:
            id, n = p
            idx = ns_with_id.index(p)

            if n == 0:
                continue

            n_idx = (idx + n) % (mx - 1)

            ns_with_id.remove(p)
            ns_with_id.insert(n_idx, p)

    z_idx = ns.index(0)
    z_pos = ns_with_id.index((z_idx,0))
    sns = [ns_with_id[(i+z_pos)%mx][1] for i in [1000, 2000, 3000]]
    return sum(sns)


