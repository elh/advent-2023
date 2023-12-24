Loc = tuple[int, ...]  # (x, y, z)
Vel = tuple[int, ...]  # (dx, dy, dz)
Stone = tuple[Loc, Vel]

REAL_INPUT = True

# Bounding box
MIN = 200000000000000 if REAL_INPUT else 7
MAX = 400000000000000 if REAL_INPUT else 27


def parse_input(input: str) -> list[Stone]:
    stones = []
    for line in input.split("\n"):
        parts = line.split(" @ ")
        stones.append(
            (
                tuple(int(v) for v in parts[0].split(", ")),
                tuple(int(v) for v in parts[1].split(", ")),
            )
        )

    return stones


def part1(input: str) -> int:
    stones = parse_input(input)
    line_linear_args = []
    for stone in stones:
        # y = mx + b
        (x, y, _), (dx, dy, _) = stone
        m = dy / dx
        b = y - m * x

        line_linear_args.append((stone, m, b))

    count = 0
    for i, args1 in enumerate(line_linear_args):
        for j, args2 in enumerate(line_linear_args[:i]):
            if args1 == args2:
                continue
            ((stone1_x, _, _), (stone1_dx, _, _)), m1, b1 = args1
            ((stone2_x, _, _), (stone2_dx, _, _)), m2, b2 = args2

            # ignore if parallel
            if m1 == m2:
                continue

            # solve for interection x. calculate y
            new_x = (b2 - b1) / (m1 - m2)
            new_y = m1 * new_x + b1

            if not (MIN <= new_x <= MAX) or not (MIN <= new_y <= MAX):
                continue

            # ignore if they crossed in the past. determine based on dx
            x_dir1 = stone1_dx // abs(stone1_dx)
            x_dir2 = stone2_dx // abs(stone2_dx)
            if (x_dir1 > 0 and new_x < stone1_x) or (x_dir1 < 0 and new_x > stone1_x):
                continue
            if (x_dir2 > 0 and new_x < stone2_x) or (x_dir2 < 0 and new_x > stone2_x):
                continue

            count += 1

    return count


def part2(input: str) -> int:
    raise Exception("Not implemented yet")
    data = parse_input(input)
    _ = data
    # print(data)

    return 0
