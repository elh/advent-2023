from functools import reduce
import operator


# a list of races where each race is a tuple (time, distance)
def parse_input(input: str) -> list:
    lists = [line.split() for line in input.split("\n")]
    return list(zip(list(map(int, lists[0][1:])), list(map(int, lists[1][1:]))))


def distance(time_held: int, total_time: int) -> int:
    if time_held >= total_time:
        return 0
    return time_held * (total_time - time_held)


def product(l: list) -> int:
    return reduce(operator.mul, l, 1)


def part1(input: str) -> int:
    races = parse_input(input)

    all_ways = []
    for race in races:
        ways = sum(
            [1 if distance(i, race[0]) > race[1] else 0 for i in range(0, race[0])]
        )
        all_ways.append(ways)
    return product(all_ways)


def part2(input: str) -> int:
    return 0
