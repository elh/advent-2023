def parse_input(input: str) -> list[list[str]]:
    return [[char for char in line] for line in input.split("\n")]


def translate(loc: tuple[int, int], dir: tuple[int, int]) -> tuple[int, int]:
    return (loc[0] + dir[0], loc[1] + dir[1])


# return # of lit squares
def cast_light(grid: list[list[str]]) -> int:
    # as sets of tuples of (y, x) and direction (dy, dx)
    light_history = set()
    lights = {((0, 0), (0, 1))}  # initial beam

    while len(lights) > 0:
        light = lights.pop()
        if light in light_history:
            continue
        cur_loc, cur_dir = light

        if cur_loc[0] < 0 or cur_loc[1] < 0:
            continue
        if cur_loc[0] >= len(grid) or cur_loc[1] >= len(grid[0]):
            continue

        light_history.add((cur_loc, cur_dir))

        cur_content = grid[cur_loc[0]][cur_loc[1]]
        if cur_content == ".":
            next_loc = translate(cur_loc, cur_dir)
            lights.add((next_loc, cur_dir))
        # reflect 90 degrees
        elif cur_content == "/":
            next_dir = (-1 * cur_dir[1], -1 * cur_dir[0])
            next_loc = translate(cur_loc, next_dir)
            lights.add((next_loc, next_dir))
        elif cur_content == "\\":
            next_dir = (cur_dir[1], cur_dir[0])
            next_loc = translate(cur_loc, next_dir)
            lights.add((next_loc, next_dir))
        # split
        elif cur_content == "|":
            if cur_dir[0] != 0:
                next_loc = translate(cur_loc, cur_dir)
                lights.add((next_loc, cur_dir))
            else:
                for next_dir in [(1, 0), (-1, 0)]:
                    next_loc = translate(cur_loc, next_dir)
                    lights.add((next_loc, next_dir))
        elif cur_content == "-":
            if cur_dir[1] != 0:
                next_loc = translate(cur_loc, cur_dir)
                lights.add((next_loc, cur_dir))
            else:
                for next_dir in [(0, 1), (0, -1)]:
                    next_loc = translate(cur_loc, next_dir)
                    lights.add((next_loc, next_dir))
        else:
            raise Exception("Invalid grid content")

    return len({loc for loc, _ in light_history})


def part1(input: str) -> int:
    grid = parse_input(input)
    return cast_light(grid)


def part2(input: str) -> int:
    data = parse_input(input)
    _ = data
    # print(data)

    return 0
