import functools
from collections.abc import Callable


def parse_input(input: str, with_jokers: bool = False) -> list:
    def to_values(s: str) -> list:
        face_cards = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
        if with_jokers:
            face_cards["J"] = 1
        return [int(c) if c.isdigit() else face_cards[c] for c in s]

    lines = [line.split() for line in input.split("\n")]
    hands = [(to_values(line[0]), int(line[1])) for line in lines]
    return hands


def score(hand: list, with_jokers: bool = False) -> int:
    d: dict[int, int] = {}  # card to count
    for card in hand:
        if card in d:
            d[card] += 1
        else:
            d[card] = 1

    # corner case: check this first for the corner case of all jokers
    if len(d) == 1:
        return 7  # highest rank

    # pre-process the jokers! just treat them as the highest card
    if with_jokers and 1 in d:
        num_jokers = d[1]
        del d[1]

        max_key = max(d, key=lambda k: d[k])
        d[max_key] += num_jokers

    if len(d) == 1:
        return 7  # highest rank
    elif len(d) == 2:
        if 4 in d.values():
            return 6
        else:
            return 5
    elif len(d) == 3:
        if 3 in d.values():
            return 4
        else:
            return 3
    elif len(d) == 4:
        return 2
    else:
        return 1


def compare_hands_fn(with_jokers: bool = False) -> Callable:
    def fn(t1: tuple, t2: tuple):
        h1 = t1[0]
        h2 = t2[0]

        if score(h1, with_jokers) > score(h2, with_jokers):
            return 1
        elif score(h1, with_jokers) < score(h2, with_jokers):
            return -1
        else:
            # tie breaker
            for i, card in enumerate(h1):
                if card > h2[i]:
                    return 1
                elif card < h2[i]:
                    return -1

            raise Exception("tie breaker failed")

    return fn


def part1(input: str) -> int:
    data = parse_input(input)
    sorted_data = sorted(data, key=functools.cmp_to_key(compare_hands_fn()))

    score = 0
    for i, hand in enumerate(sorted_data):
        score += (i + 1) * hand[1]

    return score


def part2(input: str) -> int:
    data = parse_input(input, with_jokers=True)
    sorted_data = sorted(
        data, key=functools.cmp_to_key(compare_hands_fn(with_jokers=True))
    )

    score = 0
    for i, hand in enumerate(sorted_data):
        score += (i + 1) * hand[1]

    return score
