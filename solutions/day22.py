import pprint
import copy

VERBOSE = False


def debug(*args):
    if VERBOSE:
        print(args)


# return a list of tuples (start, end) where start and end are a pair of x,y,z
# coords that form the start and end of a brick
def parse_input(input: str) -> list[list[list[int]]]:
    lines = input.split("\n")
    bricks = []
    for line in lines:
        parts_str = line.split("~")
        parts = []
        for part_str in parts_str:
            parts.append([int(v) for v in (part_str.split(","))])
        bricks.append(parts)
    return bricks


def overlaps(a_start, a_stop, b_start, b_stop) -> bool:
    return a_start <= b_stop and b_start <= a_stop


# return true if the brick is blocked on the z axis going down by any of the
# other blocks
def is_blocked(
    brick: tuple[tuple[int, int, int], tuple[int, int, int]],
    other_bricks: list[tuple[tuple[int, int, int], tuple[int, int, int]]],
) -> bool:
    brick_lowest_z = min(brick[0][2], brick[1][2])

    debug("is_blocked", brick, other_bricks)
    is_blocked = False
    blockers = []
    for other_brick in other_bricks:
        debug("checking blocked", brick, other_brick)
        other_highest_z = max(other_brick[0][2], other_brick[1][2])

        debug("other_highest_z", other_highest_z)
        debug("brick_lowest_z", brick_lowest_z)

        is_right_above = other_highest_z + 1 == brick_lowest_z

        if not is_right_above:
            continue

        x_overlaps = overlaps(
            brick[0][0], brick[1][0], other_brick[0][0], other_brick[1][0]
        )
        y_overlaps = overlaps(
            brick[0][1], brick[1][1], other_brick[0][1], other_brick[1][1]
        )

        debug("x_overlaps", x_overlaps)
        debug("y_overlaps", y_overlaps)
        debug("is_right_above", is_right_above)

        if x_overlaps and y_overlaps:
            debug("BLOCKED")
            is_blocked = True
            blockers.append(other_brick)

    return is_blocked, blockers


def drop(bricks: list[list[list[int]]]) -> list[list[list[int]]]:
    blocking_bricks = {}  # brick -> bricks it depends on

    bricks = copy.deepcopy(bricks)
    for i in range(len(bricks)):
        brick = bricks[i]
        previous_bricks = bricks[:i]
        debug("dropping", brick)
        while True:
            # drop the brick until it hits another brick or z = 0
            if brick[0][2] == 1 or brick[1][2] == 1:
                break
            am_blocked, blockers = is_blocked(brick, previous_bricks)
            if am_blocked:
                h = hashable_brick(brick)
                if h not in blocking_bricks:
                    blocking_bricks[h] = set()
                for blocker in blockers:
                    blocking_bricks[h].add(hashable_brick(blocker))
                break
            brick[0][2] -= 1
            brick[1][2] -= 1
    return bricks, blocking_bricks


def hashable_brick(brick):
    return (
        brick[0][0],
        brick[0][1],
        brick[0][2],
        brick[1][0],
        brick[1][1],
        brick[1][2],
    )


def part1(input: str) -> int:
    bricks = parse_input(input)
    pprint.pprint(bricks)

    # sorted by z value. they fall in this order
    bricks.sort(key=lambda b: min(b[0][2], b[1][2]))
    pprint.pprint(bricks)

    dropped_bricks, blocking_bricks = drop(bricks)
    pprint.pprint(dropped_bricks)
    pprint.pprint(blocking_bricks)

    solo_blockers = set()
    for brick, blockers in blocking_bricks.items():
        if len(blockers) == 1:
            solo_blockers.add(list(blockers)[0])

    return len(bricks) - len(solo_blockers)


def part2(input: str) -> int:
    raise Exception("Not implemented yet")
    data = parse_input(input)
    _ = data
    # print(data)

    return 0
