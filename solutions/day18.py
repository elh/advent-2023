def parse_input_p1(input: str):
    lines = [line.split() for line in input.split("\n")]
    return [(line[0], int(line[1])) for line in lines]


def parse_input_p2(input: str):
    lines = [line.split() for line in input.split("\n")]
    out = []
    for line in lines:
        hex_part = line[2]  # like (#d2c081)
        direction = hex_int_to_dir[hex_part[-2]]
        size = int(hex_part[2:-2], 16)
        out.append((direction, size))

    return out


hex_int_to_dir = {
    "0": "R",
    "1": "D",
    "2": "L",
    "3": "U",
}

deltas = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1),
}


def part1(input: str) -> int:
    lines = parse_input_p1(input)
    coord_arr = [(0, 0)]  # (y,x)
    for dir, size in lines:
        delta = deltas[dir]
        for _ in range(size):
            coord_arr.append((coord_arr[-1][0] + delta[0], coord_arr[-1][1] + delta[1]))

    if coord_arr[0] != coord_arr[-1]:
        raise ValueError("Path does not end at the start")

    coords = set(coord_arr)

    # flood fill from the outside to find the total size enclodes by coords
    # find min and max y and x on the exterior
    min_y, min_x = coord_arr[0]
    max_y, max_x = coord_arr[0]
    for y, x in coords:
        min_y = min(min_y, y)
        min_x = min(min_x, x)
        max_y = max(max_y, y)
        max_x = max(max_x, x)

    outside_min_y = min_y - 1
    outside_min_x = min_x - 1
    outside_max_y = max_y + 1
    outside_max_x = max_x + 1

    # flood fill the outside
    seen = set()
    fringe = [(outside_min_y, outside_min_x)]
    while fringe:
        y, x = fringe.pop()
        if (y, x) in seen:
            continue
        if (y, x) in coords:
            continue
        if (
            y < outside_min_y
            or y > outside_max_y
            or x < outside_min_x
            or x > outside_max_x
        ):
            continue
        seen.add((y, x))
        fringe.append((y - 1, x))
        fringe.append((y + 1, x))
        fringe.append((y, x - 1))
        fringe.append((y, x + 1))

    box_size = (outside_max_y - outside_min_y + 1) * (outside_max_x - outside_min_x + 1)
    enclosed = box_size - len(seen)
    return enclosed


def part2(input: str) -> int:
    lines = parse_input_p2(input)
    print(lines)

    return 0
