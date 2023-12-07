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
    i = 0
    while i < len(initial_values):
        initial_ranges.append((initial_values[i], initial_values[i + 1]))
        i += 2
    initial_ranges.sort(key=lambda x: x[0])

    return {
        "initial_values": initial_values,
        "maps": ms,
        # optimizations for part 2
        "maps_reversed": ms[::-1],
        "initial_ranges": initial_ranges,
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


# brute force by reversing them through the maps starting from 0 until we find
# a valid initial value
def part2(input: str) -> int:
    parsed = parse_input(input)

    n = 0
    while True:
        v = get_reversed_value(n, parsed)
        if is_valid_init_value(v, parsed):
            return n

        # next
        n += 1
        # if n % 100000 == 0:
        #     print("n =", n)
        if n > 1000000000:
            raise Exception("too many iterations")
