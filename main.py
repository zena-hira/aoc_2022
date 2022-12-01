from solutions import aoc_1, aoc_2


def read_in(filename):
    return open(filename).read().splitlines()


_input = list(read_in('inputs/1.txt'))
print('Problem 1 A: ' + str(aoc_1.one(_input)))
print('Problem 1 B: ' + str(aoc_1.two(_input)))

_input = list(read_in('inputs/2.txt'))
print('Problem 2 A: ' + str(aoc_2.one(_input)))
print('Problem 2 B: ' + str(aoc_2.two(_input)))
