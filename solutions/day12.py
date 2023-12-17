from functools import cache


# tuple of (characters, run lens)
def parse_input(input: str):
    lines = [
        line.removeprefix("// ").split()
        for line in input.split("\n")
        if not line.startswith("// ")
    ]
    return [
        ([c for c in line[0]], [int(c) for c in line[1].split(",")]) for line in lines
    ]


# "unfold" it
def expand_row(data: tuple[list[str], list[int]]) -> tuple[list[str], list[int]]:
    new_arrangement = []
    new_run_lens = []
    for i in range(5):
        if i == 0:
            new_arrangement += data[0]
        else:
            new_arrangement += ["?"]
            new_arrangement += data[0]

        new_run_lens += data[1]

    return new_arrangement, new_run_lens


# DP implementation
@cache
def count_valid_arrangements(
    arrangement: tuple[str, ...],  # fyi tuple makes this hashable for cache decorator
    run_lens: tuple[int, ...],
    current_run_len: int,  # if >1, we are in an active run
) -> int:
    # if end of arrangement, return if current run exactly matches final desired run
    if len(arrangement) == 0:
        return (len(run_lens) == 0 and current_run_len == 0) or (
            len(run_lens) == 1 and current_run_len == run_lens[0]
        )

    # if current run greater than next desired run, fail
    if (current_run_len > 0 and len(run_lens) == 0) or (
        len(run_lens) > 0 and current_run_len > run_lens[0]
    ):
        return 0

    # early exit if insufficient chars left in arrangement to produce run_lens
    # `len(run_lens) - 1` term because runs must be separated
    if sum(run_lens) + len(run_lens) - 1 > len(arrangement) + current_run_len:
        return 0

    count = 0
    curr, next_arrangement = arrangement[0], arrangement[1:]

    # next iteration solving arrangement[1:]. when runs end, pop off run_lens
    chars = ["#", "."] if curr == "?" else [curr]
    for char in chars:
        next_run_lens, next_current_run_len = run_lens, current_run_len

        if char == "#":
            next_current_run_len = current_run_len + 1
        else:
            if current_run_len > 0:
                if len(run_lens) == 0 or current_run_len != run_lens[0]:
                    continue
                next_run_lens = run_lens[1:]
                next_current_run_len = 0

        count += count_valid_arrangements(
            next_arrangement, next_run_lens, next_current_run_len
        )
    return count


def part1(input: str) -> int:
    data = parse_input(input)
    counts = [count_valid_arrangements(tuple(l[0]), tuple(l[1]), 0) for l in data]
    return sum(counts)


def part2(input: str) -> int:
    data = parse_input(input)
    expanded = [expand_row(d) for d in data]
    counts = [count_valid_arrangements(tuple(l[0]), tuple(l[1]), 0) for l in expanded]
    return sum(counts)
