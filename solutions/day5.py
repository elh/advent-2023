def parse_input(input: str) -> dict:
    initial_values = [int(v) for v in input.split("\n")[0].split(": ")[1].split()]

    ms = []
    for block in input.split("\n\n")[1:]:
        m = [[int(v) for v in line.split()] for line in block.split("\n")[1:]]
        m.sort(key=lambda x: x[1])  # sorted by source range start
        ms.append(m)

    return {
        "initial_values": initial_values,
        "maps": ms,
    }


def get_reversed_value(v: int, data: dict) -> int:
    for m in reversed(data["maps"]):
        for dest_start, source_start, range_len in m:
            if v >= dest_start and v < dest_start + range_len:
                v = source_start + (v - dest_start)
                break
    return v


def is_valid_init_value(v: int, data: dict) -> bool:
    i = 0
    while i < len(data["initial_values"]):
        if (
            v >= data["initial_values"][i]
            and v < data["initial_values"][i] + data["initial_values"][i + 1]
        ):
            return True
        i += 2
    return False


def part1(input: str) -> int:
    parsed = parse_input(input)

    vs = []
    for initial_value in parsed["initial_values"]:
        v = initial_value
        for m in parsed["maps"]:
            for dest_start, source_start, range_len in m:
                if v >= source_start and v < source_start + range_len:
                    v = dest_start + (v - source_start)
                    break
        vs.append(v)
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
