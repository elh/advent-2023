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


def part2(input: str) -> int:
    return 0
