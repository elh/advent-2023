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

    for row in expanded_grid:
        for i in reversed(range(width)):
            if idx_to_expand[i]:
                row.insert(i, ".")

    return expanded_grid


def all_distance_pairs(grid: list[list[str]]) -> list[int]:
    locs = []
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == "#":
                locs.append((y, x))
    dists = []
    for i, loc1 in enumerate(locs):
        for loc2 in locs[i + 1 :]:
            dists.append(abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1]))

    return dists


def part1(input: str) -> int:
    data = parse_input(input)
    expanded = expand(data)
    dists = all_distance_pairs(expanded)
    return sum(dists)


################################################################################
# part 2
################################################################################

emptiness_factor = 1000000 - 1


# list of empty row and column indices, sorted
def emptiness(grid: list[list[str]]) -> tuple[list[int], list[int]]:
    rows, cols = [], []

    for i, row in enumerate(grid):
        should_expand_row = True
        for char in row:
            if char == "#":
                should_expand_row = False
                break
        if should_expand_row:
            rows.append(i)

    width = len(grid[0])
    for i in range(width):
        should_expand_row = True
        for row in grid:
            char = row[i]
            if char == "#":
                should_expand_row = False
                break
        if should_expand_row:
            cols.append(i)

    return rows, cols


def all_distance_pairs_with_emptiness(
    grid: list[list[str]], emptiness: tuple[list[int], list[int]]
) -> list[int]:
    empty_rows, empty_cols = emptiness

    locs = []
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == "#":
                locs.append((y, x))
    dists = []
    for i, loc1 in enumerate(locs):
        for loc2 in locs[i + 1 :]:
            dist = abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])

            # add emptiness
            # NOTE: perf could be improved with more efficient iteration
            #       perhaps embed the emptiness values in the grid
            for row_idx in empty_rows:
                if (row_idx > loc1[0] and row_idx < loc2[0]) or (
                    row_idx > loc2[0] and row_idx < loc1[0]
                ):
                    dist += emptiness_factor
            for col_idx in empty_cols:
                if (col_idx > loc1[1] and col_idx < loc2[1]) or (
                    col_idx > loc2[1] and col_idx < loc1[1]
                ):
                    dist += emptiness_factor

            dists.append(dist)

    return dists


def part2(input: str) -> int:
    data = parse_input(input)
    e = emptiness(data)
    dists = all_distance_pairs_with_emptiness(data, e)
    return sum(dists)
