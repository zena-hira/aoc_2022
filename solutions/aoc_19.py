import itertools
import collections as col
import pandas as pd
import heapq
import bisect
import datetime as dt
import re

Blueprint = col.namedtuple("Blueprint", ['id', 'ore_robot', 'clay_robot', 'obs_robot', 'geo_robot'])

State = col.namedtuple("State", ['time', 'ore', 'clay', 'obs', 'geo', 'ore_robots', 'clay_robots', 'obs_robots', 'geo_robots'])

def parse(line):
    id, ore_ore, clay_ore, obs_ore, obs_clay, geo_ore, geo_obs = re.findall(r'\d+', line)

    return Blueprint(int(id),
                     ore_robot={'ore': int(ore_ore)},
                     clay_robot={'ore': int(clay_ore)},
                     obs_robot={'ore': int(obs_ore),
                                'clay': int(obs_clay)},
                     geo_robot={'ore': int(geo_ore),
                                'obs': int(geo_obs)}
                     )

def init_state():
    return State(time=0, ore=0, clay=0, obs=0, geo=0, ore_robots=1, clay_robots=0, obs_robots=0, geo_robots=0)

def next_states(s : State, bp : Blueprint):
    max_ore_needed = max(bp.ore_robot['ore'], bp.clay_robot['ore'], bp.obs_robot['ore'], bp.geo_robot['ore'])

    base_next_state = s._replace(time=s.time+1,
                                 ore=s.ore+s.ore_robots,
                                 clay=s.clay+s.clay_robots,
                                 obs=s.obs+s.obs_robots,
                                 geo=s.geo+s.geo_robots
                                 )

    if s.ore >= bp.geo_robot['ore'] and s.obs >= bp.geo_robot['obs']:
        yield base_next_state._replace(ore=base_next_state.ore - bp.geo_robot['ore'],
                                       obs=base_next_state.obs - bp.geo_robot['obs'],
                                       geo_robots=base_next_state.geo_robots + 1
                                       )
        return

    if s.obs_robots < bp.geo_robot['obs'] and s.ore >= bp.obs_robot['ore'] and s.clay >= bp.obs_robot['clay']:
        yield base_next_state._replace(ore=base_next_state.ore - bp.obs_robot['ore'],
                                       clay=base_next_state.clay - bp.obs_robot['clay'],
                                       obs_robots=base_next_state.obs_robots+1
                                       )

    if s.clay_robots < bp.obs_robot['clay'] and s.ore >= bp.clay_robot['ore']:
        yield base_next_state._replace(ore=base_next_state.ore - bp.clay_robot['ore'],
                                       clay_robots=base_next_state.clay_robots+1)

    if s.ore_robots < max_ore_needed and s.ore >= bp.ore_robot['ore']:
        yield base_next_state._replace(ore=base_next_state.ore - bp.ore_robot['ore'],
                                       ore_robots=base_next_state.ore_robots+1)

    yield base_next_state


def one(lines):
    return
    bps = list(map(parse, lines))
    return sum(bp.id * find_max_geodes_faster(bp, 24) for bp in bps)

def two(lines):
    bps = list(map(parse, lines))[0:3]

    return find_max_geodes_faster(bps[0], 32) * \
           find_max_geodes_faster(bps[1], 32) * \
           find_max_geodes_faster(bps[2], 32)

def find_max_geodes_faster(bp, max_time):
    print(bp)
    s = init_state()
    now = {s}
    nxt = init_ts()

    for t in range(max_time):
        print(f"{t} - {len(now)}")
        for c in now:
            for n in next_states(c, bp):
                nxt = add_to_ts(nxt, n, max_time)
        now = list(ts_to_s(nxt))
        nxt = init_ts()
    return max(s.geo for s in now)


def init_ts():
    return (0,set({}))

keys = ['ore', 'clay', 'obs', 'geo', 'ore_robots', 'clay_robots', 'obs_robots', 'geo_robots']
max_key = 7

def max_possible_geodes(s:State, max_time):
    return 0 # s.geo + (s.geo_robots*(max_time - s.time - 1)) + sum(range(max_time - s.time - 1))

def add_to_ts(ts, s: State, max_time):
    v = max_possible_geodes(s, max_time)
    ev, es = ts
    if v == ev:
        es.add(s)
        return (ev, es)
    if v > ev:
        return (v, {s})
    return ts

def ts_to_s(ts):
    return ts[1]


