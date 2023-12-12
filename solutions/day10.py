def parse_input(input: str) -> list[list[str]]:
    return [[char for char in line] for line in input.split("\n")]


# if the pipe is at (0,0), what 2 adjacents pipes does it connect to?
pipe_connecting_dirs = {
    "|": [(-1, 0), (1, 0)],
    "-": [(0, -1), (0, 1)],
    "L": [(-1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(1, 0), (0, -1)],
    "F": [(1, 0), (0, 1)],
}

dirs = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]


# NOTE: cannot use this to find "S" during a walk. "S" is a special case
def is_connected_to_start(
    start_loc: tuple[int, int], neighbor_loc: tuple[int, int], grid: list[list[str]]
) -> bool:
    candidate = grid[neighbor_loc[0]][neighbor_loc[1]]
    if candidate not in pipe_connecting_dirs:
        return False
    for delta in pipe_connecting_dirs[candidate]:
        if translate(neighbor_loc, delta) == start_loc:
            return True
    return False


# returns 1) a list of all locs in the cycle 2) an updated grid for p2
# updated grid turns all unconnected pipes to "." and replaces "S" with a pipe
def walk(grid: list[list[str]]) -> tuple[set[tuple[int, int]], list[list[str]]]:
    # find "S"
    start_loc = None
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if char == "S":
                start_loc = (y, x)
                break
    if start_loc is None:
        raise ValueError("No start location found")

    # find an initial direction to walk away from "S"
    first_loc = None
    for dir in dirs:
        candidate_loc = translate(start_loc, dir)
        if is_connected_to_start(start_loc, candidate_loc, grid):
            first_loc = candidate_loc
            break
    if first_loc is None:
        raise ValueError("No initial direction found")

    # iterative BFS
    fringe = [(first_loc, start_loc)]  # loc, prior_loc (to prevent backtracking)
    visited = {start_loc, first_loc}  # the walk path
    while len(fringe) > 0:
        loc, prior_loc = fringe.pop(0)
        char = grid[loc[0]][loc[1]]
        candidate_locs = [translate(loc, dir) for dir in pipe_connecting_dirs[char]]

        for candidate_loc in candidate_locs:
            # check if out of bounds
            if (
                candidate_loc[0] < 0
                or candidate_loc[0] >= len(grid)
                or candidate_loc[1] < 0
                or candidate_loc[0] >= len(grid[0])
            ):
                continue

            if candidate_loc == prior_loc:
                continue
            if grid[candidate_loc[0]][candidate_loc[1]] == "S":
                break
            if candidate_loc in visited:
                continue
            visited.add(candidate_loc)
            fringe.append((candidate_loc, loc))

    updated_grid = [row.copy() for row in grid]

    # turn all unconnected elements into "."
    for i in range(len(updated_grid)):
        for j in range(len(updated_grid[0])):
            if (i, j) not in visited:
                updated_grid[i][j] = "."

    # replace "S" with the equivalent pipe character
    start_connected_dirs = []
    for loc in visited:
        if loc == start_loc:
            continue
        dir = (loc[0] - start_loc[0], loc[1] - start_loc[1])
        if dir in dirs and is_connected_to_start(start_loc, loc, grid):
            start_connected_dirs.append(dir)
    start_connected_dirs = sorted(start_connected_dirs)

    for k, vs in pipe_connecting_dirs.items():
        if sorted(vs) == start_connected_dirs:
            updated_grid[start_loc[0]][start_loc[1]] = k

    return visited, updated_grid


def translate(loc: tuple[int, int], dir: tuple[int, int]) -> tuple[int, int]:
    return (loc[0] + dir[0], loc[1] + dir[1])


# a loc is enclosed if in all dirs, it is bounded by the path an odd number of times
def is_enclosed(loc: tuple[int, int], grid: list[list[str]]) -> bool:
    for dir in dirs:
        wall_count = 0
        prev_connection = None  # to handle 90 degree corners. last side connected

        cur_loc = translate(loc, dir)
        while (
            cur_loc[0] >= 0
            and cur_loc[0] < len(grid)
            and cur_loc[1] >= 0
            and cur_loc[1] < len(grid[0])
        ):
            cur_char = grid[cur_loc[0]][cur_loc[1]]
            cur_loc = translate(cur_loc, dir)  # the loop iteration

            if cur_char == ".":
                continue

            orthogonal_idx = 1 if dir == (-1, 0) or dir == (1, 0) else 0
            connections = []
            for d in pipe_connecting_dirs[cur_char]:
                if d[orthogonal_idx] != 0:
                    connections.append(d[orthogonal_idx])

            # this complexity is mainly managing corners
            if len(connections) == 2:  # a wall like "|" or "-"
                wall_count += 1
            elif len(connections) == 1:  # a corner
                if prev_connection is None:
                    prev_connection = connections[0]
                elif connections[0] == prev_connection:
                    prev_connection = None
                else:
                    prev_connection = None
                    wall_count += 1

        if wall_count % 2 == 0:
            return False
    return True


def part1(input: str) -> int:
    data = parse_input(input)
    walk_locs, _ = walk(data)
    return len(walk_locs) // 2


def part2(input: str) -> int:
    grid = parse_input(input)
    walk_locs, updated_grid = walk(grid)

    # NOTE: you could get a perf speed up by building up results incrementally.
    #       keeping track of corners would be added complexity for state though.
    enclosed = []
    for i, row in enumerate(updated_grid):
        for j, char in enumerate(row):
            if char != ".":
                continue
            loc = (i, j)
            if loc not in walk_locs and is_enclosed(loc, updated_grid):
                enclosed.append(loc)

    return len(enclosed)
