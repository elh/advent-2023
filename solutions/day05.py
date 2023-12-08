"""
naive solution took ~8s but ~5 with binary search.
was not worth bothering with but was a good refresher on binary search.
"""


def parse_input(input: str) -> dict:
    initial_values = [int(v) for v in input.split("\n")[0].split(": ")[1].split()]

    ms = []
    for block in input.split("\n\n")[1:]:
        m = [[int(v) for v in line.split()] for line in block.split("\n")[1:]]
        # for part 2: sorted by destination range start. enable binary search
        m.sort(key=lambda x: x[0])
        ms.append(m)

    initial_ranges = []
    boundary_values = []
    i = 0
    while i < len(initial_values):
        initial_ranges.append((initial_values[i], initial_values[i + 1]))
        boundary_values.append(initial_values[i])
        boundary_values.append(initial_values[i] + initial_values[i + 1])
        i += 2
    initial_ranges.sort(key=lambda x: x[0])

    return {
        "initial_values": initial_values,
        "maps": ms,
        # optimizations for part 2
        "maps_reversed": ms[::-1],
        "initial_ranges": initial_ranges,
        "boundary_values": boundary_values,  # when inputs are ranges in part 2
    }


def get_mapped_value(v: int, data: dict) -> int:
    for m in data["maps"]:
        for dest_start, source_start, range_len in m:
            if v >= source_start and v < source_start + range_len:
                v = dest_start + (v - source_start)
                break
    return v


# via binary search
def get_reversed_value(v: int, data: dict) -> int:
    for m in data["maps_reversed"]:
        l = 0
        r = len(m)
        while l < r:
            i = (l + r) // 2
            dest_start, source_start, range_len = m[i]
            if v >= dest_start and v < dest_start + range_len:
                v = source_start + (v - dest_start)
                break
            elif v < dest_start:
                r = i
            else:
                l = i + 1
    return v


# via binary search
def is_valid_init_value(v: int, data: dict) -> bool:
    l = 0
    r = len(data["initial_ranges"])
    while l < r:
        i = (l + r) // 2
        start, size = data["initial_ranges"][i]
        if v >= start and v < start + size:
            return True
        elif v < start:
            r = i
        else:
            l = i + 1
    return False


def part1(input: str) -> int:
    parsed = parse_input(input)
    vs = [get_mapped_value(v, parsed) for v in parsed["initial_values"]]
    return min(vs)


# trace the initial ranges through the maps tracking all possible boundary values
#
# NOTE: i am considering a lot of values in later maps that actually are not
# reachable but the reduction in search space is already huge
def part2(input: str) -> int:
    parsed = parse_input(input)

    curs = parsed["boundary_values"]
    for m in parsed["maps"]:
        # add all possible boundary values given the map source ranges
        for dest_start, source_start, range_len in m:
            if source_start not in curs:
                curs.append(source_start)
            if source_start + range_len not in curs:
                curs.append(source_start + range_len)

        # then translate them to the map destination ranges
        new_curs = []
        for cur in curs:
            was_mapped = False
            for dest_start, source_start, range_len in m:
                if cur >= source_start and cur < source_start + range_len:
                    new_curs.append(dest_start + (cur - source_start))
                    was_mapped = True
                    break
            if not was_mapped:
                new_curs.append(cur)

        curs = new_curs

    # sort the final values and return the first valid initial value
    curs.sort()
    for cur in curs:
        v = get_reversed_value(cur, parsed)
        if is_valid_init_value(v, parsed):
            return cur

    raise Exception("no valid initial value found")
