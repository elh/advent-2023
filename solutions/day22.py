import copy


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
    # sorted by z value. they fall in this order
    bricks.sort(key=lambda b: min(b[0][2], b[1][2]))
    return bricks


# lol: still remember first deriving this working on appt scheduling
def overlaps(a_start, a_stop, b_start, b_stop) -> bool:
    return a_start <= b_stop and b_start <= a_stop


# return true if the brick is blocked on the z axis going down by any of the
# other blocks
def is_blocked(
    brick: list[list[int]],
    other_bricks: list[list[list[int]]],
) -> tuple[bool, list[list[list[int]]]]:
    brick_lowest_z = min(brick[0][2], brick[1][2])

    is_blocked = False
    blockers = []
    for other_brick in other_bricks:
        other_highest_z = max(other_brick[0][2], other_brick[1][2])

        if not other_highest_z + 1 == brick_lowest_z:
            # block has to be right above you
            continue
        # TODO: perf: maybe worth sorting the bricks by z so we can break early on gaps
        #       could do it by keeping bricks as a dict keyed by z

        x_overlaps = overlaps(
            brick[0][0], brick[1][0], other_brick[0][0], other_brick[1][0]
        )
        y_overlaps = overlaps(
            brick[0][1], brick[1][1], other_brick[0][1], other_brick[1][1]
        )
        if x_overlaps and y_overlaps:
            is_blocked = True
            blockers.append(other_brick)

    return is_blocked, blockers


def drop(
    bricks: list[list[list[int]]],
) -> tuple[list[list[list[int]]], dict[tuple, set]]:
    blocking_bricks: dict[tuple, set] = {}  # brick -> bricks it depends on

    bricks = copy.deepcopy(bricks)
    for i in range(len(bricks)):
        brick = bricks[i]
        previous_bricks = bricks[:i]
        while True:
            # drop the brick until it hits another brick or z = 0
            if brick[0][2] == 1 or brick[1][2] == 1:
                break
            am_blocked, blockers = is_blocked(brick, previous_bricks)
            if am_blocked:
                h = hashed(brick)
                if h not in blocking_bricks:
                    blocking_bricks[h] = set()
                for blocker in blockers:
                    blocking_bricks[h].add(hashed(blocker))
                break
            brick[0][2] -= 1
            brick[1][2] -= 1
    return bricks, blocking_bricks


# returns a hashed brick
def hashed(brick):
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
    _, blocking_bricks = drop(bricks)

    solo_blockers = set()
    for blockers in blocking_bricks.values():
        if len(blockers) == 1:
            solo_blockers.add(list(blockers)[0])

    return len(bricks) - len(solo_blockers)


def num_dependers(bricks, dropped_brick):
    dropped = {hashed(dropped_brick)}
    while True:
        no_change = True
        for k, v in bricks.items():
            if k in dropped:
                continue
            if v.issubset(dropped):
                dropped.add(k)
                no_change = False
        if no_change:
            break
    return len(dropped) - 1


def part2(input: str) -> int:
    bricks = parse_input(input)
    dropped_bricks, blocking_bricks = drop(bricks)
    return sum([num_dependers(blocking_bricks, b) for b in dropped_bricks])
