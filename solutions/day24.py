import pprint


Loc = tuple[int, ...]  # (x, y, z)
Vel = tuple[int, ...]  # (dx, dy, dz)
Stone = tuple[Loc, Vel]

REAL_INPUT = False

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


# idx 0 means "x", idx 1 means "y", idx 2 means "z"
def collides_with_all(stone: Stone, stones: list[Stone], idx: int) -> bool:
    # x = x0 + dx * t
    (loc0, vel) = stone
    dx = vel[idx]
    x0 = loc0[idx]
    for other_stone in stones:
        print(other_stone)
        (other_loc0, other_vel) = other_stone
        other_dx = other_vel[idx]
        other_x0 = other_loc0[idx]

        # if they are moving in the same direction, they will never collide
        if dx == other_dx:
            return False

        # solve for t
        t = (other_x0 - x0) / (dx - other_dx)
        print(t)

        # assumption: t is an integer
        if not t.is_integer():
            return False

        # if t is negative, they will not collide
        if t < 0:
            return False

    return True


def part2(input: str) -> int:
    stones = parse_input(input)
    # pprint.pprint(stones)

    x_datas = [(stone[0][0], stone[1][0]) for stone in stones]
    pprint.pprint(x_datas)

    EXAMPLE_SOLN = ((24, 13, 10), (-3, 1, 2))
    print(collides_with_all(EXAMPLE_SOLN, stones, 0))

    # histories = []
    # # populate histories with the x position of each stone for each time step
    # for x_data in x_datas:
    #     history = []
    #     x, dx = x_data
    #     for i in range(0, 15):
    #         history.append(x)
    #         x += dx
    #     histories.append(history)
    # pprint.pprint(histories)

    # # for each stone, the time range where X is within MIN and MAX
    # valid_time_ranges = []
    # for x_data in x_datas:
    #     x, dx = x_data
    #     r = [max((MIN - x) // dx, 0), max((MAX - x) // dx, 0)]
    #     r.sort()
    #     valid_time_ranges.append(r)
    # pprint.pprint(valid_time_ranges)
