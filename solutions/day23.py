RED = "\033[91m"
ENDC = "\033[0m"

all_dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def parse_input(input: str, clear_slopes=False) -> list[list[str]]:
    if clear_slopes:
        return [[c if c == "#" else " " for c in line] for line in input.split("\n")]
    return [
        [c if c in ["#", "^", ">", "v", "<"] else " " for c in line]
        for line in input.split("\n")
    ]


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


# return a list of locations of branch points
# note: assumes that it is a "cleared grid"
def all_branch_locs(grid: list[list[str]]) -> list[tuple[int, int]]:
    branch_locs = []
    for i, line in enumerate(grid):
        for j, c in enumerate(line):
            if c == "#":
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

                if grid[new_loc[0]][new_loc[1]] != "#":
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

        cur_char = grid[cur_loc[0]][cur_loc[1]]
        dirs = all_dirs
        if cur_char == "^":
            dirs = [(-1, 0)]
        elif cur_char == "v":
            dirs = [(1, 0)]
        elif cur_char == "<":
            dirs = [(0, -1)]
        elif cur_char == ">":
            dirs = [(0, 1)]

        for dir in dirs:
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


def max_dist(
    graph: dict[tuple[int, int], dict[tuple[int, int], int]],
    start_loc: tuple[int, int],
    end_loc: tuple[int, int],
) -> int:
    # list of (loc, prev_set, steps_taken)
    fringe: list[tuple[tuple[int, int], set, int]] = [(start_loc, set(), 0)]
    max_dist = -1
    while fringe:
        cur_loc, cur_prev_set, cur_steps_taken = fringe.pop()
        if cur_loc == end_loc:
            # if cur_steps_taken > max_dist:
            #     print("new max dist:", cur_steps_taken)
            max_dist = max(cur_steps_taken, max_dist)
            continue

        # if exit is connected to cur_loc, you must go there else it will be blocked
        if end_loc in graph[cur_loc]:
            new_set = cur_prev_set.copy()
            new_set.add(end_loc)

            fringe.append((end_loc, new_set, cur_steps_taken + graph[cur_loc][end_loc]))
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


def part1(input: str) -> int:
    grid = parse_input(input)
    start_loc, end_loc = start_and_end_locs(grid)

    # pre-process the maze into a graph
    branch_locs = all_branch_locs(grid)
    locs = branch_locs + [start_loc, end_loc]
    graph = {loc: loc_edges(grid, loc, locs) for loc in locs}

    return max_dist(graph, start_loc, end_loc)


def part2(input: str) -> int:
    grid = parse_input(input, clear_slopes=True)
    start_loc, end_loc = start_and_end_locs(grid)

    # pre-process the maze into a graph
    branch_locs = all_branch_locs(grid)
    locs = branch_locs + [start_loc, end_loc]
    graph = {loc: loc_edges(grid, loc, locs) for loc in locs}

    return max_dist(graph, start_loc, end_loc)
