def parse_input(input: str) -> list[str]:
    return input.split(",")


def holiday_hash(s: str) -> int:
    cur = 0
    for char in s:
        cur += ord(char)
        cur *= 17
        cur %= 256
    return cur


def part1(input: str) -> int:
    steps = parse_input(input)
    values = [holiday_hash(step) for step in steps]
    return sum(values)


def part2(input: str) -> int:
    data = parse_input(input)
    _ = data
    # print(data)

    return 0
