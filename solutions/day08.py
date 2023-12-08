from collections.abc import Callable
from functools import reduce
from math import gcd


def parse_input(input: str) -> tuple:
    lines = input.split("\n")
    directions = [char for char in lines[0]]

    links = {}
    for stmt in lines[2:]:
        root, children = stmt.split(" = ")
        links[root] = children.removeprefix("(").removesuffix(")").split(", ")

    return (directions, links)


def length_to_end(cur: str, directions: list, links: dict, is_end: Callable) -> int:
    i = 0
    count = 0
    while True:
        count += 1
        if count > 100000000:
            raise Exception("Too many iterations")

        cur_dir = directions[i % len(directions)]
        if cur_dir == "L":
            cur = links[cur][0]
        elif cur_dir == "R":
            cur = links[cur][1]
        else:
            raise Exception("Invalid direction")

        if is_end(cur):
            return count

        i += 1


def part1(input: str) -> int:
    directions, links = parse_input(input)
    return length_to_end("AAA", directions, links, lambda cur: cur == "ZZZ")


# find the cycle length for each guy then find the lcm cycle time
def part2(input: str) -> int:
    directions, links = parse_input(input)

    curs = [root for root in links if root.endswith("A")]
    cycle_lens = [
        length_to_end(cur, directions, links, lambda cur: cur.endswith("Z"))
        for cur in curs
    ]

    def lcm(a, b):
        return abs(a * b) // gcd(a, b)

    return reduce(lcm, cycle_lens)
