def parse_card(line: str) -> dict:
    parts = line.split(": ")
    card_number = int(parts[0].split()[1])
    number_parts = parts[1].split(" | ")

    return {
        "card_number": card_number,
        "winning_numbers": number_parts[0].strip().split(),
        "your_numbers": number_parts[1].strip().split(),
    }


def score(card: dict) -> int:
    num_matches = 0
    for n in card["your_numbers"]:
        if n in card["winning_numbers"]:
            num_matches += 1
    if num_matches == 0:
        return 0
    elif num_matches == 1:
        return 1
    else:
        return pow(2, num_matches - 1)


def part1(input: str) -> int:
    cards = [parse_card(line) for line in input.split("\n")]
    scores = [score(c) for c in cards]
    return sum(scores)


def part2(input: str) -> int:
    return 0
