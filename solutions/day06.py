from functools import reduce
import operator
from math import sqrt, floor, ceil


# a list of races where each race is a tuple (time, distance)
def parse_input(input: str) -> list:
    lists = [line.split() for line in input.split("\n")]
    return list(zip(list(map(int, lists[0][1:])), list(map(int, lists[1][1:]))))


def product(l: list) -> int:
    return reduce(operator.mul, l, 1)


# return # of ways to hold to exceed dist
def number_of_ways(time: int, dist: int) -> int:
    """
    distance = time * (time - time_held)
    time_held = (time ± sqrt(time**2 - 4 * distance)) / 2
    """
    th1 = floor((time + sqrt(time**2 - 4 * dist)) / 2)
    th2 = ceil((time - sqrt(time**2 - 4 * dist)) / 2)
    return th1 - th2 + 1


def part1(input: str) -> int:
    races = parse_input(input)
    all_ways = [number_of_ways(race[0], race[1]) for race in races]
    return product(all_ways)


def part2(input: str) -> int:
    def combined_int(l: list[int]) -> int:
        return int("".join(map(str, l)))

    races = parse_input(input)
    time = combined_int([r[0] for r in races])
    dist = combined_int([r[1] for r in races])

    return number_of_ways(time, dist)
