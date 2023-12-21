def parse_input(input: str):
    grid = [[c for c in line] for line in input.split("\n")]
    start_loc = None
    for i, line in enumerate(grid):
        for j, c in enumerate(line):
            if c == "S":
                start_loc = (i, j)
                grid[i][j] = "."
    if start_loc is None:
        raise Exception("No start location found")
    return grid, start_loc


State = tuple[tuple[int, int], int]  # ((y, x), step_count)

dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def part1(input: str) -> int:
    grid, star_loc = parse_input(input)

    limit = 64
    final_locs: set[tuple[int, int]] = set()
    seen_states: set[State] = set()

    fringe: list[State] = [(star_loc, 0)]
    # cur_layer = 1
    while fringe:
        cur = fringe.pop(0)
        # if cur[1] >= cur_layer:
        #     cur_layer += 1
        #     print(cur_layer, len(fringe))
        if cur[1] >= limit:
            final_locs.add(cur[0])
            continue
        for dir in dirs:
            new = (cur[0][0] + dir[0], cur[0][1] + dir[1])
            if (
                new[0] < 0
                or new[0] >= len(grid)
                or new[1] < 0
                or new[1] >= len(grid[0])
            ):
                continue
            if grid[new[0]][new[1]] == "#":
                continue
            if (new, cur[1] + 1) in seen_states:
                continue
            seen_states.add((new, cur[1] + 1))
            fringe.append((new, cur[1] + 1))

    return len(final_locs)


def part2(input: str) -> int:
    raise Exception("Not implemented yet")
    data = parse_input(input)
    _ = data
    # print(data)

    return 0
