import pprint


def parse_input(input: str) -> list[list[str]]:
    return [[char for char in line] for line in input.split("\n")]


def translate(loc: tuple[int, int], dir: tuple[int, int]) -> tuple[int, int]:
    return (loc[0] + dir[0], loc[1] + dir[1])


# return # of lit squares
# light beams represented as tuples of location (y, x) and direction (dy, dx)
def cast_light(
    grid: list[list[str]],
    light: tuple[tuple[int, int], tuple[int, int]],
    known_lights: dict[
        tuple[tuple[int, int], tuple[int, int]],
        set[tuple[tuple[int, int], tuple[int, int]]],
    ],
) -> dict[
    tuple[tuple[int, int], tuple[int, int]],
    set[tuple[tuple[int, int], tuple[int, int]]],
]:
    # TODO: return a dict of all lights -> sets they cover (is this gonna be too much mem...?)
    # fringe of (beam, history) tuples

    out: dict[
        tuple[tuple[int, int], tuple[int, int]],
        set[tuple[tuple[int, int], tuple[int, int]]],
    ] = (
        known_lights if known_lights is not None else {}
    )
    lights = [(light, None)]

    while len(lights) > 0:
        light, prior = lights.pop()
        if light in out:
            if prior not in out:
                out[prior] = set()
            out[prior].add(light)
            continue
        cur_loc, cur_dir = light

        if cur_loc[0] < 0 or cur_loc[1] < 0:
            continue
        if cur_loc[0] >= len(grid) or cur_loc[1] >= len(grid[0]):
            continue

        if prior is not None:
            if prior not in out:
                out[prior] = set()
            out[prior].add(light)

        cur_content = grid[cur_loc[0]][cur_loc[1]]
        if cur_content == ".":
            next_loc = translate(cur_loc, cur_dir)
            lights.append(((next_loc, cur_dir), light))
        # reflect 90 degrees
        elif cur_content == "/":
            next_dir = (-1 * cur_dir[1], -1 * cur_dir[0])
            next_loc = translate(cur_loc, next_dir)
            lights.append(((next_loc, next_dir), light))
        elif cur_content == "\\":
            next_dir = (cur_dir[1], cur_dir[0])
            next_loc = translate(cur_loc, next_dir)
            lights.append(((next_loc, next_dir), light))
        # split
        elif cur_content == "|":
            if cur_dir[0] != 0:
                next_loc = translate(cur_loc, cur_dir)
                lights.append(((next_loc, cur_dir), light))
            else:
                for next_dir in [(1, 0), (-1, 0)]:
                    next_loc = translate(cur_loc, next_dir)
                    lights.append(((next_loc, next_dir), light))
        elif cur_content == "-":
            if cur_dir[1] != 0:
                next_loc = translate(cur_loc, cur_dir)
                lights.append(((next_loc, cur_dir), light))
            else:
                for next_dir in [(0, 1), (0, -1)]:
                    next_loc = translate(cur_loc, next_dir)
                    lights.append(((next_loc, next_dir), light))
        else:
            raise Exception("Invalid grid content")

    return out


# TODO: memoize this
def crawl(
    d: dict[
        tuple[tuple[int, int], tuple[int, int]],
        set[tuple[tuple[int, int], tuple[int, int]]],
    ],
    light: tuple[tuple[int, int], tuple[int, int]],
) -> int:
    seen = set()
    locs = set()
    fringe = [light]
    while len(fringe) > 0:
        cur = fringe.pop()
        if cur in seen:
            continue

        seen.add(cur)
        locs.add(cur[0])
        if cur in d:
            for child in d[cur]:
                fringe.append(child)

    return len(locs)


def part1(input: str) -> int:
    grid = parse_input(input)
    start_light = ((0, 0), (0, 1))
    light_data = cast_light(grid, start_light, None)
    return crawl(light_data, start_light)


# TODO: perf: memoize lit squares given a specific beam (loc, dir)
def part2(input: str) -> int:
    grid = parse_input(input)

    candidates = []
    for i in range(len(grid)):
        candidates.append(((i, 0), (0, 1)))
        candidates.append(((i, len(grid[0]) - 1), (0, -1)))
    for i in range(len(grid[0])):
        candidates.append(((0, i), (1, 0)))
        candidates.append(((len(grid) - 1, i), (-1, 0)))

    counts = []
    known_lights = None
    for candidate in candidates:
        known_lights = cast_light(grid, candidate, known_lights)
        counts.append(crawl(known_lights, candidate))

    return max(counts)
