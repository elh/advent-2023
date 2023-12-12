def parse_input(input: str):
    lines = [line.split() for line in input.split("\n")]
    return [
        ([c for c in line[0]], [int(c) for c in line[1].split(",")]) for line in lines
    ]


def is_valid(arrangement: list[str], run_lens: list[int]) -> bool:
    actual_run_lens = []
    for i in range(len(arrangement)):
        if arrangement[i] == "#":
            if i == 0 or arrangement[i - 1] == ".":
                actual_run_lens.append(1)
            else:
                actual_run_lens[-1] += 1
    return actual_run_lens == run_lens


# backtracking count
# TODO: this is very slow because I'm not yet early terminating impossible sequences
def count_valid_arrangements(
    arrangement: list[str], run_lens: list[int], idx: int
) -> int:
    if idx == len(arrangement):
        return is_valid(arrangement, run_lens)

    if arrangement[idx] == "?":
        count = 0
        for c in ["#", "."]:
            arrangement[idx] = c
            count += count_valid_arrangements(arrangement, run_lens, idx + 1)
        arrangement[idx] = "?"
        return count
    else:
        return count_valid_arrangements(arrangement, run_lens, idx + 1)


def part1(input: str) -> int:
    data = parse_input(input)
    counts = [count_valid_arrangements(l[0], l[1], 0) for l in data]
    return sum(counts)


def part2(input: str) -> int:
    data = parse_input(input)
    print(data)

    return 0
