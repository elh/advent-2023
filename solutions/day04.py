def parse_card(line: str) -> dict:
    parts = line.split(": ")
    number_parts = parts[1].split(" | ")
    return {
        "winners": number_parts[0].strip().split(),
        "yours": number_parts[1].strip().split(),
    }


def score(card: dict) -> int:
    num_matches = sum([1 if n in card["winners"] else 0 for n in card["yours"]])
    if num_matches == 0:
        return 0
    else:
        return pow(2, num_matches - 1)


def part1(input: str) -> int:
    cards = [parse_card(line) for line in input.split("\n")]
    scores = [score(c) for c in cards]
    return sum(scores)


def part2(input: str) -> int:
    cards = [parse_card(line) for line in input.split("\n")]
    card_count = [1 for _ in cards]
    for i, card in enumerate(cards):
        num_matches = sum([1 if n in card["winners"] else 0 for n in card["yours"]])
        if num_matches == 0:
            continue
        for j in range(i + 1, i + 1 + num_matches):
            card_count[j] += card_count[i]

    return sum(card_count)
