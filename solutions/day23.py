import pprint


def parse_input(input: str):
    return [[c for c in line] for line in input.split("\n")]


def print_grid(grid):
    for line in grid:
        for c in line:
            print(c, end="")
        print()


all_dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def part1(input: str) -> int:
    grid = parse_input(input)
    print_grid(grid)

    start_loc = None
    for i, c in enumerate(grid[0]):
        if c == ".":
            start_loc = (0, i)
            break
    if start_loc is None:
        raise Exception("No start location found")

    end_loc = None
    for i, c in enumerate(grid[(len(grid) - 1)]):
        if c == ".":
            end_loc = (len(grid) - 1, i)
            break
    if end_loc is None:
        raise Exception("No start location found")

    print(start_loc, end_loc)
    print(len(grid), len(grid[0]))

    # find longest walk to the end loc
    fringe = [
        (start_loc, set(), 0, None)
    ]  # (loc, prev_set, steps_taken, next_step_must_be)
    max_dist = -1
    while fringe:
        cur_loc, cur_prev_set, cur_steps_taken, cur_next_step_must_be = fringe.pop(0)
        if cur_loc == end_loc:
            max_dist = max(cur_steps_taken, max_dist)
            continue

        dirs = all_dirs
        if cur_next_step_must_be is not None:
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


def part2(input: str) -> int:
    raise Exception("Not implemented yet")
    data = parse_input(input)
    _ = data
    # print(data)

    return 0
