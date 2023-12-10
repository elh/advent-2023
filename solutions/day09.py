def parse_input(input: str):
    return [[int(x) for x in line.split()] for line in input.split("\n")]


# build the next line in the pyramid
def step(line: list[int]) -> list[int]:
    out = []
    for i in range(1, len(line)):
        out.append(line[i] - line[i - 1])
    return out


def next_value(line: list[int]) -> int:
    # build the pyramid
    seqs = [line]
    while len(set(seqs[-1])) != 1:
        seqs.append(step(seqs[-1]))

    # sum up the pyramid to the predicted next value
    add_int = seqs[-1][0]
    for seq in reversed(seqs[:-1]):
        add_int += seq[-1]

    return add_int


def part1(input: str) -> int:
    data = parse_input(input)
    return sum([next_value(line) for line in data])


def part2(input: str) -> int:
    data = parse_input(input)
    print(data)

    return 0
