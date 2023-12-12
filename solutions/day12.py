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


def count_runs(arrangement: list[str]) -> list[int]:
    run_lens = []
    for i in range(len(arrangement)):
        if arrangement[i] == "?":
            break
        if arrangement[i] == "#":
            if i == 0 or arrangement[i - 1] == ".":
                run_lens.append(1)
            else:
                run_lens[-1] += 1
    return run_lens


def is_valid(actual_run_lens: list[int], expected_run_lens: list[int]) -> bool:
    return actual_run_lens == expected_run_lens


# is valid prefix
# NOTE: this seems essential
# TODO: not considering if we are on an active run or for a sure the run is over
def is_valid_prefix(actual_run_lens: list[int], expected_run_lens: list[int]) -> bool:
    return actual_run_lens == expected_run_lens[: len(actual_run_lens)] or (
        len(actual_run_lens) > 0
        and len(actual_run_lens) <= len(expected_run_lens)
        and (
            actual_run_lens[: len(actual_run_lens) - 1]
            == expected_run_lens[: len(actual_run_lens) - 1]
            and actual_run_lens[len(actual_run_lens) - 1]
            < expected_run_lens[len(actual_run_lens) - 1]
        )
    )


# backtracking count
# NOTE: turning final case of incrementing idx into iterative does not help either
def count_valid_arrangements(
    arrangement: list[str], run_lens: list[int], idx: int
) -> int:
    actual_run_lens = count_runs(arrangement)
    # print(
    #     "".join(arrangement),
    #     actual_run_lens,
    #     run_lens,
    #     idx,
    #     is_valid_prefix(actual_run_lens, run_lens),
    # )

    if not is_valid_prefix(actual_run_lens, run_lens):
        return 0

    # early terminate if there are not enough remaining ?s to fill the run lengths
    # NOTE: these 2 seem useless...
    # TODO: different idea: instead of just checking the prefix, check entire run with possible gaps
    # if sum(actual_run_lens) + sum(
    #     [1 if c == "?" or c == "#" else 0 for c in arrangement[idx:]]
    # ) < sum(run_lens):
    #     return 0

    # if len(actual_run_lens) + sum(
    #     [1 if c == "?" or c == "." else 0 for c in arrangement[idx:]]
    # ) < len(run_lens):
    #     return 0

    if idx == len(arrangement):
        return 1 if is_valid(actual_run_lens, run_lens) else 0

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
    expanded = [expand_row(d) for d in data]
    counts = [count_valid_arrangements(l[0], l[1], 0) for l in expanded]
    return sum(counts)
