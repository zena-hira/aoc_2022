from solutions.aoc_1 import test


def read_in(filename):
    return open(filename).read().splitlines()


_input = list(map(int, read_in('inputs/1.txt')))
print('Problem 1 A: ' + str(test(_input)))
print('Problem 1 B: ' + str(test(_input)))
