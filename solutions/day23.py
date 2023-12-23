RED = "\033[91m"
ENDC = "\033[0m"

all_dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def parse_input(input: str, should_clear=False) -> list[list[str]]:
    if should_clear:
        return [["#" if c == "#" else " " for c in line] for line in input.split("\n")]
    return [[c for c in line] for line in input.split("\n")]


def print_grid(grid, walked):
    if walked is None:
        walked = set()
    for i, line in enumerate(grid):
        for j, c in enumerate(line):
            if (i, j) in walked:
                print(RED + "◼" + ENDC, end="")
            else:
                print(c, end="")
        print()


def start_and_end_locs(
    grid: list[list[str]],
) -> tuple[tuple[int, int], tuple[int, int]]:
    try:
        start_loc = 0, next(i for i, c in enumerate(grid[0]) if c != "#")
        end_loc = len(grid) - 1, next(i for i, c in enumerate(grid[-1]) if c != "#")
    except StopIteration:
        raise Exception("No start or end location found")

    return start_loc, end_loc


def part1(input: str) -> int:
    grid = parse_input(input)
    start_loc, end_loc = start_and_end_locs(grid)

    # find longest walk to the end loc
    # list of (loc, prev_set, steps_taken, next_step_must_be)
    fringe: list[tuple[tuple[int, int], set, int, tuple[int, int] | None]] = [
        (start_loc, set(), 0, None)
    ]
    max_dist = -1
    while fringe:
        cur_loc, cur_prev_set, cur_steps_taken, cur_next_step_must_be = fringe.pop(0)
        if cur_loc == end_loc:
            max_dist = max(cur_steps_taken, max_dist)
            continue

        dirs = all_dirs
        if cur_next_step_must_be is not None:  # because of a slope
            dirs = [cur_next_step_must_be]
        for dir in dirs:
            new = (cur_loc[0] + dir[0], cur_loc[1] + dir[1])
            if (
                new[0] < 0
                or new[0] >= len(grid)
                or new[1] < 0
                or new[1] >= len(grid[0])
            ):
                continue

            if new in cur_prev_set:
                continue

            next_char = grid[new[0]][new[1]]
            if next_char == "#":
                continue

            next_step_must_be = None
            if next_char == "^":
                next_step_must_be = (-1, 0)
            elif next_char == "v":
                next_step_must_be = (1, 0)
            elif next_char == "<":
                next_step_must_be = (0, -1)
            elif next_char == ">":
                next_step_must_be = (0, 1)

            new_set = cur_prev_set.copy()
            new_set.add(new)

            fringe.append((new, new_set, cur_steps_taken + 1, next_step_must_be))

    return max_dist


# return a list of locations of branch points
# note: assumes that it is a "cleared grid"
def all_branch_locs(grid: list[list[str]]) -> list[tuple[int, int]]:
    branch_locs = []
    for i, line in enumerate(grid):
        for j, c in enumerate(line):
            if c != " ":
                continue

            clear_neighbors = 0
            for dir in all_dirs:
                new_loc = (i + dir[0], j + dir[1])
                if (
                    new_loc[0] < 0
                    or new_loc[0] >= len(grid)
                    or new_loc[1] < 0
                    or new_loc[1] >= len(grid[0])
                ):
                    continue

                if grid[new_loc[0]][new_loc[1]] == " ":
                    clear_neighbors += 1

            if clear_neighbors > 2:
                branch_locs.append((i, j))
    return branch_locs


# return edges as a dict of the connected_locs and their distances
def loc_edges(
    grid: list[list[str]], start_loc: tuple[int, int], locs: list[tuple[int, int]]
) -> dict[tuple[int, int], int]:
    fringe = [(start_loc, 0)]
    seen = set()

    dists = {}  # other loc -> dist
    while fringe:
        cur_loc, cur_dist = fringe.pop(0)
        if cur_loc in seen:
            continue
        seen.add(cur_loc)

        if cur_loc != start_loc and cur_loc in locs:
            dists[cur_loc] = cur_dist
            continue

        for dir in all_dirs:
            new_loc = (cur_loc[0] + dir[0], cur_loc[1] + dir[1])
            if (
                new_loc[0] < 0
                or new_loc[0] >= len(grid)
                or new_loc[1] < 0
                or new_loc[1] >= len(grid[0])
            ):
                continue

            if grid[new_loc[0]][new_loc[1]] == "#":
                continue

            fringe.append((new_loc, cur_dist + 1))

    return dists


def part2(input: str) -> int:
    grid = parse_input(input, should_clear=True)
    start_loc, end_loc = start_and_end_locs(grid)

    # pre-process the maze into a graph
    branch_locs = all_branch_locs(grid)
    locs = branch_locs + [start_loc, end_loc]
    graph = {loc: loc_edges(grid, loc, locs) for loc in locs}

    # list of (loc, prev_set, steps_taken)
    fringe: list[tuple[tuple[int, int], set, int]] = [(start_loc, set(), 0)]
    max_dist = -1
    while fringe:
        cur_loc, cur_prev_set, cur_steps_taken = fringe.pop()
        if cur_loc == end_loc:
            max_dist = max(cur_steps_taken, max_dist)
            continue

        for next_loc in graph[cur_loc]:
            if next_loc in cur_prev_set:
                continue

            new_set = cur_prev_set.copy()
            new_set.add(next_loc)

            fringe.append(
                (next_loc, new_set, cur_steps_taken + graph[cur_loc][next_loc])
            )

    return max_dist
