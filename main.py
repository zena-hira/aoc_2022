from solutions import aoc_1, aoc_2, aoc_3, aoc_4, aoc_5, aoc_6, aoc_7, aoc_8, aoc_9, aoc_10, aoc_11, aoc_12, aoc_13


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

lines = list(read_in('inputs/7.txt'))
print('Problem 7 A: ' + str(aoc_7.one(lines)))
print('Problem 7 B: ' + str(aoc_7.two(lines)))

lines = list(read_in('inputs/8.txt'))
print('Problem 8 A: ' + str(aoc_8.one(lines)))
print('Problem 8 B: ' + str(aoc_8.two(lines)))

lines = list(read_in('inputs/9.txt'))
print('Problem 9 A: ' + str(aoc_9.one(lines)))
print('Problem 9 B: ' + str(aoc_9.two(lines)))

lines = list(read_in('inputs/10.txt'))
print('Problem 10 A: ' + str(aoc_10.one(lines)))
aoc_10.two(lines)

lines = list(read_in('inputs/11.txt'))
print('Problem 11 A: ' + str(aoc_11.one(lines)))
print('Problem 11 B: ' + str(aoc_11.two(lines)))

lines = list(read_in('inputs/12.txt'))
print('Problem 12 A: ' + str(aoc_12.one(lines)))
print('Problem 12 B: ' + str(aoc_12.two(lines)))

lines = list(read_in('inputs/13.txt'))
print('Problem 13 A: ' + str(aoc_13.one(lines)))
print('Problem 13 B: ' + str(aoc_13.two(lines)))