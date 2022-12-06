from solutions import aoc_1, aoc_2, aoc_3, aoc_4, aoc_5, aoc_6


def read_in(filename):
    return open(filename).read().splitlines()


lines = list(read_in('inputs/1.txt'))
print('Problem 1 A: ' + str(aoc_1.one(lines)))
print('Problem 1 B: ' + str(aoc_1.two(lines)))

lines = list(read_in('inputs/2.txt'))
print('Problem 2 A: ' + str(aoc_2.one(lines)))
print('Problem 2 B: ' + str(aoc_2.two(lines)))

lines = list(read_in('inputs/3.txt'))
print('Problem 3 A: ' + str(aoc_3.one(lines)))
print('Problem 3 B: ' + str(aoc_3.two(lines)))

lines = list(read_in('inputs/4.txt'))
print('Problem 4 A: ' + str(aoc_4.one(lines)))
print('Problem 4 B: ' + str(aoc_4.two(lines)))

lines = list(read_in('inputs/5.txt'))
print('Problem 5 A: ' + str(aoc_5.one(lines)))
print('Problem 5 B: ' + str(aoc_5.two(lines)))

lines = list(read_in('inputs/6.txt'))
print('Problem 6 A: ' + str(aoc_6.one(lines)))
print('Problem 6 B: ' + str(aoc_6.two(lines)))