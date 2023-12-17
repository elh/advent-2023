# NOTE: perf: fast lookup of where all boulders are. never scan for them.
def parse_input(input: str) -> list[list[str]]:
    return [[char for char in line] for line in input.split("\n")]


# always tilts back towards idx 0. use on grid via transpositions and rotations
# NOTE: perf: you could speed this up by removing the need for transposing the
#             entire grid but I liked the generality
def tilt(l: list[str]) -> list[str]:
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


def transpose(grid: list[list[str]] | tuple[tuple[str, ...], ...]) -> list[list[str]]:
    return [list(row) for row in zip(*grid)]


def part1(input: str) -> int:
    grid = parse_input(input)
    transposed = transpose(grid)
    tilted = [tilt(row) for row in transposed]
    loads = [count_load(row) for row in tilted]
    return sum(loads)


def hashed(grid: list[list[str]]) -> tuple[tuple[str, ...], ...]:
    return tuple(tuple(row) for row in grid)


def part2(input: str) -> int:
    grid = parse_input(input)
    seen: dict[tuple[tuple[str, ...], ...], int] = {}
    seen_arr = []

    # tilt until cycles detected
    cycle_start, cycle_len = None, None
    for i in range(100000):
        grid = transpose([tilt(row) for row in transpose(grid)])  # north
        grid = [tilt(row) for row in grid]  # west
        grid = transpose([tilt(row[::-1])[::-1] for row in transpose(grid)])  # south
        grid = [tilt(row[::-1])[::-1] for row in grid]  # east

        h = hashed(grid)

        if h in seen:
            cycle_start = seen[h]
            cycle_len = i - cycle_start
            break

        seen[h] = i
        seen_arr.append(h)

    if cycle_start is None or cycle_len is None:
        raise Exception("cycle not found in N iterations")

    # find 1000000000th (0-indexed) grid using cycles
    equiv_idx = ((1000000000 - 1 - cycle_start) % cycle_len) + cycle_start
    equiv_grid = seen_arr[equiv_idx]

    loads = [count_load(row) for row in transpose(equiv_grid)]
    return sum(loads)
