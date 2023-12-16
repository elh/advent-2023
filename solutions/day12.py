import time
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


# def count_runs(arrangement: list[str]) -> list[int]:
#     run_lens = []
#     for i in range(len(arrangement)):
#         if arrangement[i] == "?":
#             break
#         if arrangement[i] == "#":
#             if i == 0 or arrangement[i - 1] == ".":
#                 run_lens.append(1)
#             else:
#                 run_lens[-1] += 1
#     return run_lens


def is_valid(actual_run_lens: list[int], expected_run_lens: list[int]) -> bool:
    return actual_run_lens == expected_run_lens


# is valid prefix
# NOTE: this seems essential
# TODO: not considering if we are on an active run or for a sure the run is over
# TODO: more efficient check. one that makes more sense for the memoized sub problem approach
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


# DP implementation
@cache
def count_valid_arrangements_2(
    arrangement: tuple[str, ...],  # fyi tuple makes this hashable for cache decorator
    run_lens: tuple[int, ...],
    current_run_len: int,  # if >1, we are in an active run
) -> int:
    # if current run greater than next desired run, fail
    if (current_run_len > 0 and len(run_lens) == 0) or (
        len(run_lens) > 0 and current_run_len > run_lens[0]
    ):
        return 0

    # if end of arrangement, return if current run exactly matches final desired run
    if len(arrangement) == 0:
        return (
            1
            if (current_run_len == 0 and len(run_lens) == 0)
            or (current_run_len == run_lens[0] and len(run_lens) == 1)
            else 0
        )

    count = 0
    curr, next_arrangement = arrangement[0], arrangement[1:]

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

        count += count_valid_arrangements_2(
            next_arrangement, next_run_lens, next_current_run_len
        )
    return count


# backtracking count
# NOTE: turning final case of incrementing idx into iterative does not help either
# TODO: NEW: turn this into a memoized function. optimize memoization by removing idx and making it always act against the remining arrangement
# chop off prefix as you go. figure out how to handle run_lens and idx_current_run_lens
def count_valid_arrangements(
    arrangement: list[str],
    run_lens: list[int],
    idx: int,
    idx_current_run_lens: list[int],
    idx_active_run: bool,
) -> int:
    # actual_run_lens = count_runs(arrangement)

    # print(
    #     "".join(arrangement),
    #     idx_current_run_lens,
    #     run_lens,
    #     idx,
    #     is_valid_prefix(idx_current_run_lens, run_lens),
    # )

    if not is_valid_prefix(idx_current_run_lens, run_lens):
        return 0

    # early terminate if there are not enough remaining "?"s and "#"s to fill the run lengths
    # TODO: different idea: instead of just checking the prefix, check entire run with possible gaps
    if sum(idx_current_run_lens) + sum(
        [1 if c == "?" or c == "#" else 0 for c in arrangement[idx:]]
    ) < sum(run_lens):
        return 0

    # NOTE: this doesnt seem to help
    # if (
    #     len(idx_current_run_lens)
    #     + sum([1 if c == "?" or c == "." else 0 for c in arrangement[idx:]])
    #     < len(run_lens) - 1
    # ):
    #     return 0

    if idx == len(arrangement):
        return 1 if is_valid(idx_current_run_lens, run_lens) else 0

    count = 0
    is_question_mark = arrangement[idx] == "?"
    chars = ["#", "."] if is_question_mark else [arrangement[idx]]

    for char in chars:
        # TODO: this isnt really functional but helps visualize
        arrangement[idx] = char
        next_current_run_lens = None
        if char == "#":
            if idx_active_run:
                next_current_run_lens = idx_current_run_lens.copy()
                next_current_run_lens[-1] += 1
            else:
                next_current_run_lens = idx_current_run_lens + [1]
        else:
            next_current_run_lens = idx_current_run_lens

        next_active_run = char == "#"
        count += count_valid_arrangements(
            arrangement,
            run_lens,
            idx + 1,
            next_current_run_lens,
            next_active_run,
        )
    # TODO: this isnt really functional but helps visualize
    if is_question_mark:
        arrangement[idx] = "?"
    return count


def timed(fn):
    start_t = time.time()
    res = fn()
    print("time:", time.time() - start_t)
    return res


def part1(input: str) -> int:
    data = parse_input(input)
    # counts = [
    #     timed(lambda: count_valid_arrangements(l[0], l[1], 0, [], False)) for l in data
    # ]
    # counts = [count_valid_arrangements(l[0], l[1], 0, [], False) for l in data]
    counts = [count_valid_arrangements_2(tuple(l[0]), tuple(l[1]), 0) for l in data]
    return sum(counts)


def part2(input: str) -> int:
    # raise Exception("Not implemented")

    data = parse_input(input)
    expanded = [expand_row(d) for d in data]
    # counts = [
    #     timed(lambda: count_valid_arrangements(l[0], l[1], 0, [], False))
    #     for l in expanded
    # ]
    # counts = [count_valid_arrangements(l[0], l[1], 0, [], False) for l in expanded]
    counts = [count_valid_arrangements_2(tuple(l[0]), tuple(l[1]), 0) for l in expanded]
    return sum(counts)
