import pprint


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


def walk(grid: list[list[str]]) -> set[tuple[int, int]]:
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
    visited = {start_loc, first_loc}
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
                return visited
            if candidate_loc in visited:
                continue
            visited.add(candidate_loc)
            fringe.append((candidate_loc, loc))

    raise ValueError("dead end")


def translate(loc: tuple[int, int], dir: tuple[int, int]) -> tuple[int, int]:
    return (loc[0] + dir[0], loc[1] + dir[1])


def is_enclosed(loc: tuple[int, int], grid: list[list[str]]) -> bool:
    for dir in dirs:
        wall_count = 0
        prev_connection = None  # to handle 90 degree corners. last side connected

        # TODO: generalize this with rotations?
        cur_loc = translate(loc, dir)
        while (
            cur_loc[0] >= 0
            and cur_loc[0] < len(grid)
            and cur_loc[1] >= 0
            and cur_loc[1] < len(grid[0])
        ):
            cur_char = grid[cur_loc[0]][cur_loc[1]]
            if cur_char == ".":
                cur_loc = translate(cur_loc, dir)
                continue

            # TODO: handle "S" earlier
            if cur_char == "S":
                cur_loc = translate(cur_loc, dir)
                continue

            orthogonal_idx = 1 if dir == (-1, 0) or dir == (1, 0) else 0
            connections = []
            for d in pipe_connecting_dirs[cur_char]:
                if d[orthogonal_idx] != 0:
                    connections.append(d[orthogonal_idx])

            if len(connections) == 2:
                wall_count += 1
            elif len(connections) == 1:
                if prev_connection == None:
                    prev_connection = connections[0]
                elif connections[0] == prev_connection:
                    prev_connection == None
                else:
                    prev_connection == None
                    wall_count += 1

            cur_loc = translate(cur_loc, dir)

        if wall_count % 2 == 0:
            return False
    return True


def part1(input: str) -> int:
    data = parse_input(input)
    walk_locs = walk(data)
    return len(walk_locs) // 2


# TODO: handle corner case. need to turn S into a pipe as well
def part2(input: str) -> int:
    grid = parse_input(input)
    # pprint.pprint(grid)
    walk_locs = walk(grid)

    # TODO: turn unconnected pipes into "."

    enclosed = []
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char != ".":
                continue
            loc = (i, j)
            if loc not in walk_locs and is_enclosed(loc, grid):
                enclosed.append(loc)

    return len(enclosed)
