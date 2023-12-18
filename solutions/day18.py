from functools import cmp_to_key


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


def list_to_pairs(l: list):
    return [[l[2 * i], l[2 * i + 1]] for i in range(len(l) // 2)]


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
    lines = [
        ("R", 1),
        ("U", 2),
        ("R", 2),
        ("D", 4),
        ("L", 3),
        ("U", 2),
    ]
    # TODO: use parse_input_p2
    lines = parse_input_p2(input)
    # print(lines)
    corners = [(0, 0)]  # (y,x)
    for dir, size in lines:
        delta = (deltas[dir][0] * size, deltas[dir][1] * size)
        corners.append((corners[-1][0] + delta[0], corners[-1][1] + delta[1]))

    if corners[0] != corners[-1]:
        raise ValueError("Path does not end at the start")

    corners = corners[:-1]
    # print(corners)

    def compare_corners(l1: tuple[int, int], l2: tuple[int, int]):
        if l1[0] < l2[0]:
            return -1
        elif l1[0] > l2[0]:
            return 1
        else:
            if l1[1] < l2[1]:
                return -1
            elif l1[1] > l2[1]:
                return 1
            else:
                return 0

    grouped = []  # list of tuples (y, list of x pairs)
    sorted_corners = sorted(corners, key=cmp_to_key(compare_corners))
    for corner in sorted_corners:
        if not grouped or grouped[-1][0] != corner[0]:
            grouped.append((corner[0], []))
        grouped[-1][1].append(corner[1])
    grouped = [(y, list_to_pairs(xs)) for y, xs in grouped]
    print(grouped)

    area = 0
    prev_y = grouped[0][0]
    active_ranges = grouped[0][1]
    # print(active_ranges)
    for group_y, group_xs in grouped[1:]:
        print("----------------------------------------")
        print("area:", area)
        print("active_ranges:", active_ranges)
        print("current:", group_y, group_xs)
        # add new area for the previous active ranges
        for active_range in active_ranges:
            print(
                "+= area",
                (group_y - prev_y) * (active_range[1] - active_range[0] + 1),
            )
            area += (group_y - prev_y) * (active_range[1] - active_range[0] + 1)
        prev_y = group_y

        # update active ranges
        print("--------------------------")
        print("group_xs", group_xs)
        for group_x in group_xs:
            new_active_ranges = []
            was_combined = False
            for active_range in active_ranges:
                print("group_x", group_x)
                print("active_range", active_range)
                # possible cases
                # group_x == active_range -> remove it
                # group_x and active_range share 1 corner -> expand or shrink it
                # group_x within active_range -> split it into 2
                # group_x totally outside of active_range -> add it

                # is group_x == active_range, remove it
                if group_x[0] == active_range[0] and group_x[1] == active_range[1]:
                    # special case for grid arithmatic. add this line to the area
                    area += active_range[1] - active_range[0] + 1
                    print("END")
                    was_combined = True
                    continue

                # is group_x and active_range share 1 corner, expand or shrink it
                if group_x[1] == active_range[0]:
                    print("EXPAND")
                    new_active_ranges.append((group_x[0], active_range[1]))
                    was_combined = True
                    continue
                if group_x[0] == active_range[1]:
                    print("EXPAND")
                    new_active_ranges.append((active_range[0], group_x[1]))
                    was_combined = True
                    continue
                if group_x[0] == active_range[0]:
                    print("SHRINK")
                    new_active_ranges.append((group_x[1], active_range[1]))
                    was_combined = True
                    continue
                if group_x[1] == active_range[1]:
                    print("SHRINK")
                    new_active_ranges.append((active_range[0], group_x[0]))
                    was_combined = True
                    continue

                # is group_x within active_range, split it into 2
                if group_x[0] > active_range[0] and group_x[1] < active_range[1]:
                    print("SPLIT")
                    new_active_ranges.append((active_range[0], group_x[0]))
                    new_active_ranges.append((group_x[1], active_range[1]))
                    was_combined = True
                    continue

                # default case. nop
                new_active_ranges.append(active_range)

            # group_x totally outside of active_range -> add it
            if not was_combined:
                print("ADD NEW")
                new_active_ranges.append(group_x)

            active_ranges = new_active_ranges

    return area
