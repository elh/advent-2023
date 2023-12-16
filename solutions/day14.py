def parse_input(input: str) -> list[list[str]]:
    return [[char for char in line] for line in input.split("\n")]


# to be used with transpositions
def tilt_left(l: list[str]) -> list[str]:
    for i in range(len(l)):
        if l[i] != "O":
            continue

        l[i] = "."
        to_idx = i
        for j in reversed(range(i + 1)):
            if l[j] != ".":
                break
            to_idx = j
        l[to_idx] = "O"

    return l


def count_load(l: list[str]) -> int:
    sum = 0
    for i, char in enumerate(l):
        if char == "O":
            sum += len(l) - i
    return sum


def transpose(grid: list[list[str]]) -> list[list[str]]:
    return [list(row) for row in zip(*grid)]


def part1(input: str) -> int:
    grid = parse_input(input)
    transposed = transpose(grid)
    tilted = [tilt_left(row) for row in transposed]
    loads = [count_load(row) for row in tilted]
    return sum(loads)


def part2(input: str) -> int:
    data = parse_input(input)
    _ = data
    # print(data)

    return 0
