import functools


def parse_input(input: str) -> list:
    def to_values(s: str) -> list:
        face_cards = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
        return [int(c) if c.isdigit() else face_cards[c] for c in s]

    lines = [line.split() for line in input.split("\n")]
    hands = [(to_values(line[0]), int(line[1])) for line in lines]
    return hands


def score(hand: list) -> int:
    d = {}
    for card in hand:
        if card in d:
            d[card] += 1
        else:
            d[card] = 1

    if len(d) == 1:
        return 7  # highest
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


def is_h1_tie_breaker(h1: list, h2: list) -> bool:
    for i, card in enumerate(h1):
        if card > h2[i]:
            return True
        elif card < h2[i]:
            return False


def compare_hands(t1: tuple, t2: tuple) -> int:
    h1 = t1[0]
    h2 = t2[0]

    if score(h1) > score(h2):
        return 1
    elif score(h1) < score(h2):
        return -1
    else:
        if is_h1_tie_breaker(h1, h2):
            return 1
        else:
            return -1


def part1(input: str) -> int:
    data = parse_input(input)
    sorted_data = sorted(data, key=functools.cmp_to_key(compare_hands))

    score = 0
    for i, hand in enumerate(sorted_data):
        score += (i + 1) * hand[1]

    return score


def part2(input: str) -> int:
    data = parse_input(input)
    print(data)

    return 0
