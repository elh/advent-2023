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
    # "." is a nop
}

dirs = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]


# NOTE: cannot use this to find "S" during a walk. "S" is a special case
# TODO: probably should just remove this
def is_neighbor_connected(
    cur_loc: tuple[int, int], neighbor_loc: tuple[int, int], grid: list[list[str]]
) -> bool:
    candidate = grid[neighbor_loc[0]][neighbor_loc[1]]
    if candidate not in pipe_connecting_dirs:
        return False
    for delta in pipe_connecting_dirs[candidate]:
        if (neighbor_loc[0] + delta[0], neighbor_loc[1] + delta[1]) == cur_loc:
            return True
    return False


def part1(input: str) -> int:
    data = parse_input(input)

    # find "S"
    start_loc = None
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == "S":
                start_loc = (y, x)
                break
    if start_loc is None:
        raise ValueError("No start location found")

    # find an initial direction to walk away from "S"
    first_loc = None
    for dir in dirs:
        candidate_loc = (start_loc[0] + dir[0], start_loc[1] + dir[1])
        if is_neighbor_connected(start_loc, candidate_loc, data):
            first_loc = candidate_loc
            break
    if first_loc is None:
        raise ValueError("No initial direction found")

    # iterative BFS
    fringe = [(first_loc, 1, start_loc)]  # loc, walk_len, prior_loc
    visited = {start_loc, first_loc}
    while len(fringe) > 0:
        loc, walk_len, prior_loc = fringe.pop(0)
        char = data[loc[0]][loc[1]]
        candidate_locs = [
            (loc[0] + dir[0], loc[1] + dir[1]) for dir in pipe_connecting_dirs[char]
        ]

        for candidate_loc in candidate_locs:
            # check if out of bounds
            if (
                candidate_loc[0] < 0
                or candidate_loc[0] >= len(data)
                or candidate_loc[1] < 0
                or candidate_loc[0] >= len(data[0])
            ):
                continue

            if candidate_loc == prior_loc:
                continue
            if data[candidate_loc[0]][candidate_loc[1]] == "S":
                return (walk_len + 1) // 2
            if candidate_loc in visited:
                continue
            visited.add(candidate_loc)
            fringe.append((candidate_loc, walk_len + 1, loc))

    raise ValueError("dead end")


def part2(input: str) -> int:
    data = parse_input(input)

    return 0
