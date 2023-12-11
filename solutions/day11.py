def parse_input(input: str) -> list[list[str]]:
    return [[char for char in line] for line in input.split("\n")]


def expand(grid: list[list[str]]) -> list[list[str]]:
    # expand rows
    expanded_grid = []
    for row in grid:
        should_expand_row = True
        for char in row:
            if char == "#":
                should_expand_row = False
                break

        expanded_grid.append(row)
        if should_expand_row:
            row_copy = row.copy()
            expanded_grid.append(row_copy)

    # expand cols
    width = len(grid[0])
    idx_to_expand = {i: True for i in range(width)}
    for x in range(width):
        for row in grid:
            char = row[x]
            if char == "#":
                idx_to_expand[x] = False
                break
    # print(idx_to_expand)

    for row in expanded_grid:
        for i in reversed(range(width)):
            if idx_to_expand[i]:
                row.insert(i, ".")

    return expanded_grid


def print_grid(grid):
    for row in grid:
        print(*row)


def all_distance_pairs(grid: list[list[str]]) -> list[int]:
    locs = []
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == "#":
                locs.append((y, x))
    dists = []
    for loc1 in locs:
        for loc2 in locs:
            if loc1 == loc2:
                continue
            dists.append(abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1]))

    return dists


def part1(input: str) -> int:
    data = parse_input(input)
    # print("---")
    # print_grid(data)

    expanded = expand(data)
    # print("---")
    # print_grid(expanded)

    vs = all_distance_pairs(expanded)
    return sum(vs) // 2


def part2(input: str) -> int:
    data = parse_input(input)
    # print(data)

    return 0
